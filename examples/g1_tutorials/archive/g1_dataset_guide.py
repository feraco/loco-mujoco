#!/usr/bin/env python3
"""
🎬 G1 Dataset Discovery Guide
============================================================
Quick guide to ALL available datasets for UnitreeG1 in LocoMuJoCo
"""

from loco_mujoco.task_factories import ImitationFactory, LAFAN1DatasetConf, DefaultDatasetConf


def test_dataset_availability(name, dataset_config, dataset_type="default"):
    """Test if a dataset loads successfully"""
    try:
        if dataset_type == "lafan1":
            env = ImitationFactory.make("UnitreeG1", lafan1_dataset_conf=dataset_config)
        else:
            env = ImitationFactory.make("UnitreeG1", default_dataset_conf=dataset_config)
        
        print(f"✅ {name} - Available and ready!")
        del env
        return True
    except Exception as e:
        print(f"❌ {name} - {str(e)[:80]}...")
        return False


def main():
    print("🎬 G1 Dataset Discovery Guide")
    print("=" * 60)
    
    # 1. DEFAULT DATASETS (Basic motions - confirmed available)
    print("\n📦 DEFAULT DATASETS (Basic Motions)")
    print("-" * 40)
    default_datasets = ["walk", "run", "squat", "balance"]
    
    available_default = []
    for dataset in default_datasets:
        if test_dataset_availability(dataset, DefaultDatasetConf([dataset])):
            available_default.append(dataset)
    
    print(f"\n✅ Available Default: {len(available_default)} datasets")
    
    # 2. LAFAN1 DATASETS (Motion capture - extensive library) 
    print("\n📦 LAFAN1 DATASETS (Motion Capture)")
    print("-" * 40)
    print("🔍 Testing key LAFAN1 datasets...")
    
    # Test a few representative LAFAN1 datasets
    lafan1_examples = [
        "dance2_subject4",  # Dance motion
        "walk1_subject1",   # Natural walking
        "run1_subject2",    # Running motion
        "jumps1_subject1"   # Jumping actions
    ]
    
    available_lafan1 = []
    for dataset in lafan1_examples:
        if test_dataset_availability(f"lafan1_{dataset}", LAFAN1DatasetConf([dataset]), "lafan1"):
            available_lafan1.append(dataset)
    
    print(f"\n✅ LAFAN1 Examples Working: {len(available_lafan1)}/4 tested")
    
    # 3. Show all available LAFAN1 options
    print("\n📋 COMPLETE LAFAN1 DATASET CATALOG")
    print("-" * 40)
    
    print("🚶 LOCOMOTION (16 datasets):")
    locomotion = [
        'walk1_subject1', 'walk1_subject2', 'walk1_subject5', 'walk2_subject1',
        'walk2_subject3', 'walk2_subject4', 'walk3_subject1', 'walk3_subject2', 
        'walk3_subject3', 'walk3_subject4', 'walk3_subject5', 'walk4_subject1',
        'run1_subject2', 'run1_subject5', 'run2_subject1', 'run2_subject4'
    ]
    for i, dataset in enumerate(locomotion):
        print(f"   {i+1:2d}. {dataset}")
    
    print("\n💃 DANCE (8 datasets):")
    dance = [
        'dance1_subject1', 'dance1_subject2', 'dance1_subject3', 'dance2_subject1',
        'dance2_subject2', 'dance2_subject3', 'dance2_subject4', 'dance2_subject5'
    ]
    for i, dataset in enumerate(dance):
        print(f"   {i+1:2d}. {dataset}")
    
    print("\n🎬 ACTION (11 datasets):")
    action = [
        'fallAndGetUp1_subject1', 'fallAndGetUp1_subject4', 'fallAndGetUp1_subject5',
        'fallAndGetUp2_subject2', 'fallAndGetUp2_subject3', 'fallAndGetUp3_subject1',
        'fight1_subject2', 'fight1_subject3', 'fight1_subject5',
        'fightAndSports1_subject1', 'fightAndSports1_subject4', 
        'jumps1_subject1', 'jumps1_subject2', 'jumps1_subject5'
    ]
    for i, dataset in enumerate(action):
        print(f"   {i+1:2d}. {dataset}")
    
    print("\n🌍 AMASS DATASETS (Advanced Setup Required)")
    print("-" * 40)
    print("📝 AMASS provides thousands of motion capture sequences:")
    print("   • Requires manual download and setup due to licensing")
    print("   • Register at: https://amass.is.tue.mpg.de/")
    print("   • Includes: DanceDB, KIT, HUMAN4D, and many more")
    print("   • Setup: loco-mujoco-set-amass-path --path /your/path")
    
    print(f"\n🎯 HOW TO USE THESE DATASETS")
    print("=" * 60)
    
    print("💡 Single dataset:")
    print("   from loco_mujoco.task_factories import ImitationFactory, LAFAN1DatasetConf")
    print("   env = ImitationFactory.make('UnitreeG1',")
    print("       lafan1_dataset_conf=LAFAN1DatasetConf(['dance2_subject4']))")
    
    print("\n💡 Multiple datasets:")
    print("   env = ImitationFactory.make('UnitreeG1',")
    print("       default_dataset_conf=DefaultDatasetConf(['walk', 'run']),")
    print("       lafan1_dataset_conf=LAFAN1DatasetConf(['dance1_subject1', 'walk1_subject1']))")
    
    print("\n💡 Predefined groups:")
    print("   # Get all locomotion datasets at once")
    print("   env = ImitationFactory.make('UnitreeG1',")
    print("       lafan1_dataset_conf=LAFAN1DatasetConf(dataset_group='LAFAN1_LOCOMOTION_DATASETS'))")
    print("   ")
    print("   # Available groups:")
    print("   # - 'LAFAN1_LOCOMOTION_DATASETS' (16 walking/running)")
    print("   # - 'LAFAN1_DANCE_DATASETS' (8 dance motions)")
    print("   # - 'LAFAN1_ALL_DATASETS' (35+ total motions)")
    
    print(f"\n🎥 VIDEO RECORDING")
    print("=" * 60)
    print("💡 To record any of these datasets:")
    print("   env.play_trajectory(")
    print("       n_episodes=1, n_steps_per_episode=180,")
    print("       recorder_params={'save_path': 'my_video', 'record_frames': True},")
    print("       render=False)")
    
    print(f"\n🏆 SUMMARY")
    print("=" * 60)
    print(f"✅ You have access to 39+ motion datasets:")
    print(f"   • 4 Default datasets (walk, run, squat, balance)")  
    print(f"   • 35+ LAFAN1 datasets (locomotion, dance, actions)")
    print(f"   • Thousands of AMASS datasets (with setup)")
    print(f"")
    print(f"🎯 Perfect for:")
    print(f"   • Imitation learning experiments")
    print(f"   • Robot behavior demonstrations") 
    print(f"   • Motion analysis and comparison")
    print(f"   • Educational robotics content")


if __name__ == "__main__":
    main()