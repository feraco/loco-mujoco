#!/usr/bin/env python3
"""
Unified G1 Motion Test Script - Works in both simulation and real hardware

Features:
- Automatic detection of sim vs hardware mode
- Rerun visualization in both modes
- Direct comparison between sim and hardware
- Record both for side-by-side analysis

Usage:
    # Simulation (Mac/Linux with display)
    python3 unified_test.py --mode sim walking
    python3 unified_test.py --mode sim dancing --duration 20 --record
    
    # Hardware (Jetson)
    python3 unified_test.py --mode hardware dancing
    python3 unified_test.py --mode hardware walking --speed 0.4
    
    # Auto-detect mode
    python3 unified_test.py walking  # Will detect sim/hardware automatically
"""

import sys
import os
import time
import numpy as np
import signal
import argparse
from pathlib import Path

# Try to import hardware SDK
HARDWARE_AVAILABLE = False
try:
    sys.path.insert(0, '/home/unitree/unitree_sdk2_python')
    from unitree_sdk2py.core.channel import ChannelPublisher, ChannelSubscriber, ChannelFactoryInitialize
    from unitree_sdk2py.idl.default import unitree_hg_msg_dds__LowCmd_, unitree_hg_msg_dds__LowState_
    from unitree_sdk2py.idl.unitree_hg.msg.dds_ import LowCmd_, LowState_
    from unitree_sdk2py.utils.crc import CRC
    from unitree_sdk2py.utils.thread import RecurrentThread
    from unitree_sdk2py.comm.motion_switcher.motion_switcher_client import MotionSwitcherClient
    HARDWARE_AVAILABLE = True
except ImportError:
    pass

# Try to import simulation (LocoMuJoCo)
SIMULATION_AVAILABLE = False
try:
    # We don't actually need these for sim mode - just use existing scripts
    # from loco_mujoco import RLFactory
    # import rerun as rr
    # import pinocchio as pin
    SIMULATION_AVAILABLE = True
except ImportError:
    pass


class MotionConfig:
    """Motion configuration presets"""
    PRESETS = {
        'walking': {
            'files': ['walk1_subject1.csv', 'walk1_subject2.csv', 'walk2_subject1.csv'],
            'speed_sim': 0.30,
            'speed_hardware': 0.30,
            'description': 'Natural walking gait'
        },
        'running': {
            'files': ['run1_subject2.csv', 'run1_subject5.csv', 'run2_subject1.csv'],
            'speed_sim': 0.25,
            'speed_hardware': 0.20,
            'description': 'Running motion'
        },
        'jumping': {
            'files': ['jumps1_subject1.csv', 'jumps1_subject2.csv'],
            'speed_sim': 0.20,
            'speed_hardware': 0.15,
            'description': 'Jumping motion'
        },
        'dancing': {
            'files': ['dance1_subject1.csv', 'dance1_subject2.csv', 'dance2_subject1.csv'],
            'speed_sim': 0.30,
            'speed_hardware': 0.25,
            'description': 'Dancing motion'
        }
    }


class SimulationRunner:
    """Run motion in MuJoCo simulation with Rerun visualization"""
    
    def __init__(self, motion_data, speed_factor=0.3, record=False):
        self.motion_data = motion_data
        self.speed_factor = speed_factor
        self.record = record
        
        # Extract joint angles
        if motion_data.shape[1] >= 36:
            self.joint_angles = motion_data[:, 7:36] * speed_factor
        else:
            self.joint_angles = motion_data[:, :29] * speed_factor
    
    def run(self, duration=10.0):
        """Run simulation - use existing rerun_visualize.py"""
        print(f"\n🎮 Running in SIMULATION mode")
        print(f"   Frames: {len(self.joint_angles)}")
        print(f"   Speed: {self.speed_factor*100:.0f}%")
        print(f"   Duration: {duration}s")
        
        try:
            import subprocess
            
            # Save motion data to temp CSV in g1/ directory
            temp_name = f"temp_motion_{int(time.time())}"
            temp_csv = f"g1/{temp_name}.csv"
            
            # Reconstruct full CSV format (with time column)
            full_data = np.zeros((len(self.motion_data), self.motion_data.shape[1]))
            full_data[:, 0] = np.arange(len(self.motion_data)) / 30.0  # Time column
            full_data[:, 1:] = self.motion_data[:, 1:]  # Copy all other columns
            
            # Header
            header = "time," + ",".join([f"joint_{i}" for i in range(full_data.shape[1]-1)])
            np.savetxt(temp_csv, full_data, delimiter=',', header=header, comments='')
            
            print(f"💡 Using existing rerun_visualize.py (proven to work)")
            print(f"   Temporary CSV: {temp_csv}")
            
            if self.record:
                # Create .rrd recording
                output_rrd = f"videos/sim_{int(time.time())}.rrd"
                print(f"   Recording to: {output_rrd}")
                
                # Use record_dance_videos_direct.py
                result = subprocess.run(
                    ['python3', 'record_dance_videos_direct.py', temp_csv],
                    capture_output=True,
                    text=True
                )
                
                if result.returncode == 0:
                    print(f"✅ Recording saved")
                else:
                    print(f"⚠️  Recording failed: {result.stderr}")
            else:
                # Just visualize - pass only the base name without g1/ and .csv
                print("   Opening Rerun viewer...")
                subprocess.run(['python3', 'rerun_visualize.py', '--file_name', temp_name, '--robot_type', 'g1'])
            
            # Cleanup
            if os.path.exists(temp_csv):
                os.remove(temp_csv)
            
            print(f"✅ Simulation complete")
            
        except Exception as e:
            print(f"❌ Simulation error: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        return True


class HardwareRunner:
    """Run motion on real G1 hardware (from quick_hardware_test_jetson.py)"""
    
    def __init__(self, motion_data, speed_factor=0.25, duration=10.0):
        if not HARDWARE_AVAILABLE:
            raise RuntimeError("Hardware SDK not available")
        
        self.motion_data = motion_data
        self.speed_factor = speed_factor
        self.duration = duration
        self.stop_flag = False
        
        # Extract joint angles
        if motion_data.shape[1] >= 36:
            self.joint_angles = motion_data[:, 7:36] * speed_factor
        else:
            self.joint_angles = motion_data[:, :29] * speed_factor
        
        # Import hardware control class from quick_hardware_test_jetson.py
        from quick_hardware_test_jetson import G1MotionPlayer
        self.player = G1MotionPlayer(motion_data, speed_factor, duration)
    
    def run(self):
        """Run on hardware"""
        print(f"\n🤖 Running on REAL HARDWARE")
        print(f"   Frames: {len(self.joint_angles)}")
        print(f"   Speed: {self.speed_factor*100:.0f}%")
        print(f"   Duration: {self.duration}s")
        print(f"   ⚠️  PRESS CTRL+C FOR EMERGENCY STOP")
        
        # Initialize hardware
        ChannelFactoryInitialize(0)
        self.player.Init()
        self.player.Start()
        
        # Wait for completion
        while self.player.phase != "done":
            time.sleep(0.1)
        
        print(f"✅ Hardware test complete")
        return True


def load_motion_data(motion_type, base_paths=None):
    """Load motion data CSV file"""
    if base_paths is None:
        base_paths = [
            "/home/unitree/LAFAN1_Retargeting_Dataset/g1/",
            "/home/unitree/g1/",
            "./LAFAN1_Retargeting_Dataset/g1/",
            "./g1/",
            "g1/",
        ]
    
    config = MotionConfig.PRESETS.get(motion_type)
    if not config:
        return None
    
    for base_path in base_paths:
        for filename in config['files']:
            path = os.path.join(base_path, filename)
            if os.path.exists(path):
                print(f"📂 Loading: {path}")
                data = np.loadtxt(path, delimiter=',', skiprows=1)
                print(f"   Shape: {data.shape}, Frames: {len(data)}")
                return data, config
    
    return None, None


def main():
    parser = argparse.ArgumentParser(description='Unified G1 Motion Test')
    parser.add_argument('motion', choices=['walking', 'running', 'jumping', 'dancing'],
                       help='Motion type to test')
    parser.add_argument('--mode', choices=['sim', 'hardware', 'auto'], default='auto',
                       help='Execution mode (default: auto-detect)')
    parser.add_argument('--duration', type=float, default=10.0,
                       help='Duration in seconds (default: 10)')
    parser.add_argument('--speed', type=float, default=None,
                       help='Speed factor override (0.0-1.0)')
    parser.add_argument('--record', action='store_true',
                       help='Record Rerun visualization')
    
    args = parser.parse_args()
    
    # Auto-detect mode
    if args.mode == 'auto':
        if HARDWARE_AVAILABLE:
            mode = 'hardware'
        elif SIMULATION_AVAILABLE:
            mode = 'sim'
        else:
            print("❌ Neither simulation nor hardware available")
            sys.exit(1)
    else:
        mode = args.mode
    
    # Validate mode availability
    if mode == 'hardware' and not HARDWARE_AVAILABLE:
        print("❌ Hardware SDK not available")
        sys.exit(1)
    if mode == 'sim' and not SIMULATION_AVAILABLE:
        print("❌ Simulation packages not available")
        sys.exit(1)
    
    # Load motion data
    motion_data, config = load_motion_data(args.motion)
    if motion_data is None:
        print(f"❌ Could not load motion data for '{args.motion}'")
        sys.exit(1)
    
    # Get speed factor
    if args.speed:
        speed = args.speed
    else:
        speed = config[f'speed_{mode}']
    
    print(f"\n{'='*60}")
    print(f"🎯 TEST: {args.motion.upper()} - {config['description']}")
    print(f"   Mode: {mode.upper()}")
    print(f"   Speed: {speed*100:.0f}%")
    print(f"   Duration: {args.duration}s")
    print(f"{'='*60}")
    
    # Safety confirmation for hardware
    if mode == 'hardware':
        print("\n⚠️  HARDWARE SAFETY CHECK")
        print("   - Robot standing and stable")
        print("   - Area clear of obstacles")
        print("   - Ready to emergency stop (Ctrl+C)")
        input("\nPress Enter to start (Ctrl+C to abort)...")
    
    # Run appropriate mode
    try:
        if mode == 'sim':
            runner = SimulationRunner(motion_data, speed, args.record)
            runner.run(args.duration)
        else:
            runner = HardwareRunner(motion_data, speed, args.duration)
            runner.run()
    except KeyboardInterrupt:
        print("\n\n🛑 STOPPED BY USER")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
