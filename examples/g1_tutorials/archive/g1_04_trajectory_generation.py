#!/usr/bin/env python3
"""
G1 Dataset Tutorial 4: Numerical Data Analysis and Understanding
This tutorial helps understand what the G1 robot data looks like numerically
"""

import numpy as np
import matplotlib.pyplot as plt
from loco_mujoco.task_factories import ImitationFactory, DefaultDatasetConf
import time

def generate_g1_standing_trajectory(env, n_steps=200):
    """Generate a standing still trajectory for G1"""
    print("🧍 Generating G1 standing trajectory...")
    
    # Reset environment
    key = jax.random.PRNGKey(42)
    state = env.reset(key)
    
    trajectory_data = []
    
    for step in range(n_steps):
        # Use zero actions for standing still
        action = jnp.zeros(env.action_space.shape[0])
        
        # Small random perturbations to maintain balance
        if step > 10:  # Allow settling first
            noise = jax.random.normal(key, action.shape) * 0.02
            key, _ = jax.random.split(key)
            action = action + noise
        
        # Step environment
        state = env.step(state, action)
        
        # Store trajectory data
        trajectory_data.append({
            'step': step,
            'qpos': state.info.qpos,
            'qvel': state.info.qvel, 
            'action': action,
            'obs': state.info.obs
        })
        
        if step % 50 == 0:
            print(f"   Generated step {step}/{n_steps}")
    
    return trajectory_data

def generate_g1_walking_pattern(env, n_steps=300):
    """Generate a simple walking pattern for G1"""
    print("🚶 Generating G1 walking pattern...")
    
    key = jax.random.PRNGKey(123)
    state = env.reset(key)
    
    trajectory_data = []
    
    for step in range(n_steps):
        # Simple sinusoidal walking pattern
        t = step * 0.05  # Time parameter
        
        # Create walking-like action pattern
        action = jnp.zeros(env.action_space.shape[0])
        
        # Assume first 12 DOF are legs (simplified)
        if env.action_space.shape[0] >= 12:
            # Left leg pattern
            action = action.at[0].set(0.3 * jnp.sin(t))      # Hip pitch
            action = action.at[1].set(0.1 * jnp.cos(t))      # Hip roll  
            action = action.at[3].set(0.5 * jnp.abs(jnp.sin(t)))  # Knee
            
            # Right leg pattern (phase shifted)
            action = action.at[6].set(0.3 * jnp.sin(t + jnp.pi))    # Hip pitch
            action = action.at[7].set(-0.1 * jnp.cos(t + jnp.pi))   # Hip roll
            action = action.at[9].set(0.5 * jnp.abs(jnp.sin(t + jnp.pi)))  # Knee
        
        # Add some noise for realism
        noise = jax.random.normal(key, action.shape) * 0.05
        key, _ = jax.random.split(key)
        action = action + noise
        
        # Step environment
        state = env.step(state, action)
        
        # Store trajectory data
        trajectory_data.append({
            'step': step,
            'qpos': state.info.qpos,
            'qvel': state.info.qvel,
            'action': action,
            'obs': state.info.obs
        })
        
        if step % 75 == 0:
            print(f"   Generated step {step}/{n_steps}")
    
    return trajectory_data

def analyze_trajectory(trajectory_data):
    """Analyze trajectory statistics"""
    print("\n📊 Trajectory Analysis:")
    
    # Extract data for analysis
    actions = jnp.stack([data['action'] for data in trajectory_data])
    observations = jnp.stack([data['obs'] for data in trajectory_data])
    
    # Action statistics
    action_mean = jnp.mean(actions, axis=0)
    action_std = jnp.std(actions, axis=0)
    action_range = jnp.max(actions, axis=0) - jnp.min(actions, axis=0)
    
    print(f"   Action Statistics:")
    print(f"     Mean magnitude: {jnp.mean(jnp.abs(action_mean)):.4f}")
    print(f"     Average std: {jnp.mean(action_std):.4f}")
    print(f"     Average range: {jnp.mean(action_range):.4f}")
    
    # Observation statistics  
    obs_mean = jnp.mean(observations, axis=0)
    obs_std = jnp.std(observations, axis=0)
    
    print(f"   Observation Statistics:")
    print(f"     Mean magnitude: {jnp.mean(jnp.abs(obs_mean)):.4f}")
    print(f"     Average std: {jnp.mean(obs_std):.4f}")
    
    # Stability metrics
    action_smoothness = jnp.mean(jnp.diff(actions, axis=0)**2)
    obs_smoothness = jnp.mean(jnp.diff(observations, axis=0)**2)
    
    print(f"   Smoothness Metrics:")
    print(f"     Action smoothness: {action_smoothness:.6f}")  
    print(f"     Observation smoothness: {obs_smoothness:.6f}")

def main():
    print("🤖 UnitreeG1 Dataset Tutorial 4: Trajectory Generation")
    print("=" * 60)
    
    try:
        print("🔄 Creating UnitreeG1 environment for trajectory generation...")
        
        # Create basic environment (no pre-loaded datasets)
        env = ImitationFactory.make("UnitreeG1")
        
        print("✅ Environment created!")
        print(f"📊 Action space: {env.info.action_space.shape}")
        print(f"📊 Observation space: {env.info.observation_space.shape}")
        
        # Generate different trajectory types
        trajectories = {}
        
        # 1. Standing trajectory
        trajectories['standing'] = generate_g1_standing_trajectory(env, n_steps=150)
        
        # 2. Walking trajectory  
        trajectories['walking'] = generate_g1_walking_pattern(env, n_steps=200)
        
        # Analyze each trajectory
        for traj_name, traj_data in trajectories.items():
            print(f"\n🔍 Analyzing {traj_name} trajectory:")
            analyze_trajectory(traj_data)
        
        print("\n🎬 Replaying generated trajectories...")
        
        # Replay trajectories (simplified visualization)
        for traj_name, traj_data in trajectories.items():
            print(f"\n▶️  Playing {traj_name} trajectory...")
            
            # Reset environment
            key = jax.random.PRNGKey(0)
            state = env.reset(key)
            
            # Replay the trajectory
            for i, data in enumerate(traj_data[:100]):  # Show first 100 steps
                action = data['action']
                state = env.step(state, action)
                
                if i % 20 == 0:
                    print(f"     Step {i:3d}/100")
        
        print("\n✅ G1 trajectory generation and analysis completed!")
        print("   Generated custom standing and walking patterns")
        print("   Analyzed trajectory statistics and smoothness")
        
    except Exception as e:
        print(f"❌ Error in trajectory generation: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()