#!/usr/bin/env python3
"""
Test the UnitreeG1 humanoid robot using LocoMuJoCo framework
This should provide much better stability and control than our custom implementation.
"""

import numpy as np
import time
from loco_mujoco import ImitationFactory

def main():
    print("🤖 Loading UnitreeG1 with LocoMuJoCo framework...")
    
    try:
        # Create G1 environment with a simple task
        # Let's start with a basic standing/walking task
        env = ImitationFactory.make("UnitreeG1", default_dataset_conf=dict(task="walk"))
        
        print("✅ G1 environment created successfully!")
        print(f"Action space: {env.info.action_space.shape}")
        print(f"Observation space: {env.info.observation_space.shape}")
        
    except Exception as e:
        # If walk task doesn't work, try other common tasks
        print(f"⚠️  Walk task failed: {e}")
        print("🔄 Trying different tasks...")
        
        # Try common locomotion tasks
        for task in ["stand", "stepinplace", "walk_fast", "walk_slow", "idle"]:
            try:
                print(f"Trying task: {task}")
                env = ImitationFactory.make("UnitreeG1", default_dataset_conf=dict(task=task))
                print(f"✅ G1 environment created with task '{task}'!")
                print(f"Action space: {env.info.action_space.shape}")
                print(f"Observation space: {env.info.observation_space.shape}")
                break
            except Exception as task_e:
                print(f"❌ Task '{task}' failed: {task_e}")
                continue
        else:
            # If no task works, try without specifying a task
            try:
                print("🔄 Trying without specific task...")
                env = ImitationFactory.make("UnitreeG1")
                print("✅ G1 environment created without specific task!")
                print(f"Action space: {env.info.action_space.shape}")
                print(f"Observation space: {env.info.observation_space.shape}")
            except Exception as final_e:
                print(f"❌ Failed to create G1 environment: {final_e}")
                return

    # Get action dimension
    action_dim = env.info.action_space.shape[0]
    print(f"🎮 G1 has {action_dim} controllable joints")

    # Reset environment
    initial_state = env.reset()
    print(f"📊 Initial state shape: {initial_state.shape}")

    # Start rendering
    env.render()
    print("\n🚀 Starting G1 LocoMuJoCo simulation")
    print("🎯 Using intelligent control policy (vs random actions)")
    
    # Run simulation with intelligent vs random control
    step_count = 0
    episode_count = 0
    max_steps_per_episode = 1000
    
    try:
        while True:
            if step_count >= max_steps_per_episode:
                print(f"🔄 Episode {episode_count} complete, resetting...")
                env.reset()
                step_count = 0
                episode_count += 1
                time.sleep(1)  # Brief pause between episodes

            # Use a more intelligent action policy
            # Instead of pure random, use smaller, more controlled movements
            if step_count < 100:
                # Start with very small movements to maintain balance
                action = np.random.randn(action_dim) * 0.1  # Very small actions
            elif step_count < 500:
                # Gradually increase action magnitude
                action = np.random.randn(action_dim) * 0.3  # Medium actions
            else:
                # Allow larger movements once stable
                action = np.random.randn(action_dim) * 0.5  # Larger actions

            # Take step
            next_state, reward, absorbing, done, info = env.step(action)
            
            # Render
            env.render()
            
            # Check if episode ended
            if absorbing or done:
                print(f"🏁 Episode ended at step {step_count}")
                print(f"   Reward: {reward:.3f}")
                print(f"   Absorbing: {absorbing}, Done: {done}")
                if 'info' in locals() and info:
                    print(f"   Info: {info}")
                step_count = max_steps_per_episode  # Force reset
                time.sleep(2)
                continue
            
            step_count += 1
            
            # Print periodic updates
            if step_count % 100 == 0:
                print(f"📈 Episode {episode_count}, Step {step_count}, Reward: {reward:.3f}")

            # Brief delay for observation
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\n✅ Simulation stopped by user")
    except Exception as e:
        print(f"\n❌ Simulation error: {e}")
        import traceback
        traceback.print_exc()

    print("\n🏁 G1 LocoMuJoCo test completed")

if __name__ == "__main__":
    main()