#!/usr/bin/env python3
"""
🎬 Complete G1 Dataset Explorer & Recorder
============================================================
Demonstrates how to access ALL available datasets in LocoMuJoCo:
1. Default datasets (basic motions)
2. LAFAN1 datasets (motion capture from LAFAN1 database) 
3. AMASS datasets (requires manual setup)

This script shows you every available dataset and how to use them!
"""

import os
import time
from datetime import datetime
from loco_mujoco.task_factories import ImitationFactory, LAFAN1DatasetConf, DefaultDatasetConf


def explore_default_datasets():
    """🏃 Explore the default datasets (already downloaded)"""
    print("\n🎯 DEFAULT DATASETS (Basic Motions)")
    print("=" * 50)
    
    # These are the 4 confirmed available datasets
    default_motions = ["walk", "run", "squat", "balance"]
    
    for motion in default_motions:
        print(f"📹 Testing: {motion}")
        try:
            env = ImitationFactory.make("UnitreeG1", 
                                      default_dataset_conf=DefaultDatasetConf([motion]))
            traj_info = env.get_trajectory_info()
            print(f"   ✅ Available! Duration: {traj_info.duration:.1f}s, Steps: {len(traj_info.obs)}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        finally:
            if 'env' in locals():
                del env
    
    return default_motions


def explore_lafan1_datasets():
    """🕺 Explore LAFAN1 datasets (automatically downloaded)"""
    print("\n🎯 LAFAN1 DATASETS (Motion Capture)")
    print("=" * 50)
    
    # Available LAFAN1 dataset categories
    lafan1_categories = {
        "Locomotion": [
            'walk1_subject1', 'walk1_subject2', 'walk1_subject5',
            'walk2_subject1', 'walk2_subject3', 'walk2_subject4', 
            'walk3_subject1', 'walk3_subject2', 'walk3_subject3',
            'walk3_subject4', 'walk3_subject5', 'walk4_subject1',
            'run1_subject2', 'run1_subject5', 'run2_subject1', 'run2_subject4',
            'sprint1_subject2', 'sprint1_subject4'
        ],
        "Dance": [
            'dance1_subject1', 'dance1_subject2', 'dance1_subject3',
            'dance2_subject1', 'dance2_subject2', 'dance2_subject3',
            'dance2_subject4', 'dance2_subject5'
        ],
        "Action": [
            'fallAndGetUp1_subject1', 'fallAndGetUp1_subject4', 'fallAndGetUp1_subject5',
            'fallAndGetUp2_subject2', 'fallAndGetUp2_subject3', 'fallAndGetUp3_subject1',
            'fight1_subject2', 'fight1_subject3', 'fight1_subject5',
            'fightAndSports1_subject1', 'fightAndSports1_subject4',
            'jumps1_subject1', 'jumps1_subject2', 'jumps1_subject5'
        ]
    }
    
    available_datasets = []
    
    for category, datasets in lafan1_categories.items():
        print(f"\n📂 {category} Datasets:")
        
        for dataset in datasets:
            print(f"🔍 Testing: {dataset}")
            try:
                env = ImitationFactory.make("UnitreeG1", 
                                          lafan1_dataset_conf=LAFAN1DatasetConf([dataset]))
                traj_info = env.get_trajectory_info() 
                print(f"   ✅ Available! Duration: {traj_info.duration:.1f}s, Steps: {len(traj_info.obs)}")
                available_datasets.append(f"lafan1_{dataset}")
            except Exception as e:
                print(f"   ❌ Not available: {str(e)[:60]}...")
            finally:
                if 'env' in locals():
                    del env
    
    return available_datasets


def explore_lafan1_groups():
    """🎭 Explore LAFAN1 predefined groups"""
    print("\n🎯 LAFAN1 PREDEFINED GROUPS")
    print("=" * 50)
    
    groups = ["LAFAN1_LOCOMOTION_DATASETS", "LAFAN1_DANCE_DATASETS", "LAFAN1_ALL_DATASETS"]
    
    for group in groups:
        print(f"📦 Testing group: {group}")
        try:
            env = ImitationFactory.make("UnitreeG1", 
                                      lafan1_dataset_conf=LAFAN1DatasetConf(dataset_group=group))
            traj_info = env.get_trajectory_info()
            print(f"   ✅ Available! Total duration: {traj_info.duration:.1f}s, Total steps: {len(traj_info.obs)}")
        except Exception as e:
            print(f"   ❌ Error: {e}")
        finally:
            if 'env' in locals():
                del env


def show_amass_info():
    """🌍 Show info about AMASS datasets (requires manual setup)"""
    print("\n🎯 AMASS DATASETS (Requires Manual Setup)")
    print("=" * 50)
    print("🔧 AMASS datasets require manual installation due to licensing:")
    print("   1. Register at: https://amass.is.tue.mpg.de/")
    print("   2. Download SMPL models")
    print("   3. Download AMASS datasets") 
    print("   4. Set paths with LocoMuJoCo commands")
    print("\n📋 Setup commands:")
    print("   loco-mujoco-set-amass-path --path /path/to/amass")
    print("   loco-mujoco-set-smpl-model-path --path /path/to/smpl")
    print("\n🎬 Example AMASS datasets include:")
    amass_examples = [
        "DanceDB/DanceDB/20120911_TheodorosSourmelis/Capoeira_Theodoros_v2_C3D_poses",
        "KIT/12/WalkInClockwiseCircle11_poses", 
        "HUMAN4D/HUMAN4D/Subject3_Medhi/INF_JumpingJack_S3_01_poses",
        "KIT/359/walking_fast05_poses"
    ]
    for example in amass_examples:
        print(f"   • {example}")


def record_available_dataset(dataset_name, dataset_config, record_video=False):
    """🎥 Record a single dataset"""
    if not record_video:
        return
        
    print(f"\n🎬 Recording {dataset_name}...")
    
    try:
        # Create environment
        if dataset_name.startswith("lafan1_"):
            env = ImitationFactory.make("UnitreeG1", lafan1_dataset_conf=dataset_config)
        else:
            env = ImitationFactory.make("UnitreeG1", default_dataset_conf=dataset_config)
        
        # Create recording directory
        timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        record_dir = f"G1_Complete_Dataset_Videos/{dataset_name}_{timestamp}"
        
        # Record video (18 seconds)
        recorder_params = {
            'save_path': record_dir,
            'record_frames': True,
            'frame_prefix': 'frame_',
            'compress_video': False,  # Avoid ffmpeg issues
            'recorder_fps': 30
        }
        
        print(f"   📹 Recording 18s of {dataset_name} motion...")
        env.play_trajectory(
            n_episodes=1, 
            n_steps_per_episode=180,  # 6 seconds at 30 FPS 
            recorder_params=recorder_params,
            render=False  # Disable display to avoid macOS issues
        )
        
        # Check if video was created
        video_files = []
        if os.path.exists(record_dir):
            for file in os.listdir(record_dir):
                if file.endswith('.mp4'):
                    video_files.append(os.path.join(record_dir, file))
        
        if video_files:
            video_size = os.path.getsize(video_files[0]) / (1024*1024)  # MB
            print(f"   ✅ Video saved: {video_files[0]} ({video_size:.1f}MB)")
        else:
            print(f"   ❌ Video not found in {record_dir}")
            
    except Exception as e:
        print(f"   ❌ Recording failed: {e}")
    finally:
        if 'env' in locals():
            del env


def main():
    """🚀 Main exploration function"""
    print("🎬 Complete G1 Dataset Explorer")
    print("=" * 60)
    print("🎯 Discovering ALL available datasets for UnitreeG1...")
    print("📝 This will show you every motion type you can use!")
    
    # Explore all dataset types
    default_datasets = explore_default_datasets()
    lafan1_datasets = explore_lafan1_datasets() 
    explore_lafan1_groups()
    show_amass_info()
    
    # Summary
    total_available = len(default_datasets) + len(lafan1_datasets)
    print(f"\n🏁 EXPLORATION COMPLETE")
    print("=" * 60)
    print(f"✅ Found {total_available} available datasets:")
    print(f"   • {len(default_datasets)} Default datasets")
    print(f"   • {len(lafan1_datasets)} LAFAN1 datasets")
    print(f"   • AMASS datasets available with setup")
    
    # Ask if user wants to record videos
    print(f"\n🎥 OPTIONAL: Record videos of available datasets?")
    print("   This will create MP4 files for each dataset")
    response = input("   Record videos? (y/N): ").strip().lower()
    
    if response in ['y', 'yes']:
        print("\n🎬 Starting video recording...")
        
        # Record default datasets
        for dataset in default_datasets:
            record_available_dataset(
                dataset, 
                DefaultDatasetConf([dataset]), 
                record_video=True
            )
        
        # Record a few LAFAN1 examples
        example_lafan1 = ['dance2_subject4', 'walk1_subject1', 'jumps1_subject1']
        for dataset in example_lafan1:
            if f"lafan1_{dataset}" in lafan1_datasets:
                record_available_dataset(
                    f"lafan1_{dataset}",
                    LAFAN1DatasetConf([dataset]),
                    record_video=True
                )
    
    print(f"\n🎓 HOW TO USE MORE DATASETS:")
    print("=" * 60)
    print("💡 To use LAFAN1 datasets in your code:")
    print("   from loco_mujoco.task_factories import ImitationFactory, LAFAN1DatasetConf")
    print("   env = ImitationFactory.make('UnitreeG1',")
    print("       lafan1_dataset_conf=LAFAN1DatasetConf(['dance2_subject4']))")
    print("")
    print("💡 To use multiple datasets:")
    print("   env = ImitationFactory.make('UnitreeG1',")
    print("       default_dataset_conf=DefaultDatasetConf(['walk', 'run']),")
    print("       lafan1_dataset_conf=LAFAN1DatasetConf(['dance1_subject1', 'jumps1_subject1']))")
    print("")
    print("💡 To use predefined groups:")
    print("   env = ImitationFactory.make('UnitreeG1',")
    print("       lafan1_dataset_conf=LAFAN1DatasetConf(dataset_group='LAFAN1_DANCE_DATASETS'))")


if __name__ == "__main__":
    main()