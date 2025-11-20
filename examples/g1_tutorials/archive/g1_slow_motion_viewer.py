#!/usr/bin/env python3
"""
G1 Slow Motion Viewer - Extended observation of G1 movements
This version is optimized for detailed observation with longer viewing times
"""

import numpy as np
import time
from loco_mujoco.task_factories import ImitationFactory, DefaultDatasetConf, LAFAN1DatasetConf

def show_dataset_menu():
    """Display available datasets and let user choose"""
    print("\n📋 Available G1 Motion Datasets:")
    print("=" * 40)
    
    default_datasets = [
        ("walk", "Natural walking gait"),
        ("squat", "Squatting exercise"),
        ("stand", "Standing posture"),
        ("walk_slow", "Slow walking pace"),
        ("walk_fast", "Fast walking pace"),
        ("jump", "Jumping motion"),
    ]
    
    lafan1_datasets = [
        ("walk1_subject1", "Human walking capture 1"),
        ("walk1_subject2", "Human walking capture 2"), 
        ("dance2_subject4", "Dance choreography"),
        ("run1_subject1", "Running motion"),
    ]
    
    print("🏃 Default Datasets (Built-in):")
    for i, (name, desc) in enumerate(default_datasets, 1):
        print(f"  {i:2d}. {name:<15} - {desc}")
    
    print("\n🎭 LAFAN1 Datasets (Motion Capture):")
    for i, (name, desc) in enumerate(lafan1_datasets, len(default_datasets) + 1):
        print(f"  {i:2d}. {name:<15} - {desc}")
    
    print(f"\n  {len(default_datasets) + len(lafan1_datasets) + 1:2d}. ALL           - Show all datasets sequentially")
    
    return default_datasets, lafan1_datasets

def play_single_motion(dataset_name, dataset_type="default", duration_multiplier=2.0):
    """Play a single motion with extended viewing time"""
    
    print(f"\n🤖 Preparing G1 for: {dataset_name}")
    print("=" * 50)
    
    try:
        # Create environment based on dataset type
        if dataset_type == "default":
            env = ImitationFactory.make("UnitreeG1",
                                       default_dataset_conf=DefaultDatasetConf([dataset_name]),
                                       n_substeps=30)  # Very high substeps for smooth motion
        else:  # LAFAN1
            env = ImitationFactory.make("UnitreeG1", 
                                       lafan1_dataset_conf=LAFAN1DatasetConf([dataset_name]),
                                       n_substeps=35)  # Even higher for motion capture
        
        print(f"✅ Environment created for {dataset_name}")
        print(f"🎬 Starting extended playback...")
        print(f"⏱️  Duration: ~{int(60 * duration_multiplier)} seconds per episode")
        print(f"🎮 Controls:")
        print(f"   - SPACE: Pause/Resume")
        print(f"   - ESC: Exit")
        print(f"   - R: Restart episode")
        print(f"   - Mouse: Rotate camera view")
        
        # Calculate steps for desired duration (assuming ~30 FPS)
        steps_per_episode = int(900 * duration_multiplier)  # Base 30 seconds * multiplier
        
        # Play with very long episodes for detailed observation
        env.play_trajectory(
            n_episodes=3,                # Multiple episodes to see variations
            n_steps_per_episode=steps_per_episode,
            render=True
        )
        
        print(f"✅ Completed viewing: {dataset_name}")
        
    except Exception as e:
        print(f"❌ Error playing {dataset_name}: {e}")
        return False
    
    return True

def main():
    print("🤖 G1 Slow Motion Viewer")
    print("=" * 60)
    print("🎯 Purpose: Extended observation of G1 humanoid movements")
    print("⏱️  Each motion plays for 60-120 seconds for detailed study")
    print("🎮 Interactive controls available during playback")
    
    default_datasets, lafan1_datasets = show_dataset_menu()
    
    while True:
        try:
            choice = input(f"\nEnter choice (1-{len(default_datasets) + len(lafan1_datasets) + 1}) or 'q' to quit: ").strip().lower()
            
            if choice == 'q' or choice == 'quit':
                print("👋 Exiting G1 Slow Motion Viewer")
                break
            
            choice_num = int(choice)
            
            # All datasets
            if choice_num == len(default_datasets) + len(lafan1_datasets) + 1:
                print("\n🎬 Playing ALL datasets sequentially...")
                print("⚠️  This will take 15-20 minutes total")
                proceed = input("Continue? (y/n): ").strip().lower()
                if proceed != 'y':
                    continue
                
                # Play all default datasets
                for name, desc in default_datasets:
                    print(f"\n🔄 Next: {name} - {desc}")
                    time.sleep(2)
                    if not play_single_motion(name, "default", 1.5):
                        continue
                    time.sleep(3)
                
                # Play all LAFAN1 datasets
                for name, desc in lafan1_datasets:
                    print(f"\n🔄 Next: {name} - {desc}")
                    time.sleep(2) 
                    if not play_single_motion(name, "lafan1", 2.0):
                        continue
                    time.sleep(3)
                
                print("\n✅ All datasets completed!")
                
            # Single default dataset
            elif 1 <= choice_num <= len(default_datasets):
                name, desc = default_datasets[choice_num - 1]
                print(f"\n🎯 Selected: {name} - {desc}")
                play_single_motion(name, "default", 2.0)
                
            # Single LAFAN1 dataset  
            elif len(default_datasets) < choice_num <= len(default_datasets) + len(lafan1_datasets):
                idx = choice_num - len(default_datasets) - 1
                name, desc = lafan1_datasets[idx]
                print(f"\n🎯 Selected: {name} - {desc}")
                play_single_motion(name, "lafan1", 2.5)
                
            else:
                print("❌ Invalid choice. Please try again.")
                
        except ValueError:
            print("❌ Please enter a valid number or 'q' to quit.")
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted by user. Exiting...")
            break
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
            
    print("\n🤖 Thank you for using G1 Slow Motion Viewer!")

if __name__ == "__main__":
    main()