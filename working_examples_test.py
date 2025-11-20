#!/usr/bin/env python3
"""
Working LocoMuJoCo Examples - Focus on what actually works
Based on successful examples we've identified
"""

import numpy as np
import time

def test_dataset_replay():
    """Test the dataset replay functionality that we know works"""
    print("🎭 Testing Dataset Replay (Motion Capture)")
    print("-" * 40)
    
    try:
        from loco_mujoco.task_factories import ImitationFactory, DefaultDatasetConf
        
        print("✅ Creating UnitreeH1 with motion datasets...")
        
        # This approach worked in our previous test
        env = ImitationFactory.make("UnitreeH1",
                                   default_dataset_conf=DefaultDatasetConf(["walk"]),
                                   n_substeps=20)
        
        print("✅ Environment created successfully!")
        print(f"📊 Action space: {env.info.action_space.shape}")
        print(f"📊 Observation space: {env.info.observation_space.shape}")
        
        print("\n🎥 Playing motion capture trajectories...")
        
        # Play just 1 episode with shorter duration for testing
        env.play_trajectory(n_episodes=1, n_steps_per_episode=200, render=True)
        
        print("✅ Motion capture replay completed!")
        return True
        
    except Exception as e:
        print(f"❌ Dataset replay failed: {e}")
        return False

def test_trajectory_generation():
    """Test trajectory generation that we know works"""
    print("\n🚶 Testing Trajectory Generation")
    print("-" * 40)
    
    try:
        # This uses the approach from the standing_humanoid.py example
        from loco_mujoco import LocoEnv
        
        print("✅ Creating UnitreeH1 environment for trajectory generation...")
        
        # Use the approach that worked in standing_humanoid.py
        env = LocoEnv.make("UnitreeH1", init_state_type="DefaultInitialStateHandler")
        
        print("✅ Environment created!")
        
        # Simple trajectory test
        print("🎯 Generating simple standing trajectory...")
        
        # Reset environment
        import jax
        key = jax.random.PRNGKey(0)
        state = env.reset(key)
        
        print(f"📊 Initial state shape: {state.info.obs.shape}")
        
        # Simple trajectory - just hold position for a few steps
        n_steps = 100
        trajectory_data = []
        
        for step in range(n_steps):
            # Use zero actions (just stand still)
            action = jax.numpy.zeros(env.action_space.shape[0])
            
            # Step environment
            state = env.step(state, action)
            
            # Store trajectory data
            trajectory_data.append({
                'step': step,
                'obs': state.info.obs,
                'action': action
            })
            
            if step % 20 == 0:
                print(f"   Generated step {step}/{n_steps}")
        
        print(f"✅ Generated {len(trajectory_data)} trajectory steps!")
        return True
        
    except Exception as e:
        print(f"❌ Trajectory generation failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_basic_environment():
    """Test basic environment functionality"""
    print("\n🤖 Testing Basic Environment")
    print("-" * 40)
    
    try:
        from loco_mujoco import LocoEnv
        import jax
        import jax.numpy as jnp
        
        print("✅ Creating basic UnitreeH1 environment...")
        
        env = LocoEnv.make("UnitreeH1")
        
        print("✅ Environment created!")
        print(f"📊 Action space shape: {env.action_space.shape}")
        print(f"📊 Observation space shape: {env.observation_space.shape}")
        
        # Test reset
        key = jax.random.PRNGKey(42)
        state = env.reset(key)
        
        print(f"📊 Reset successful, observation shape: {state.info.obs.shape}")
        
        # Test a few steps with small actions
        print("🎮 Testing environment steps...")
        
        for step in range(10):
            # Small random actions for stability
            action = jax.random.normal(key, (env.action_space.shape[0],)) * 0.1
            key, _ = jax.random.split(key)
            
            state = env.step(state, action)
            
            if step % 3 == 0:
                print(f"   Step {step}: obs_shape={state.info.obs.shape}")
        
        print("✅ Basic environment test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Basic environment test failed: {e}")
        return False

def main():
    print("🚀 LocoMuJoCo Working Examples Test")
    print("=" * 50)
    
    success_count = 0
    total_tests = 3
    
    # Test 1: Dataset Replay (we know this works)
    if test_dataset_replay():
        success_count += 1
    
    # Test 2: Trajectory Generation (we saw this working)
    if test_trajectory_generation():
        success_count += 1
    
    # Test 3: Basic Environment
    if test_basic_environment():
        success_count += 1
    
    print(f"\n📊 Test Results: {success_count}/{total_tests} tests passed")
    
    if success_count > 0:
        print("✅ LocoMuJoCo is working! Some functionality is available.")
        
        if success_count == total_tests:
            print("🎉 All tests passed! LocoMuJoCo is fully functional.")
        else:
            print("⚠️  Some features may need additional setup or dependencies.")
            
    else:
        print("❌ LocoMuJoCo tests failed. May need dependency fixes.")
    
    print("\n🏁 Testing complete!")

if __name__ == "__main__":
    main()