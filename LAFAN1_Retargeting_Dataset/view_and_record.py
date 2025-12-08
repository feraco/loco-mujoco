#!/usr/bin/env python3
"""
Open Rerun recordings and automatically record them as videos using ffmpeg screen capture.

Usage:
    python3 view_and_record.py dance1_subject1
    python3 view_and_record.py --all
    python3 view_and_record.py dance1_subject1 --manual  # Manual recording only

For macOS, this uses ffmpeg with avfoundation to capture the screen.
For Linux, this uses ffmpeg with x11grab.
"""

import argparse
import subprocess
import time
from pathlib import Path
import os
import sys
import signal


def open_rerun_viewer(rrd_file):
    """Open Rerun viewer for an .rrd file"""
    print(f"\n{'='*60}")
    print(f"Opening: {rrd_file}")
    print(f"{'='*60}")
    
    if not os.path.exists(rrd_file):
        print(f"❌ File not found: {rrd_file}")
        return None
    
    try:
        # Open rerun viewer (non-blocking)
        process = subprocess.Popen(['rerun', str(rrd_file)])
        print(f"✅ Rerun viewer opened (PID: {process.pid})")
        return process
    except FileNotFoundError:
        print(f"❌ 'rerun' command not found. Install with:")
        print(f"   pip install rerun-sdk")
        return None
    except Exception as e:
        print(f"❌ Error opening viewer: {e}")
        return None


def start_screen_recording_macos(output_file, duration=None):
    """Start screen recording on macOS using ffmpeg"""
    print(f"\n🎬 Starting screen recording...")
    print(f"   Output: {output_file}")
    
    # Wait for user to position Rerun window
    print(f"\n⚠️  IMPORTANT:")
    print(f"   1. Make sure Rerun viewer window is visible and maximized")
    print(f"   2. Press spacebar in Rerun to start playback NOW")
    print(f"   3. This will record for {duration}s" if duration else "   3. Press Ctrl+C to stop recording")
    print(f"\n   ⚡ Screen recording will start in 3 seconds...")
    time.sleep(3)
    
    # For macOS avfoundation:
    # Device 2 = "Capture screen 0" (main display)
    # Use :none for no audio
    
    cmd = [
        'ffmpeg',
        '-f', 'avfoundation',
        '-framerate', '30',
        '-i', '2:none',  # Screen capture device 2, no audio
        '-vcodec', 'mpeg4',
        '-q:v', '5',  # Quality (1-31, lower = better)
        '-pix_fmt', 'yuv420p',
        '-y',  # Overwrite output file
        str(output_file)
    ]
    
    if duration:
        cmd.extend(['-t', str(duration)])
    
    print(f"🔴 Recording started! ({duration}s)" if duration else "🔴 Recording started!")
    print(f"   DO NOT move or minimize the Rerun window")
    
    try:
        # Redirect stderr to see ffmpeg output
        process = subprocess.Popen(cmd, 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.STDOUT,
                                  universal_newlines=True)
        return process
    except Exception as e:
        print(f"❌ Error starting recording: {e}")
        return None


def start_screen_recording_linux(output_file, duration=None):
    """Start screen recording on Linux using ffmpeg"""
    print(f"\n🎬 Starting screen recording...")
    print(f"   Output: {output_file}")
    
    print(f"\n⚠️  IMPORTANT:")
    print(f"   1. Position the Rerun viewer window prominently")
    print(f"   2. Press spacebar in Rerun to start playback")
    input(f"\nPress Enter when ready to start recording...")
    
    cmd = [
        'ffmpeg',
        '-video_size', '1920x1080',
        '-framerate', '30',
        '-f', 'x11grab',
        '-i', ':0.0',
        '-vcodec', 'h264_videotoolbox',
        '-b:v', '5000k',
        '-pix_fmt', 'yuv420p',
        '-y',
        str(output_file)
    ]
    
    if duration:
        cmd.extend(['-t', str(duration)])
    
    print(f"▶️  Recording started! (Press Ctrl+C to stop)")
    
    try:
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return process
    except Exception as e:
        print(f"❌ Error starting recording: {e}")
        return None


def stop_recording(process):
    """Stop the recording process gracefully"""
    if process and process.poll() is None:
        print(f"\n⏹️  Stopping recording...")
        process.send_signal(signal.SIGINT)  # Send Ctrl+C
        try:
            process.wait(timeout=10)
            print(f"✅ Recording stopped")
        except subprocess.TimeoutExpired:
            process.kill()
            print(f"⚠️  Recording force stopped")


def record_dataset(rrd_file, output_video, auto_record=True, duration=None):
    """Open Rerun viewer and optionally start screen recording"""
    
    # Open Rerun viewer
    viewer_process = open_rerun_viewer(rrd_file)
    if not viewer_process:
        return False
    
    # Wait for viewer to fully load
    print(f"⏳ Waiting for Rerun viewer to load (5 seconds)...")
    time.sleep(5)
    
    print(f"\n{'='*60}")
    print(f"⚠️  SETUP INSTRUCTIONS:")
    print(f"{'='*60}")
    print(f"1. Make sure the Rerun window is visible (maximize it)")
    print(f"2. Press SPACEBAR in Rerun to start the animation")
    print(f"3. The animation should now be playing")
    print(f"{'='*60}")
    input(f"\nPress Enter when the animation is PLAYING...")
    
    recording_process = None
    
    if auto_record:
        # Detect OS and start appropriate recording
        if sys.platform == 'darwin':  # macOS
            recording_process = start_screen_recording_macos(output_video, duration)
        elif sys.platform.startswith('linux'):
            recording_process = start_screen_recording_linux(output_video, duration)
        else:
            print(f"⚠️  Automatic recording not supported on {sys.platform}")
            print(f"   Use QuickTime or OBS Studio manually")
            auto_record = False
    
    if auto_record and recording_process:
        try:
            if duration:
                # Wait for specified duration
                print(f"⏱️  Recording for {duration} seconds...")
                print(f"   Progress: ", end='', flush=True)
                
                for i in range(duration):
                    time.sleep(1)
                    if (i + 1) % 10 == 0:
                        print(f"{i+1}s ", end='', flush=True)
                
                print(f"\n⏹️  Duration complete, stopping recording...")
                recording_process.send_signal(signal.SIGINT)
                
                # Give FFmpeg time to finalize the file
                print(f"⏳ Finalizing video file...")
                try:
                    stdout, _ = recording_process.communicate(timeout=10)
                except subprocess.TimeoutExpired:
                    print(f"⚠️  FFmpeg taking too long, forcing stop...")
                    recording_process.kill()
                    stdout, _ = recording_process.communicate()
                if stdout:
                    print(f"\nFFmpeg output (last lines):")
                    lines = stdout.split('\n')
                    for line in lines[-5:]:
                        if line.strip():
                            print(f"  {line}")
            else:
                # Wait for user to stop
                print(f"\n⏺️  Recording in progress...")
                print(f"   Press Ctrl+C to stop recording")
                recording_process.wait()
        except KeyboardInterrupt:
            stop_recording(recording_process)
        except subprocess.TimeoutExpired:
            recording_process.kill()
    else:
        # Manual mode - just wait for user
        print(f"\n📹 Manual recording mode")
        print(f"   Close the Rerun viewer when done")
        try:
            viewer_process.wait()
        except KeyboardInterrupt:
            pass
    
    # Cleanup
    if viewer_process and viewer_process.poll() is None:
        print(f"🧹 Closing Rerun viewer...")
        viewer_process.terminate()
        time.sleep(1)
    
    if recording_process and recording_process.poll() is None:
        stop_recording(recording_process)
    
    # Verify output file
    if os.path.exists(output_video):
        size = os.path.getsize(output_video)
        size_mb = size / (1024 * 1024)
        print(f"\n✅ Video created: {output_video}")
        print(f"   Size: {size_mb:.1f} MB")
        return True
    else:
        print(f"\n⚠️  Warning: Output file not found: {output_video}")
        return False


def print_recording_instructions():
    """Print instructions for screen recording"""
    print(f"\n{'='*60}")
    print("📹 HOW TO RECORD VIDEOS FROM RERUN")
    print(f"{'='*60}\n")
    
    print("Method 1: macOS QuickTime Player (Easiest)")
    print("-" * 40)
    print("1. Open QuickTime Player")
    print("2. File > New Screen Recording")
    print("3. Click the red record button")
    print("4. Select the Rerun viewer window")
    print("5. In Rerun: Press spacebar to play the animation")
    print("6. When done, click Stop in menu bar")
    print("7. File > Export As > 1080p or 4K")
    print("8. Save as .mp4")
    
    print("\nMethod 2: OBS Studio (Free, All Platforms)")
    print("-" * 40)
    print("1. Download OBS Studio: https://obsproject.com/")
    print("2. Add Source > Window Capture")
    print("3. Select Rerun viewer window")
    print("4. Click Start Recording")
    print("5. In Rerun: Press spacebar to play")
    print("6. When done, click Stop Recording")
    print("7. Videos saved to ~/Movies/ or ~/Videos/")
    
    print("\nMethod 3: ffmpeg Screen Capture (Advanced)")
    print("-" * 40)
    print("macOS:")
    print("  ffmpeg -f avfoundation -i '1:0' -r 30 output.mp4")
    print("Linux:")
    print("  ffmpeg -video_size 1920x1080 -framerate 30 -f x11grab \\")
    print("    -i :0.0 output.mp4")
    
    print("\n💡 Rerun Viewer Tips:")
    print("-" * 40)
    print("• Timeline is at the bottom of the viewer")
    print("• Spacebar = Play/Pause")
    print("• Drag timeline scrubber to navigate")
    print("• Mouse drag = Rotate view")
    print("• Scroll = Zoom")
    print("• Right-click drag = Pan")
    
    print(f"\n{'='*60}\n")


def main():
    parser = argparse.ArgumentParser(description='View and record Rerun visualizations')
    parser.add_argument('dataset', type=str, nargs='?',
                       help='Dataset name (e.g., dance1_subject1) or use --all')
    parser.add_argument('--all', action='store_true', help='Record all datasets')
    parser.add_argument('--manual', action='store_true', help='Manual recording mode (no auto screen capture)')
    parser.add_argument('--duration', type=int, help='Recording duration in seconds (auto-calculated from data if not specified)')
    parser.add_argument('--instructions', action='store_true', help='Show recording instructions only')
    args = parser.parse_args()
    
    if args.instructions:
        print_recording_instructions()
        return
    
    # Dance datasets with durations (frames / 30 fps)
    dance_info = {
        'dance1_subject1': 3944 / 30,  # ~131 seconds
        'dance1_subject2': 3944 / 30,  # ~131 seconds
        'dance2_subject1': 6770 / 30,  # ~226 seconds
    }
    
    videos_dir = Path('videos')
    if not videos_dir.exists():
        print(f"❌ Videos directory not found: {videos_dir}")
        print("   Run record_dance_videos_direct.py first to create .rrd files")
        return
    
    # Determine which recordings to process
    if args.all:
        datasets = list(dance_info.keys())
    elif args.dataset:
        datasets = [args.dataset]
    else:
        # Show available recordings
        rrd_files = list(videos_dir.glob('*.rrd'))
        if not rrd_files:
            print(f"❌ No .rrd files found in {videos_dir}/")
            print("   Run record_dance_videos_direct.py first")
            return
        
        print(f"\n📹 Available recordings in {videos_dir}/:")
        for i, rrd in enumerate(rrd_files, 1):
            print(f"   {i}. {rrd.name}")
        
        print("\nUsage:")
        print(f"  python3 {Path(__file__).name} dance1_subject1")
        print(f"  python3 {Path(__file__).name} --all")
        print(f"  python3 {Path(__file__).name} dance1_subject1 --manual")
        print(f"  python3 {Path(__file__).name} --instructions")
        return
    
    if not args.manual:
        print(f"\n{'='*60}")
        print("🎬 AUTOMATIC SCREEN RECORDING MODE")
        print(f"{'='*60}")
        print(f"This will use ffmpeg to capture the Rerun viewer.")
        print(f"Make sure ffmpeg is installed: which ffmpeg")
        print(f"\nFor manual recording, use: --manual flag")
        print(f"{'='*60}\n")
    
    # Process each dataset
    for dataset in datasets:
        rrd_file = videos_dir / f"{dataset}.rrd"
        output_video = videos_dir / f"{dataset}.mp4"
        
        if not rrd_file.exists():
            print(f"\n⚠️  Recording not found: {rrd_file}")
            continue
        
        # Calculate duration
        duration = args.duration
        if not duration and dataset in dance_info:
            duration = int(dance_info[dataset]) + 5  # Add 5 seconds buffer
        
        print(f"\n{'='*60}")
        print(f"Dataset: {dataset}")
        if duration:
            print(f"Duration: {duration} seconds")
        print(f"Output: {output_video}")
        print(f"{'='*60}")
        
        # Record
        success = record_dataset(rrd_file, output_video, 
                                auto_record=not args.manual, 
                                duration=duration)
        
        if success and not args.manual:
            print(f"\n✅ Video saved: {output_video}")
        
        if args.all and dataset != datasets[-1]:
            print(f"\n⏸️  Press Enter to continue to next dataset...")
            input()
    
    print(f"\n{'='*60}")
    print(f"✅ All done! Videos in: {videos_dir.absolute()}/")
    print(f"{'='*60}")


if __name__ == "__main__":
    main()
