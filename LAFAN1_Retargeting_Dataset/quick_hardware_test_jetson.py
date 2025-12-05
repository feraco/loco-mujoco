#!/usr/bin/env python3
"""
Quick G1 Hardware Test Script - Run directly on Jetson
Tests motion data playback on real Unitree G1 robot.

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

# Global variables for emergency stop
_stop_flag = False
_global_controller = None

def signal_handler(signum, frame):
    """Handle Ctrl+C for emergency stop"""
    global _stop_flag, _global_controller
    print("\n\n🛑 EMERGENCY STOP - Ctrl+C detected!")
    _stop_flag = True
    
    if _global_controller is not None:
        print("Sending zero torque commands...")
        try:
            # Send zero commands to stop robot
            msg = _global_controller._create_motor_cmd()
            for i in range(29):
                msg.motor_cmd[i].mode = 1
                msg.motor_cmd[i].q = 0.0
                msg.motor_cmd[i].dq = 0.0
                msg.motor_cmd[i].tau = 0.0
                msg.motor_cmd[i].kp = 0.0
                msg.motor_cmd[i].kd = 0.0
            _global_controller.motor_cmd_pub.Write(msg)
            time.sleep(0.1)
            _global_controller.motor_cmd_pub.Write(msg)
        except Exception as e:
            print(f"Error sending stop command: {e}")
    
    print("Robot should be stopped. Exiting...")
    sys.exit(0)

# Register signal handler
signal.signal(signal.SIGINT, signal_handler)

# Add SDK to path
sys.path.insert(0, '/home/unitree/unitree_sdk2_python')

try:
    from unitree_sdk2py.core.channel import ChannelPublisher, ChannelSubscriber, ChannelFactoryInitialize
    from unitree_sdk2py.idl.unitree_hg.msg.dds_ import LowCmd_ as hg_LowCmd, LowState_ as hg_LowState
    from unitree_sdk2py.idl.default import unitree_hg_msg_dds__LowCmd_
    from unitree_sdk2py.utils.crc import CRC
    from unitree_sdk2py.comm.motion_switcher.motion_switcher_client import MotionSwitcherClient
    import threading
    print("✓ Unitree SDK2 Python imported successfully")
except ImportError as e:
    print(f"✗ Failed to import SDK: {e}")
    print("\nMake sure you're on the Jetson with:")
    print("  export PYTHONPATH=/home/unitree/unitree_sdk2_python:$PYTHONPATH")
    sys.exit(1)

# DDS Topics
kTopicLowCommand = "rt/lowcmd"
kTopicLowState = "rt/lowstate"

# Gains from xr_teleoperate - use higher gains for legs
KP_HIGH = 300.0  # For legs
KP_LOW = 80.0    # For arms and weak joints
KD_HIGH = 3.0
KD_LOW = 3.0

# Per-joint gains based on G1 structure
# Joints 0-11: Legs (high gains)
# Joints 12-14: Waist (low gains - weak motors)
# Joints 15-28: Arms (low gains)
def get_joint_gains(joint_idx):
    if joint_idx < 12:  # Legs
        return KP_HIGH, KD_HIGH
    else:  # Waist and arms
        return KP_LOW, KD_LOW


class DataBuffer:
    """Thread-safe data buffer"""
    def __init__(self):
        self.data = None
        self.lock = threading.Lock()

    def GetData(self):
        with self.lock:
            return self.data

    def SetData(self, data):
        with self.lock:
            self.data = data


class G1HardwareController:
    """Direct hardware control for G1 robot using DDS"""
    
    def __init__(self):
        global _global_controller
        self.crc = CRC()
        
        # Initialize SDK
        print("Initializing SDK channel...")
        ChannelFactoryInitialize(0)  # 0 for real robot
        time.sleep(0.5)
        
        # Release any high-level mode (ai, normal, etc) to allow low-level control
        print("Releasing high-level control mode...")
        try:
            self.motion_switcher = MotionSwitcherClient()
            self.motion_switcher.SetTimeout(5.0)
            self.motion_switcher.Init()
            
            # Check current mode
            code, mode_info = self.motion_switcher.CheckMode()
            print(f"  Current mode: {mode_info}")
            
            # Release the mode
            release_code, _ = self.motion_switcher.ReleaseMode()
            print(f"  Release result: code={release_code}")
            time.sleep(1.0)  # Give time for mode to release
        except Exception as e:
            print(f"  Warning: Could not release mode: {e}")
        
        # Create publisher and subscriber
        print("Creating DDS publisher/subscriber...")
        self.motor_cmd_pub = ChannelPublisher(kTopicLowCommand, hg_LowCmd)
        self.motor_cmd_pub.Init()
        
        self.lowstate_subscriber = ChannelSubscriber(kTopicLowState, hg_LowState)
        self.lowstate_subscriber.Init()
        
        self.lowstate_buffer = DataBuffer()
        
        # Start subscriber thread
        self.subscribe_thread = threading.Thread(target=self._subscribe_motor_state)
        self.subscribe_thread.daemon = True
        self.subscribe_thread.start()
        
        # Wait for first state
        print("Waiting for robot state...")
        timeout = 5.0
        start = time.time()
        while not self.lowstate_buffer.GetData():
            if time.time() - start > timeout:
                print("⚠️  Timeout waiting for robot state - continuing anyway")
                break
            time.sleep(0.1)
        
        # Get mode_machine from robot state (like xr_teleoperate does)
        state = self.lowstate_buffer.GetData()
        if state is not None:
            self.mode_machine = state.mode_machine
            print(f"  Robot mode_machine: {self.mode_machine}")
        else:
            self.mode_machine = 5  # Default for G1
            print(f"  Using default mode_machine: {self.mode_machine}")
        
        # Store reference for emergency stop
        _global_controller = self
        
        print("✓ Hardware controller initialized")
    
    def _subscribe_motor_state(self):
        """Background thread to receive robot state"""
        while True:
            msg = self.lowstate_subscriber.Read()
            if msg is not None:
                self.lowstate_buffer.SetData(msg)
            time.sleep(0.001)
    
    def _create_motor_cmd(self):
        """Create a motor command message"""
        msg = unitree_hg_msg_dds__LowCmd_()
        msg.mode_pr = 0
        msg.mode_machine = self.mode_machine  # Use value from robot
        return msg
    
    def get_current_positions(self):
        """Get current joint positions from robot"""
        state = self.lowstate_buffer.GetData()
        if state is None:
            return np.zeros(29)
        positions = np.array([state.motor_state[i].q for i in range(29)])
        return positions
    
    def go_to_zero(self, duration=3.0):
        """Smoothly move robot to zero position"""
        global _stop_flag
        print(f"Moving to zero position over {duration}s...")
        
        start_pos = self.get_current_positions()
        target_pos = np.zeros(29)
        
        steps = int(duration * 50)  # 50 Hz
        
        for step in range(steps):
            if _stop_flag:
                return False
                
            t = step / steps
            # Smooth interpolation
            smooth_t = t * t * (3 - 2 * t)
            
            current_target = start_pos + (target_pos - start_pos) * smooth_t
            
            msg = self._create_motor_cmd()
            for i in range(29):
                kp, kd = get_joint_gains(i)
                msg.motor_cmd[i].mode = 1
                msg.motor_cmd[i].q = float(current_target[i])
                msg.motor_cmd[i].dq = 0.0
                msg.motor_cmd[i].tau = 0.0
                msg.motor_cmd[i].kp = kp
                msg.motor_cmd[i].kd = kd
            
            msg.crc = self.crc.Crc(msg)
            self.motor_cmd_pub.Write(msg)
            time.sleep(0.02)
        
        print("✓ At zero position")
        return True
    
    def interpolate_to_pose(self, target_positions, duration=2.0):
        """Smoothly interpolate from current position to target pose"""
        global _stop_flag
        print(f"Smoothly transitioning to start pose over {duration}s...")
        
        start_pos = self.get_current_positions()
        steps = int(duration * 50)  # 50 Hz
        
        for step in range(steps):
            if _stop_flag:
                return False
                
            t = step / steps
            # Very smooth interpolation (ease-in-out)
            smooth_t = t * t * (3 - 2 * t)
            
            current_target = start_pos + (target_positions - start_pos) * smooth_t
            
            msg = self._create_motor_cmd()
            for i in range(29):
                kp, kd = get_joint_gains(i)
                msg.motor_cmd[i].mode = 1
                msg.motor_cmd[i].q = float(current_target[i])
                msg.motor_cmd[i].dq = 0.0
                msg.motor_cmd[i].tau = 0.0
                msg.motor_cmd[i].kp = kp
                msg.motor_cmd[i].kd = kd
            
            msg.crc = self.crc.Crc(msg)
            self.motor_cmd_pub.Write(msg)
            time.sleep(0.02)
        
        print("✓ At start pose")
        return True
    
    def send_position_command(self, positions):
        """Send position command to all joints"""
        msg = self._create_motor_cmd()
        
        for i in range(29):
            kp, kd = get_joint_gains(i)
            msg.motor_cmd[i].mode = 1
            msg.motor_cmd[i].q = float(positions[i])
            msg.motor_cmd[i].dq = 0.0
            msg.motor_cmd[i].tau = 0.0
            msg.motor_cmd[i].kp = kp
            msg.motor_cmd[i].kd = kd
        
        msg.crc = self.crc.Crc(msg)
        self.motor_cmd_pub.Write(msg)


def load_motion_data(motion_type):
    """Load motion data CSV file"""
    # Map motion types to file patterns
    motion_files = {
        'walking': ['walk1_subject1.csv', 'walk1_subject2.csv', 'walk2_subject1.csv'],
        'running': ['run1_subject2.csv', 'run1_subject5.csv', 'run2_subject1.csv'],
        'jumping': ['jumps1_subject1.csv', 'jumps1_subject2.csv'],
        'dancing': ['dance1_subject1.csv', 'dance1_subject2.csv', 'dance2_subject1.csv'],
    }
    
    files = motion_files.get(motion_type, [])
    
    # Try different possible locations
    base_paths = [
        "/home/unitree/LAFAN1_Retargeting_Dataset/g1/",
        "/home/unitree/g1/",
        "./g1/",
        "g1/",
    ]
    
    for base_path in base_paths:
        for filename in files:
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


def run_motion_test(motion_type, speed_factor=0.1, duration=10.0):
    """Run a motion test on the hardware"""
    global _stop_flag
    
    # Motion-specific speed factors (slower = safer)
    speed_factors = {
        'walking': 0.10,    # 10% speed
        'running': 0.05,    # 5% speed  
        'jumping': 0.03,    # 3% speed
        'dancing': 0.02,    # 2% speed (most dynamic)
    }
    
    speed = speed_factors.get(motion_type, speed_factor)
    print(f"\n{'='*60}")
    print(f"G1 HARDWARE TEST: {motion_type.upper()}")
    print(f"Speed: {speed*100:.0f}% | Duration: {duration}s")
    print(f"Press Ctrl+C to EMERGENCY STOP")
    print(f"{'='*60}\n")
    
    # Load motion data
    motion_data = load_motion_data(motion_type)
    if motion_data is None:
        return False
    
    # Extract joint angles (columns 7-35 are the 29 joint angles, not 0-35)
    # Columns 0-6 are root position and orientation
    if motion_data.shape[1] >= 36:
        joint_angles = motion_data[:, 7:36]  # 29 DOF
    else:
        joint_angles = motion_data[:, :29]
    
    print(f"Joint angles shape: {joint_angles.shape}")
    
    # Scale the motion amplitude for safety
    joint_angles_scaled = joint_angles * speed
    
    # Initialize controller
    print("\nInitializing hardware controller...")
    controller = G1HardwareController()
    
    # Safety pause
    print("\n⚠️  SAFETY CHECK")
    print("  - Robot should be standing")
    print("  - Area should be clear")
    print("  - Be ready to press Ctrl+C")
    input("\nPress Enter to start (or Ctrl+C to abort)...")
    
    if _stop_flag:
        return False
    
    # First, go to zero position
    if not controller.go_to_zero(duration=2.0):
        return False
    
    time.sleep(0.5)
    
    # Then smoothly interpolate to first frame of motion
    first_frame = joint_angles_scaled[0]
    if not controller.interpolate_to_pose(first_frame, duration=2.0):
        return False
    
    time.sleep(0.5)
    
    # Play motion
    print(f"\n▶️  Playing {motion_type} motion...")
    
    start_time = time.time()
    frame_idx = 0
    frame_time = 1.0 / 30.0  # Original 30 FPS
    
    try:
        while time.time() - start_time < duration:
            if _stop_flag:
                break
                
            # Get current frame
            frame = joint_angles_scaled[frame_idx % len(joint_angles_scaled)]
            
            # Send command
            controller.send_position_command(frame)
            
            # Progress
            elapsed = time.time() - start_time
            if frame_idx % 30 == 0:  # Print every second
                print(f"  Time: {elapsed:.1f}s / {duration:.1f}s | Frame: {frame_idx}")
            
            # Next frame
            frame_idx += 1
            time.sleep(frame_time)
            
    except Exception as e:
        print(f"\n✗ Error during playback: {e}")
    
    # Return to zero
    print("\n⏹️  Returning to zero position...")
    controller.go_to_zero(duration=2.0)
    
    print(f"\n✅ Test completed: {motion_type}")
    return True


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python3 quick_hardware_test_jetson.py <motion_type>")
        print("  Motion types: walking, running, jumping, dancing")
        print("\nExample:")
        print("  python3 quick_hardware_test_jetson.py walking")
        sys.exit(1)
    
    motion_type = sys.argv[1].lower()
    
    valid_motions = ['walking', 'running', 'jumping', 'dancing']
    if motion_type not in valid_motions:
        print(f"Unknown motion type: {motion_type}")
        print(f"Valid types: {valid_motions}")
        sys.exit(1)
    
    # Optional duration argument
    duration = 10.0
    if len(sys.argv) >= 3:
        try:
            duration = float(sys.argv[2])
        except ValueError:
            pass
    
    success = run_motion_test(motion_type, duration=duration)
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
