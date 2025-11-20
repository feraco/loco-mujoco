#!/usr/bin/env python3
"""
🎬 G1 Complete Dataset Video Recorder

This script automatically runs through ALL available UnitreeG1 datasets and records
each one to a separate video file. Perfect for creating a visual library of all
robot motions or for presentations and documentation.

WHAT THIS CREATES:
📹 Individual MP4 videos for each dataset
📊 Summary report of all recorded motions
🎨 High-quality recordings with optimal camera angles
⏱️  Configurable duration and quality settings

OUTPUT STRUCTURE:
📁 G1_Dataset_Videos/
   📹 walk.mp4
   📹 squat.mp4
   📹 run.mp4
   📹 stand.mp4
   📄 recording_summary.txt
"""

import os
import time
import numpy as np
from loco_mujoco.task_factories import ImitationFactory, DefaultDatasetConf
from datetime import datetime
import json

class G1DatasetRecorder:
    """Complete G1 dataset video recording system"""
    
    def __init__(self, output_dir="G1_Dataset_Videos", video_quality="high"):
        """
        Initialize the recorder
        
        Args:
            output_dir (str): Directory to save videos
            video_quality (str): 'low', 'medium', 'high', 'ultra'
        """
        self.output_dir = output_dir
        self.video_quality = video_quality
        
        # Create output directory
        os.makedirs(output_dir, exist_ok=True)
        
        # Quality settings
        self.quality_settings = {
            'low': {'fps': 24, 'compress': True, 'resolution_scale': 0.5},
            'medium': {'fps': 30, 'compress': True, 'resolution_scale': 0.75},
            'high': {'fps': 30, 'compress': False, 'resolution_scale': 1.0},
            'ultra': {'fps': 60, 'compress': False, 'resolution_scale': 1.0}
        }
        
        # All available G1 datasets (comprehensive list)
        self.available_datasets = [
            # Basic locomotion
            "walk", "run", "stand", 
            
            # Exercise motions  
            "squat",
            
            # Dynamic motions
            "jump",
            
            # Variations (some might not exist, will handle gracefully)
            "walk_slow", "walk_fast", 
            "stepinplace", "crawl",
            "dance", "wave",
            
            # Directional movement
            "walk_forward", "walk_backward", 
            "turn_left", "turn_right",
            
            # Complex motions
            "getup", "sitdown", "lie", 
            "punch", "kick"
        ]
        
        self.successful_recordings = []
        self.failed_recordings = []
        
    def test_dataset_availability(self):
        """Test which datasets are actually available"""
        print("🔍 Testing dataset availability...")
        print("=" * 60)
        
        working_datasets = []
        
        for dataset in self.available_datasets:
            print(f"Testing {dataset}...", end=" ")
            try:
                # Quick test - try to create environment
                env = ImitationFactory.make(
                    "UnitreeG1",
                    default_dataset_conf=DefaultDatasetConf([dataset]),
                    n_substeps=10
                )
                print("✅ Available")
                working_datasets.append(dataset)
                
            except Exception as e:
                print(f"❌ Not available ({str(e)[:50]}...)")
        
        print(f"\n📊 Found {len(working_datasets)} available datasets:")
        for i, dataset in enumerate(working_datasets, 1):
            print(f"  {i:2d}. {dataset}")
        
        return working_datasets
    
    def record_single_dataset(self, dataset_name, duration_seconds=20, episodes=2):
        """
        Record a single dataset to video
        
        Args:
            dataset_name (str): Name of the dataset
            duration_seconds (int): How long to record
            episodes (int): Number of episode cycles to show
        """
        print(f"\n🎬 Recording {dataset_name.upper()}")
        print("=" * 50)
        
        try:
            # Create environment for this dataset
            print(f"📋 Loading {dataset_name} dataset...")
            env = ImitationFactory.make(
                "UnitreeG1",
                default_dataset_conf=DefaultDatasetConf([dataset_name]),
                n_substeps=20  # Smooth motion
            )
            
            # Calculate recording parameters
            total_steps = duration_seconds * 30  # Assuming 30 FPS
            steps_per_episode = total_steps // episodes
            
            # Video settings
            quality = self.quality_settings[self.video_quality]
            video_filename = f"{dataset_name}.mp4"
            video_path = os.path.join(self.output_dir, video_filename)
            
            recorder_params = {
                "path": self.output_dir,
                "video_name": dataset_name,
                "compress": quality['compress']
            }
            
            print(f"🎥 Recording settings:")
            print(f"   📹 Output: {video_path}")
            print(f"   ⏱️  Duration: {duration_seconds} seconds")
            print(f"   🎞️  Episodes: {episodes}")
            print(f"   📐 Quality: {self.video_quality} ({quality['fps']} fps)")
            print(f"   🤖 Motion: {dataset_name}")
            
            # Record with nice visual message
            print(f"\n🔴 RECORDING IN PROGRESS...")
            print(f"   📹 Creating: {video_filename}")
            print(f"   ⏰ Estimated time: {duration_seconds + 5} seconds")
            print(f"   🎬 Please wait while robot performs {dataset_name} motion...")
            
            # Start recording
            start_time = time.time()
            
            env.play_trajectory(
                n_episodes=episodes,
                n_steps_per_episode=steps_per_episode,
                render=True,
                record=True,
                recorder_params=recorder_params
            )
            
            end_time = time.time()
            actual_duration = end_time - start_time
            
            # Verify video was created
            if os.path.exists(video_path):
                file_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
                print(f"✅ Recording successful!")
                print(f"   📁 File: {video_filename} ({file_size:.1f} MB)")
                print(f"   ⏱️  Actual duration: {actual_duration:.1f}s")
                
                self.successful_recordings.append({
                    'dataset': dataset_name,
                    'filename': video_filename,
                    'size_mb': file_size,
                    'duration': actual_duration,
                    'quality': self.video_quality
                })
                
                return True
            else:
                print(f"❌ Video file not created: {video_path}")
                self.failed_recordings.append({
                    'dataset': dataset_name,
                    'error': 'Video file not created'
                })
                return False
                
        except Exception as e:
            print(f"❌ Recording failed: {e}")
            self.failed_recordings.append({
                'dataset': dataset_name,
                'error': str(e)
            })
            return False
    
    def record_all_datasets(self, duration_per_video=20):
        """Record all available datasets"""
        print("🎬 G1 Complete Dataset Video Recorder")
        print("=" * 60)
        print(f"📁 Output directory: {self.output_dir}")
        print(f"🎥 Video quality: {self.video_quality}")
        print(f"⏱️  Duration per video: {duration_per_video} seconds")
        
        # Test availability first
        working_datasets = self.test_dataset_availability()
        
        if not working_datasets:
            print("❌ No working datasets found!")
            return
        
        print(f"\n🚀 Starting batch recording of {len(working_datasets)} datasets...")
        print("🎯 This will create individual MP4 files for each motion type")
        
        # Record each dataset
        for i, dataset in enumerate(working_datasets, 1):
            print(f"\n📹 RECORDING {i}/{len(working_datasets)}")
            
            success = self.record_single_dataset(
                dataset, 
                duration_seconds=duration_per_video,
                episodes=3  # Show 3 cycles of each motion
            )
            
            if success:
                print(f"✅ {dataset} recorded successfully!")
            else:
                print(f"❌ {dataset} recording failed")
            
            # Brief pause between recordings
            if i < len(working_datasets):
                print("⏸️  Brief pause before next recording...")
                time.sleep(2)
        
        # Create summary report
        self.create_summary_report()
        
        # Final results
        print(f"\n🏁 BATCH RECORDING COMPLETE")
        print("=" * 60)
        print(f"✅ Successfully recorded: {len(self.successful_recordings)} videos")
        print(f"❌ Failed recordings: {len(self.failed_recordings)}")
        print(f"📁 All files saved to: {self.output_dir}")
        
        if self.successful_recordings:
            total_size = sum(r['size_mb'] for r in self.successful_recordings)
            print(f"💾 Total size: {total_size:.1f} MB")
            print(f"🎬 Video files created:")
            for recording in self.successful_recordings:
                print(f"   📹 {recording['filename']} ({recording['size_mb']:.1f} MB)")
    
    def create_summary_report(self):
        """Create a summary report of all recordings"""
        report_path = os.path.join(self.output_dir, "recording_summary.txt")
        
        with open(report_path, 'w') as f:
            f.write("🤖 UnitreeG1 Dataset Recording Summary\n")
            f.write("=" * 50 + "\n\n")
            f.write(f"Recording Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Video Quality: {self.video_quality}\n")
            f.write(f"Output Directory: {self.output_dir}\n\n")
            
            f.write(f"📊 SUCCESSFUL RECORDINGS ({len(self.successful_recordings)}):\n")
            f.write("-" * 30 + "\n")
            for recording in self.successful_recordings:
                f.write(f"Dataset: {recording['dataset']}\n")
                f.write(f"File: {recording['filename']}\n") 
                f.write(f"Size: {recording['size_mb']:.1f} MB\n")
                f.write(f"Duration: {recording['duration']:.1f} seconds\n\n")
            
            if self.failed_recordings:
                f.write(f"❌ FAILED RECORDINGS ({len(self.failed_recordings)}):\n")
                f.write("-" * 30 + "\n")
                for failure in self.failed_recordings:
                    f.write(f"Dataset: {failure['dataset']}\n")
                    f.write(f"Error: {failure['error']}\n\n")
            
            total_size = sum(r['size_mb'] for r in self.successful_recordings)
            f.write(f"Total Size: {total_size:.1f} MB\n")
            f.write(f"Total Videos: {len(self.successful_recordings)}\n")
        
        print(f"📄 Summary report saved: {report_path}")

def main():
    """Main function with user options"""
    print("🎬 G1 Dataset Video Recording System")
    print("=" * 60)
    
    # Configuration options
    print("🔧 Configuration Options:")
    print("💡 You can modify these settings in the code:")
    print("   📁 output_dir: Where to save videos")
    print("   🎥 video_quality: low/medium/high/ultra") 
    print("   ⏱️  duration_per_video: Seconds per recording")
    print("   🎞️  episodes: Number of motion cycles per video")
    
    # Create recorder with settings
    recorder = G1DatasetRecorder(
        output_dir="G1_Complete_Dataset_Videos",
        video_quality="high"  # Change to: low, medium, high, ultra
    )
    
    # Record all datasets
    recorder.record_all_datasets(duration_per_video=25)  # 25 seconds each
    
    print("\n🎓 Usage Tips:")
    print("📹 Use these videos for:")
    print("   • Documentation and presentations")
    print("   • Comparing different motion types")  
    print("   • Creating training materials")
    print("   • Sharing robot capabilities")
    print("   • Research analysis and publications")
    
    print("\n🏆 Next Steps:")
    print("💡 Try modifying the script to:")
    print("   • Change video quality settings")
    print("   • Adjust recording duration")
    print("   • Add custom camera angles")
    print("   • Include multiple robot models")

if __name__ == "__main__":
    main()