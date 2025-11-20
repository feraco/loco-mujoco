#!/usr/bin/env python3
"""
🎬 G1 Dance Dataset Recorder
============================================================
Records videos of all available LAFAN1 dance datasets for the UnitreeG1 robot.
Creates individual MP4 files for each dance motion.
"""

import os
import glob
from datetime import datetime
from loco_mujoco.task_factories import ImitationFactory, LAFAN1DatasetConf


def record_dance_dataset(dataset_name):
    """🎥 Record a single dance dataset"""
    print(f"\n🎬 Recording dance: {dataset_name}")
    
    try:
        # Create environment with dance dataset
        env = ImitationFactory.make("UnitreeG1", 
                                  lafan1_dataset_conf=LAFAN1DatasetConf([dataset_name]))
        
        # Create recording directory
        timestamp = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        record_dir = f"G1_Dance_Videos/{dataset_name}_{timestamp}"
        
        # Recording configuration - extended duration for full dance
        recorder_params = {
            'save_path': record_dir,
            'record_frames': True,
            'frame_prefix': 'frame_',
            'compress_video': False,  # Avoid ffmpeg compression issues
            'recorder_fps': 30
        }
        
        print(f"   📹 Recording full dance sequence...")
        
        # Record longer sequence to capture full dance (30 seconds)
        env.play_trajectory(
            n_episodes=1, 
            n_steps_per_episode=900,  # 30 seconds at 30 FPS
            recorder_params=recorder_params,
            render=False  # Disable visual display to avoid macOS issues
        )
        
        # Check for created video files
        video_files = glob.glob(os.path.join(record_dir, "*.mp4"))
        
        if video_files:
            # Get the first video file and check its size
            video_file = video_files[0]
            video_size = os.path.getsize(video_file) / (1024*1024)  # MB
            
            # Rename to a cleaner name
            clean_name = f"G1_Dance_Videos/{dataset_name}_dance.mp4"
            os.makedirs("G1_Dance_Videos", exist_ok=True)
            
            # Copy to cleaner location
            import shutil
            shutil.copy2(video_file, clean_name)
            
            print(f"   ✅ Dance recorded! File: {clean_name} ({video_size:.1f}MB)")
            return clean_name
        else:
            print(f"   ❌ Video file not found in {record_dir}")
            return None
            
    except Exception as e:
        print(f"   ❌ Recording failed: {str(e)[:100]}...")
        return None
    finally:
        if 'env' in locals():
            del env


def main():
    """🚀 Record all dance datasets"""
    print("🎬 G1 Dance Dataset Recorder")
    print("=" * 60)
    print("💃 Recording all available LAFAN1 dance motions...")
    
    # All LAFAN1 dance datasets
    dance_datasets = [
        'dance1_subject1',
        'dance1_subject2', 
        'dance1_subject3',
        'dance2_subject1',
        'dance2_subject2',
        'dance2_subject3',
        'dance2_subject4',
        'dance2_subject5'
    ]
    
    print(f"🎯 Found {len(dance_datasets)} dance datasets to record")
    
    # Create output directory
    os.makedirs("G1_Dance_Videos", exist_ok=True)
    
    successful_recordings = []
    failed_recordings = []
    
    # Record each dance dataset
    for i, dataset in enumerate(dance_datasets, 1):
        print(f"\n[{i:2d}/{len(dance_datasets)}] Processing: {dataset}")
        
        video_file = record_dance_dataset(dataset)
        
        if video_file:
            successful_recordings.append((dataset, video_file))
        else:
            failed_recordings.append(dataset)
    
    # Summary report
    print(f"\n🏁 DANCE RECORDING COMPLETE")
    print("=" * 60)
    print(f"✅ Successfully recorded: {len(successful_recordings)} dances")
    print(f"❌ Failed recordings: {len(failed_recordings)} dances")
    
    if successful_recordings:
        print(f"\n📹 SUCCESSFUL DANCE VIDEOS:")
        print("-" * 40)
        total_size = 0
        for dataset, video_file in successful_recordings:
            if os.path.exists(video_file):
                size_mb = os.path.getsize(video_file) / (1024*1024)
                total_size += size_mb
                print(f"   🎭 {dataset:<20} → {os.path.basename(video_file)} ({size_mb:.1f}MB)")
        
        print(f"\n📊 Total video library: {total_size:.1f}MB")
    
    if failed_recordings:
        print(f"\n❌ FAILED RECORDINGS:")
        print("-" * 40)
        for dataset in failed_recordings:
            print(f"   • {dataset}")
    
    # List all video files
    print(f"\n📁 DANCE VIDEO COLLECTION:")
    print("=" * 60)
    dance_videos = glob.glob("G1_Dance_Videos/*.mp4")
    if dance_videos:
        print(f"🎬 Found {len(dance_videos)} dance videos in G1_Dance_Videos/:")
        for video in sorted(dance_videos):
            size_mb = os.path.getsize(video) / (1024*1024)
            print(f"   📹 {os.path.basename(video):<30} ({size_mb:.1f}MB)")
    else:
        print("   No dance videos found.")
    
    print(f"\n🎓 USAGE TIPS:")
    print("=" * 60)
    print("🎥 These videos are perfect for:")
    print("   • Demonstrating G1 robot capabilities")
    print("   • Research presentations on humanoid motion")
    print("   • Educational content on imitation learning")
    print("   • Social media showcasing robot dance abilities")
    print("")
    print("🔧 Technical notes:")
    print("   • Videos are 30 seconds long at 30 FPS")
    print("   • Uncompressed MP4 format for quality")
    print("   • Each dance shows different movement styles")
    print("   • Motion capture data from real human dancers")


if __name__ == "__main__":
    main()