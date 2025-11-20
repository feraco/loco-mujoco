#!/usr/bin/env python3
"""
🎬 G1 LAFAN1 Dataset Demo
============================================================
Demonstrates how to use the extensive LAFAN1 motion capture datasets
with the UnitreeG1 robot. These give you 35+ additional motions!
"""

from loco_mujoco.task_factories import ImitationFactory, LAFAN1DatasetConf, DefaultDatasetConf


def demo_individual_lafan1_datasets():
    """🎯 Demo: Load individual LAFAN1 datasets"""
    print("\n🎯 INDIVIDUAL LAFAN1 DATASETS")
    print("=" * 50)
    
    # Example 1: Dance motion
    print("💃 Loading dance motion...")
    env = ImitationFactory.make("UnitreeG1", 
                              lafan1_dataset_conf=LAFAN1DatasetConf(['dance2_subject4']))
    print("   ✅ Dance dataset loaded! Robot can now perform dance moves.")
    env.play_trajectory(n_episodes=1, n_steps_per_episode=100, render=False)
    del env
    
    # Example 2: Natural walking variations  
    print("\n🚶 Loading walking variations...")
    env = ImitationFactory.make("UnitreeG1",
                              lafan1_dataset_conf=LAFAN1DatasetConf(['walk1_subject1', 'walk2_subject3']))
    print("   ✅ Multiple walk styles loaded! Robot has walking variety.")
    env.play_trajectory(n_episodes=1, n_steps_per_episode=100, render=False)
    del env
    
    # Example 3: Action sequences
    print("\n🤸 Loading action sequences...")
    env = ImitationFactory.make("UnitreeG1",
                              lafan1_dataset_conf=LAFAN1DatasetConf(['jumps1_subject1', 'fallAndGetUp1_subject1']))
    print("   ✅ Action sequences loaded! Robot can jump and recover from falls.")
    env.play_trajectory(n_episodes=1, n_steps_per_episode=100, render=False)
    del env


def demo_lafan1_groups():
    """🎯 Demo: Use predefined LAFAN1 groups"""
    print("\n🎯 PREDEFINED LAFAN1 GROUPS")
    print("=" * 50)
    
    # Example 1: All locomotion motions
    print("🏃 Loading ALL locomotion datasets...")
    env = ImitationFactory.make("UnitreeG1",
                              lafan1_dataset_conf=LAFAN1DatasetConf(dataset_group='LAFAN1_LOCOMOTION_DATASETS'))
    print("   ✅ 16 locomotion datasets loaded! Walking, running, sprinting variations.")
    env.play_trajectory(n_episodes=1, n_steps_per_episode=50, render=False)
    del env
    
    # Example 2: All dance motions
    print("\n💃 Loading ALL dance datasets...")
    env = ImitationFactory.make("UnitreeG1",
                              lafan1_dataset_conf=LAFAN1DatasetConf(dataset_group='LAFAN1_DANCE_DATASETS'))
    print("   ✅ 8 dance datasets loaded! Complete dance repertoire.")
    env.play_trajectory(n_episodes=1, n_steps_per_episode=50, render=False)
    del env


def demo_mixed_datasets():
    """🎯 Demo: Combine default + LAFAN1 datasets"""
    print("\n🎯 MIXED DATASET COMBINATIONS")
    print("=" * 50)
    
    print("🎭 Combining default + LAFAN1 datasets...")
    env = ImitationFactory.make("UnitreeG1",
                              default_dataset_conf=DefaultDatasetConf(['walk', 'squat']),
                              lafan1_dataset_conf=LAFAN1DatasetConf(['dance2_subject4', 'jumps1_subject1']))
    print("   ✅ Mixed datasets loaded! Basic motions + advanced behaviors.")
    env.play_trajectory(n_episodes=1, n_steps_per_episode=50, render=False)
    del env


def record_lafan1_examples():
    """🎥 Record videos of interesting LAFAN1 motions"""
    print("\n🎯 RECORDING LAFAN1 EXAMPLES")
    print("=" * 50)
    
    interesting_motions = [
        ('dance2_subject4', 'Dynamic dance sequence'),
        ('jumps1_subject1', 'Athletic jumping motions'),
        ('fallAndGetUp1_subject1', 'Recovery from falls'),
        ('fight1_subject2', 'Combat movements')
    ]
    
    for motion, description in interesting_motions:
        print(f"\n🎬 Recording: {motion} ({description})")
        
        try:
            # Create environment
            env = ImitationFactory.make("UnitreeG1",
                                      lafan1_dataset_conf=LAFAN1DatasetConf([motion]))
            
            # Record video
            recorder_params = {
                'save_path': f'G1_LAFAN1_Videos/{motion}_demo',
                'record_frames': True,
                'frame_prefix': 'frame_',
                'compress_video': False,
                'recorder_fps': 30
            }
            
            env.play_trajectory(
                n_episodes=1,
                n_steps_per_episode=180,  # 6 seconds
                recorder_params=recorder_params,
                render=False
            )
            
            print(f"   ✅ Video recorded: {motion}_demo.mp4")
            
        except Exception as e:
            print(f"   ❌ Recording failed: {e}")
        
        finally:
            if 'env' in locals():
                del env


def main():
    """🚀 Main demo function"""
    print("🎬 G1 LAFAN1 Dataset Demo")
    print("=" * 60)
    print("🎯 Exploring 35+ additional motion capture datasets!")
    
    # Run demos
    demo_individual_lafan1_datasets()
    demo_lafan1_groups()
    demo_mixed_datasets()
    
    print("\n🎥 OPTIONAL VIDEO RECORDING")
    print("=" * 50)
    response = input("Record example LAFAN1 videos? (y/N): ").strip().lower()
    if response in ['y', 'yes']:
        record_lafan1_examples()
    
    print(f"\n🎓 NEXT STEPS")
    print("=" * 60)
    print("✨ You now have access to 39+ G1 datasets:")
    print("   • 4 Default: walk, run, squat, balance")
    print("   • 16 LAFAN1 Locomotion: various walking/running styles")  
    print("   • 8 LAFAN1 Dance: expressive dance movements")
    print("   • 11 LAFAN1 Action: jumps, falls, fights, sports")
    print("")
    print("🔧 Pro Tips:")
    print("   • Use dataset_group for bulk loading")
    print("   • Mix default + LAFAN1 for variety")
    print("   • Each dataset has different motion characteristics")
    print("   • Perfect for imitation learning experiments!")
    print("")
    print("📚 For AMASS (1000+ more datasets):")
    print("   • Visit: https://amass.is.tue.mpg.de/")
    print("   • Download manually due to licensing")
    print("   • Run: loco-mujoco-set-amass-path --path /your/path")


if __name__ == "__main__":
    main()