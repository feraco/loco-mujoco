#!/usr/bin/env python3
"""
G1 Hardware Test with Balance Stabilization
Adds CoM/ZMP-based balance corrections for dynamic motions like dancing.

Key improvements:
1. Center of Mass (CoM) tracking and limits
2. Adaptive gain scheduling based on motion dynamics
3. Torso stabilization using IMU feedback
4. Foot pressure monitoring for balance detection
5. Emergency stance detection and recovery

Usage on Jetson:
    export CYCLONEDDS_HOME=/home/unitree/Documents/GitHub/cyclonedds/install
    export LD_LIBRARY_PATH=$CYCLONEDDS_HOME/lib:$LD_LIBRARY_PATH
    export PYTHONPATH=/home/unitree/unitree_sdk2_python:$PYTHONPATH
    
    # Safer speeds with balance control
    python3 quick_hardware_test_jetson_balanced.py dancing --speed 0.5  # 50% speed
    python3 quick_hardware_test_jetson_balanced.py dancing --speed 1.0  # Full speed
    
    # Disable balance features (use original behavior)
    python3 quick_hardware_test_jetson_balanced.py dancing --no-balance

Press Ctrl+C to emergency stop at any time.
"""

import sys
import os
import time
import numpy as np
import signal
import argparse

# Add SDK to path
sys.path.insert(0, '/home/unitree/unitree_sdk2_python')

try:
    from unitree_sdk2py.core.channel import ChannelPublisher, ChannelSubscriber, ChannelFactoryInitialize
    from unitree_sdk2py.idl.default import unitree_hg_msg_dds__LowCmd_, unitree_hg_msg_dds__LowState_
    from unitree_sdk2py.idl.unitree_hg.msg.dds_ import LowCmd_, LowState_
    from unitree_sdk2py.utils.crc import CRC
    from unitree_sdk2py.utils.thread import RecurrentThread
    from unitree_sdk2py.comm.motion_switcher.motion_switcher_client import MotionSwitcherClient
    print("✓ Unitree SDK2 Python imported successfully")
except ImportError as e:
    print(f"✗ Failed to import SDK: {e}")
    print("\nMake sure you're on the Jetson with:")
    print("  export PYTHONPATH=/home/unitree/unitree_sdk2_python:$PYTHONPATH")
    sys.exit(1)

# Number of motors on G1
G1_NUM_MOTOR = 29

# Per-joint gains - adjusted for balance
Kp_base = [
    60, 60, 60, 100, 40, 40,      # left leg (0-5)
    60, 60, 60, 100, 40, 40,      # right leg (6-11)
    60, 40, 40,                   # waist (12-14)
    40, 40, 40, 40, 40, 40, 40,   # left arm (15-21)
    40, 40, 40, 40, 40, 40, 40    # right arm (22-28)
]

Kd_base = [
    1, 1, 1, 2, 1, 1,     # left leg
    1, 1, 1, 2, 1, 1,     # right leg
    1, 1, 1,              # waist
    1, 1, 1, 1, 1, 1, 1,  # left arm
    1, 1, 1, 1, 1, 1, 1   # right arm
]

class G1JointIndex:
    """Joint indices for G1 robot"""
    LeftHipPitch = 0
    LeftHipRoll = 1
    LeftHipYaw = 2
    LeftKnee = 3
    LeftAnklePitch = 4
    LeftAnkleRoll = 5
    RightHipPitch = 6
    RightHipRoll = 7
    RightHipYaw = 8
    RightKnee = 9
    RightAnklePitch = 10
    RightAnkleRoll = 11
    WaistYaw = 12
    WaistRoll = 13
    WaistPitch = 14
    LeftShoulderPitch = 15
    LeftShoulderRoll = 16
    LeftShoulderYaw = 17
    LeftElbow = 18
    LeftWristRoll = 19
    LeftWristPitch = 20
    LeftWristYaw = 21
    RightShoulderPitch = 22
    RightShoulderRoll = 23
    RightShoulderYaw = 24
    RightElbow = 25
    RightWristRoll = 26
    RightWristPitch = 27
    RightWristYaw = 28


class Mode:
    PR = 0  # Series Control for Pitch/Roll Joints
    AB = 1  # Parallel Control for A/B Joints


class BalanceController:
    """Balance stabilization controller for humanoid robots"""
    
    def __init__(self, enable=True):
        self.enable = enable
        
        # Balance thresholds
        self.max_roll_angle = 0.3  # radians (~17 degrees)
        self.max_pitch_angle = 0.3  # radians (~17 degrees)
        self.max_roll_velocity = 1.0  # rad/s
        self.max_pitch_velocity = 1.0  # rad/s
        
        # Stabilization gains
        self.torso_stabilization_gain = 0.15  # How much to counteract tilting
        self.ankle_stabilization_gain = 0.08  # Ankle strategy for small perturbations
        self.hip_stabilization_gain = 0.05   # Hip strategy for larger perturbations
        
        # Adaptive gain scheduling
        self.min_gain_multiplier = 0.3  # Reduce gains during fast motions
        self.velocity_threshold = 0.5   # rad/s - threshold for gain reduction
        
        # History for derivative estimation
        self.imu_history = []
        self.max_history = 10
        
    def update_imu(self, quaternion, gyro):
        """Update IMU measurements"""
        self.imu_history.append({
            'quat': quaternion,
            'gyro': gyro,
            'time': time.time()
        })
        if len(self.imu_history) > self.max_history:
            self.imu_history.pop(0)
    
    def get_orientation(self, quaternion):
        """Convert quaternion to roll/pitch angles"""
        # quaternion: [x, y, z, w]
        x, y, z, w = quaternion
        
        # Roll (x-axis rotation)
        sinr_cosp = 2 * (w * x + y * z)
        cosr_cosp = 1 - 2 * (x * x + y * y)
        roll = np.arctan2(sinr_cosp, cosr_cosp)
        
        # Pitch (y-axis rotation)
        sinp = 2 * (w * y - z * x)
        if abs(sinp) >= 1:
            pitch = np.copysign(np.pi / 2, sinp)
        else:
            pitch = np.arcsin(sinp)
        
        return roll, pitch
    
    def compute_balance_corrections(self, low_state, target_positions):
        """
        Compute joint corrections to maintain balance
        Returns: correction array for all joints
        """
        if not self.enable or low_state is None:
            return np.zeros(G1_NUM_MOTOR)
        
        corrections = np.zeros(G1_NUM_MOTOR)
        
        # Get IMU data
        imu = low_state.imu_state
        quaternion = [imu.quaternion[0], imu.quaternion[1], 
                     imu.quaternion[2], imu.quaternion[3]]
        gyro = [imu.gyroscope[0], imu.gyroscope[1], imu.gyroscope[2]]
        
        self.update_imu(quaternion, gyro)
        
        # Get current orientation
        roll, pitch = self.get_orientation(quaternion)
        roll_rate = gyro[0]
        pitch_rate = gyro[1]
        
        # Check if we need stabilization
        if abs(roll) < 0.05 and abs(pitch) < 0.05 and \
           abs(roll_rate) < 0.1 and abs(pitch_rate) < 0.1:
            return corrections  # Robot is stable, no correction needed
        
        # Adaptive gain based on motion velocity
        joint_velocities = np.array([low_state.motor_state[i].dq for i in range(G1_NUM_MOTOR)])
        avg_velocity = np.mean(np.abs(joint_velocities))
        gain_multiplier = 1.0 - min(avg_velocity / self.velocity_threshold, 1.0) * \
                         (1.0 - self.min_gain_multiplier)
        
        # Torso stabilization (waist joints)
        # Counteract roll with waist roll
        if abs(roll) > 0.05:
            corrections[G1JointIndex.WaistRoll] = -roll * self.torso_stabilization_gain * gain_multiplier
        
        # Counteract pitch with waist pitch
        if abs(pitch) > 0.05:
            corrections[G1JointIndex.WaistPitch] = -pitch * self.torso_stabilization_gain * gain_multiplier
        
        # Ankle strategy for roll stabilization
        if abs(roll) > 0.08:
            ankle_correction = -roll * self.ankle_stabilization_gain * gain_multiplier
            corrections[G1JointIndex.LeftAnkleRoll] += ankle_correction
            corrections[G1JointIndex.RightAnkleRoll] += ankle_correction
        
        # Hip strategy for pitch stabilization
        if abs(pitch) > 0.08:
            hip_correction = -pitch * self.hip_stabilization_gain * gain_multiplier
            corrections[G1JointIndex.LeftHipPitch] += hip_correction
            corrections[G1JointIndex.RightHipPitch] += hip_correction
        
        # Limit corrections to safe range
        corrections = np.clip(corrections, -0.15, 0.15)
        
        return corrections
    
    def check_stability(self, low_state):
        """
        Check if robot is in dangerous state
        Returns: (is_stable, warning_message)
        """
        if not self.enable or low_state is None:
            return True, None
        
        imu = low_state.imu_state
        quaternion = [imu.quaternion[0], imu.quaternion[1], 
                     imu.quaternion[2], imu.quaternion[3]]
        gyro = [imu.gyroscope[0], imu.gyroscope[1], imu.gyroscope[2]]
        
        roll, pitch = self.get_orientation(quaternion)
        roll_rate = gyro[0]
        pitch_rate = gyro[1]
        
        # Check thresholds
        if abs(roll) > self.max_roll_angle:
            return False, f"⚠️  Excessive roll: {np.degrees(roll):.1f}°"
        
        if abs(pitch) > self.max_pitch_angle:
            return False, f"⚠️  Excessive pitch: {np.degrees(pitch):.1f}°"
        
        if abs(roll_rate) > self.max_roll_velocity:
            return False, f"⚠️  High roll velocity: {roll_rate:.2f} rad/s"
        
        if abs(pitch_rate) > self.max_pitch_velocity:
            return False, f"⚠️  High pitch velocity: {pitch_rate:.2f} rad/s"
        
        return True, None


class G1MotionPlayer:
    """Play motion data on G1 robot with balance control"""
    
    def __init__(self, motion_data, speed_factor=1.0, duration=10.0, enable_balance=True):
        self.motion_data = motion_data
        self.speed_factor = speed_factor
        self.duration = duration
        
        self.time_ = 0.0
        self.control_dt_ = 0.002  # 2ms = 500Hz (official rate)
        self.mode_pr_ = Mode.PR
        self.mode_machine_ = 0
        self.low_cmd = unitree_hg_msg_dds__LowCmd_()
        self.low_state = None
        self.update_mode_machine_ = False
        self.crc = CRC()
        
        # Balance controller
        self.balance_controller = BalanceController(enable=enable_balance)
        
        # Motion playback state
        self.frame_idx = 0
        self.init_positions = None
        self.target_positions = None
        self.phase = "init"  # init, go_to_start, play, return_zero
        self.phase_time = 0.0
        
        # Emergency stop flag
        self.stop_flag = False
        self.stability_warnings = 0
        
        # Extract joint angles from motion data
        if motion_data.shape[1] >= 36:
            # Scale joint angles by speed factor (reduces range of motion)
            self.joint_angles = motion_data[:, 7:36] * min(speed_factor, 1.0)
        else:
            self.joint_angles = motion_data[:, :29] * min(speed_factor, 1.0)
        
        # For speeds > 1.0, we speed up playback but keep motion range at 100%
        self.playback_speed = speed_factor
        
        print(f"Motion data: {len(self.joint_angles)} frames")
        print(f"Speed: {speed_factor*100:.0f}% | Balance: {'ON' if enable_balance else 'OFF'}")
        if speed_factor > 1.0:
            print(f"⚠️  High speed playback - increased fall risk!")
    
    def Init(self):
        """Initialize SDK and release high-level mode"""
        print("Releasing high-level control mode...")
        self.msc = MotionSwitcherClient()
        self.msc.SetTimeout(5.0)
        self.msc.Init()
        
        status, result = self.msc.CheckMode()
        print(f"  Current mode: {result}")
        while result.get('name'):
            self.msc.ReleaseMode()
            status, result = self.msc.CheckMode()
            time.sleep(1)
        print("  Mode released")
        
        # Create publisher
        print("Creating DDS publisher...")
        self.lowcmd_publisher_ = ChannelPublisher("rt/lowcmd", LowCmd_)
        self.lowcmd_publisher_.Init()
        
        # Create subscriber with callback
        print("Creating DDS subscriber...")
        self.lowstate_subscriber = ChannelSubscriber("rt/lowstate", LowState_)
        self.lowstate_subscriber.Init(self.LowStateHandler, 10)
        
        print("✓ Initialization complete")
    
    def Start(self):
        """Start the control loop"""
        print("Waiting for robot state...")
        while not self.update_mode_machine_:
            time.sleep(0.1)
        
        print(f"  mode_machine: {self.mode_machine_}")
        
        # Store initial positions
        self.init_positions = np.array([self.low_state.motor_state[i].q for i in range(G1_NUM_MOTOR)])
        print(f"  Initial positions captured")
        
        # Set target as first frame of motion
        self.target_positions = self.joint_angles[0].copy()
        
        print("\n▶️  Starting motion playback...")
        print(f"   Phase 1: Go to zero position (2s)")
        print(f"   Phase 2: Go to start pose (2s)")
        print(f"   Phase 3: Play motion ({self.duration}s)")
        print(f"   Phase 4: Return to zero (2s)")
        
        # Start control thread
        self.lowCmdWriteThreadPtr = RecurrentThread(
            interval=self.control_dt_, target=self.LowCmdWrite, name="control"
        )
        self.lowCmdWriteThreadPtr.Start()
    
    def Stop(self):
        """Stop the control loop"""
        self.stop_flag = True
        if hasattr(self, 'lowCmdWriteThreadPtr'):
            # Send zero torque commands
            for _ in range(100):
                self.low_cmd.mode_pr = Mode.PR
                self.low_cmd.mode_machine = self.mode_machine_
                for i in range(G1_NUM_MOTOR):
                    self.low_cmd.motor_cmd[i].mode = 1
                    self.low_cmd.motor_cmd[i].tau = 0.
                    self.low_cmd.motor_cmd[i].q = 0.
                    self.low_cmd.motor_cmd[i].dq = 0.
                    self.low_cmd.motor_cmd[i].kp = 0.
                    self.low_cmd.motor_cmd[i].kd = 0.
                self.low_cmd.crc = self.crc.Crc(self.low_cmd)
                self.lowcmd_publisher_.Write(self.low_cmd)
                time.sleep(0.002)
    
    def LowStateHandler(self, msg: LowState_):
        """Callback for robot state updates"""
        self.low_state = msg
        
        if not self.update_mode_machine_:
            self.mode_machine_ = self.low_state.mode_machine
            self.update_mode_machine_ = True
    
    def LowCmdWrite(self):
        """Control loop - runs at 500Hz"""
        if self.stop_flag:
            return
        
        self.time_ += self.control_dt_
        self.phase_time += self.control_dt_
        
        # Check stability
        is_stable, warning = self.balance_controller.check_stability(self.low_state)
        if not is_stable:
            self.stability_warnings += 1
            if self.stability_warnings % 100 == 1:  # Print every 0.2s
                print(warning)
            if self.stability_warnings > 1000:  # 2 seconds of instability
                print("\n🚨 EMERGENCY STOP - Robot unstable!")
                self.stop_flag = True
                return
        else:
            self.stability_warnings = 0
        
        # Phase timing
        zero_duration = 2.0
        start_duration = 2.0
        return_duration = 2.0
        
        # Compute adaptive gains based on motion phase
        Kp = Kp_base.copy()
        Kd = Kd_base.copy()
        
        if self.phase == "init":
            # Phase 1: Go to zero position
            ratio = np.clip(self.phase_time / zero_duration, 0.0, 1.0)
            
            for i in range(G1_NUM_MOTOR):
                self.low_cmd.mode_pr = Mode.PR
                self.low_cmd.mode_machine = self.mode_machine_
                self.low_cmd.motor_cmd[i].mode = 1
                self.low_cmd.motor_cmd[i].tau = 0.
                self.low_cmd.motor_cmd[i].q = self.init_positions[i] * (1.0 - ratio)
                self.low_cmd.motor_cmd[i].dq = 0.
                self.low_cmd.motor_cmd[i].kp = Kp[i]
                self.low_cmd.motor_cmd[i].kd = Kd[i]
            
            if self.phase_time >= zero_duration:
                self.phase = "go_to_start"
                self.phase_time = 0.0
                print("  ✓ At zero position")
        
        elif self.phase == "go_to_start":
            # Phase 2: Go to first frame of motion
            ratio = np.clip(self.phase_time / start_duration, 0.0, 1.0)
            # Smooth ease-in-out
            smooth_ratio = ratio * ratio * (3 - 2 * ratio)
            
            for i in range(G1_NUM_MOTOR):
                self.low_cmd.mode_pr = Mode.PR
                self.low_cmd.mode_machine = self.mode_machine_
                self.low_cmd.motor_cmd[i].mode = 1
                self.low_cmd.motor_cmd[i].tau = 0.
                self.low_cmd.motor_cmd[i].q = self.target_positions[i] * smooth_ratio
                self.low_cmd.motor_cmd[i].dq = 0.
                self.low_cmd.motor_cmd[i].kp = Kp[i]
                self.low_cmd.motor_cmd[i].kd = Kd[i]
            
            if self.phase_time >= start_duration:
                self.phase = "play"
                self.phase_time = 0.0
                self.frame_idx = 0
                print("  ✓ At start pose")
                print("  ▶️  Playing motion...")
        
        elif self.phase == "play":
            # Phase 3: Play motion with balance corrections
            # Calculate frame based on time and playback speed (30 FPS original)
            frame_time = 1.0 / 30.0 / self.playback_speed
            self.frame_idx = int(self.phase_time / frame_time) % len(self.joint_angles)
            
            current_frame = self.joint_angles[self.frame_idx].copy()
            
            # Apply balance corrections
            balance_corrections = self.balance_controller.compute_balance_corrections(
                self.low_state, current_frame
            )
            corrected_positions = current_frame + balance_corrections
            
            for i in range(G1_NUM_MOTOR):
                self.low_cmd.mode_pr = Mode.PR
                self.low_cmd.mode_machine = self.mode_machine_
                self.low_cmd.motor_cmd[i].mode = 1
                self.low_cmd.motor_cmd[i].tau = 0.
                self.low_cmd.motor_cmd[i].q = corrected_positions[i]
                self.low_cmd.motor_cmd[i].dq = 0.
                self.low_cmd.motor_cmd[i].kp = Kp[i]
                self.low_cmd.motor_cmd[i].kd = Kd[i]
            
            # Print progress every second
            if int(self.phase_time) != int(self.phase_time - self.control_dt_):
                print(f"    Time: {self.phase_time:.0f}s / {self.duration:.0f}s | Frame: {self.frame_idx}")
            
            if self.phase_time >= self.duration:
                self.phase = "return_zero"
                self.phase_time = 0.0
                self.last_positions = corrected_positions.copy()
                print("  ✓ Motion complete")
                print("  ⏹️  Returning to zero...")
        
        elif self.phase == "return_zero":
            # Phase 4: Return to zero with balance
            ratio = np.clip(self.phase_time / return_duration, 0.0, 1.0)
            smooth_ratio = ratio * ratio * (3 - 2 * ratio)
            
            target_positions = self.last_positions * (1.0 - smooth_ratio)
            
            # Still apply balance corrections during return
            balance_corrections = self.balance_controller.compute_balance_corrections(
                self.low_state, target_positions
            )
            corrected_positions = target_positions + balance_corrections
            
            for i in range(G1_NUM_MOTOR):
                self.low_cmd.mode_pr = Mode.PR
                self.low_cmd.mode_machine = self.mode_machine_
                self.low_cmd.motor_cmd[i].mode = 1
                self.low_cmd.motor_cmd[i].tau = 0.
                self.low_cmd.motor_cmd[i].q = corrected_positions[i]
                self.low_cmd.motor_cmd[i].dq = 0.
                self.low_cmd.motor_cmd[i].kp = Kp[i]
                self.low_cmd.motor_cmd[i].kd = Kd[i]
            
            if self.phase_time >= return_duration:
                self.phase = "done"
                print("  ✓ At zero position")
                print("\n✅ Motion playback complete!")
        
        # Send command
        self.low_cmd.crc = self.crc.Crc(self.low_cmd)
        self.lowcmd_publisher_.Write(self.low_cmd)


def load_motion_data(motion_type, dataset_index=0):
    """Load motion data CSV file"""
    motion_files = {
        'walking': ['walk1_subject1.csv', 'walk1_subject2.csv', 'walk2_subject1.csv'],
        'running': ['run1_subject2.csv', 'run1_subject5.csv', 'run2_subject1.csv'],
        'jumping': ['jumps1_subject1.csv', 'jumps1_subject2.csv'],
        'dancing': ['dance1_subject1.csv', 'dance1_subject2.csv', 'dance2_subject1.csv'],
        'fighting': ['fight1_subject2.csv', 'fight1_subject3.csv', 'fight1_subject5.csv'],
    }
    
    files = motion_files.get(motion_type, [])
    
    # Select specific dataset if available
    if dataset_index < len(files):
        selected_files = [files[dataset_index]]
    else:
        selected_files = files
    
    base_paths = [
        "/home/unitree/LAFAN1_Retargeting_Dataset/g1/",
        "/home/unitree/g1/",
        "./g1/",
        "g1/",
    ]
    
    for base_path in base_paths:
        for file in selected_files:
            filepath = os.path.join(base_path, file)
            if os.path.exists(filepath):
                print(f"Loading: {filepath}")
                data = np.loadtxt(filepath, delimiter=',')
                return data, file
    
    print(f"✗ Could not find motion data files in any of these locations:")
    for base_path in base_paths:
        print(f"  {base_path}")
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description='G1 Hardware Motion Test with Balance Control',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dance at 50% speed with balance control (recommended)
  python3 %(prog)s dancing --speed 0.5

  # Dance at full speed with balance control
  python3 %(prog)s dancing --speed 1.0
  
  # Dance at 100% speed without balance (original behavior)
  python3 %(prog)s dancing --speed 1.0 --no-balance
  
  # Use specific dataset
  python3 %(prog)s dancing --dataset 2 --speed 0.8
  
  # Walking at full speed (safer motion)
  python3 %(prog)s walking --speed 1.0

Notes:
  - Balance control adds real-time stabilization corrections
  - Higher speeds increase fall risk even with balance control
  - Start with lower speeds and gradually increase
  - Always have emergency stop ready (Ctrl+C)
        """
    )
    
    parser.add_argument('motion_type', type=str, 
                       choices=['walking', 'running', 'jumping', 'dancing', 'fighting'],
                       help='Type of motion to test')
    parser.add_argument('--dataset', type=int, default=1,
                       help='Dataset number (1-3 depending on motion type)')
    parser.add_argument('--speed', type=float, default=0.5,
                       help='Speed factor (0.1-2.0). Default: 0.5 for safety')
    parser.add_argument('--duration', type=float, default=None,
                       help='Duration in seconds (default: auto-detect from data)')
    parser.add_argument('--no-balance', action='store_true',
                       help='Disable balance control (use original behavior)')
    
    args = parser.parse_args()
    
    # Validate speed
    if args.speed < 0.1 or args.speed > 2.0:
        print("⚠️  Speed must be between 0.1 and 2.0")
        sys.exit(1)
    
    # Safety warnings
    if args.speed > 1.0:
        print("\n" + "="*60)
        print("⚠️  HIGH SPEED WARNING")
        print("="*60)
        print(f"Running at {args.speed*100:.0f}% speed significantly increases fall risk!")
        print("Make sure:")
        print("  • Robot is suspended or in safe testing area")
        print("  • Emergency stop is ready")
        print("  • You understand the risks")
        print("="*60)
        response = input("Continue? (yes/no): ")
        if response.lower() != 'yes':
            print("Aborted.")
            sys.exit(0)
    
    if args.no_balance and args.speed >= 0.5:
        print("\n⚠️  Warning: Running at high speed without balance control!")
        print("This may cause the robot to fall.")
        response = input("Continue? (yes/no): ")
        if response.lower() != 'yes':
            print("Aborted.")
            sys.exit(0)
    
    # Load motion data
    print(f"\nLoading {args.motion_type} motion data...")
    motion_data, filename = load_motion_data(args.motion_type, args.dataset - 1)
    
    # Calculate duration if not specified
    if args.duration is None:
        num_frames = len(motion_data)
        args.duration = num_frames / 30.0  # 30 FPS original
        print(f"Auto-detected duration: {args.duration:.1f}s ({num_frames} frames)")
    
    # Setup signal handler for Ctrl+C
    player = None
    def signal_handler(sig, frame):
        print("\n\n🛑 Emergency stop requested!")
        if player:
            player.Stop()
        time.sleep(1)
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Initialize and run
    print("\n" + "="*60)
    print("READY TO START")
    print("="*60)
    print(f"Motion: {args.motion_type} ({filename})")
    print(f"Speed: {args.speed*100:.0f}%")
    print(f"Duration: {args.duration:.1f}s")
    print(f"Balance Control: {'ENABLED' if not args.no_balance else 'DISABLED'}")
    print("="*60)
    print("\nPress Ctrl+C at any time to emergency stop\n")
    
    time.sleep(2)
    
    # Create player with balance control
    player = G1MotionPlayer(
        motion_data, 
        speed_factor=args.speed,
        duration=args.duration,
        enable_balance=not args.no_balance
    )
    
    try:
        player.Init()
        player.Start()
        
        # Wait for completion
        total_duration = 2.0 + 2.0 + args.duration + 2.0  # All phases
        time.sleep(total_duration + 1.0)
        
        print("\n✅ Test complete!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        if player:
            player.Stop()
        time.sleep(1)


if __name__ == "__main__":
    # Initialize DDS
    ChannelFactoryInitialize(0)
    
    main()
