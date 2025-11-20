#!/usr/bin/env python3
"""
G1 Dataset Tutorial 3: Dataset-Guided Control (FIXED VERSION)
This tutorial shows G1 performing dataset motions with stability improvements.
PREVIOUS ISSUE: Random actions caused falling - now using proper dataset playback!
"""

import numpy as np
import time
from loco_mujoco.task_factories import ImitationFactory, DefaultDatasetConf

def main():
    print("🤖 UnitreeG1 Dataset Tutorial 3: Dataset-Guided Control (FIXED)")
    print("=" * 70)
    print("🔧 PREVIOUS ISSUE: Random actions caused G1 to fall constantly")
    print("✅ SOLUTION: Now using proper dataset playback for stable motion")
    
    try:
        print("\n🔄 Creating UnitreeG1 environment with multiple datasets...")
        
        # Create environment with ONLY working datasets  
        env = ImitationFactory.make("UnitreeG1",
                                   default_dataset_conf=DefaultDatasetConf([
                                       "walk",   # Walking motion (✅ WORKS)
                                       "squat",  # Squatting motion (✅ WORKS)
                                       "run"     # Running motion (✅ WORKS)
                                   ]),
                                   n_substeps=25)  # Higher substeps for stability
        
        print("✅ Environment created successfully!")
        print(f"📊 Action space: {env.info.action_space.shape[0]} joints")
        
        # Create dataset for reference motions
        dataset = env.create_dataset()
        print("📊 Dataset loaded successfully!")
        
        print("\n🎮 G1 Dataset-Guided Motion Demonstration")
        print("   Instead of random actions, G1 will follow dataset trajectories")
        print("   This prevents falling and shows realistic humanoid motion")
        print("   Duration: ~90 seconds total")
        
        # Motion demonstrations using proper dataset playback
        motion_demos = [
            {
                "name": "Standing Stability",
                "dataset": ["stand"], 
                "description": "G1 maintains standing posture with micro-adjustments",
                "episodes": 1,
                "steps": 300
            },
            {
                "name": "Walking Motion",
                "dataset": ["walk"],
                "description": "G1 performs natural walking gait from dataset",
                "episodes": 2,
                "steps": 400
            },
            {
                "name": "Squatting Exercise", 
                "dataset": ["squat"],
                "description": "G1 performs squatting motion for leg strength",
                "episodes": 1,
                "steps": 350
            }
        ]
        
        for demo in motion_demos:
            print(f"\n🎯 Demo: {demo['name']}")
            print(f"   {demo['description']}")
            print(f"   Duration: ~{demo['steps'] * demo['episodes'] // 30} seconds")
            
            # Create environment for this specific motion
            demo_env = ImitationFactory.make("UnitreeG1",
                                           default_dataset_conf=DefaultDatasetConf(demo['dataset']),
                                           n_substeps=25)
            
            print(f"   🎬 Playing {demo['name']} motion...")
            
            # Use proper dataset playback instead of random actions
            demo_env.play_trajectory(
                n_episodes=demo['episodes'],
                n_steps_per_episode=demo['steps'],
                render=True
            )
            
            print(f"   ✅ {demo['name']} completed successfully!")
            
            # Brief pause between demos
            time.sleep(2)
        
        print(f"\n✅ All dataset-guided motions completed!")
        print("💡 Key Improvement: Using dataset playback prevents falling!")
        print("🔧 Previous version used random actions → constant falling")
        print("✅ Fixed version uses motion capture data → stable movement")
        
    except Exception as e:
        print(f"❌ Error in interactive control: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()