#!/usr/bin/env python3
"""
🎬 Simple G1 Dataset Video Recorder

A streamlined version that records only the datasets we know work well.
Perfect for quick video generation of core G1 robot motions.

CREATES:
📹 walk.mp4 - Natural human walking motion
📹 squat.mp4 - Up/down squatting exercise  
📹 run.mp4 - Running motion (if available)
📹 stand.mp4 - Standing balance motion
"""

import os
import time
from loco_mujoco.task_factories import ImitationFactory, DefaultDatasetConf

def record_dataset_video(dataset_name, output_dir="G1_Videos", duration_seconds=20):
    """
    Record a single dataset to MP4 video
    
    Args:
        dataset_name (str): Dataset to record (walk, squat, etc.)
        output_dir (str): Directory to save video
        duration_seconds (int): How long to record
    """
    print(f"\n🎬 Recording {dataset_name.upper()} motion")
    print("=" * 50)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        print(f"📋 Loading {dataset_name} dataset...")
        
        # Create environment
        env = ImitationFactory.make(
            "UnitreeG1",
            default_dataset_conf=DefaultDatasetConf([dataset_name]),
            n_substeps=20  # Smooth motion
        )
        
        print(f"✅ Dataset loaded successfully!")
        
        # Calculate episodes and steps
        episodes = 3  # Show 3 cycles
        steps_per_episode = (duration_seconds * 30) // episodes  # ~30 FPS
        
        # Recording parameters (no compression to avoid ffmpeg issues)
        recorder_params = {
            "path": output_dir,
            "video_name": f"{dataset_name}_demo",
            "compress": False  # No compression for compatibility
        }
        
        print(f"🎥 Recording details:")
        print(f"   📹 Output: {output_dir}/{dataset_name}_demo.mp4")
        print(f"   ⏱️  Duration: ~{duration_seconds} seconds")
        print(f"   🎞️  Episodes: {episodes} cycles")
        print(f"   🤖 Motion type: {dataset_name}")
        
        print(f"\n🔴 RECORDING STARTED...")
        print(f"   📹 Creating video of G1 robot performing {dataset_name}")
        print(f"   ⏰ Please wait approximately {duration_seconds + 5} seconds...")
        
        # Record the motion
        start_time = time.time()
        
        env.play_trajectory(
            n_episodes=episodes,
            n_steps_per_episode=steps_per_episode,
            render=True,
            record=True,
            recorder_params=recorder_params
        )
        
        end_time = time.time()
        
        # Check if video was created (may be in timestamped subfolder)
        import glob
        video_pattern = os.path.join(output_dir, "**", f"{dataset_name}_demo.mp4")
        video_files = glob.glob(video_pattern, recursive=True)
        
        if video_files:
            video_path = video_files[0]  # Take the first match
            file_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
            print(f"✅ Recording completed successfully!")
            print(f"   📁 File: {os.path.relpath(video_path, output_dir)}")
            print(f"   💾 Size: {file_size:.1f} MB")
            print(f"   ⏱️  Time taken: {end_time - start_time:.1f} seconds")
            return True
        else:
            print(f"❌ Video file not found in: {output_dir}")
            return False
            
    except Exception as e:
        print(f"❌ Recording failed for {dataset_name}: {e}")
        return False

def main():
    """Record all core G1 datasets"""
    print("🎬 Simple G1 Dataset Video Recorder")
    print("=" * 60)
    print("🤖 Creating MP4 videos of UnitreeG1 robot motions")
    
    # Core datasets that usually work
    datasets_to_record = [
        "walk",    # Walking motion - most reliable
        "squat",   # Squatting motion - usually available
        "run",     # Running motion - may or may not exist
        "stand"    # Standing motion - basic balance
    ]
    
    output_directory = "G1_Motion_Videos"
    video_duration = 25  # seconds per video
    
    print(f"📁 Output directory: {output_directory}")
    print(f"⏱️  Video duration: {video_duration} seconds each")
    print(f"🎯 Datasets to record: {len(datasets_to_record)}")
    
    successful_recordings = []
    failed_recordings = []
    
    # Record each dataset
    for i, dataset in enumerate(datasets_to_record, 1):
        print(f"\n📹 RECORDING {i}/{len(datasets_to_record)}: {dataset}")
        
        success = record_dataset_video(
            dataset_name=dataset,
            output_dir=output_directory,
            duration_seconds=video_duration
        )
        
        if success:
            successful_recordings.append(dataset)
            print(f"✅ {dataset} → Successfully recorded!")
        else:
            failed_recordings.append(dataset)
            print(f"❌ {dataset} → Recording failed")
        
        # Brief pause between recordings (except for last one)
        if i < len(datasets_to_record):
            print("⏸️  Preparing next recording...")
            time.sleep(3)
    
    # Final summary
    print(f"\n🏁 RECORDING SESSION COMPLETE")
    print("=" * 60)
    print(f"✅ Successful: {len(successful_recordings)} videos")
    print(f"❌ Failed: {len(failed_recordings)} videos")
    
    if successful_recordings:
        print(f"\n📹 Successfully created videos:")
        for dataset in successful_recordings:
            print(f"   ✅ {dataset}_demo.mp4")
    
    if failed_recordings:
        print(f"\n⚠️  Failed to create videos for:")
        for dataset in failed_recordings:
            print(f"   ❌ {dataset} (dataset may not exist)")
    
    print(f"\n📁 All videos saved to: {output_directory}/")
    
    # Usage suggestions
    print(f"\n🎓 How to use these videos:")
    print("📺 Perfect for:")
    print("   • Presentations and demos")
    print("   • Understanding robot motion types") 
    print("   • Comparing different locomotion patterns")
    print("   • Educational materials and documentation")
    print("   • Social media and sharing robot capabilities")
    
    print(f"\n💡 Next steps:")
    print("🔧 Customize this script by:")
    print("   • Adding more datasets to the list")
    print("   • Changing video duration (video_duration variable)")
    print("   • Adjusting output directory name")
    print("   • Modifying video quality settings")

if __name__ == "__main__":
    main()