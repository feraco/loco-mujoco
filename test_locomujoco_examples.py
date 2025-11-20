#!/usr/bin/env python3
"""
Test LocoMuJoCo UnitreeG1 Basic Tutorial
Modified version of 01_creating_mujoco_env.py for UnitreeG1
"""

import numpy as np
import time

def test_basic_locomujoco():
    """Test basic LocoMuJoCo functionality with error handling"""
    print("🤖 Testing LocoMuJoCo UnitreeG1 Basic Environment...")
    
    try:
        # Try to import LocoMuJoCo
        from loco_mujoco import ImitationFactory
        print("✅ LocoMuJoCo imported successfully!")
        
        # List available environments/robots
        print("\n🤖 Trying to create UnitreeG1 environment...")
        
        # Try different ways to create G1 environment
        environments_to_try = [
            ("UnitreeG1", {}),
            ("UnitreeG1", {"task": "stand"}),
            ("UnitreeG1", {"task": "walk"}),
            ("UnitreeH1", {}),  # Fallback to H1 if G1 doesn't work
        ]
        
        env = None
        for env_name, config in environments_to_try:
            try:
                print(f"  Trying {env_name} with config: {config}")
                if config:
                    env = ImitationFactory.make(env_name, default_dataset_conf=config)
                else:
                    env = ImitationFactory.make(env_name)
                print(f"✅ Successfully created {env_name} environment!")
                break
            except Exception as e:
                print(f"  ❌ Failed to create {env_name}: {e}")
                continue
        
        if env is None:
            print("❌ Could not create any humanoid environment")
            return False
        
        # Get environment info
        action_dim = env.info.action_space.shape[0]
        obs_dim = env.info.observation_space.shape[0]
        
        print(f"\n📊 Environment Info:")
        print(f"  Action space: {action_dim}")
        print(f"  Observation space: {obs_dim}")
        
        # Reset environment
        initial_state = env.reset()
        print(f"  Initial state shape: {initial_state.shape}")
        
        # Start rendering
        env.render()
        print("\n🚀 Starting simulation loop...")
        
        # Run simulation
        absorbing = False
        step_count = 0
        max_steps = 500  # Shorter test
        
        print("🎮 Running with intelligent control (small actions)...")
        
        while step_count < max_steps:
            # Reset if episode ends
            if absorbing:
                print(f"  Episode ended at step {step_count}, resetting...")
                env.reset()
                absorbing = False
                time.sleep(1)
            
            # Use small, controlled actions instead of pure random
            action = np.random.randn(action_dim) * 0.2  # Small actions
            
            # Take step
            next_state, reward, absorbing, done, info = env.step(action)
            
            # Render
            env.render()
            
            # Progress update
            if step_count % 100 == 0:
                print(f"  Step {step_count}: reward={reward:.3f}")
            
            step_count += 1
            time.sleep(0.01)  # Small delay for observation
        
        print(f"✅ Completed {step_count} steps successfully!")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Suggestion: Install missing dependencies or use alternative approach")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_alternative_simple_environment():
    """Test a simpler environment approach if LocoMuJoCo fails"""
    print("\n🔄 Trying alternative simple environment approach...")
    
    try:
        # Try the simpler approach without complex dependencies
        print("Using basic MuJoCo with LocoMuJoCo models...")
        
        # This would use just the model files without the full framework
        import mujoco
        import mujoco.viewer
        
        # Try to load a LocoMuJoCo model directly
        model_paths = [
            "loco_mujoco/models/unitree_g1/g1.xml",
            "../loco_mujoco/models/unitree_g1/g1.xml",
        ]
        
        for model_path in model_paths:
            try:
                print(f"  Trying model path: {model_path}")
                model = mujoco.MjModel.from_xml_path(model_path)
                data = mujoco.MjData(model)
                print(f"✅ Loaded model from {model_path}")
                
                # Basic simulation
                viewer = mujoco.viewer.launch_passive(model, data)
                print("🎮 Basic simulation running...")
                
                for i in range(1000):
                    # Apply simple control
                    data.ctrl[:] = np.random.randn(model.nu) * 0.1
                    mujoco.mj_step(model, data)
                    viewer.sync()
                    time.sleep(0.01)
                    
                    if not viewer.is_running():
                        break
                
                viewer.close()
                return True
                
            except Exception as e:
                print(f"  ❌ Failed to load {model_path}: {e}")
                continue
        
        print("❌ Could not load any LocoMuJoCo models directly")
        return False
        
    except Exception as e:
        print(f"❌ Alternative approach failed: {e}")
        return False

if __name__ == "__main__":
    print("🚀 LocoMuJoCo Examples Test")
    print("=" * 50)
    
    # Try the main approach first
    success = test_basic_locomujoco()
    
    # If that fails, try alternative
    if not success:
        success = test_alternative_simple_environment()
    
    if success:
        print("\n✅ LocoMuJoCo test completed successfully!")
    else:
        print("\n❌ LocoMuJoCo test failed - may need dependency fixes")
        
    print("\n🏁 Test finished")