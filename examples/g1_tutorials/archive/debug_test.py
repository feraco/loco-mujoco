#!/usr/bin/env python3
"""
Debug Test: Check what's wrong with tutorial 2 and 3
"""

import jax
import numpy as np
from loco_mujoco.task_factories import RLFactory
import time

def test_basic_rl_environment():
    print("🔍 Testing basic RL environment...")
    
    # Create environment
    env = RLFactory.make(
        "UnitreeG1",
        horizon=100,
        headless=False  # Should show viewer
    )
    
    print("✅ Environment created")
    print(f"Action space: {env.info.action_space.shape}")
    print(f"Observation space: {env.info.observation_space.shape}")
    
    # Reset environment
    key = jax.random.PRNGKey(42)
    obs = env.reset(key)
    print(f"✅ Environment reset, obs shape: {obs.shape}")
    
    # Try stepping
    print("🎮 Testing environment step...")
    action = np.zeros(env.info.action_space.shape[0])
    
    try:
        step_result = env.step(action)
        print(f"✅ Step successful, got {len(step_result)} return values")
        
        if len(step_result) == 4:
            obs, reward, done, info = step_result
            print(f"   New obs shape: {obs.shape}")
            print(f"   Reward: {reward}")
            print(f"   Done: {done}")
        elif len(step_result) == 3:
            obs, reward, done = step_result
            print(f"   New obs shape: {obs.shape}")
            print(f"   Reward: {reward}") 
            print(f"   Done: {done}")
        else:
            print(f"   Unexpected return format: {step_result}")
            
    except Exception as e:
        print(f"❌ Step failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Try rendering
    print("🎨 Testing rendering...")
    try:
        env.render()
        print("✅ Render successful")
    except Exception as e:
        print(f"❌ Render failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Run a few steps to see if viewer appears
    print("🏃 Running a few steps with rendering...")
    for i in range(20):
        action = np.random.randn(env.info.action_space.shape[0]) * 0.1
        try:
            step_result = env.step(action)
            env.render()
            time.sleep(0.1)  # Brief pause to see if viewer appears
            print(f"   Step {i+1}/20 completed")
        except Exception as e:
            print(f"❌ Step {i+1} failed: {e}")
            break
    
    print("🏁 Test completed!")

if __name__ == "__main__":
    test_basic_rl_environment()