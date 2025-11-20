#!/usr/bin/env python3
"""
📚 Lesson 1.3: Basic Datasets  
=============================

GOAL: Explore different types of robot motions (walk, run, squat)
WHY: Understand how robots can perform diverse human movements

WHAT YOU'LL LEARN:
✅ Loading different motion types
✅ Comparing motion characteristics  
✅ Understanding dataset variety
✅ Concepts of motion primitives

See how one robot can perform many different human actions!
"""

from loco_mujoco.task_factories import ImitationFactory, DefaultDatasetConf
import time


def introduce_motion_variety():
    """💡 Introduce the concept of diverse motions"""
    print("💡 UNDERSTANDING MOTION VARIETY")
    print("=" * 40)
    print("🎭 Humans perform countless different movements:")
    print("   • Locomotion: walking, running, jumping")
    print("   • Exercise: squatting, stretching, dancing")
    print("   • Daily activities: sitting, reaching, waving")
    print("   • Sports: kicking, throwing, balancing")
    print("")
    print("🤖 For robots to be useful, they need this same variety!")
    print("")
    print("📚 Motion Datasets provide this variety:")
    print("   • Each dataset = one type of motion")
    print("   • Multiple examples of the same motion type")
    print("   • Recorded from real humans performing actions")
    print("   • Converted to robot joint commands")


def available_basic_motions():
    """📋 List available basic motion types"""
    print("\n📋 AVAILABLE BASIC MOTIONS")
    print("=" * 40)
    
    motions = [
        {
            "name": "walk",
            "description": "Natural human walking gait",
            "characteristics": "Steady, balanced, efficient forward movement",
            "use_cases": "Basic locomotion, navigation, everyday movement"
        },
        {
            "name": "run", 
            "description": "Faster locomotion with running gait",
            "characteristics": "Higher speed, more dynamic, aerial phases",
            "use_cases": "Fast travel, emergency response, athletic performance"
        },
        {
            "name": "squat",
            "description": "Up and down squatting exercise",
            "characteristics": "Vertical movement, strength, balance control",
            "use_cases": "Exercise routines, sitting/standing, strength training"
        },
        {
            "name": "balance",
            "description": "Maintaining upright standing position",  
            "characteristics": "Static stability, small adjustments, postural control",
            "use_cases": "Standing tasks, waiting, maintaining position"
        }
    ]
    
    for i, motion in enumerate(motions, 1):
        print(f"\n{i}. {motion['name'].upper()}")
        print(f"   📝 Description: {motion['description']}")
        print(f"   🎯 Key traits: {motion['characteristics']}")
        print(f"   💼 Applications: {motion['use_cases']}")
    
    return [m["name"] for m in motions]


def demonstrate_motion(motion_name, duration=15):
    """🎬 Demonstrate a single motion type"""
    print(f"\n🎬 DEMONSTRATING: {motion_name.upper()}")
    print("=" * 50)
    
    try:
        print(f"📋 Loading {motion_name} motion data...")
        
        # Create environment for this specific motion
        env = ImitationFactory.make(
            "UnitreeG1",
            default_dataset_conf=DefaultDatasetConf([motion_name]),
            n_substeps=20
        )
        
        print(f"✅ {motion_name.title()} data loaded!")
        print(f"⏱️  Playing {duration} seconds of {motion_name}...")
        print("👀 Watch the robot's movement pattern")
        
        # Calculate steps for duration
        steps_per_episode = duration * 30  # 30 FPS
        
        # Play the motion
        env.play_trajectory(
            n_episodes=1,
            n_steps_per_episode=steps_per_episode,
            render=True
        )
        
        print(f"✅ {motion_name.title()} demonstration complete!")
        
        # Clean up
        del env
        return True
        
    except Exception as e:
        print(f"❌ Failed to demonstrate {motion_name}: {e}")
        print(f"💡 {motion_name.title()} dataset may not be available")
        return False


def compare_motion_characteristics():
    """⚖️ Help students compare different motions"""
    print("\n⚖️ COMPARING MOTION CHARACTERISTICS")
    print("=" * 50)
    print("As you watch each motion, compare these aspects:")
    print("")
    print("🏃 SPEED & RHYTHM:")
    print("   • How fast does the robot move?")
    print("   • What's the rhythm of the movement?")
    print("   • Are movements smooth or jerky?")
    print("")
    print("⚖️ BALANCE & STABILITY:")
    print("   • How does the robot maintain balance?")
    print("   • Which joints work hardest for stability?")
    print("   • How much does the body sway?")
    print("")
    print("🎯 PURPOSE & FUNCTION:")
    print("   • What is this motion trying to achieve?")
    print("   • How efficient is the movement?")
    print("   • What makes it different from other motions?")
    print("")
    print("🦵 JOINT COORDINATION:")
    print("   • Which body parts move the most?")
    print("   • How do legs and arms coordinate?")
    print("   • What stays still vs. what moves?")


def motion_analysis_activity():
    """📊 Simple analysis questions for students"""
    print("\n📊 MOTION ANALYSIS ACTIVITY")
    print("=" * 40)
    print("🎯 After watching all motions, think about:")
    print("")
    print("❓ OBSERVATION QUESTIONS:")
    print("   1. Which motion covers the most ground?")
    print("   2. Which motion requires the most balance?")
    print("   3. Which motion looks most natural/human-like?")
    print("   4. Which motion would be hardest for a robot to learn?")
    print("")
    print("💭 ANALYSIS QUESTIONS:")
    print("   1. Why might 'walk' be easier than 'run' for robots?")
    print("   2. How does 'squat' help robots learn strength control?")
    print("   3. What makes 'balance' a foundation for other motions?")
    print("   4. Which motion would be most useful for a household robot?")
    print("")
    print("🔬 SCIENTIFIC THINKING:")
    print("   • What patterns do you notice across all motions?")
    print("   • How might you measure motion 'quality'?")
    print("   • What sensors would help robots perform these better?")


def explain_dataset_concepts():
    """🧠 Explain key dataset concepts"""
    print("\n🧠 KEY CONCEPTS: Motion Datasets")
    print("=" * 40)
    print("📚 DATASET = Collection of related motions")
    print("   • Multiple examples of the same action type")
    print("   • Recorded from different human subjects")
    print("   • Various speeds, styles, and variations")
    print("")
    print("🎭 MOTION PRIMITIVE = Basic building block")
    print("   • Simple, fundamental movement patterns")
    print("   • Can be combined to create complex behaviors")
    print("   • Example: walk + turn = navigation")
    print("")
    print("🔄 MOTION TRANSFER = Human → Robot")
    print("   • Human joint angles → Robot joint angles")
    print("   • Scale adjustments (human vs robot proportions)")
    print("   • Physics adaptations (robot weight, materials)")
    print("")
    print("🎯 MOTION QUALITY depends on:")
    print("   • Accuracy of original motion capture")
    print("   • Quality of human → robot conversion")
    print("   • Robot's physical capabilities")
    print("   • Environmental factors (gravity, friction)")


def main():
    """🚀 Main lesson function"""
    print("📚 Lesson 1.3: Basic Datasets")
    print("=" * 50)
    print("🎯 Goal: Explore different types of robot motions")
    print("⏱️  Time: ~8 minutes")
    print("🎓 Difficulty: Beginner")
    
    # Introduction
    introduce_motion_variety()
    motion_list = available_basic_motions()
    
    # Motion comparison framework
    compare_motion_characteristics()
    
    print(f"\n🎬 MOTION DEMONSTRATIONS")
    print("=" * 50)
    print("We'll now demonstrate each motion type.")
    print("Watch carefully and compare their characteristics!")
    
    # Demonstrate each available motion
    successful_demos = 0
    for i, motion in enumerate(motion_list, 1):
        print(f"\n{'='*60}")
        print(f"🎭 MOTION {i}/{len(motion_list)}: {motion.upper()}")
        print(f"{'='*60}")
        
        if demonstrate_motion(motion, duration=12):
            successful_demos += 1
        
        # Pause between demonstrations
        if i < len(motion_list):
            print("\n⏱️  Preparing next motion...")
            time.sleep(2)
    
    # Analysis and concepts
    motion_analysis_activity()
    explain_dataset_concepts()
    
    print(f"\n🎓 LESSON COMPLETE!")
    print("=" * 50)
    print(f"✅ Successfully demonstrated: {successful_demos}/{len(motion_list)} motions")
    print("✅ You've learned:")
    print("   • Different types of robot motions")
    print("   • How motion datasets work") 
    print("   • Motion analysis and comparison")
    print("   • Key concepts in motion transfer")
    print("")
    print("🚀 Ready for Lesson 1.4: LAFAN1 Datasets (Advanced Motions)")
    print("")
    print("🏆 EXPERIMENT IDEAS:")
    print("💡 Try loading multiple motions together:")
    print("   DefaultDatasetConf(['walk', 'run', 'squat'])")
    print("💡 Change n_substeps to make motions smoother/faster")
    print("💡 Pause during motions to study specific poses")
    print("💡 Count how many steps each motion type takes")


if __name__ == "__main__":
    main()