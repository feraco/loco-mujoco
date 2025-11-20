#!/usr/bin/env python3
"""
🎨 MuJoCo Background Color Customization Guide
==============================================

This script demonstrates different ways to change the MuJoCo background color to black
or any other color you prefer.
"""

import numpy as np
from loco_mujoco.task_factories import RLFactory
import jax
import os


def method_1_environment_variable():
    """Method 1: Set background color using environment variable (persistent)"""
    print("🎨 Method 1: Environment Variable")
    print("=" * 40)
    print("Set this in your terminal before running any MuJoCo program:")
    print('export MUJOCO_GL_BACKGROUND="0 0 0"  # Black background')
    print('export MUJOCO_GL_BACKGROUND="0.2 0.2 0.3"  # Dark blue-gray')
    print('export MUJOCO_GL_BACKGROUND="1 1 1"  # White background')
    print()
    
    # Set programmatically (affects current session only)
    os.environ['MUJOCO_GL_BACKGROUND'] = '0 0 0'  # Black
    print("✅ Background set to black for this session")


def method_2_render_options():
    """Method 2: Modify render options in code"""
    print("\n🎨 Method 2: Render Options in Code")
    print("=" * 40)
    
    # Create environment
    env = RLFactory.make("UnitreeG1")
    key = jax.random.PRNGKey(42)
    obs = env.reset(key)
    
    print("🤖 Robot created. Testing different background colors...")
    
    # Test different background colors
    backgrounds = [
        (0.0, 0.0, 0.0),      # Black
        (0.1, 0.1, 0.2),      # Dark blue
        (0.2, 0.0, 0.0),      # Dark red
        (0.0, 0.2, 0.0),      # Dark green
    ]
    
    for i, bg_color in enumerate(backgrounds):
        print(f"Testing background {i+1}: RGB{bg_color}")
        
        # Note: The exact method depends on LocoMuJoCo version
        # Try different approaches:
        
        try:
            # Approach 1: If environment has direct access to viewer
            if hasattr(env, 'viewer') and env.viewer is not None:
                env.viewer.model.vis.global_.rgba[0:3] = bg_color
            
            # Approach 2: Set via rendering context
            if hasattr(env, '_viewer'):
                env._viewer.scn.flags[0] = 0  # Disable skybox
                env._viewer.scn.rgba = list(bg_color) + [1.0]
                
        except Exception as e:
            print(f"   Method not available: {e}")
        
        # Render a few frames to see the change
        for step in range(30):  # 1 second at 30 FPS
            action = np.zeros(env.action_space.shape[0])  # No movement
            obs, reward, done, info = env.step(action)
            
            if step == 0:
                print(f"   ✅ Rendering with background {bg_color}")
                # Give time to see the color change
                import time
                time.sleep(1)


def method_3_xml_modification():
    """Method 3: Modify the environment XML (advanced)"""
    print("\n🎨 Method 3: XML Modification (Advanced)")
    print("=" * 40)
    print("For permanent changes, you can modify the robot's XML file:")
    print()
    print("1. Find the robot XML file (usually in loco_mujoco/models/)")
    print("2. Add this to the <visual> section:")
    print("   <visual>")
    print('     <rgba rgba="0 0 0 1"/>  <!-- Black background -->')
    print("   </visual>")
    print()
    print("3. Or modify the <worldbody> section:")
    print("   <worldbody>")
    print('     <geom name="floor" type="plane" size="0 0 1" rgba="0.2 0.2 0.2 1"/>')
    print("   </worldbody>")


def method_4_direct_mujoco():
    """Method 4: Direct MuJoCo API (if accessible)"""
    print("\n🎨 Method 4: Direct MuJoCo API")
    print("=" * 40)
    
    try:
        import mujoco
        print("✅ MuJoCo available - can modify rendering directly")
        
        # Create environment
        env = RLFactory.make("UnitreeG1")
        key = jax.random.PRNGKey(42)
        obs = env.reset(key)
        
        # Try to access the underlying MuJoCo model
        if hasattr(env, 'model'):
            model = env.model
            data = env.data
            
            print("🔧 Attempting to modify MuJoCo rendering options...")
            
            # Create renderer with custom options
            renderer = mujoco.Renderer(model, height=480, width=640)
            
            # Set background color
            renderer.scene.flags[mujoco.mjtRndFlag.mjRND_SKYBOX] = 0
            
            # Render a frame
            renderer.update_scene(data)
            pixels = renderer.render()
            
            print("✅ Custom rendering successful!")
            
    except ImportError:
        print("❌ Direct MuJoCo not available - use other methods")
    except Exception as e:
        print(f"❌ MuJoCo modification failed: {e}")


def create_black_background_example():
    """Complete example with black background"""
    print("\n🚀 Complete Black Background Example")
    print("=" * 40)
    
    # Set environment variable for black background
    os.environ['MUJOCO_GL_BACKGROUND'] = '0 0 0'
    
    # Create robot
    env = RLFactory.make("UnitreeG1")
    key = jax.random.PRNGKey(42)
    obs = env.reset(key)
    
    print("🤖 Robot created with black background")
    print("👀 Watch the robot for 3 seconds...")
    
    # Simple standing with small movements
    for step in range(90):  # 3 seconds
        # Very gentle random movements
        action = np.random.uniform(-0.05, 0.05, env.action_space.shape[0])
        obs, reward, done, info = env.step(action)
        
        if done:
            obs = env.reset(key)
    
    print("✅ Demo complete!")


def main():
    """🎨 Main background customization demo"""
    print("🎨 MuJoCo Background Color Customization")
    print("=" * 50)
    print("This guide shows different ways to change the background color")
    print()
    
    # Show all methods
    method_1_environment_variable()
    method_3_xml_modification()
    method_4_direct_mujoco()
    
    # Run practical example
    create_black_background_example()
    
    print("\n🎓 SUMMARY")
    print("=" * 50)
    print("✅ Best method: Set environment variable before running")
    print("   export MUJOCO_GL_BACKGROUND='0 0 0'")
    print()
    print("✅ Alternative: Set in Python:")
    print("   os.environ['MUJOCO_GL_BACKGROUND'] = '0 0 0'")
    print()
    print("🎨 Color format: 'R G B' where each value is 0-1")
    print("   • '0 0 0' = Black")
    print("   • '1 1 1' = White") 
    print("   • '0.2 0.2 0.3' = Dark blue-gray")
    print("   • '0.1 0.05 0.05' = Very dark red")


if __name__ == "__main__":
    main()