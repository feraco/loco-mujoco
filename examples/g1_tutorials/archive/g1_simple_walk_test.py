#!/usr/bin/env python3
"""
G1 Simple Walk Test - Maximum viewing time for walk motion
This script focuses on just showing G1 walking with extended duration
"""

import numpy as np
import time
from loco_mujoco.task_factories import ImitationFactory, DefaultDatasetConf

def main():
    print("🤖 G1 Simple Walk Test - Extended Viewing")
    print("=" * 50)
    print("🎯 Purpose: Show G1 walking motion with maximum viewing time")
    print("⏱️  Each episode will run for ~60 seconds")
    print("🎮 MuJoCo viewer controls:")
    print("   - Mouse drag: Rotate view")
    print("   - Mouse wheel: Zoom")
    print("   - SPACE: Pause/Resume simulation")
    print("   - ESC: Exit viewer")
    print("   - R: Reset simulation")
    
    try:
        print("\n🔄 Creating G1 environment with walk dataset...")
        
        # Create environment with just walk dataset
        env = ImitationFactory.make("UnitreeG1",
                                   default_dataset_conf=DefaultDatasetConf(["walk"]),
                                   n_substeps=25)  # High substeps for smooth motion
        
        print("✅ UnitreeG1 environment created successfully!")
        
        # Get dataset info (without using len() which isn't supported)
        dataset = env.create_dataset()
        print(f"📊 Walk dataset loaded successfully!")
        print(f"📊 Dataset type: {type(dataset).__name__}")
        
        print("\n🚶 Starting G1 walk demonstration...")
        print("   Episode 1: Standard speed (60 seconds)")
        print("   Episode 2: Extended viewing (90 seconds)")  
        print("   Episode 3: Final demonstration (60 seconds)")
        
        print("\n🎬 MuJoCo viewer should now open and stay visible!")
        print("⚠️  If viewer closes quickly, there may be a graphics/display issue")
        
        # Play with maximum duration for observation
        env.play_trajectory(
            n_episodes=3,              # 3 episodes for variety
            n_steps_per_episode=2000,  # Very long episodes (60+ seconds each)
            render=True                # Enable MuJoCo viewer
        )
        
        print("\n✅ G1 walk demonstration completed!")
        print("💡 Total viewing time was approximately 3-4 minutes")
        
    except Exception as e:
        print(f"\n❌ Error during G1 walk test: {e}")
        print("\n🔧 Troubleshooting tips:")
        print("   1. Make sure you're in the unitree_mujoco conda environment")
        print("   2. Verify LocoMuJoCo is properly installed")
        print("   3. Check that MuJoCo viewer can run on your system")
        print("   4. Try running from the correct directory")
        
        # Additional error details
        import traceback
        print(f"\n📋 Full error details:")
        traceback.print_exc()

if __name__ == "__main__":
    main()