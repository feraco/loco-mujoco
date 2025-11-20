#!/usr/bin/env python3
"""
🎨 Quick Background Color Demo
=============================

Run this to test different background colors with your G1 robot.
Press Enter to cycle through different backgrounds!
"""

import numpy as np
from loco_mujoco.task_factories import RLFactory
import jax
import os
import time


def set_background(color_name, rgb_values):
    """Set MuJoCo background color"""
    os.environ['MUJOCO_GL_BACKGROUND'] = rgb_values
    print(f"🎨 Background: {color_name} ({rgb_values})")


def main():
    """Demo different background colors"""
    print("🎨 MuJoCo Background Color Demo")
    print("=" * 35)
    
    # Background options
    backgrounds = [
        ("Black (Sleek)", "0 0 0"),
        ("Dark Blue (Professional)", "0.05 0.05 0.15"),
        ("Dark Gray (Neutral)", "0.1 0.1 0.1"),
        ("Very Dark Red (Dramatic)", "0.1 0.02 0.02"),
        ("Deep Purple (Cool)", "0.08 0.04 0.12"),
        ("White (Clean)", "1 1 1"),
        ("Default (Original)", "0.2 0.3 0.4"),
    ]
    
    # Create robot
    print("🤖 Creating G1 robot...")
    env = RLFactory.make("UnitreeG1")
    key = jax.random.PRNGKey(42)
    
    for i, (name, rgb) in enumerate(backgrounds):
        print(f"\n--- Background {i+1}/{len(backgrounds)} ---")
        set_background(name, rgb)
        
        # Reset with new background
        obs = env.reset(key)
        
        print(f"👀 Now showing: {name}")
        print("🎬 Watch the robot for 3 seconds...")
        
        # Simple movement to show the background
        for step in range(60):  # 2 seconds at 30fps
            # Very gentle swaying motion
            t = step * 0.1
            action = np.sin(t) * 0.03 * np.ones(env.action_space.shape[0])
            obs, reward, done, info = env.step(action)
            
            if done:
                obs = env.reset(key)
        
        if i < len(backgrounds) - 1:  # Don't wait after last one
            input("👍 Press Enter for next background...")
    
    print("\n🎓 Demo Complete!")
    print("=" * 35)
    print("💡 To use your favorite background:")
    print("   1. Add this to your terminal/script:")
    print(f"      export MUJOCO_GL_BACKGROUND='0 0 0'  # (or your preferred RGB)")
    print("   2. Or add this to your Python code:")
    print("      os.environ['MUJOCO_GL_BACKGROUND'] = '0 0 0'")
    print("")
    print("🎨 Remember: RGB values are 0-1 (not 0-255)")


if __name__ == "__main__":
    main()