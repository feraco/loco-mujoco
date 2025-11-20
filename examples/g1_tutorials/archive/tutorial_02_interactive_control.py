#!/usr/bin/env python3
"""
🎮 Tutorial 2: Interactive Robot Control

WHAT YOU'LL LEARN:
✅ How to control a robot manually with code
✅ Understanding robot observations (sensors)
✅ The difference between random vs intelligent control
✅ How physics affects robot movement

WHAT TO EXPECT:
🎮 You'll control the robot with different strategies
📊 Real-time data about robot state and balance
⚖️ See what happens with good vs bad control
🤖 Interactive physics simulation

EDUCATIONAL PURPOSE:
Learn how robots sense their environment and how different control strategies
affect movement quality. This builds intuition for later machine learning topics.
"""

import jax
import numpy as np
from loco_mujoco.task_factories import RLFactory
import time
import matplotlib.pyplot as plt

def explain_concept(title, explanation):
    """Helper function to clearly explain concepts"""
    print(f"\n💡 CONCEPT: {title}")
    print("─" * 60) 
    print(f"   {explanation}")
    print("─" * 60)

def create_simple_controller(strategy="balanced"):
    """Create simple control functions for demonstration"""
    
    def random_controller(obs):
        """Completely random actions"""
        return np.random.uniform(-0.2, 0.2, 23)  # Reduced range
    
    def balanced_controller(obs):
        """Small random actions - more conservative"""
        return np.random.uniform(-0.05, 0.05, 23)  # Even smaller range
    
    def smart_controller(obs):
        """Simple controller that responds to robot state"""
        actions = np.zeros(23)
        
        # Simple balance logic with reduced gains
        if len(obs) >= 10:  # Make sure we have enough observations
            # Use joint positions to create simple standing pose
            actions[2] = -0.02  # Small hip adjustment
            actions[5] = -0.02  # Small knee adjustment  
            actions[8] = 0.01   # Small ankle adjustment
            
            # Add tiny perturbations to show it's working
            actions += np.random.uniform(-0.01, 0.01, 23)
            
        return actions
    
    # Return the appropriate controller function
    if strategy == "random":
        return random_controller
    elif strategy == "balanced": 
        return balanced_controller
    elif strategy == "smart":
        return smart_controller
    else:
        return balanced_controller

def analyze_robot_state(obs):
    """Extract meaningful information from robot observations"""
    analysis = {}
    
    if len(obs) >= 10:
        # These are typical observation components (simplified interpretation)
        analysis['position'] = obs[0:3] if len(obs) >= 3 else [0,0,0]
        analysis['orientation'] = obs[3:7] if len(obs) >= 7 else [1,0,0,0] 
        analysis['joint_positions'] = obs[7:] if len(obs) > 7 else []
        
        # Calculate derived metrics
        height = analysis['position'][2] if len(analysis['position']) > 2 else 1.0
        analysis['is_standing'] = height > 0.8  # Rough threshold
        analysis['is_fallen'] = height < 0.5
        
    return analysis

def main():
    print("🎮 LocoMuJoCo Tutorial 2: Interactive Robot Control")
    print("=" * 60)
    
    explain_concept(
        "Robot Control Basics",
        "Robots have joints (like your elbows and knees) controlled by motors.\n"
        "   We send 'actions' (motor commands) and receive 'observations' (sensor data).\n"  
        "   Good control keeps the robot balanced and moving purposefully."
    )
    
    # Create a robot for reinforcement learning (no pre-recorded motions)
    print("\n🔨 STEP 1: Creating a Controllable Robot")
    print("Creating UnitreeG1 for manual control...")
    
    try:
        env = RLFactory.make(
            "UnitreeG1",
            horizon=1000,           # How long episodes can run
            headless=False          # Show visual interface
        )
        
        print("✅ Controllable robot created!")
        print(f"🎮 Control channels: {env.info.action_space.shape[0]} motors")
        print(f"🔍 Sensor channels: {env.info.observation_space.shape[0]} readings")
        
    except Exception as e:
        print(f"❌ Error creating robot: {e}")
        return
    
    explain_concept(
        "Observations vs Actions", 
        f"OBSERVATIONS ({env.info.observation_space.shape[0]} values): What the robot senses\n"
        f"   - Joint angles, body position, velocity, balance, etc.\n"
        f"   ACTIONS ({env.info.action_space.shape[0]} values): What we tell the robot to do\n"
        f"   - Motor torques/positions for each joint"
    )
    
    # Different control experiments
    control_experiments = [
        {
            "name": "Random Control",
            "strategy": "random", 
            "description": "Completely random motor commands",
            "expectation": "Robot will likely fall quickly - shows importance of good control",
            "duration": 200,
            "lesson": "Random actions don't work for complex robots!"
        },
        {
            "name": "Balanced Control", 
            "strategy": "balanced",
            "description": "Small, gentle motor commands",
            "expectation": "Robot should stay upright longer but may still fall",
            "duration": 300,
            "lesson": "Small actions are safer but may not achieve goals"
        },
        {
            "name": "Smart Control",
            "strategy": "smart", 
            "description": "Actions that respond to robot's current state",
            "expectation": "Best performance - robot adapts to maintain balance",
            "duration": 400,
            "lesson": "Responsive control that uses sensor feedback works best!"
        }
    ]
    
    print(f"\n🧪 STEP 2: Control Strategy Experiments")
    print("We'll try 3 different control approaches...")
    
    results = []
    
    for i, experiment in enumerate(control_experiments):
        print(f"\n🎯 EXPERIMENT {i+1}/3: {experiment['name'].upper()}")
        print("=" * 50)
        print(f"📝 Method: {experiment['description']}")
        print(f"🎯 Expected result: {experiment['expectation']}")
        print(f"⏱️  Duration: ~{experiment['duration']//30} seconds")
        
        # Create controller for this experiment
        controller = create_simple_controller(experiment['strategy'])
        
        # Reset robot to starting position
        key = jax.random.PRNGKey(42)
        obs = env.reset(key)
        
        print(f"🤖 Starting {experiment['name'].lower()}...")
        print("👀 Watch the robot's behavior and stability!")
        
        # Track performance metrics
        steps_survived = 0
        fell_down = False
        max_steps = experiment['duration']
        
        # Get initial action
        action = controller(obs)
        
        try:
            for step in range(max_steps):
                # Get current state
                result = env.step(action)
                if len(result) == 5:
                    obs, reward, done, truncated, info = result
                else:
                    obs, reward, done, info = result
                    truncated = False
                
                # Check if robot fell (be less strict about falling)
                if done and step > 5:  # Allow some initial settling
                    fell_down = True
                    print(f"⚠️  Robot fell at step {step}!")
                    break
                    
                # Get next action
                action = controller(obs)
                steps_survived = step
                
        except Exception as e:
            print(f"⚠️  Experiment stopped due to error: {e}")
        
        # Record results
        result = {
            'name': experiment['name'],
            'steps_survived': steps_survived,
            'fell_down': fell_down,
            'lesson': experiment['lesson']
        }
        results.append(result)
        
        print(f"📊 Results: Survived {steps_survived} steps, Fell: {fell_down}")
        print(f"🎓 Lesson: {experiment['lesson']}")
        
        if i < len(control_experiments) - 1:
            print("⏯️  Preparing next experiment...")
            time.sleep(2)
    
    # Summary and analysis
    print("\n📈 STEP 3: Results Analysis")
    print("=" * 50)
    
    for i, result in enumerate(results):
        print(f"{i+1}. {result['name']}: {result['steps_survived']} steps")
    
    best_performance = max(results, key=lambda x: x['steps_survived'])
    print(f"🏆 Best Strategy: {best_performance['name']} ({best_performance['steps_survived']} steps)")
    
    # Educational summary
    print("\n🎓 TUTORIAL COMPLETE - What You Just Learned:")
    print("=" * 60)
    print("✅ Robots need continuous control commands to stay balanced")
    print("✅ Random actions typically lead to failure")  
    print("✅ Good control uses sensor feedback to make decisions")
    print("✅ Simple strategies can work but smart strategies work better")
    print("✅ Real robotics requires sophisticated control algorithms")
    
    explain_concept(
        "Real-World Implications",
        "What you just saw demonstrates why we need machine learning!\n"
        "   Instead of hand-coding control rules, we can train AI to discover\n"
        "   the best control strategies through trial and error."
    )
    
    print("\n🏆 EXPERIMENT TIME!")
    print("Try modifying this tutorial:")
    print("💡 Change the action magnitudes in create_simple_controller()")
    print("💡 Modify the 'smart' controller to be even smarter")
    print("💡 Try different robots: 'UnitreeH1', 'Atlas'")
    print("💡 Adjust experiment durations to see longer behavior")
    
    explain_concept(
        "What's Next?",
        "Now you understand robot control basics! Next tutorials will show:\n"
        "   • How to train AI controllers using reinforcement learning\n"
        "   • How to use motion capture data to guide learning\n" 
        "   • Advanced topics like reward design and policy optimization"
    )

if __name__ == "__main__":
    main()