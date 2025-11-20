#!/usr/bin/env python3
"""
🎬 G1 Dance Dataset Recorder (Fixed)
============================================================
Records videos of all LAFAN1 dance datasets using the working approach.
"""

import os
import time
import glob
from datetime import datetime
from loco_mujoco.task_factories import ImitationFactory, LAFAN1DatasetConf


def record_dance_video(dance_name):
    """🎥 Record a dance video using the working method"""
    print(f"\n🎬 Recording: {dance_name}")
    
    try:
        # Create environment
        env = ImitationFactory.make("UnitreeG1", 
                                  lafan1_dataset_conf=LAFAN1DatasetConf([dance_name]))
        
        print(f"   📹 Recording 30s dance sequence...")
        
        # Use the working approach from our previous recorders
        env.play_trajectory(
            n_episodes=3,  # Multiple episodes for variety
            n_steps_per_episode=300,  # 10 seconds each episode
            render=True,  # Enable rendering
            recorder_params={
                'record_video': True,
                'video_path': f'G1_Dance_Videos/{dance_name}_dance.mp4',
                'fps': 30
            }
        )
        
        # Check if video was created
        expected_video = f'G1_Dance_Videos/{dance_name}_dance.mp4'
        if os.path.exists(expected_video):
            size_mb = os.path.getsize(expected_video) / (1024*1024)
            print(f"   ✅ Success! {expected_video} ({size_mb:.1f}MB)")
            return expected_video
        else:
            # Look for any mp4 files that might have been created
            video_files = glob.glob('LocoMuJoCo_recordings/**/*.mp4', recursive=True)
            if video_files:
                # Use the most recent one
                latest_video = max(video_files, key=os.path.getmtime)
                
                # Move and rename it
                os.makedirs('G1_Dance_Videos', exist_ok=True)
                new_name = f'G1_Dance_Videos/{dance_name}_dance.mp4'
                
                import shutil
                shutil.copy2(latest_video, new_name)
                
                size_mb = os.path.getsize(new_name) / (1024*1024)
                print(f"   ✅ Success! {new_name} ({size_mb:.1f}MB)")
                return new_name
            else:
                print(f"   ❌ No video file found")
                return None
                
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:80]}...")
        return None
    finally:
        if 'env' in locals():
            del env


def main():
    """🚀 Record all dance datasets"""
    print("🎬 G1 Dance Dataset Recorder (Fixed)")
    print("=" * 60)
    
    # All dance datasets
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
    
    print(f"💃 Recording {len(dance_datasets)} dance datasets...")
    
    # Create output directory
    os.makedirs('G1_Dance_Videos', exist_ok=True)
    
    successful_recordings = []
    
    # Record each dance
    for i, dance in enumerate(dance_datasets, 1):
        print(f"\n[{i}/{len(dance_datasets)}] {dance}")
        
        video_file = record_dance_video(dance)
        if video_file:
            successful_recordings.append((dance, video_file))
        
        # Small delay between recordings
        time.sleep(1)
    
    # Final summary
    print(f"\n🏁 RECORDING COMPLETE")
    print("=" * 60)
    print(f"✅ Successfully recorded: {len(successful_recordings)}/{len(dance_datasets)} dances")
    
    if successful_recordings:
        print(f"\n🎭 DANCE VIDEO LIBRARY:")
        total_size = 0
        for dance, video_file in successful_recordings:
            if os.path.exists(video_file):
                size_mb = os.path.getsize(video_file) / (1024*1024)
                total_size += size_mb
                print(f"   📹 {dance:<20} → {os.path.basename(video_file)} ({size_mb:.1f}MB)")
        
        print(f"\n📊 Total library size: {total_size:.1f}MB")
        print(f"📁 All videos saved in: G1_Dance_Videos/")
        
        print(f"\n🎯 HOW TO USE:")
        print("   • Perfect for showcasing G1 robot dance capabilities")
        print("   • Great for research presentations and demos") 
        print("   • Educational content on humanoid motion")
        print("   • Social media content")
    
    else:
        print("\n❌ No videos were successfully recorded.")
        print("💡 Try running individual dance recordings to debug issues.")


if __name__ == "__main__":
    main()