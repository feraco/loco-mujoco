#!/usr/bin/env python3
"""
🎬 G1 Dance Video Recorder
============================================================
Records videos of all LAFAN1 dance datasets using the proven method.
Creates individual MP4 files showcasing G1 robot dance performances.
"""

import os
import time
import glob
from loco_mujoco.task_factories import ImitationFactory, LAFAN1DatasetConf


def record_dance_dataset(dance_name, output_dir="G1_Dance_Videos"):
    """🎥 Record a single dance dataset to video"""
    print(f"\n🎬 Recording {dance_name.upper()} dance")
    print("=" * 50)
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        print(f"💃 Loading {dance_name} dataset...")
        
        # Create environment with dance dataset
        env = ImitationFactory.make(
            "UnitreeG1",
            lafan1_dataset_conf=LAFAN1DatasetConf([dance_name]),
            n_substeps=20  # Smooth motion
        )
        
        print(f"✅ Dance dataset loaded successfully!")
        
        # Recording parameters (using proven method)
        recorder_params = {
            "path": output_dir,
            "video_name": f"{dance_name}_dance",
            "compress": False  # No compression for compatibility
        }
        
        print(f"🎥 Recording details:")
        print(f"   📹 Output: {output_dir}/{dance_name}_dance.mp4")
        print(f"   ⏱️  Duration: ~30 seconds")
        print(f"   💃 Motion: {dance_name} dance sequence")
        
        print(f"\n🔴 RECORDING STARTED...")
        print(f"   📹 Creating video of G1 robot dancing")
        print(f"   ⏰ Please wait approximately 35 seconds...")
        
        # Record the dance motion - longer for full dance
        start_time = time.time()
        
        env.play_trajectory(
            n_episodes=1,  # Single continuous performance
            n_steps_per_episode=900,  # 30 seconds at 30 FPS
            render=True,
            record=True,
            recorder_params=recorder_params
        )
        
        end_time = time.time()
        
        # Check if video was created (may be in timestamped subfolder)
        video_pattern = os.path.join(output_dir, "**", f"{dance_name}_dance.mp4")
        video_files = glob.glob(video_pattern, recursive=True)
        
        if video_files:
            video_path = video_files[0]  # Take the first match
            file_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
            
            # Move to main directory for easier access
            main_video_path = os.path.join(output_dir, f"{dance_name}_dance.mp4")
            if video_path != main_video_path:
                import shutil
                shutil.copy2(video_path, main_video_path)
            
            print(f"✅ Dance recording completed successfully!")
            print(f"   📁 File: {dance_name}_dance.mp4")
            print(f"   💾 Size: {file_size:.1f} MB")
            print(f"   ⏱️  Time taken: {end_time - start_time:.1f} seconds")
            return main_video_path
        else:
            print(f"❌ Video file not found in: {output_dir}")
            return None
            
    except Exception as e:
        print(f"❌ Recording failed for {dance_name}: {e}")
        return None
    
    finally:
        if 'env' in locals():
            del env


def main():
    """🚀 Record all available dance datasets"""
    print("🎬 G1 Dance Video Recorder")
    print("=" * 60)
    print("💃 Creating complete dance video library for UnitreeG1 robot")
    
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
    
    print(f"\n🎯 Found {len(dance_datasets)} dance datasets to record")
    print("📝 Each video will be approximately 30 seconds long")
    
    successful_recordings = []
    failed_recordings = []
    
    # Record each dance dataset
    for i, dance in enumerate(dance_datasets, 1):
        print(f"\n{'='*60}")
        print(f"🎭 DANCE {i}/{len(dance_datasets)}: {dance}")
        print(f"{'='*60}")
        
        video_file = record_dance_dataset(dance)
        
        if video_file and os.path.exists(video_file):
            successful_recordings.append((dance, video_file))
            print(f"   🎉 SUCCESS: {dance} recorded!")
        else:
            failed_recordings.append(dance)
            print(f"   💥 FAILED: {dance} could not be recorded")
        
        # Small delay between recordings
        if i < len(dance_datasets):
            print(f"\n⏱️  Preparing for next recording...")
            time.sleep(2)
    
    # Final summary report
    print(f"\n🏁 DANCE RECORDING SESSION COMPLETE")
    print("=" * 60)
    print(f"✅ Successfully recorded: {len(successful_recordings)} dances")
    print(f"❌ Failed recordings: {len(failed_recordings)} dances")
    
    if successful_recordings:
        print(f"\n🎭 DANCE VIDEO LIBRARY CREATED:")
        print("-" * 40)
        total_size = 0
        
        for dance, video_file in successful_recordings:
            if os.path.exists(video_file):
                size_mb = os.path.getsize(video_file) / (1024*1024)
                total_size += size_mb
                print(f"   💃 {dance:<20} → {os.path.basename(video_file)} ({size_mb:.1f}MB)")
        
        print(f"\n📊 LIBRARY STATISTICS:")
        print(f"   🎬 Total videos: {len(successful_recordings)}")
        print(f"   💾 Total size: {total_size:.1f}MB") 
        print(f"   📁 Location: G1_Dance_Videos/")
        print(f"   ⏱️  Average duration: ~30 seconds each")
    
    if failed_recordings:
        print(f"\n❌ FAILED RECORDINGS:")
        print("-" * 40)
        for dance in failed_recordings:
            print(f"   • {dance}")
        print(f"   💡 These may require manual debugging")
    
    # Usage instructions
    print(f"\n🎓 HOW TO USE YOUR DANCE VIDEOS:")
    print("=" * 60)
    print("🎥 Perfect for:")
    print("   • Showcasing G1 robot dance capabilities")
    print("   • Research presentations on humanoid motion")
    print("   • Educational content on imitation learning")
    print("   • Social media demonstrations")
    print("   • Comparative motion analysis studies")
    print("")
    print("🔧 Technical details:")
    print("   • Format: Uncompressed MP4")
    print("   • Duration: ~30 seconds each")
    print("   • FPS: 30 frames per second")
    print("   • Source: LAFAN1 motion capture database")
    print("   • Robot: UnitreeG1 humanoid")
    
    if successful_recordings:
        print(f"\n🚀 Next steps:")
        print("   1. Review videos in G1_Dance_Videos/ folder")
        print("   2. Use for your research/educational needs")
        print("   3. Share robot dance capabilities!")


if __name__ == "__main__":
    main()