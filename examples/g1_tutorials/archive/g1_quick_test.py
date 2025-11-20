#!/usr/bin/env python3
"""
G1 Quick Test - Minimal script to test G1 walking without dataset complications
"""

import numpy as np
from loco_mujoco.task_factories import ImitationFactory, DefaultDatasetConf

def main():
    print("🤖 G1 Quick Walk Test - Minimal Version")
    print("=" * 50)
    print("🎯 Simple test of G1 walking motion")
    print("⏱️  Will show G1 walking for extended time")
    
    try:
        print("\n🔄 Creating G1 environment...")
        
        # Create environment with just walk dataset - minimal setup
        env = ImitationFactory.make("UnitreeG1",
                                   default_dataset_conf=DefaultDatasetConf(["walk"]),
                                   n_substeps=25)
        
        print("✅ G1 environment created!")
        
        print("\n🚶 Starting G1 walk...")
        print("🎮 MuJoCo viewer will open - use SPACE to pause, ESC to exit")
        print("⏱️  Duration: ~2 minutes total")
        
        # Simple play without dataset complications
        env.play_trajectory(
            n_episodes=4,              # 4 episodes
            n_steps_per_episode=1000,  # ~30 seconds each
            render=True                # Show MuJoCo viewer
        )
        
        print("\n✅ G1 walk test completed successfully!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("🔧 This indicates a setup issue with LocoMuJoCo or MuJoCo")
        
        # More detailed error info
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()