#!/usr/bin/env python3
"""
Simple LocoMuJoCo Tutorial - Modified for stability
Based on 01_creating_mujoco_env.py but with error handling and UnitreeG1
"""

import numpy as np
import time

def main():
    print("🤖 LocoMuJoCo Simple Tutorial - UnitreeG1")
    print("=" * 50)
    
    try:
        # Try the new factory method (avoiding deprecated LocoEnv.make)
        from loco_mujoco import ImitationFactory
        print("✅ Successfully imported ImitationFactory")
        
        # Try to create UnitreeG1 environment
        print("🔄 Creating UnitreeG1 environment...")
        
        # Try different approaches
        approaches = [
            lambda: ImitationFactory.make("UnitreeG1"),
            lambda: ImitationFactory.make("UnitreeH1"),  # Fallback to H1
            lambda: ImitationFactory.make("Atlas"),       # Fallback to Atlas
        ]
        
        env = None
        for i, approach in enumerate(approaches):
            try:
                env = approach()
                robot_name = ["UnitreeG1", "UnitreeH1", "Atlas"][i]
                print(f"✅ Successfully created {robot_name} environment!")
                break
            except Exception as e:
                print(f"❌ Approach {i+1} failed: {e}")
                continue
        
        if env is None:
            print("❌ Could not create any humanoid environment")
            return
        
        # Get action dimension
        action_dim = env.info.action_space.shape[0]
        obs_dim = env.info.observation_space.shape[0]
        
        print(f"\n📊 Environment Info:")
        print(f"   Action dimension: {action_dim}")
        print(f"   Observation dimension: {obs_dim}")
        
        # Reset environment
        print("\n🔄 Resetting environment...")
        initial_obs = env.reset()
        print(f"   Initial observation shape: {initial_obs.shape}")
        
        # Start rendering
        print("\n🎥 Starting visualization...")
        env.render()
        
        # Run simulation loop
        print("\n🚀 Running simulation (500 steps)...")
        
        absorbing = False
        step_count = 0
        max_steps = 500
        
        start_time = time.time()
        
        while step_count < max_steps:
            # Reset if episode ended
            if step_count == 0 or absorbing:
                if absorbing:
                    print(f"   Episode ended at step {step_count}, resetting...")
                env.reset()
                absorbing = False
                time.sleep(0.5)
            
            # Generate controlled action (not purely random)
            # Use smaller action magnitudes for stability
            action_magnitude = 0.1 + 0.2 * (step_count / max_steps)  # Gradually increase
            action = np.random.randn(action_dim) * action_magnitude
            
            # Take step
            next_state, reward, absorbing, done, info = env.step(action)
            
            # Render
            env.render()
            
            # Print progress
            if step_count % 50 == 0:
                elapsed = time.time() - start_time
                fps = step_count / elapsed if elapsed > 0 else 0
                print(f"   Step {step_count:3d}: reward={reward:6.3f}, fps={fps:5.1f}")
            
            step_count += 1
            
            # Brief delay for stable visualization
            time.sleep(0.02)
        
        total_time = time.time() - start_time
        avg_fps = max_steps / total_time
        
        print(f"\n✅ Simulation completed!")
        print(f"   Total steps: {max_steps}")
        print(f"   Total time: {total_time:.2f}s")
        print(f"   Average FPS: {avg_fps:.1f}")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Make sure LocoMuJoCo is properly installed")
        print("💡 Try: pip install -e . in the loco-mujoco directory")
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        
    print("\n🏁 Tutorial finished!")

if __name__ == "__main__":
    main()