#!/usr/bin/env python3
"""
🎬 Extended G1 Dataset Video Recorder

This version tests many more potential datasets to find all available motions
and creates a comprehensive video library of the UnitreeG1 robot capabilities.
"""

import os
import time
from loco_mujoco.task_factories import ImitationFactory, DefaultDatasetConf

def test_and_record_dataset(dataset_name, output_dir="G1_Extended_Videos", duration=20):
    """
    Test if a dataset exists and record it if available
    
    Returns: (success, file_info)
    """
    print(f"\n🔍 Testing {dataset_name}...", end="")
    
    try:
        # Quick test - try to create environment
        env = ImitationFactory.make(
            "UnitreeG1",
            default_dataset_conf=DefaultDatasetConf([dataset_name]),
            n_substeps=15
        )
        
        print(" ✅ Available! Recording...")
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Recording parameters
        episodes = 2 if duration <= 15 else 3
        steps_per_episode = (duration * 30) // episodes
        
        recorder_params = {
            "path": output_dir,
            "video_name": f"{dataset_name}_motion",
            "compress": False
        }
        
        print(f"   📹 Recording {duration}s of {dataset_name} motion...")
        
        # Record
        start_time = time.time()
        env.play_trajectory(
            n_episodes=episodes,
            n_steps_per_episode=steps_per_episode,
            render=True,
            record=True,
            recorder_params=recorder_params
        )
        end_time = time.time()
        
        # Find the created video file
        import glob
        video_pattern = os.path.join(output_dir, "**", f"{dataset_name}_motion.mp4")
        video_files = glob.glob(video_pattern, recursive=True)
        
        if video_files:
            video_path = video_files[0]
            file_size = os.path.getsize(video_path) / (1024 * 1024)
            
            print(f"   ✅ Recorded! {file_size:.1f}MB in {end_time-start_time:.1f}s")
            
            return True, {
                'dataset': dataset_name,
                'path': video_path,
                'size_mb': file_size,
                'duration': end_time - start_time
            }
        else:
            print(f"   ❌ Video not found after recording")
            return False, None
            
    except Exception as e:
        error_msg = str(e)
        if "404" in error_msg or "Entry Not Found" in error_msg:
            print(" ❌ Not available")
        else:
            print(f" ❌ Error: {error_msg[:50]}...")
        return False, None

def main():
    """Record all available G1 datasets"""
    print("🎬 Extended G1 Dataset Discovery & Recording")
    print("=" * 60)
    print("🔍 Testing all possible dataset names and recording available ones...")
    
    # Comprehensive list of potential dataset names
    potential_datasets = [
        # Basic locomotion
        "walk", "run", "jog", "sprint",
        "walk_slow", "walk_fast", "walk_normal",
        "walk_forward", "walk_backward",
        
        # Directional movement
        "turn_left", "turn_right", "turn_around",
        "sidestep_left", "sidestep_right",
        "strafe_left", "strafe_right",
        
        # Exercise motions
        "squat", "squat_deep", "squat_shallow",
        "lunge", "lunge_left", "lunge_right",
        
        # Dynamic motions
        "jump", "jump_forward", "jump_backward",
        "hop", "leap", "bound",
        
        # Basic postures
        "stand", "stand_still", "balance",
        "sit", "sitdown", "getup",
        "lie", "liedown", "rest",
        
        # Step patterns
        "step", "stepinplace", "march",
        "step_forward", "step_backward",
        
        # Complex motions
        "crawl", "creep", "crouch",
        "kneel", "bow", "bend",
        
        # Athletic motions
        "kick", "punch", "wave",
        "stretch", "reach", "grab",
        
        # Dance/expressive
        "dance", "dance1", "dance2",
        "gesture", "point", "salute",
        
        # Recovery motions
        "recover", "stabilize", "correct",
        "stumble", "slip", "catch",
    ]
    
    print(f"🎯 Testing {len(potential_datasets)} potential datasets...")
    
    successful_recordings = []
    failed_datasets = []
    
    # Test each potential dataset
    for i, dataset in enumerate(potential_datasets, 1):
        print(f"\n[{i:2d}/{len(potential_datasets)}]", end="")
        
        success, file_info = test_and_record_dataset(
            dataset, 
            output_dir="G1_Extended_Videos",
            duration=18  # 18 seconds per video
        )
        
        if success:
            successful_recordings.append(file_info)
        else:
            failed_datasets.append(dataset)
        
        # Brief pause between tests
        time.sleep(1)
    
    # Results summary
    print(f"\n\n🏁 DISCOVERY & RECORDING COMPLETE")
    print("=" * 60)
    print(f"✅ Successfully recorded: {len(successful_recordings)} datasets")
    print(f"❌ Not available: {len(failed_datasets)} datasets")
    
    if successful_recordings:
        total_size = sum(r['size_mb'] for r in successful_recordings)
        print(f"💾 Total video size: {total_size:.1f} MB")
        
        print(f"\n📹 RECORDED DATASETS:")
        print("-" * 40)
        for i, recording in enumerate(successful_recordings, 1):
            print(f"{i:2d}. {recording['dataset']:<15} ({recording['size_mb']:5.1f}MB)")
    
    if failed_datasets:
        print(f"\n❌ UNAVAILABLE DATASETS:")
        print("-" * 40)
        # Show first 20 failed datasets to avoid clutter
        show_count = min(20, len(failed_datasets))
        for i, dataset in enumerate(failed_datasets[:show_count], 1):
            print(f"{i:2d}. {dataset}")
        if len(failed_datasets) > show_count:
            print(f"    ... and {len(failed_datasets) - show_count} more")
    
    # Create a summary file
    summary_path = "G1_Extended_Videos/dataset_summary.txt"
    os.makedirs("G1_Extended_Videos", exist_ok=True)
    
    with open(summary_path, 'w') as f:
        f.write("🤖 UnitreeG1 Extended Dataset Discovery Results\n")
        f.write("=" * 50 + "\n\n")
        f.write(f"Total datasets tested: {len(potential_datasets)}\n")
        f.write(f"Available datasets: {len(successful_recordings)}\n")
        f.write(f"Unavailable datasets: {len(failed_datasets)}\n\n")
        
        f.write("📹 AVAILABLE DATASETS:\n")
        f.write("-" * 30 + "\n")
        for recording in successful_recordings:
            f.write(f"{recording['dataset']} - {recording['size_mb']:.1f}MB\n")
        
        f.write(f"\n❌ UNAVAILABLE DATASETS:\n")
        f.write("-" * 30 + "\n")
        for dataset in failed_datasets:
            f.write(f"{dataset}\n")
    
    print(f"\n📄 Summary saved to: {summary_path}")
    print(f"📁 All videos in: G1_Extended_Videos/")
    
    print(f"\n🎓 USAGE IDEAS:")
    print("📺 Use these videos for:")
    print("   • Complete motion capability demonstrations") 
    print("   • Comparative analysis of locomotion types")
    print("   • Educational content and tutorials")
    print("   • Research presentations and papers")
    print("   • Social media content showcasing robot abilities")

if __name__ == "__main__":
    main()