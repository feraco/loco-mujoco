#!/usr/bin/env python3
"""
🎬 Single Dance Test
Test recording one dance to make sure our method works
"""

import os
import time
import glob
from loco_mujoco.task_factories import ImitationFactory, LAFAN1DatasetConf

def test_single_dance():
    """Test recording a single dance"""
    print("🎬 Testing single dance recording...")
    
    dance_name = "dance2_subject4"  # Known working dance
    output_dir = "G1_Dance_Test"
    
    os.makedirs(output_dir, exist_ok=True)
    
    try:
        print(f"💃 Loading {dance_name}...")
        
        env = ImitationFactory.make(
            "UnitreeG1",
            lafan1_dataset_conf=LAFAN1DatasetConf([dance_name])
        )
        
        print("✅ Dataset loaded!")
        
        recorder_params = {
            "path": output_dir,
            "video_name": f"{dance_name}_test",
            "compress": False
        }
        
        print("🎥 Recording 10 seconds...")
        
        env.play_trajectory(
            n_episodes=1,
            n_steps_per_episode=300,  # 10 seconds
            render=True,
            record=True,
            recorder_params=recorder_params
        )
        
        # Check for video
        video_files = glob.glob(f"{output_dir}/**/*.mp4", recursive=True)
        
        if video_files:
            print(f"✅ SUCCESS! Video created: {video_files[0]}")
            size_mb = os.path.getsize(video_files[0]) / (1024*1024)
            print(f"   Size: {size_mb:.1f}MB")
            return True
        else:
            print("❌ No video file found")
            return False
            
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    finally:
        if 'env' in locals():
            del env

if __name__ == "__main__":
    test_single_dance()