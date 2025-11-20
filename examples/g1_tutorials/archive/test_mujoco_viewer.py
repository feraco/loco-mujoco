#!/usr/bin/env python3
"""
G1 MuJoCo Viewer Test - Check if viewer stays open
"""

import mujoco
import mujoco.viewer
import numpy as np
import time

def test_mujoco_viewer():
    """Test basic MuJoCo viewer functionality"""
    
    print("🔍 Testing MuJoCo Viewer Settings...")
    
    # Try to create a simple model
    model_xml = """
    <mujoco>
        <worldbody>
            <light diffuse=".5 .5 .5" pos="0 0 3" dir="0 0 -1"/>
            <geom type="plane" size="1 1 0.1" rgba=".9 0 0 1"/>
            <body pos="0 0 1">
                <joint type="free"/>
                <geom type="box" size=".1 .1 .1" rgba="0 .9 0 1"/>
            </body>
        </worldbody>
    </mujoco>
    """
    
    try:
        model = mujoco.MjModel.from_xml_string(model_xml)
        data = mujoco.MjData(model)
        
        print("✅ MuJoCo model created successfully")
        print("🎮 Opening MuJoCo viewer...")
        print("   This viewer should stay open and be interactive")
        print("   Press ESC or close window when done")
        
        # Launch viewer with explicit settings
        with mujoco.viewer.launch_passive(model, data) as viewer:
            print("✅ Viewer launched successfully!")
            print("⏱️  Running for 30 seconds...")
            
            # Run simulation for 30 seconds
            start_time = time.time()
            while time.time() - start_time < 30:
                # Step simulation
                mujoco.mj_step(model, data)
                
                # Update viewer
                viewer.sync()
                
                # Small delay
                time.sleep(0.01)
                
                # Check if viewer is still open
                if not viewer.is_running():
                    print("ℹ️  Viewer was closed by user")
                    break
            
            print("✅ Viewer test completed!")
            
    except Exception as e:
        print(f"❌ MuJoCo viewer test failed: {e}")
        return False
    
    return True

def main():
    print("🤖 G1 MuJoCo Viewer Test")
    print("=" * 40)
    
    # Test basic viewer
    if test_mujoco_viewer():
        print("\n✅ MuJoCo viewer is working properly!")
        print("💡 The G1 tutorials should now stay open longer")
    else:
        print("\n❌ MuJoCo viewer issues detected")
        print("💡 This might be why G1 tutorials close quickly")

if __name__ == "__main__":
    main()