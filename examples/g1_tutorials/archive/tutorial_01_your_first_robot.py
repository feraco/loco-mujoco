#!/usr/bin/env python3
"""
🤖 Tutorial 1: Your First LocoMuJoCo Robot 

WHAT YOU'LL LEARN:
✅ How to create a humanoid robot environment
✅ Load and play motion capture datasets  
✅ Understand different motion types (walk, squat, jump)
✅ Basic robot control and observation concepts

WHAT TO EXPECT:
🎬 Beautiful 3D robot simulation with realistic physics
🏃 Multiple types of human motion (walking, squatting, jumping)
⏰ About 2-3 minutes of guided demonstrations
🎮 Interactive viewer with controls (SPACE=pause, R=restart)

EDUCATIONAL PURPOSE:
This tutorial introduces you to imitation learning - teaching robots to copy human movements.
You'll see how motion capture data from humans gets translated into robot actions.
"""

import jax
import numpy as np
from loco_mujoco.task_factories import ImitationFactory, DefaultDatasetConf
import time

def explain_concept(title, explanation):
    """Helper function to clearly explain concepts"""
    print(f"\n💡 CONCEPT: {title}")
    print("─" * 60)
    print(f"   {explanation}")
    print("─" * 60)

def main():
    print("🚀 LocoMuJoCo Tutorial 1: Your First Humanoid Robot")
    print("=" * 60)
    
    explain_concept(
        "What is LocoMuJoCo?", 
        "LocoMuJoCo is a toolkit for teaching robots to move like humans using\n"
        "   motion capture data. Think of it as a dance teacher for robots!"
    )
    
    explain_concept(
        "Imitation Learning",
        "Instead of programming every movement, we show robots videos of humans\n"
        "   moving and they learn to copy those movements. It's like learning\n"
        "   to dance by watching someone else!"
    )
    
    # Step 1: Create the robot environment
    print("\n🔨 STEP 1: Creating Your Robot")
    print("Creating a UnitreeG1 humanoid robot...")
    
    try:
        # Create robot with multiple motion types for variety
        env = ImitationFactory.make(
            "UnitreeG1",                           # Robot model (23 joints, human-like)
            default_dataset_conf=DefaultDatasetConf([
                "walk",                            # Natural human walking
                "squat",                           # Squatting exercise motion
                "jump"                             # Jumping motion
            ]),
            n_substeps=20                          # Smooth physics simulation
        )
        
        print("✅ Robot created successfully!")
        print(f"🤖 Robot has {env.info.action_space.shape[0]} controllable joints")
        print(f"👀 Robot observes {env.info.observation_space.shape[0]} sensor readings")
        
    except Exception as e:
        print(f"❌ Error creating robot: {e}")
        print("💡 Trying with just walking motion...")
        
        # Fallback to just walking if multiple datasets fail
        env = ImitationFactory.make(
            "UnitreeG1",
            default_dataset_conf=DefaultDatasetConf(["walk"]),
            n_substeps=20
        )
        print("✅ Robot created with walking motion only!")
    
    explain_concept(
        "Robot Joints & Sensors",
        f"Your robot has {env.info.action_space.shape[0]} motors (like muscles) that control movement.\n"
        f"   It has {env.info.observation_space.shape[0]} sensors (like eyes/ears) that tell it about its body\n"
        f"   position, balance, and the world around it."
    )
    
    # Step 2: Load motion data
    print("\n📚 STEP 2: Loading Human Motion Data")
    print("Loading motion capture datasets...")
    
    dataset = env.create_dataset()
    print("✅ Motion data loaded successfully!")
    
    explain_concept(
        "Motion Capture Data",
        "This data comes from real humans wearing special suits with sensors.\n"
        "   When they walk, squat, or jump, we record every joint angle and\n"
        "   position. Your robot will try to copy these exact movements!"
    )
    
    # Step 3: Motion demonstrations
    print("\n🎬 STEP 3: Robot Motion Demonstrations")
    print("Your robot will now perform different types of human movements...")
    print("🎮 VIEWER CONTROLS:")
    print("   SPACEBAR = Pause/Resume")
    print("   R = Restart current motion") 
    print("   ESC = Exit viewer")
    print("   Mouse = Rotate camera view")
    
    # Motion showcase with explanations
    motions = [
        {
            "name": "Walking",
            "dataset": "walk",
            "description": "Natural human walking gait with proper balance",
            "why_important": "Walking is fundamental for mobile robots",
            "episodes": 2,
            "steps": 800
        },
        {
            "name": "Squatting", 
            "dataset": "squat",
            "description": "Up and down squatting exercise motion",
            "why_important": "Shows strength and balance control",
            "episodes": 2, 
            "steps": 600
        },
        {
            "name": "Jumping",
            "dataset": "jump", 
            "description": "Explosive jumping motion with landing",
            "why_important": "Demonstrates dynamic movement and impact handling",
            "episodes": 2,
            "steps": 400
        }
    ]
    
    for i, motion in enumerate(motions):
        print(f"\n🎯 DEMONSTRATION {i+1}/3: {motion['name'].upper()}")
        print("=" * 50)
        print(f"📝 What you'll see: {motion['description']}")
        print(f"🎓 Why it matters: {motion['why_important']}")
        print(f"⏱️  Duration: ~{motion['steps']//30} seconds")
        
        try:
            # Create focused environment for this motion
            motion_env = ImitationFactory.make(
                "UnitreeG1",
                default_dataset_conf=DefaultDatasetConf([motion['dataset']]),
                n_substeps=20
            )
            
            print(f"🤖 Robot is now learning: {motion['name']}")
            print("👀 Watch how the robot copies human movement patterns!")
            
            # Play the motion
            motion_env.play_trajectory(
                n_episodes=motion['episodes'],
                n_steps_per_episode=motion['steps'],
                render=True
            )
            
            print(f"✅ {motion['name']} demonstration complete!")
            
            if i < len(motions) - 1:
                print("⏯️  Preparing next demonstration...")
                time.sleep(2)
                
        except Exception as e:
            print(f"⚠️  Skipping {motion['name']} due to error: {e}")
            continue
    
    # Educational summary
    print("\n🎓 TUTORIAL COMPLETE - What You Just Learned:")
    print("=" * 60)
    print("✅ How to create a humanoid robot simulation")
    print("✅ How motion capture data teaches robots to move")
    print("✅ Different types of locomotion (walking, squatting, jumping)")
    print("✅ The basics of imitation learning")
    
    explain_concept(
        "What's Next?",
        "Now you understand the basics! You can:\n"
        "   • Try different robots (UnitreeH1, Atlas, etc.)\n" 
        "   • Experiment with different datasets (LAFAN1, AMASS)\n"
        "   • Learn about training your own movement controllers\n"
        "   • Explore advanced topics like reward functions and policy learning"
    )
    
    print("\n🏆 EXPERIMENT TIME!")
    print("Try modifying this tutorial:")
    print("💡 Change 'UnitreeG1' to 'UnitreeH1' for a different robot")
    print("💡 Add 'run' to the dataset list for running motion") 
    print("💡 Increase n_substeps for smoother (slower) motion")
    print("💡 Change n_episodes for longer/shorter demonstrations")

if __name__ == "__main__":
    main()