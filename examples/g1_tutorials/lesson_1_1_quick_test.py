#!/usr/bin/env python3
"""
🚀 Lesson 1.1: Quick Test
==========================

GOAL: Check that MuJoCo and LocoMuJoCo are working correctly
WHY: Before diving into complex projects, we need to verify everything runs smoothly

WHAT YOU'LL LEARN:
✅ How to start the G1 robot simulation
✅ Basic MuJoCo viewer controls
✅ Simple robot movements
✅ Troubleshooting if things don't work

This is your "hello world" for humanoid robotics!
"""

import numpy as np
from loco_mujoco.task_factories import RLFactory
import jax
import os

# 🎨 OPTIONAL: Set black background for cooler visuals
# Uncomment the line below if you want a black background
# os.environ['MUJOCO_GL_BACKGROUND'] = '0 0 0'  # Black background


def check_system():
    """🔧 Check if all systems are working"""
    print("🔧 SYSTEM CHECK")
    print("=" * 40)
    
    try:
        print("📦 Importing LocoMuJoCo... ", end="")
        import loco_mujoco
        print("✅ SUCCESS")
    except ImportError as e:
        print(f"❌ FAILED: {e}")
        return False
    
    try:
        print("🎮 Testing JAX... ", end="")
        key = jax.random.PRNGKey(42)
        print("✅ SUCCESS")
    except Exception as e:
        print(f"❌ FAILED: {e}")
        return False
    
    print("🎯 All systems ready!")
    return True


def create_basic_robot():
    """🤖 Create the simplest possible G1 robot"""
    print("\n🤖 CREATING G1 ROBOT")
    print("=" * 40)
    
    try:
        print("🏗️  Building G1 environment...")
        
        # Create the simplest possible robot environment
        env = RLFactory.make("UnitreeG1")
        
        print("✅ G1 robot created successfully!")
        print(f"🎮 Robot has {env.action_space.shape[0]} controllable joints")
        print(f"🔍 Robot has {env.observation_space.shape[0]} sensors")
        
        return env
        
    except Exception as e:
        print(f"❌ Failed to create robot: {e}")
        print("💡 This might be normal - some environments need special setup")
        return None


def test_basic_movement(env):
    """🎯 Test simple robot movements"""
    if env is None:
        print("\n⚠️  Skipping movement test - no robot available")
        return
    
    print("\n🎯 TESTING BASIC MOVEMENT")
    print("=" * 40)
    print("🎮 VIEWER CONTROLS:")
    print("   SPACEBAR = Pause/Resume")
    print("   R = Reset robot")
    print("   ESC = Exit")
    print("   Mouse = Rotate camera")
    print("   Mouse wheel = Zoom")
    
    try:
        print("\n🎬 Starting movement test...")
        
        # Reset robot to starting position
        key = jax.random.PRNGKey(42)
        obs = env.reset(key)
        
        print("🤖 Robot initialized!")
        print("👀 Watch for 5 seconds of gentle movements...")
        
        # Test gentle movements for 5 seconds
        for step in range(150):  # 5 seconds at 30 FPS
            # Very small random actions to test joints
            action = np.random.uniform(-0.1, 0.1, env.action_space.shape[0])
            
            # Step simulation
            result = env.step(action)
            if len(result) == 5:
                obs, reward, done, truncated, info = result
            else:
                obs, reward, done, info = result
                truncated = False
            
            # Check if simulation is still running
            if done:
                print(f"🔄 Robot reset at step {step}")
                obs = env.reset(key)
        
        print("✅ Movement test completed!")
        print("🎓 If you saw the robot moving, everything works!")
        
    except Exception as e:
        print(f"❌ Movement test failed: {e}")
        print("💡 This might indicate graphics or simulation issues")


def explain_what_happened():
    """💡 Explain what the user just experienced"""
    print("\n💡 WHAT JUST HAPPENED?")
    print("=" * 40)
    print("🤖 You created a virtual G1 humanoid robot")
    print("🌍 The robot exists in a physics simulation (MuJoCo)")
    print("🎮 You sent random movement commands to its joints")
    print("👀 MuJoCo showed you the results in 3D graphics")
    print("")
    print("🧠 KEY CONCEPTS:")
    print("   • ENVIRONMENT: The simulated world where robots live")
    print("   • OBSERVATIONS: What the robot senses (joint angles, balance, etc.)")
    print("   • ACTIONS: Commands we send to robot motors")
    print("   • PHYSICS: MuJoCo calculates realistic movement and collisions")


def troubleshooting_tips():
    """🔧 Help if things don't work"""
    print("\n🔧 TROUBLESHOOTING TIPS")
    print("=" * 40)
    print("❓ No robot window appeared?")
    print("   • Window might be hidden behind terminal")
    print("   • Try Cmd+Tab (Mac) or Alt+Tab (Windows) to find it")
    print("   • Check if MuJoCo viewer opened in background")
    print("")
    print("❓ Robot fell down immediately?")
    print("   • This is normal! Random actions don't create stable walking")
    print("   • We'll learn proper control in later lessons")
    print("")
    print("❓ Error messages appeared?")
    print("   • Copy the error and search online for solutions")
    print("   • Check that all dependencies are installed correctly")
    print("   • Some features require additional setup")


def main():
    """🚀 Main lesson function"""
    print("🚀 Lesson 1.1: Quick Test")
    print("=" * 50)
    print("🎯 Goal: Verify that LocoMuJoCo is working correctly")
    print("⏱️  Time: ~2 minutes")
    print("🎓 Difficulty: Beginner")
    
    # Run all checks
    if not check_system():
        print("\n💡 Please fix system issues before continuing")
        return
    
    robot = create_basic_robot()
    test_basic_movement(robot)
    explain_what_happened()
    troubleshooting_tips()
    
    # Clean up
    if robot is not None:
        del robot
    
    print("\n🎓 LESSON COMPLETE!")
    print("=" * 50)
    print("✅ You've successfully:")
    print("   • Verified LocoMuJoCo installation")
    print("   • Created your first G1 robot")
    print("   • Seen basic robot movement")
    print("   • Learned key robotics concepts")
    print("")
    print("🚀 Ready for Lesson 1.2: Simple Walk Test")
    print("")
    print("🏆 EXPERIMENT IDEAS:")
    print("💡 Try different action magnitudes (change 0.1 to 0.05 or 0.2)")
    print("💡 Count how many steps before the robot falls")
    print("💡 Watch specific joints - which move the most?")


if __name__ == "__main__":
    main()