#!/usr/bin/env python3
"""
🚀 LocoMuJoCo Tutorial 4: Learning to Walk - Reinforcement Learning Basics
==========================================================================

This tutorial introduces the basic concepts of how robots learn to walk
through reinforcement learning - trial and error with rewards!

LEARNING OBJECTIVES:
📚 Understand what reinforcement learning is
🎯 See how reward functions guide robot behavior
🤖 Watch a robot gradually improve at walking
🧠 Grasp the training process and why it works

No advanced ML knowledge required - just curiosity!
"""

import os
import time
import numpy as np
import jax
import jax.numpy as jnp
from loco_mujoco.task_factories import RLFactory, ImitationFactory, DefaultDatasetConf


def explain_reinforcement_learning():
    """💡 Explain RL concepts with analogies"""
    print("\n💡 CONCEPT: What is Reinforcement Learning?")
    print("─" * 60)
    print("   Imagine teaching a child to ride a bike:")
    print("   • TRIAL: Child tries to balance and pedal")
    print("   • ERROR: Child wobbles or falls")  
    print("   • REWARD: 'Good job!' when they stay upright")
    print("   • LEARNING: Child gradually gets better")
    print("   ")
    print("   For robots, it's the same:")
    print("   • Robot tries different movements (ACTIONS)")
    print("   • Environment gives feedback (REWARDS)")
    print("   • Robot learns which actions work best")
    print("   • Eventually robot masters the skill!")
    print("─" * 60)


def demonstrate_reward_system():
    """🎯 Show how reward functions work"""
    print("\n💡 CONCEPT: Reward Functions - Teaching Robots What's Good")
    print("─" * 60)
    print("   A reward function is like a teacher's grading system:")
    print("   ")
    print("   🏆 POSITIVE REWARDS (Good behavior):")
    print("   • +10 points for walking forward")
    print("   • +5 points for staying upright") 
    print("   • +2 points for smooth movements")
    print("   ")
    print("   💥 NEGATIVE REWARDS (Bad behavior):")
    print("   • -20 points for falling down")
    print("   • -5 points for moving backward")
    print("   • -1 point for jerky movements")
    print("   ")
    print("   🧠 The robot learns to maximize total reward!")
    print("─" * 60)


def simulate_learning_process():
    """🎓 Simulate the learning process conceptually"""
    print("\n🎓 STEP 1: Simulating the Learning Process")
    print("Let's see how a robot might learn to walk over time...")
    
    # Simulate learning progress
    episodes = [
        {"episode": 1, "reward": -150, "behavior": "Falls immediately", "lesson": "Random actions don't work"},
        {"episode": 10, "reward": -45, "behavior": "Stands for 3 seconds", "lesson": "Learning to balance"},
        {"episode": 50, "reward": 25, "behavior": "Takes 2 steps forward", "lesson": "Discovering walking motion"},
        {"episode": 100, "reward": 180, "behavior": "Walks 5 meters smoothly", "lesson": "Mastering coordination"},
        {"episode": 500, "reward": 450, "behavior": "Walks gracefully, turns", "lesson": "Expert-level performance"}
    ]
    
    print("\n📈 Learning Progress Over Time:")
    print("=" * 70)
    
    for ep in episodes:
        print(f"\n🔄 Episode {ep['episode']:3d}: Reward = {ep['reward']:4d}")
        print(f"   🤖 Behavior: {ep['behavior']}")
        print(f"   🎓 Lesson: {ep['lesson']}")
        time.sleep(1.5)
    
    print("\n💡 Key Insight: The robot discovers successful strategies")
    print("   through thousands of trial-and-error attempts!")


def demonstrate_real_training_setup():
    """🔬 Show actual RL training environment"""
    print(f"\n🔬 STEP 2: Real RL Training Environment")
    print("Now let's see an actual reinforcement learning setup...")
    
    try:
        print(f"\n📋 Creating RL training environment...")
        
        # Create RL environment (no pre-defined motion data)
        env = RLFactory.make("UnitreeG1")
        
        print(f"✅ RL Environment created!")
        print(f"🎮 Action space: {env.num_actions} motors to control")
        print(f"🔍 Observation space: {env.num_observations} sensor readings")
        
        print(f"\n💡 CONCEPT: The Difference")
        print("─" * 60)
        print("   🎬 IMITATION Learning: Robot copies human demonstrations")  
        print("   🎯 REINFORCEMENT Learning: Robot discovers actions through rewards")
        print("   ")
        print("   RL is harder but more flexible - robots can learn")
        print("   movements that no human has ever demonstrated!")
        print("─" * 60)
        
        # Show what an untrained robot does
        print(f"\n🤖 What an untrained robot does:")
        print("   Let's see random actions (before any learning)...")
        
        key = jax.random.PRNGKey(42)
        obs = env.reset(key)
        
        print(f"   📊 Initial observation shape: {obs.shape}")
        print(f"   🎲 Taking random actions for 3 seconds...")
        
        total_reward = 0
        for step in range(90):  # 3 seconds at 30 FPS
            # Random action (untrained robot)
            action = np.random.uniform(-0.1, 0.1, env.num_actions) 
            
            result = env.step(action)
            if len(result) == 5:
                obs, reward, done, truncated, info = result
            else:
                obs, reward, done, info = result
                truncated = False
            
            total_reward += reward
            
            if done:
                print(f"   💥 Robot fell at step {step}!")
                break
        
        print(f"   📊 Total reward: {total_reward:.2f}")
        print(f"   💡 Negative reward = robot needs to learn better actions!")
        
        del env
        
    except Exception as e:
        print(f"   ⚠️  Could not create RL environment: {e}")
        print(f"   💡 This is normal - RL training requires special setup")


def compare_learning_approaches():
    """⚖️ Compare different learning approaches"""
    print(f"\n⚖️ STEP 3: Learning Approach Comparison")
    print("=" * 60)
    
    approaches = [
        {
            "name": "Imitation Learning", 
            "emoji": "🎬",
            "method": "Copy human demonstrations",
            "pros": "Fast, human-like movements",
            "cons": "Limited to demonstrated behaviors",
            "example": "Learning to dance by watching videos"
        },
        {
            "name": "Reinforcement Learning",
            "emoji": "🎯", 
            "method": "Trial-and-error with rewards",
            "pros": "Can discover novel solutions",
            "cons": "Slower, requires many trials", 
            "example": "Learning chess by playing millions of games"
        },
        {
            "name": "Hybrid Approach",
            "emoji": "🚀",
            "method": "Start with imitation, improve with RL", 
            "pros": "Fast start + continued improvement",
            "cons": "More complex to implement",
            "example": "Learn basic walking, then optimize for speed"
        }
    ]
    
    for approach in approaches:
        print(f"\n{approach['emoji']} {approach['name'].upper()}")
        print(f"   📋 Method: {approach['method']}")
        print(f"   ✅ Pros: {approach['pros']}")  
        print(f"   ⚠️  Cons: {approach['cons']}")
        print(f"   🌟 Example: {approach['example']}")


def demonstrate_with_imitation_baseline():
    """🎬 Show how we currently achieve walking with imitation"""
    print(f"\n🎬 STEP 4: Current Solution - Imitation Learning")
    print("While true RL training takes hours, let's see imitation learning...")
    
    try:
        print(f"\n📋 Loading human walking data...")
        
        # Create imitation environment (using human demonstrations)
        env = ImitationFactory.make("UnitreeG1", 
                                  default_dataset_conf=DefaultDatasetConf(["walk"]))
        
        print(f"✅ Imitation environment ready!")
        print(f"📚 This uses recorded human walking motions")
        
        print(f"\n🎯 Quick demonstration: Robot walking (10 seconds)")
        print("   This shows what RL training aims to achieve...")
        
        env.play_trajectory(
            n_episodes=1,
            n_steps_per_episode=300,  # 10 seconds
            render=True
        )
        
        print(f"✅ Beautiful walking motion achieved through imitation!")
        print(f"🎯 Goal: RL would learn to create this without human data")
        
        del env
        
    except Exception as e:
        print(f"   ⚠️  Demo unavailable: {e}")


def main():
    """🚀 Main tutorial function"""
    print("🚀 LocoMuJoCo Tutorial 4: Learning to Walk")
    print("=" * 60)
    print("🎯 Understanding how robots learn through trial and error")
    
    # Core concept explanations
    explain_reinforcement_learning()
    demonstrate_reward_system() 
    
    # Learning process simulation
    simulate_learning_process()
    
    # Technical details
    demonstrate_real_training_setup()
    compare_learning_approaches()
    demonstrate_with_imitation_baseline()
    
    # Wrap up
    print(f"\n🎓 TUTORIAL COMPLETE - What You Just Learned:")
    print("=" * 60)
    print("✅ Reinforcement learning = trial and error + rewards")
    print("✅ Reward functions guide robot behavior like a teacher")
    print("✅ Learning takes many attempts but finds novel solutions")
    print("✅ Imitation learning is faster but less flexible")
    print("✅ Real RL training would take hours/days of computation")
    
    print(f"\n💡 CONCEPT: Real-World Applications")
    print("─" * 60)
    print("   🤖 Autonomous vehicles learning to drive")
    print("   🎮 Game AI mastering complex strategies")  
    print("   🦾 Prosthetic limbs adapting to users")
    print("   🚁 Drones learning aerobatic maneuvers")
    print("   🏭 Factory robots optimizing assembly")
    print("─" * 60)
    
    print(f"\n🏆 EXPERIMENT TIME!")
    print("Try modifying this tutorial:")
    print("💡 Design your own reward function for different behaviors")
    print("💡 Think about what rewards would teach jumping vs dancing")
    print("💡 Consider multi-objective rewards (speed + efficiency)")
    print("💡 Explore how reward shaping affects learning speed")
    
    print(f"\n💡 CONCEPT: What's Next?")
    print("─" * 60)  
    print("   Now you understand how robots learn! Advanced topics:")
    print("   • Policy gradient algorithms (PPO, SAC, etc.)")
    print("   • Sim-to-real transfer (simulation → real robot)")
    print("   • Multi-agent learning (robots teaching each other)")
    print("   • Hierarchical RL (learning complex multi-step skills)")
    print("─" * 60)


if __name__ == "__main__":
    main()