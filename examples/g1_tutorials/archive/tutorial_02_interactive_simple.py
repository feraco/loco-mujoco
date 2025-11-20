#!/usr/bin/env python3
"""
🎮 Tutorial 2: Interactive Robot Control (SIMPLE VERSION)

This version uses the ImitationFactory but shows how you can interact with the robot
during the motion playback to understand control concepts.
"""

import jax
import numpy as np
from loco_mujoco.task_factories import ImitationFactory, DefaultDatasetConf
import time

def explain_concept(title, explanation):
    """Helper function to clearly explain concepts"""
    print(f"\n💡 CONCEPT: {title}")
    print("─" * 60) 
    print(f"   {explanation}")
    print("─" * 60)

def main():
    print("🎮 LocoMuJoCo Tutorial 2: Interactive Robot Control")
    print("=" * 60)
    
    explain_concept(
        "Robot Control Basics",
        "Robots have joints controlled by motors that receive commands.\n"
        "   We'll watch the robot perform different motions and see how\n"  
        "   different movement patterns affect balance and performance."
    )
    
    # Create a robot with motion data for stable demonstration
    print("\n🔨 STEP 1: Creating a Robot with Motion Data")
    print("Creating UnitreeG1 with walking motion...")
    
    try:
        env = ImitationFactory.make(
            "UnitreeG1",
            default_dataset_conf=DefaultDatasetConf(["walk"]),
            n_substeps=20
        )
        
        print("✅ Robot created successfully!")
        print(f"🎮 Control channels: {env.info.action_space.shape[0]} motors")
        print(f"🔍 Sensor channels: {env.info.observation_space.shape[0]} readings")
        
    except Exception as e:
        print(f"❌ Error creating robot: {e}")
        return
    
    explain_concept(
        "What You'll See", 
        "The robot will perform human walking motion while we analyze:\n"
        "   • How joint angles change over time\n"
        "   • How the robot maintains balance\n"
        "   • What good control looks like in practice"
    )
    
    # Reset and start motion analysis
    print("\n🧪 STEP 2: Analyzing Robot Motion")
    print("Starting motion analysis with real-time data...")
    print("👀 Watch for the MuJoCo viewer window to appear!")
    print("🖥️  If no window appears, check if another window opened behind this terminal")
    print("💡 On some systems, the viewer might not display due to graphics settings")
    print("📊 Don't worry - you can still see the data analysis below!")
    print("🎮 VIEWER CONTROLS (if window appears):")
    print("   SPACEBAR = Pause/Resume")
    print("   R = Restart") 
    print("   ESC = Exit")
    print("   Mouse = Camera control")
    
    key = jax.random.PRNGKey(42)
    obs = env.reset(key)
    
    # Track robot performance over time
    heights = []
    joint_angles = []
    step_count = 0
    
    print("\n🤖 Starting motion demonstration...")
    print("📊 Real-time robot analysis:")
    
    try:
        for step in range(500):  # About 15 seconds of motion
            # Step the environment (plays back dataset motion)
            step_result = env.step(np.zeros(env.info.action_space.shape[0]))
            
            if len(step_result) == 5:
                obs, reward, done, truncated, info = step_result
            elif len(step_result) == 4:
                obs, reward, done, info = step_result
            else:
                obs, reward, done = step_result
                info = {}
            
            # Extract robot state information
            if len(obs) >= 10:
                height = obs[2] if len(obs) > 2 else 1.0
                heights.append(height)
                
                # Store some joint angles for analysis
                if len(obs) > 7:
                    joint_angles.append(obs[7:17])  # First 10 joints
            
            # Show progress every 50 steps
            if step % 50 == 0:
                avg_height = np.mean(heights[-50:]) if heights else 1.0
                print(f"   Step {step:3d}: Height={avg_height:.3f}m, Reward={reward:.3f}")
            
            # Render the simulation
            try:
                env.render()
            except Exception as render_error:
                if step == 0:
                    print(f"⚠️  Rendering note: {render_error}")
            
            # Reset if episode ends
            if done:
                obs = env.reset(key)
                print(f"   Episode completed at step {step}, restarting...")
            
            step_count += 1
            
            # Small delay for smooth visualization
            time.sleep(0.03)
            
    except KeyboardInterrupt:
        print("\n⏸️  Demonstration stopped by user")
    except Exception as e:
        print(f"\n⚠️  Demonstration stopped: {e}")
    
    # Analysis summary
    print(f"\n📊 STEP 3: Motion Analysis Summary")
    print("=" * 50)
    
    if heights:
        avg_height = np.mean(heights)
        height_std = np.std(heights)
        print(f"📏 Average robot height: {avg_height:.3f} ± {height_std:.3f} meters")
        print(f"🎯 Height range: {np.min(heights):.3f} to {np.max(heights):.3f} meters")
        
        # Simple analysis
        if height_std < 0.1:
            print("✅ Very stable motion - robot maintains consistent height")
        elif height_std < 0.2:
            print("✅ Stable motion with some natural variation")
        else:
            print("⚠️  Dynamic motion - robot height varies significantly")
    
    if joint_angles:
        joint_angles = np.array(joint_angles)
        print(f"🦾 Analyzed {len(joint_angles)} joint configurations")
        print(f"🔄 Joint motion range: {np.std(joint_angles):.3f} radians average variation")
    
    print(f"⏱️  Total steps analyzed: {step_count}")
    
    # Educational summary
    print("\n🎓 TUTORIAL COMPLETE - What You Just Learned:")
    print("=" * 60)
    print("✅ Robots use continuous sensor feedback to maintain control")
    print("✅ Good motion has consistent patterns and stable performance")  
    print("✅ Height and joint data reveal robot stability and control quality")
    print("✅ Real-time analysis helps understand robot behavior")
    
    explain_concept(
        "Key Insights",
        "• STABLE HEIGHT: Shows the robot maintains good balance\n"
        "   • JOINT COORDINATION: Multiple joints work together smoothly\n"
        "   • CONTINUOUS CONTROL: Robot constantly adjusts to stay stable\n"
        "   • DATA ANALYSIS: Numbers reveal what's hard to see by watching"
    )
    
    print("\n🏆 EXPERIMENT TIME!")
    print("Try modifying this tutorial:")
    print("💡 Change 'walk' to 'squat' or 'jump' to see different motion patterns")
    print("💡 Increase n_substeps for smoother (slower) motion")
    print("💡 Try different robots: 'UnitreeH1', 'Atlas'")
    print("💡 Adjust the analysis period (change range(500))")
    
    explain_concept(
        "What's Next?",
        "Now you've seen stable robot control in action! Next tutorials:\n"
        "   • Learn about data visualization and motion comparison\n"
        "   • Understand how robots learn from human motion data\n" 
        "   • Explore advanced control and machine learning concepts"
    )

if __name__ == "__main__":
    main()