#!/usr/bin/env python3
"""
Quick G1 Hardware Test Script - Run directly on Jetson
Tests motion data playback on real Unitree G1 robot.

Based on official g1_low_level_example.py from Unitree SDK2.

Usage on Jetson:
    export CYCLONEDDS_HOME=/home/unitree/Documents/GitHub/cyclonedds/install
    export LD_LIBRARY_PATH=$CYCLONEDDS_HOME/lib:$LD_LIBRARY_PATH
    export PYTHONPATH=/home/unitree/unitree_sdk2_python:$PYTHONPATH
    
    python3 quick_hardware_test_jetson.py walking
    python3 quick_hardware_test_jetson.py running
    python3 quick_hardware_test_jetson.py jumping
    python3 quick_hardware_test_jetson.py dancing

Press Ctrl+C to emergency stop at any time.
"""

import sys
import os
import time
import numpy as np
import signal

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

# Per-joint gains from official g1_low_level_example.py
Kp = [
    60, 60, 60, 100, 40, 40,      # left leg (0-5)
    60, 60, 60, 100, 40, 40,      # right leg (6-11)
    60, 40, 40,                   # waist (12-14)
    40, 40, 40, 40, 40, 40, 40,   # left arm (15-21)
    40, 40, 40, 40, 40, 40, 40    # right arm (22-28)
]

Kd = [
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


class G1MotionPlayer:
    """Play motion data on G1 robot using official SDK pattern"""
    
    def __init__(self, motion_data, speed_factor=0.1, duration=10.0):
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
        
        # Motion playback state
        self.frame_idx = 0
        self.init_positions = None
        self.target_positions = None
        self.phase = "init"  # init, go_to_start, play, return_zero
        self.phase_time = 0.0
        
        # Emergency stop flag
        self.stop_flag = False
        
        # Extract joint angles from motion data
        if motion_data.shape[1] >= 36:
            self.joint_angles = motion_data[:, 7:36] * speed_factor
        else:
            self.joint_angles = motion_data[:, :29] * speed_factor
        
        print(f"Motion data: {len(self.joint_angles)} frames, speed={speed_factor*100:.0f}%")
    
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
        
        # Phase timing
        zero_duration = 2.0
        start_duration = 2.0
        return_duration = 2.0
        
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
            # Phase 3: Play motion
            # Calculate frame based on time (30 FPS original)
            frame_time = 1.0 / 30.0
            self.frame_idx = int(self.phase_time / frame_time) % len(self.joint_angles)
            
            current_frame = self.joint_angles[self.frame_idx]
            
            for i in range(G1_NUM_MOTOR):
                self.low_cmd.mode_pr = Mode.PR
                self.low_cmd.mode_machine = self.mode_machine_
                self.low_cmd.motor_cmd[i].mode = 1
                self.low_cmd.motor_cmd[i].tau = 0.
                self.low_cmd.motor_cmd[i].q = current_frame[i]
                self.low_cmd.motor_cmd[i].dq = 0.
                self.low_cmd.motor_cmd[i].kp = Kp[i]
                self.low_cmd.motor_cmd[i].kd = Kd[i]
            
            # Print progress every second
            if int(self.phase_time) != int(self.phase_time - self.control_dt_):
                print(f"    Time: {self.phase_time:.0f}s / {self.duration:.0f}s | Frame: {self.frame_idx}")
            
            if self.phase_time >= self.duration:
                self.phase = "return_zero"
                self.phase_time = 0.0
                self.last_positions = current_frame.copy()
                print("  ✓ Motion complete")
                print("  ⏹️  Returning to zero...")
        
        elif self.phase == "return_zero":
            # Phase 4: Return to zero
            ratio = np.clip(self.phase_time / return_duration, 0.0, 1.0)
            smooth_ratio = ratio * ratio * (3 - 2 * ratio)
            
            for i in range(G1_NUM_MOTOR):
                self.low_cmd.mode_pr = Mode.PR
                self.low_cmd.mode_machine = self.mode_machine_
                self.low_cmd.motor_cmd[i].mode = 1
                self.low_cmd.motor_cmd[i].tau = 0.
                self.low_cmd.motor_cmd[i].q = self.last_positions[i] * (1.0 - smooth_ratio)
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
        for filename in selected_files:
            path = os.path.join(base_path, filename)
            if os.path.exists(path):
                print(f"Loading motion data from: {path}")
                data = np.loadtxt(path, delimiter=',', skiprows=1)
                print(f"  Shape: {data.shape}")
                print(f"  Frames: {len(data)}")
                return data
    
    print(f"✗ Could not find motion data for '{motion_type}'")
    print("  Tried paths:", base_paths)
    return None


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python3 quick_hardware_test_jetson.py <motion_type> [duration] [--full] [--dataset N]")
        print("  Motion types: walking, running, jumping, dancing")
        print("  --full: Use 100% amplitude (DANGEROUS - use with caution!)")
        print("  --dataset N: Select dataset 1, 2, or 3 (default: 1)")
        print("\nExample:")
        print("  python3 quick_hardware_test_jetson.py walking")
        print("  python3 quick_hardware_test_jetson.py dancing 20")
        print("  python3 quick_hardware_test_jetson.py dancing --dataset 2  # dance1_subject2")
        print("  python3 quick_hardware_test_jetson.py walking --full  # 100% amplitude!")
        sys.exit(1)
    
    motion_type = sys.argv[1].lower()
    
    valid_motions = ['walking', 'running', 'jumping', 'dancing']
    if motion_type not in valid_motions:
        print(f"Unknown motion type: {motion_type}")
        print(f"Valid types: {valid_motions}")
        sys.exit(1)
    
    # Check for --full flag
    full_amplitude = '--full' in sys.argv
    
    # Check for --dataset flag
    dataset_index = 0
    if '--dataset' in sys.argv:
        idx = sys.argv.index('--dataset')
        if idx + 1 < len(sys.argv):
            try:
                dataset_index = int(sys.argv[idx + 1]) - 1  # Convert to 0-based
            except ValueError:
                pass
    
    # Speed factors (amplitude scaling, not time)
    # Higher = more movement (but stay conservative for safety)
    if full_amplitude:
        speed = 1.0  # 100% amplitude - FULL MOTION
        print("\n" + "="*60)
        print("⚠️  WARNING: FULL AMPLITUDE MODE (100%)")
        print("="*60)
        print("🚨 This uses FULL human motion capture amplitude!")
        print("🚨 Robot may move violently or lose balance!")
        print("🚨 Ensure:")
        print("   • Robot is secure and stable")
        print("   • Area is completely clear")
        print("   • You can reach emergency stop immediately")
        print("="*60)
    else:
        speed_factors = {
            'walking': 0.30,    # 30% amplitude
            'running': 0.20,    # 20% amplitude
            'jumping': 0.15,    # 15% amplitude
            'dancing': 0.25,    # 25% amplitude
        }
        speed = speed_factors.get(motion_type, 0.1)
    
    # Duration
    duration = 10.0
    if len(sys.argv) >= 3 and sys.argv[2] != '--full':
        try:
            duration = float(sys.argv[2])
        except ValueError:
            pass
    
    # If --full, offer to use full dataset duration
    if full_amplitude:
        # Load to check duration
        motion_data = load_motion_data(motion_type, dataset_index)
        if motion_data is not None:
            full_duration = len(motion_data) / 30.0
            print(f"\n💡 Full dataset duration: {full_duration:.1f}s")
            print(f"   Currently set to: {duration}s")
            response = input(f"   Use full duration? (y/n): ")
            if response.lower() == 'y':
                duration = full_duration
    
    print(f"\n{'='*60}")
    print(f"G1 HARDWARE TEST: {motion_type.upper()}")
    print(f"Speed: {speed*100:.0f}% | Duration: {duration}s")
    if full_amplitude:
        print(f"⚠️  MODE: FULL AMPLITUDE (100%)")
    else:
        print(f"✅ MODE: HARDWARE SAFE")
    print(f"Press Ctrl+C to EMERGENCY STOP")
    print(f"{'='*60}\n")
    
    # Load motion data
    motion_data = load_motion_data(motion_type, dataset_index)
    if motion_data is None:
        sys.exit(1)
    
    # Safety check
    print("\n⚠️  SAFETY CHECK")
    print("  - Robot should be standing")
    print("  - Area should be clear")
    print("  - Be ready to press Ctrl+C")
    input("\nPress Enter to start (or Ctrl+C to abort)...")
    
    # Initialize SDK
    print("\nInitializing SDK...")
    ChannelFactoryInitialize(0)
    
    # Create player
    player = G1MotionPlayer(motion_data, speed_factor=speed, duration=duration)
    
    # Handle Ctrl+C
    def signal_handler(signum, frame):
        print("\n\n🛑 EMERGENCY STOP!")
        player.Stop()
        sys.exit(0)
    
    signal.signal(signal.SIGINT, signal_handler)
    
    # Initialize and start
    player.Init()
    player.Start()
    
    # Wait for completion
    while player.phase != "done":
        time.sleep(0.1)
    
    time.sleep(1)
    print("\nExiting...")


if __name__ == "__main__":
    main()
