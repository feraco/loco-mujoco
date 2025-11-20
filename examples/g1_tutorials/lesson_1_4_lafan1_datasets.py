#!/usr/bin/env python3
"""
💃 Lesson 1.4: LAFAN1 Datasets
==============================

GOAL: Explore advanced human motions like dancing and acrobatics
WHY: See how expressive and dynamic movements transfer to robots

WHAT YOU'LL LEARN:
✅ What LAFAN1 dataset contains
✅ Loading dance and acrobatic motions  
✅ Difference between basic and advanced motions
✅ Challenges of complex motion transfer

Watch robots perform human dance moves and athletic actions!
"""

from loco_mujoco.task_factories import ImitationFactory, LAFAN1DatasetConf
import time


def introduce_lafan1():
    """💡 Introduce the LAFAN1 dataset"""
    print("💡 INTRODUCING LAFAN1 DATASET")
    print("=" * 40)
    print("🎭 LAFAN1 = A Rich Collection of Human Motions")
    print("")
    print("📚 What is LAFAN1?")
    print("   • Professional motion capture database")
    print("   • Recorded from skilled human performers")
    print("   • Includes dance, acrobatics, martial arts")
    print("   • High-quality, expressive movements")
    print("")
    print("🎯 Why LAFAN1 is Special:")
    print("   • Goes beyond basic locomotion")
    print("   • Captures human creativity and artistry")
    print("   • Shows robots can be expressive, not just functional")
    print("   • Demonstrates limits and possibilities of motion transfer")
    print("")
    print("🤖 For Robotics:")
    print("   • Tests robot flexibility and range of motion")
    print("   • Pushes boundaries of what's possible")
    print("   • Inspires more natural robot behavior")
    print("   • Opens doors to entertainment and art applications")


def available_lafan1_motions():
    """📋 Show available LAFAN1 motion categories"""
    print("\n📋 LAFAN1 MOTION CATEGORIES")
    print("=" * 40)
    
    categories = [
        {
            "category": "Dance Motions",
            "examples": ["dance1_subject1", "dance2_subject4"],
            "description": "Rhythmic, expressive movements with artistic flair",
            "challenges": "Complex coordination, dynamic balance, style expression"
        },
        {
            "category": "Locomotion Variants", 
            "examples": ["walk1_subject1", "run1_subject2"],
            "description": "Different styles of walking and running from various people",
            "challenges": "Individual differences, speed variations, terrain adaptation"
        },
        {
            "category": "Athletic Actions",
            "examples": ["jumps1_subject1", "fight1_subject2"],
            "description": "Dynamic sports and martial arts movements",
            "challenges": "High forces, precise timing, power generation"
        },
        {
            "category": "Recovery Actions",
            "examples": ["fallAndGetUp1_subject1"],
            "description": "Falling down and getting back up safely",
            "challenges": "Impact handling, momentum management, self-recovery"
        }
    ]
    
    for i, cat in enumerate(categories, 1):
        print(f"\n{i}. {cat['category'].upper()}")
        print(f"   📝 Description: {cat['description']}")
        print(f"   🎯 Examples: {', '.join(cat['examples'])}")
        print(f"   ⚠️  Challenges: {cat['challenges']}")
    
    return categories


def demonstrate_lafan1_motion(motion_name, description=""):
    """🎬 Demonstrate a LAFAN1 motion"""
    print(f"\n🎬 DEMONSTRATING: {motion_name}")
    print("=" * 50)
    
    try:
        print(f"📋 Loading LAFAN1 motion: {motion_name}...")
        if description:
            print(f"📝 Description: {description}")
        
        # Create environment with LAFAN1 dataset
        env = ImitationFactory.make(
            "UnitreeG1",
            lafan1_dataset_conf=LAFAN1DatasetConf([motion_name]),
            n_substeps=20
        )
        
        print(f"✅ {motion_name} data loaded!")
        print(f"⏱️  Playing ~20 seconds of {motion_name}...")
        print("👀 Watch the robot's expressive movement!")
        
        # Play the motion - longer for complex motions
        env.play_trajectory(
            n_episodes=1,
            n_steps_per_episode=600,  # 20 seconds at 30 FPS
            render=True
        )
        
        print(f"✅ {motion_name} demonstration complete!")
        
        # Clean up
        del env
        return True
        
    except Exception as e:
        print(f"❌ Failed to demonstrate {motion_name}: {e}")
        print(f"💡 {motion_name} may not be available or need special setup")
        return False


def compare_basic_vs_advanced():
    """⚖️ Compare basic datasets vs LAFAN1"""
    print("\n⚖️ BASIC vs ADVANCED MOTIONS")
    print("=" * 50)
    
    comparison = [
        {
            "aspect": "Complexity",
            "basic": "Simple, repetitive patterns",
            "lafan1": "Complex, varied, artistic sequences"
        },
        {
            "aspect": "Purpose", 
            "basic": "Functional locomotion and exercise",
            "lafan1": "Expression, entertainment, athletics"
        },
        {
            "aspect": "Coordination",
            "basic": "Basic joint coordination",
            "lafan1": "Full-body coordination with style"
        },
        {
            "aspect": "Dynamics",
            "basic": "Steady, controlled movements",
            "lafan1": "Dynamic, explosive, variable speed"
        },
        {
            "aspect": "Learning Difficulty",
            "basic": "Easier for robots to master",
            "lafan1": "Challenging, pushes robot limits"
        },
        {
            "aspect": "Applications",
            "basic": "Practical robotics tasks",
            "lafan1": "Entertainment, research, art"
        }
    ]
    
    print(f"{'Aspect':<20} {'Basic Datasets':<30} {'LAFAN1 Datasets':<30}")
    print("-" * 80)
    
    for comp in comparison:
        print(f"{comp['aspect']:<20} {comp['basic']:<30} {comp['lafan1']:<30}")


def motion_transfer_challenges():
    """⚠️ Discuss challenges of complex motion transfer"""
    print("\n⚠️ CHALLENGES OF COMPLEX MOTION TRANSFER")
    print("=" * 50)
    print("🤖 Why Advanced Motions Are Harder for Robots:")
    print("")
    print("🦴 PHYSICAL LIMITATIONS:")
    print("   • Robot joints may not match human flexibility")
    print("   • Different weight distribution and proportions")
    print("   • Motors may not provide enough speed or power")
    print("   • Balance systems work differently")
    print("")
    print("🧠 CONTROL COMPLEXITY:")
    print("   • More joints must coordinate precisely")
    print("   • Timing becomes critical for success")
    print("   • Small errors compound into major failures")
    print("   • Real-time adaptation is challenging")
    print("")
    print("🎯 MOTION FIDELITY:")
    print("   • Hard to capture subtle human nuances")
    print("   • Style and expression are difficult to transfer")
    print("   • Cultural and personal variations in movement")
    print("   • Artistic intent may be lost in translation")
    print("")
    print("💡 SOLUTIONS BEING DEVELOPED:")
    print("   • Better motion capture technology")
    print("   • Advanced robot designs with more DOF")
    print("   • Smarter control algorithms")
    print("   • Machine learning for adaptation")


def analysis_questions():
    """📊 Questions for analyzing LAFAN1 motions"""
    print("\n📊 ANALYSIS QUESTIONS")
    print("=" * 40)
    print("🎯 While watching LAFAN1 motions, consider:")
    print("")
    print("🎭 EXPRESSIVENESS:")
    print("   • How well does the robot capture human style?")
    print("   • Which aspects of the motion look most/least natural?")
    print("   • Can you 'feel' the emotion or intent in the movement?")
    print("")
    print("⚖️ TECHNICAL EXECUTION:")
    print("   • Does the robot maintain balance throughout?")
    print("   • Are movements smooth or jerky?")
    print("   • Which parts of the motion work best/worst?")
    print("")
    print("🔬 SCIENTIFIC THINKING:")
    print("   • What makes these motions harder than basic walking?")
    print("   • How might you measure 'motion quality'?")
    print("   • What improvements would help the robot perform better?")
    print("")
    print("🚀 FUTURE APPLICATIONS:")
    print("   • Where could expressive robot motions be useful?")
    print("   • What new possibilities do these motions open up?")
    print("   • How might this change how we interact with robots?")


def main():
    """🚀 Main lesson function"""
    print("💃 Lesson 1.4: LAFAN1 Datasets")
    print("=" * 50)
    print("🎯 Goal: Explore advanced human motions like dance")
    print("⏱️  Time: ~10 minutes")
    print("🎓 Difficulty: Beginner+")
    
    # Introduction
    introduce_lafan1()
    categories = available_lafan1_motions()
    compare_basic_vs_advanced()
    
    # Motion demonstrations  
    print(f"\n🎬 LAFAN1 MOTION DEMONSTRATIONS")
    print("=" * 50)
    print("We'll demonstrate several types of advanced motions.")
    print("Compare them to the basic motions from Lesson 1.3!")
    
    # Demonstrate sample motions from each category
    demo_motions = [
        ("dance2_subject4", "Expressive dance sequence with artistic flair"),
        ("walk1_subject1", "Natural walking with individual human style"),  
        ("jumps1_subject1", "Athletic jumping and landing actions"),
    ]
    
    successful_demos = 0
    for i, (motion_name, description) in enumerate(demo_motions, 1):
        print(f"\n{'='*60}")
        print(f"🎭 DEMO {i}/{len(demo_motions)}: Advanced Motion")
        print(f"{'='*60}")
        
        if demonstrate_lafan1_motion(motion_name, description):
            successful_demos += 1
        
        # Pause between demonstrations
        if i < len(demo_motions):
            print("\n⏱️  Preparing next motion...")
            time.sleep(2)
    
    # Analysis and challenges
    motion_transfer_challenges()
    analysis_questions()
    
    print(f"\n🎓 LESSON COMPLETE!")
    print("=" * 50)
    print(f"✅ Successfully demonstrated: {successful_demos}/{len(demo_motions)} LAFAN1 motions")
    print("✅ You've learned:")
    print("   • What makes LAFAN1 dataset special")
    print("   • Difference between basic and advanced motions")
    print("   • Challenges of complex motion transfer")
    print("   • How robots can be expressive, not just functional")
    print("")
    print("🚀 Ready for Lesson 1.5: Interactive Control")
    print("")
    print("🏆 EXPERIMENT IDEAS:")
    print("💡 Try other LAFAN1 motions:")
    print("   • dance1_subject1, dance1_subject2")
    print("   • fight1_subject2, fallAndGetUp1_subject1") 
    print("💡 Compare the same motion from different subjects")
    print("💡 Load multiple LAFAN1 motions together")
    print("💡 Analyze which motions work best on G1 robot")


if __name__ == "__main__":
    main()