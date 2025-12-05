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
    from unitree_sdk2py.core.channel import ChannelFactoryInitialize
    from unitree_sdk2py.g1.loco.g1_loco_client import LocoClient
    from unitree_sdk2py.g1.low_level.g1_low_level_control import G1LowLevelControl
    from unitree_sdk2py.idl.unitree_hg.msg.dds_ import LowCmd_
    from unitree_sdk2py.utils.crc import CRC
    from unitree_sdk2py.g1.motion_switcher.g1_motion_switcher_client import MotionSwitcherClient
    print("✓ Unitree SDK2 Python imported successfully")
except ImportError as e:
    print(f"✗ Failed to import SDK: {e}")
    print("\nMake sure you're on the Jetson with:")
    print("  export PYTHONPATH=/home/unitree/unitree_sdk2_python:$PYTHONPATH")
    sys.exit(1)

# Per-joint gains from SDK example
G1_KP = [
    60, 60, 60, 100, 40, 40,    # Left leg (0-5)
    60, 60, 60, 100, 40, 40,    # Right leg (6-11)
    60, 40, 40,                  # Waist (12-14)
    40, 40, 40, 40, 40, 40, 40, # Left arm (15-21)
    40, 40, 40, 40, 40, 40, 40  # Right arm (22-28)
]

G1_KD = [
    1, 1, 1, 2, 1, 1,    # Left leg
    1, 1, 1, 2, 1, 1,    # Right leg
    1, 1, 1,              # Waist
    1, 1, 1, 1, 1, 1, 1, # Left arm
    1, 1, 1, 1, 1, 1, 1  # Right arm
]


class G1HardwareController:
    """Direct hardware control for G1 robot"""
    
    def __init__(self):
        global _global_controller
        self.crc = CRC()
        
        # Initialize SDK
        print("Initializing SDK channel...")
        ChannelFactoryInitialize(0, "enp3s0")  # G1's network interface
        time.sleep(0.5)
        
        # Release AI mode first using MotionSwitcherClient
        print("Releasing AI mode...")
        try:
            self.motion_switcher = MotionSwitcherClient()
            self.motion_switcher.SetTimeout(3.0)
            self.motion_switcher.Init()
            
            # Check current mode
            status, result = self.motion_switcher.CheckMode()
            print(f"Current mode: {result}")
            
            # Release any existing mode
            release_status, release_result = self.motion_switcher.ReleaseMode()
            print(f"Release mode result: {release_result}")
            time.sleep(0.5)
        except Exception as e:
            print(f"Warning: Could not release mode: {e}")
        
        # Create low-level control
        print("Creating low-level control...")
        self.low_level = G1LowLevelControl()
        self.low_level.Init()
        
        # Get publisher for motor commands
        self.motor_cmd_pub = self.low_level.motor_cmd_puber
        self.motor_state_sub = self.low_level.lowstate_suber
        
        # Store reference for emergency stop
        _global_controller = self
        
        print("✓ Hardware controller initialized")
    
    def _create_motor_cmd(self):
        """Create a motor command message"""
        msg = LowCmd_()
        msg.mode_pr = 0
        msg.mode_machine = 5  # G1 mode
        return msg
    
    def get_current_positions(self):
        """Get current joint positions from robot"""
        state = self.low_level.GetMotorState()
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
                msg.motor_cmd[i].mode = 1
                msg.motor_cmd[i].q = float(current_target[i])
                msg.motor_cmd[i].dq = 0.0
                msg.motor_cmd[i].tau = 0.0
                msg.motor_cmd[i].kp = float(G1_KP[i])
                msg.motor_cmd[i].kd = float(G1_KD[i])
            
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
                msg.motor_cmd[i].mode = 1
                msg.motor_cmd[i].q = float(current_target[i])
                msg.motor_cmd[i].dq = 0.0
                msg.motor_cmd[i].tau = 0.0
                msg.motor_cmd[i].kp = float(G1_KP[i])
                msg.motor_cmd[i].kd = float(G1_KD[i])
            
            msg.crc = self.crc.Crc(msg)
            self.motor_cmd_pub.Write(msg)
            time.sleep(0.02)
        
        print("✓ At start pose")
        return True
    
    def send_position_command(self, positions):
        """Send position command to all joints"""
        msg = self._create_motor_cmd()
        
        for i in range(29):
            msg.motor_cmd[i].mode = 1
            msg.motor_cmd[i].q = float(positions[i])
            msg.motor_cmd[i].dq = 0.0
            msg.motor_cmd[i].tau = 0.0
            msg.motor_cmd[i].kp = float(G1_KP[i])
            msg.motor_cmd[i].kd = float(G1_KD[i])
        
        msg.crc = self.crc.Crc(msg)
        self.motor_cmd_pub.Write(msg)


def load_motion_data(motion_type):
    """Load motion data CSV file"""
    # Try different possible locations
    possible_paths = [
        f"/home/unitree/LAFAN1_Retargeting_Dataset/g1/{motion_type}_g1.csv",
        f"/home/unitree/g1/{motion_type}_g1.csv",
        f"./g1/{motion_type}_g1.csv",
        f"g1/{motion_type}_g1.csv",
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            print(f"Loading motion data from: {path}")
            data = np.loadtxt(path, delimiter=',', skiprows=1)
            print(f"  Shape: {data.shape}")
            print(f"  Frames: {len(data)}")
            return data
    
    print(f"✗ Could not find motion data for '{motion_type}'")
    print("  Tried paths:", possible_paths)
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
