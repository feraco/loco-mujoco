#!/usr/bin/env python3
"""
G1 Dataset Tutorial 2: LAFAN1 Motion Capture Data
This tutorial shows how to use LAFAN1 datasets with UnitreeG1
LAFAN1 contains high-quality motion capture data for locomotion
"""

import numpy as np
from loco_mujoco.task_factories import ImitationFactory, LAFAN1DatasetConf

def main():
    print("🤖 UnitreeG1 Dataset Tutorial 2: LAFAN1 Motion Capture")
    print("=" * 60)
    
    # Available LAFAN1 datasets (motion capture from real humans)
    lafan1_datasets = [
        # Walking motions
        "walk1_subject1",     # Walking pattern from subject 1
        "walk1_subject2",     # Walking pattern from subject 2  
        "walk1_subject5",     # Walking pattern from subject 5
        
        # Dance motions (more complex movements)
        "dance1_subject1",    # Dance choreography 1
        "dance2_subject4",    # Dance choreography 2
        "dance3_subject2",    # Dance choreography 3
        
        # Running motions
        "run1_subject1",      # Running pattern 1
        "run1_subject3",      # Running pattern 3
        
        # Other locomotion
        "obstacles_subject2", # Obstacle navigation
        "aiming1_subject3",   # Aiming and pointing motions
    ]
    
    print("📋 Available LAFAN1 Datasets (Human Motion Capture):")
    for i, dataset in enumerate(lafan1_datasets, 1):
        print(f"  {i:2d}. {dataset}")
    
    try:
        print("\n🔄 Creating UnitreeG1 environment with LAFAN1 motion capture data...")
        
        # Create environment with selected LAFAN1 datasets
        env = ImitationFactory.make("UnitreeG1",
                                   lafan1_dataset_conf=LAFAN1DatasetConf([
                                       "walk1_subject1",     # Primary walking motion
                                       "dance2_subject4",    # Dance for variety
                                   ]),
                                   n_substeps=25)  # Higher substeps for precise motion
        
        print("✅ UnitreeG1 environment with LAFAN1 created successfully!")
        print(f"📊 Action space: {env.info.action_space.shape}")
        print(f"📊 Observation space: {env.info.observation_space.shape}")
        
        # Get dataset information  
        dataset = env.create_dataset()
        print(f"📊 LAFAN1 dataset created successfully!")
        
        print("\n🎭 Playing G1 with human motion capture data...")
        print("   The G1 robot will perform motions captured from real humans")
        print("   This includes natural walking gaits and dance movements")
        print("   Press SPACE to pause/resume, ESC to exit, R to restart")
        
        # Demo each LAFAN1 dataset individually for better observation
        lafan1_demos = [
            ("walk1_subject1", "Natural human walking motion"),
            ("dance2_subject4", "Expressive dance choreography")
        ]
        
        for i, (dataset_name, description) in enumerate(lafan1_demos):
            print(f"\n🎯 LAFAN1 Demo {i+1}/{len(lafan1_demos)}: {dataset_name}")
            print("=" * 50)
            print(f"   🎭 Motion: {description}")
            
            # Create environment with single LAFAN1 dataset
            single_env = ImitationFactory.make("UnitreeG1",
                                             lafan1_dataset_conf=LAFAN1DatasetConf([dataset_name]),
                                             n_substeps=25)
            
            print(f"   🤖 G1 performing: {dataset_name}")
            print(f"   ⏱️  Duration: ~45 seconds (high-quality motion capture)")
            print(f"   🎮 Controls: SPACE=pause, ESC=exit, R=restart")
            
            # Play with extended duration for motion capture appreciation
            single_env.play_trajectory(
                n_episodes=2,              # Show multiple variations
                n_steps_per_episode=1500,  # Very long episodes (~45 seconds each)
                render=True                # Enable visualization
            )
            
            # Wait between demos
            if i < len(lafan1_demos) - 1:
                print(f"\n⏸️  LAFAN1 demo {i+1} completed. Preparing next motion...")
                import time
                time.sleep(3)  # Longer pause for motion capture transitions
        
        print("\n✅ All G1 LAFAN1 motion capture demos completed!")
        print("💡 Tip: LAFAN1 datasets provide the highest quality human motion data")
        
    except Exception as e:
        print(f"❌ Error with LAFAN1 datasets: {e}")
        print("\n💡 LAFAN1 Troubleshooting:")
        print("  1. LAFAN1 datasets may need to be downloaded first")
        print("  2. Check if LAFAN1 is properly installed")
        print("  3. Try with a single LAFAN1 dataset")
        
        # Try a simpler LAFAN1 setup
        print("\n🔄 Trying simplified LAFAN1 setup...")
        try:
            env = ImitationFactory.make("UnitreeG1",
                                       lafan1_dataset_conf=LAFAN1DatasetConf(["walk1_subject1"]))
            print("🚶 Showing G1 with human walking motion (simplified LAFAN1)")
            print("⏱️  Duration: ~20 seconds - observe the natural human-like movement!")
            env.play_trajectory(n_episodes=2, n_steps_per_episode=800, render=True)
            print("✅ Simplified LAFAN1 setup successful!")
        except Exception as e2:
            print(f"❌ Simplified setup also failed: {e2}")
            print("   LAFAN1 may not be available on this system")

if __name__ == "__main__":
    main()