#!/usr/bin/env python3
"""
Preview Hardware Test Motion in Rerun

This script shows EXACTLY what will run on the real G1 hardware,
using the same speed factors and motion scaling as quick_hardware_test_jetson.py

Usage:
    python3 preview_hardware_test.py walking
    python3 preview_hardware_test.py running
    python3 preview_hardware_test.py jumping
    python3 preview_hardware_test.py dancing
    
    # Custom duration
    python3 preview_hardware_test.py dancing 20
    
    # Select specific dataset (1, 2, or 3)
    python3 preview_hardware_test.py dancing 10 2
    
    # Full dataset at normal speed (100% amplitude)
    python3 preview_hardware_test.py dancing --full
    python3 preview_hardware_test.py walking --full --dataset 2
"""

import sys
import os
import numpy as np
import subprocess

# Speed factors from quick_hardware_test_jetson.py
# These are the ACTUAL values that will be used on hardware
HARDWARE_SPEED_FACTORS = {
    'walking': 0.30,    # 30% amplitude
    'running': 0.20,    # 20% amplitude
    'jumping': 0.15,    # 15% amplitude
    'dancing': 0.25,    # 25% amplitude
}

# Motion files from quick_hardware_test_jetson.py
MOTION_FILES = {
    'walking': ['walk1_subject1.csv', 'walk1_subject2.csv', 'walk2_subject1.csv'],
    'running': ['run1_subject2.csv', 'run1_subject5.csv', 'run2_subject1.csv'],
    'jumping': ['jumps1_subject1.csv', 'jumps1_subject2.csv'],
    'dancing': ['dance1_subject1.csv', 'dance1_subject2.csv', 'dance2_subject1.csv'],
}


def load_motion_data(motion_type, dataset_index=0):
    """Load motion data exactly as quick_hardware_test_jetson.py does"""
    files = MOTION_FILES.get(motion_type, [])
    
    # Select specific dataset if available
    if dataset_index < len(files):
        selected_files = [files[dataset_index]]
    else:
        selected_files = files
    
    base_paths = [
        "./g1/",
        "g1/",
    ]
    
    for base_path in base_paths:
        for filename in selected_files:
            path = os.path.join(base_path, filename)
            if os.path.exists(path):
                print(f"📂 Loading: {path}")
                data = np.loadtxt(path, delimiter=',', skiprows=1)
                print(f"   Shape: {data.shape}, Frames: {len(data)}")
                return data, filename
    
    print(f"❌ Could not find motion data for '{motion_type}'")
    return None, None


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 preview_hardware_test.py <motion_type> [options]")
        print("  Motion types: walking, running, jumping, dancing")
        print("\nOptions:")
        print("  [duration]      Duration in seconds (default: 10)")
        print("  [dataset_num]   Dataset 1, 2, or 3 (default: 1)")
        print("  --full          Play full dataset at 100% amplitude")
        print("  --dataset N     Select dataset number")
        print("\nExamples:")
        print("  python3 preview_hardware_test.py walking")
        print("  python3 preview_hardware_test.py dancing 20")
        print("  python3 preview_hardware_test.py dancing 10 2  # 2nd dataset")
        print("  python3 preview_hardware_test.py dancing --full  # Full, 100% amplitude")
        print("  python3 preview_hardware_test.py walking --full --dataset 2")
        sys.exit(1)
    
    motion_type = sys.argv[1].lower()
    
    if motion_type not in HARDWARE_SPEED_FACTORS:
        print(f"❌ Unknown motion type: {motion_type}")
        print(f"   Valid types: {list(HARDWARE_SPEED_FACTORS.keys())}")
        sys.exit(1)
    
    # Parse arguments
    full_dataset = '--full' in sys.argv
    duration = None  # None means full duration
    dataset_index = 0
    
    # Check for --dataset flag
    if '--dataset' in sys.argv:
        idx = sys.argv.index('--dataset')
        if idx + 1 < len(sys.argv):
            try:
                dataset_index = int(sys.argv[idx + 1]) - 1
            except ValueError:
                pass
    
    # Parse positional arguments (skip flags)
    positional_args = [arg for arg in sys.argv[2:] if not arg.startswith('--') and arg != str(dataset_index + 1)]
    
    if not full_dataset and len(positional_args) >= 1:
        try:
            duration = float(positional_args[0])
        except ValueError:
            pass
    
    if not full_dataset and len(positional_args) >= 2:
        try:
            dataset_index = int(positional_args[1]) - 1
        except ValueError:
            pass
    
    # Default duration if not full
    if duration is None and not full_dataset:
        duration = 10.0
    
    # Get speed factor
    if full_dataset:
        speed = 1.0  # 100% amplitude
        mode_desc = "FULL DATASET (100% amplitude)"
    else:
        speed = HARDWARE_SPEED_FACTORS[motion_type]
        mode_desc = f"HARDWARE SAFE ({speed*100:.0f}% amplitude)"
    
    # Show available datasets
    available = MOTION_FILES[motion_type]
    
    print(f"\n{'='*60}")
    print(f"🔍 PREVIEW: {motion_type.upper()}")
    print(f"{'='*60}")
    print(f"📚 Available datasets for {motion_type}:")
    for i, fname in enumerate(available, 1):
        marker = "👉" if i-1 == dataset_index else "  "
        print(f"   {marker} {i}. {fname}")
    print(f"")
    print(f"⚙️  Settings:")
    print(f"   Mode: {mode_desc}")
    print(f"   Speed factor: {speed*100:.0f}% amplitude scaling")
    if duration:
        print(f"   Duration: {duration}s (truncated)")
    else:
        print(f"   Duration: Full dataset")
    
    if not full_dataset:
        print(f"\n💡 This uses HARDWARE safety limits!")
    else:
        print(f"\n⚠️  WARNING: Full 100% amplitude - for simulation only!")
        print(f"   DO NOT use these settings on real hardware!")
    print(f"{'='*60}\n")
    
    # Load motion data
    motion_data, filename = load_motion_data(motion_type, dataset_index)
    if motion_data is None:
        sys.exit(1)
    
    # Calculate actual duration
    if duration is None:
        duration = len(motion_data) / 30.0  # Full dataset at 30 FPS
    
    print(f"\n📊 Motion Info:")
    print(f"   File: {filename}")
    print(f"   Total frames: {len(motion_data)}")
    print(f"   Duration at 30 FPS: {len(motion_data)/30:.1f}s")
    print(f"   Playback duration: {duration}s (will loop)")
    
    # Apply hardware speed scaling to joint angles (columns 7-36)
    scaled_data = motion_data.copy()
    if scaled_data.shape[1] >= 36:
        scaled_data[:, 7:36] = scaled_data[:, 7:36] * speed
    else:
        scaled_data[:, :29] = scaled_data[:, :29] * speed
    
    # Save to temporary CSV for visualization
    temp_name = f"preview_{motion_type}_hardware"
    temp_csv = f"g1/{temp_name}.csv"
    
    # Save with header
    np.savetxt(temp_csv, scaled_data, delimiter=',')
    
    print(f"\n🎬 Opening Rerun preview...")
    print(f"   Temporary file: {temp_csv}")
    print(f"\n⚠️  IMPORTANT:")
    print(f"   • The robot will stay centered (X,Y = 0)")
    print(f"   • Joint movements are scaled to {speed*100:.0f}% amplitude")
    print(f"   • This matches the hardware safety limits")
    print(f"   • Press SPACE to play/pause")
    print(f"   • Use mouse to rotate view")
    print(f"\n{'='*60}\n")
    
    # Open in Rerun
    try:
        subprocess.run(['python3', 'rerun_visualize.py', '--file_name', temp_name, '--robot_type', 'g1'])
    except KeyboardInterrupt:
        print("\n\n✅ Preview stopped")
    finally:
        # Cleanup
        if os.path.exists(temp_csv):
            os.remove(temp_csv)
            print(f"🧹 Cleaned up temporary file")


if __name__ == "__main__":
    main()
