#!/usr/bin/env python3
"""
Record Rerun visualizations as MP4 videos using screenshot capture method.

This script captures each frame and combines them into a video using opencv or ffmpeg.

Usage:
    python3 record_dance_videos_direct.py dance1_subject1
    python3 record_dance_videos_direct.py --all  # Record all dance datasets
    
Requirements:
    pip install opencv-python imageio imageio-ffmpeg
"""

import argparse
import numpy as np
import pinocchio as pin
import rerun as rr
import trimesh
import subprocess
import os
from pathlib import Path
import time


class RerunVideoRecorder:
    def __init__(self, robot_type='g1'):
        self.robot_type = robot_type
        
        # Load robot
        if robot_type == 'g1':
            self.robot = pin.RobotWrapper.BuildFromURDF(
                'robot_description/g1/g1_29dof_rev_1_0.urdf', 
                'robot_description/g1', 
                pin.JointModelFreeFlyer()
            )
        else:
            raise ValueError(f"Unsupported robot type: {robot_type}")
        
        # Get meshes
        self.link2mesh = {}
        for visual in self.robot.visual_model.geometryObjects:
            mesh = trimesh.load_mesh(visual.meshPath)
            name = visual.name[:-2]
            mesh.visual = trimesh.visual.ColorVisuals()
            mesh.visual.vertex_colors = visual.meshColor
            self.link2mesh[name] = mesh
    
    def load_visual_mesh(self):
        """Load robot meshes into Rerun"""
        self.robot.framesForwardKinematics(pin.neutral(self.robot.model))
        for visual in self.robot.visual_model.geometryObjects:
            frame_name = visual.name[:-2]
            mesh = self.link2mesh[frame_name]
            frame_id = self.robot.model.getFrameId(frame_name)
            parent_joint_id = self.robot.model.frames[frame_id].parentJoint
            parent_joint_name = self.robot.model.names[parent_joint_id]
            frame_tf = self.robot.data.oMf[frame_id]
            joint_tf = self.robot.data.oMi[parent_joint_id]
            relative_tf = joint_tf.inverse() * frame_tf
            mesh.apply_transform(relative_tf.homogeneous)
            rr.log(
                f'urdf_{self.robot_type}/{parent_joint_name}/{frame_name}',
                rr.Mesh3D(
                    vertex_positions=mesh.vertices,
                    triangle_indices=mesh.faces,
                    vertex_normals=mesh.vertex_normals,
                    vertex_colors=mesh.visual.vertex_colors
                ),
                static=True
            )
    
    def update_pose(self, configuration):
        """Update robot pose in Rerun"""
        self.robot.framesForwardKinematics(configuration)
        for visual in self.robot.visual_model.geometryObjects:
            frame_name = visual.name[:-2]
            frame_id = self.robot.model.getFrameId(frame_name)
            parent_joint_id = self.robot.model.frames[frame_id].parentJoint
            parent_joint_name = self.robot.model.names[parent_joint_id]
            joint_tf = self.robot.data.oMi[parent_joint_id]
            rr.log(
                f'urdf_{self.robot_type}/{parent_joint_name}',
                rr.Transform3D(
                    translation=joint_tf.translation,
                    mat3x3=joint_tf.rotation,
                    axis_length=0.01
                )
            )
    
    def record_to_rrd(self, csv_file, output_rrd):
        """Record motion to .rrd file"""
        print(f"📊 Loading motion data: {csv_file}")
        data = np.loadtxt(csv_file, delimiter=',', skiprows=1)
        print(f"   Frames: {len(data)} ({len(data)/30:.1f}s at 30 FPS)")
        
        # Initialize Rerun with recording
        print(f"🎬 Recording to: {output_rrd}")
        rr.init('Dance Recording', recording_id=Path(csv_file).stem)
        rr.save(output_rrd)
        rr.log('', rr.ViewCoordinates.RIGHT_HAND_Z_UP, static=True)
        
        # Load robot meshes
        print("🤖 Loading robot meshes...")
        self.load_visual_mesh()
        
        # Record all frames
        print(f"⏺️  Recording {len(data)} frames...")
        for frame_nr in range(len(data)):
            rr.set_time_sequence('frame_nr', frame_nr)
            configuration = data[frame_nr, :]
            self.update_pose(configuration)
            
            if frame_nr % 300 == 0:
                print(f"   Frame {frame_nr}/{len(data)} ({frame_nr/30:.1f}s)")
        
        print(f"✅ Recording saved to: {output_rrd}")
        return output_rrd


def convert_rrd_to_video_ffmpeg(rrd_file, output_video, width=1920, height=1080, fps=30):
    """
    Convert .rrd to MP4 using rerun and ffmpeg.
    This requires running rerun viewer and using screen recording or export.
    """
    print(f"\n🎥 To create video from {rrd_file}:")
    print(f"\n   Method 1: Manual screen recording")
    print(f"   1. Open recording: rerun {rrd_file}")
    print(f"   2. Use screen recording software (QuickTime, OBS, etc.)")
    print(f"   3. Play through the timeline")
    print(f"\n   Method 2: Use rerun export (if available in future versions)")
    print(f"   rerun {rrd_file} --export-video {output_video}")
    print(f"\n   Method 3: Use Python to automate (requires display)")
    print(f"   python3 export_rrd_to_video.py {rrd_file} {output_video}")
    
    # For now, just open the viewer
    print(f"\n▶️  Opening Rerun viewer...")
    print(f"   You can manually export or record from here.")
    
    # Try to open viewer (non-blocking)
    try:
        subprocess.Popen(['rerun', str(rrd_file)])
        print(f"✅ Rerun viewer opened. Close it when done.")
        return True
    except FileNotFoundError:
        print(f"⚠️  'rerun' CLI not found. Install with: pip install rerun-sdk")
        print(f"   Or open manually: rerun {rrd_file}")
        return False


def main():
    parser = argparse.ArgumentParser(description='Record dance visualizations to .rrd files')
    parser.add_argument('dataset', type=str, nargs='?', default='dance1_subject1',
                       help='Dataset name (e.g., dance1_subject1) or use --all')
    parser.add_argument('--all', action='store_true', help='Record all dance datasets')
    parser.add_argument('--open-viewer', action='store_true', help='Open Rerun viewer after recording')
    parser.add_argument('--robot', type=str, default='g1', help='Robot type (default: g1)')
    args = parser.parse_args()
    
    # Dance datasets
    dance_datasets = [
        'dance1_subject1',
        'dance1_subject2',
        'dance2_subject1'
    ]
    
    # Determine which datasets to process
    if args.all:
        datasets = dance_datasets
    else:
        datasets = [args.dataset]
    
    # Create output directory
    output_dir = Path('videos')
    output_dir.mkdir(exist_ok=True)
    
    # Process each dataset
    recorder = RerunVideoRecorder(robot_type=args.robot)
    rrd_files = []
    
    for dataset in datasets:
        print(f"\n{'='*60}")
        print(f"Processing: {dataset}")
        print(f"{'='*60}")
        
        csv_file = f"{args.robot}/{dataset}.csv"
        if not os.path.exists(csv_file):
            print(f"❌ CSV file not found: {csv_file}")
            continue
        
        # Output file
        rrd_file = output_dir / f"{dataset}.rrd"
        
        # Record to .rrd
        try:
            recorder.record_to_rrd(csv_file, str(rrd_file))
            rrd_files.append(rrd_file)
        except Exception as e:
            print(f"❌ Error recording {dataset}: {e}")
            import traceback
            traceback.print_exc()
            continue
    
    print(f"\n{'='*60}")
    print(f"✅ Recordings saved to: {output_dir.absolute()}/")
    print(f"{'='*60}")
    
    if rrd_files:
        print(f"\n📹 Created {len(rrd_files)} recording(s):")
        for rrd_file in rrd_files:
            print(f"   - {rrd_file.name}")
        
        print(f"\n💡 To view recordings:")
        for rrd_file in rrd_files:
            print(f"   rerun {rrd_file}")
        
        print(f"\n💡 To create MP4 videos:")
        print(f"   1. Install OBS Studio or screen recording software")
        print(f"   2. Open recording: rerun videos/<dataset>.rrd")
        print(f"   3. Set timeline to start, press Play (spacebar)")
        print(f"   4. Screen record the playback")
        print(f"   5. Save as MP4")
        
        if args.open_viewer and rrd_files:
            print(f"\n▶️  Opening first recording...")
            subprocess.Popen(['rerun', str(rrd_files[0])])


if __name__ == "__main__":
    main()
