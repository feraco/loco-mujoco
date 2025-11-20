#!/usr/bin/env python3
"""
G1 Dataset Tutorial: Automated Motion Recording
This script replays each available UnitreeG1 dataset and records the MuJoCo viewer output to video files.
"""

import numpy as np
from loco_mujoco.task_factories import ImitationFactory, DefaultDatasetConf
import os

def main():
    print("🤖 UnitreeG1 Automated Dataset Recording")
    print("=" * 60)
    
    # Only use datasets confirmed available
    datasets_to_record = ["walk", "squat"]
    output_dir = "./G1_recordings"
    os.makedirs(output_dir, exist_ok=True)
    
    for i, dataset_name in enumerate(datasets_to_record):
        print(f"\n🎯 Recording {i+1}/{len(datasets_to_record)}: {dataset_name.upper()}")
        print("=" * 40)
        
        # Create environment for this dataset
        env = ImitationFactory.make(
            "UnitreeG1",
            default_dataset_conf=DefaultDatasetConf([dataset_name]),
            n_substeps=20
        )
        
        recorder_params = {
            "path": output_dir,
            "video_name": f"{dataset_name}_demo",
            "fps": 30,
            "compress": True
        }
        print(f"   🤖 Recording G1 performing: {dataset_name}")
        print(f"   ⏱️  Duration: ~60 seconds")
        print(f"   📹 Output: {output_dir}/{dataset_name}_demo.mp4")
        
        # Play and record
        env.play_trajectory(
            n_episodes=3,
            n_steps_per_episode=1000,
            render=True,
            record=True,
            recorder_params=recorder_params
        )
        print(f"✅ Recording complete for {dataset_name}!\n")
    
    print("\n✅ All G1 dataset recordings completed!")
    print(f"💡 Videos saved in: {output_dir}")

if __name__ == "__main__":
    main()
