#!/usr/bin/env python3
"""
G1 Dataset Tutorial 1: Basic Motion Replay
This tutorial shows how to use default LocoMuJoCo datasets with UnitreeG1
"""

import numpy as np
from loco_mujoco.task_factories import ImitationFactory, DefaultDatasetConf, LAFAN1DatasetConf

def main():
    print("🤖 UnitreeG1 Dataset Tutorial 1: Basic Motion Replay")
    print("=" * 60)
    
    # Available default datasets that work with humanoid robots
    available_datasets = [
        "walk",           # Walking motion
        "squat",          # Squatting motion  
        "stand",          # Standing still
        "stepinplace",    # Stepping in place
        "walk_fast",      # Fast walking
        "walk_slow",      # Slow walking
        "jump",           # Jumping motion
    ]
    
    print("📋 Available Default Datasets:")
    for i, dataset in enumerate(available_datasets, 1):
        print(f"  {i}. {dataset}")
    
    try:
        print("\n🔄 Creating UnitreeG1 environment with multiple datasets...")
        
        # Create environment with multiple datasets for variety
        env = ImitationFactory.make("UnitreeG1",
                                   default_dataset_conf=DefaultDatasetConf([
                                       "walk",         # Primary walking dataset
                                       "squat",        # Squatting motion (changed from stepinplace)
                                   ]),
                                   n_substeps=20)  # Higher substeps for smoother motion
        
        print("✅ UnitreeG1 environment created successfully!")
        print(f"📊 Action space: {env.info.action_space.shape}")
        print(f"📊 Observation space: {env.info.observation_space.shape}")
        
        # Get dataset information
        dataset = env.create_dataset()
        print(f"📊 Dataset created successfully!")
        
        print("\n🎬 Playing G1 motion capture trajectories...")
        print("   This will show the G1 robot performing human motion patterns")
        print("   Press SPACE to pause/resume, ESC to exit, R to restart")
        
        # Demo each dataset individually with pauses (using only available datasets)
        datasets_to_demo = ["walk", "squat"]  # Changed from stepinplace to squat (available)
        
        for i, dataset_name in enumerate(datasets_to_demo):
            print(f"\n🎯 Demo {i+1}/{len(datasets_to_demo)}: {dataset_name.upper()}")
            print("=" * 40)
            
            # Create environment with single dataset for focused viewing
            single_env = ImitationFactory.make("UnitreeG1",
                                             default_dataset_conf=DefaultDatasetConf([dataset_name]),
                                             n_substeps=20)
            
            print(f"   🤖 Now showing G1 performing: {dataset_name}")
            print(f"   ⏱️  Duration: ~30 seconds")
            print(f"   🎮 Controls: SPACE=pause, ESC=exit, R=restart")
            
            # Play with longer duration and slower speed for better observation
            single_env.play_trajectory(
                n_episodes=3,              # Multiple episodes to see variation
                n_steps_per_episode=1000,  # Much longer episodes (30+ seconds each)
                render=True                # Enable visualization
            )
            
            # Wait between demos
            if i < len(datasets_to_demo) - 1:
                print(f"\n⏸️  Demo {i+1} completed. Preparing next demo...")
                import time
                time.sleep(2)  # Brief pause between demos
        
        print("\n✅ All G1 motion demos completed!")
        print("💡 Tip: You can run individual datasets by modifying the datasets_to_demo list")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n💡 Troubleshooting:")
        print("  1. Make sure LocoMuJoCo is properly installed")
        print("  2. Check internet connection for dataset downloads")
        print("  3. Try individual datasets instead of multiple")
        
        # Try a fallback with just one dataset
        print("\n🔄 Trying fallback with single dataset...")
        try:
            env = ImitationFactory.make("UnitreeG1",
                                       default_dataset_conf=DefaultDatasetConf(["walk"]))
            print("🚶 Showing G1 walking motion (fallback mode)")
            print("⏱️  Duration: ~15 seconds - watch carefully!")
            env.play_trajectory(n_episodes=2, n_steps_per_episode=500, render=True)
            print("✅ Fallback successful!")
        except Exception as e2:
            print(f"❌ Fallback also failed: {e2}")

if __name__ == "__main__":
    main()