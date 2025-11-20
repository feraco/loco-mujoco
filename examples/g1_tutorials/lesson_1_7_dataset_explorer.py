#!/usr/bin/env python3
"""
🗺️ Lesson 1.7: Dataset Explorer
===============================

GOAL: Become an expert explorer of all available motion datasets
WHY: Understanding what data is available helps you choose the right motions

WHAT YOU'LL LEARN:
✅ Complete overview of all available datasets
✅ How to search and filter motion data
✅ Comparing motion characteristics
✅ Building custom motion collections

Explore the entire universe of robot motions!
"""

from loco_mujoco.task_factories import ImitationFactory, DefaultDatasetConf, LAFAN1DatasetConf
import time


def introduce_dataset_explorer():
    """🗺️ Introduce the concept of dataset exploration"""
    print("🗺️ DATASET EXPLORATION FUNDAMENTALS")
    print("=" * 40)
    print("🎯 What is Dataset Exploration?")
    print("   • Systematic discovery of available motion data")
    print("   • Understanding what types of motions exist")
    print("   • Learning the characteristics of each dataset")
    print("   • Finding the right data for your project")
    print("")
    print("📊 Why Explore Datasets?")
    print("   • Know what's possible with available data")
    print("   • Choose appropriate motions for your goals")
    print("   • Understand limitations and capabilities")
    print("   • Discover unexpected motion possibilities")
    print("")
    print("🔍 Explorer Skills:")
    print("   • Systematic search and categorization")
    print("   • Quality assessment and comparison")
    print("   • Technical requirement matching")
    print("   • Creative combination possibilities")


def catalog_default_datasets():
    """📚 Catalog all default motion datasets"""
    print("\n📚 DEFAULT DATASET CATALOG")
    print("=" * 40)
    print("🏠 Built-in Motion Library")
    
    datasets = [
        {
            "name": "walk",
            "category": "Basic Locomotion",
            "description": "Steady, natural walking patterns",
            "duration": "Medium cycles",
            "complexity": "★☆☆☆☆",
            "best_for": "Learning basic robot control, stability testing",
            "characteristics": "Rhythmic, balanced, predictable"
        },
        {
            "name": "run",
            "category": "Dynamic Locomotion", 
            "description": "Fast running with flight phases",
            "duration": "Quick cycles",
            "complexity": "★★★☆☆",
            "best_for": "Speed testing, dynamic balance challenges",
            "characteristics": "High energy, aerial phases, impact forces"
        },
        {
            "name": "squat",
            "category": "Exercise Movement",
            "description": "Up-down squatting exercise",
            "duration": "Slow cycles", 
            "complexity": "★★☆☆☆",
            "best_for": "Joint range testing, strength evaluation",
            "characteristics": "Controlled, strength-based, full range"
        },
        {
            "name": "balance",
            "category": "Stability Control",
            "description": "Standing balance maintenance",
            "duration": "Continuous",
            "complexity": "★☆☆☆☆",
            "best_for": "Balance algorithm testing, steady-state analysis",
            "characteristics": "Subtle adjustments, stability focus"
        }
    ]
    
    print(f"{'Name':<12} {'Category':<18} {'Complexity':<10} {'Best For'}")
    print("-" * 70)
    
    for ds in datasets:
        print(f"{ds['name']:<12} {ds['category']:<18} {ds['complexity']:<10} {ds['best_for']}")
    
    print(f"\n📋 DETAILED DESCRIPTIONS:")
    for i, ds in enumerate(datasets, 1):
        print(f"\n{i}. {ds['name'].upper()}")
        print(f"   📝 Description: {ds['description']}")
        print(f"   ⏱️  Duration: {ds['duration']}")
        print(f"   🎯 Characteristics: {ds['characteristics']}")
        print(f"   🏆 Best for: {ds['best_for']}")
    
    return [ds['name'] for ds in datasets]


def catalog_lafan1_datasets():
    """🎭 Catalog LAFAN1 motion datasets"""
    print("\n🎭 LAFAN1 DATASET CATALOG")
    print("=" * 40)
    print("🎨 Professional Motion Capture Library")
    
    lafan1_categories = [
        {
            "category": "Dance Expressions",
            "motions": ["dance1_subject1", "dance1_subject2", "dance1_subject3", 
                       "dance2_subject1", "dance2_subject2", "dance2_subject3", 
                       "dance2_subject4", "dance2_subject5"],
            "complexity": "★★★★★",
            "description": "Artistic, expressive dance sequences",
            "best_for": "Entertainment robotics, motion quality research"
        },
        {
            "category": "Natural Locomotion",
            "motions": ["walk1_subject1", "walk1_subject2", "walk1_subject3",
                       "run1_subject1", "run1_subject2"],
            "complexity": "★★☆☆☆", 
            "description": "Individual human walking and running styles",
            "best_for": "Natural gait analysis, personalized motion"
        },
        {
            "category": "Athletic Actions", 
            "motions": ["jumps1_subject1", "jumps1_subject2", "jumps1_subject3"],
            "complexity": "★★★★☆",
            "description": "Dynamic jumping and landing sequences",
            "best_for": "Dynamic control, impact testing, agility"
        },
        {
            "category": "Combat Sports",
            "motions": ["fight1_subject1", "fight1_subject2", "fight1_subject3"],
            "complexity": "★★★★☆", 
            "description": "Martial arts and fighting movements",
            "best_for": "Reaction training, defensive robotics"
        },
        {
            "category": "Recovery Actions",
            "motions": ["fallAndGetUp1_subject1", "fallAndGetUp1_subject2"],
            "complexity": "★★★☆☆",
            "description": "Falling and recovery sequences",
            "best_for": "Safety research, self-recovery systems"
        }
    ]
    
    total_motions = 0
    print(f"{'Category':<18} {'Count':<6} {'Complexity':<10} {'Description'}")
    print("-" * 80)
    
    for cat in lafan1_categories:
        count = len(cat['motions'])
        total_motions += count
        print(f"{cat['category']:<18} {count:<6} {cat['complexity']:<10} {cat['description']}")
    
    print(f"\n📊 TOTAL LAFAN1 MOTIONS: {total_motions}")
    
    print(f"\n📋 DETAILED BREAKDOWN:")
    for i, cat in enumerate(lafan1_categories, 1):
        print(f"\n{i}. {cat['category'].upper()}")
        print(f"   🎯 Best for: {cat['best_for']}")
        print(f"   📝 Available motions:")
        for motion in cat['motions']:
            print(f"      • {motion}")
    
    return lafan1_categories


def demonstrate_dataset_search():
    """🔍 Demonstrate how to search and filter datasets"""
    print("\n🔍 DATASET SEARCH & FILTERING")
    print("=" * 40)
    print("🎯 Search by Motion Characteristics")
    
    search_criteria = [
        {
            "name": "Beginner-Friendly Motions",
            "filter": "Low complexity, stable, educational",
            "recommendations": ["walk", "balance", "walk1_subject1"]
        },
        {
            "name": "High-Energy Dynamics", 
            "filter": "Fast, dynamic, challenging",
            "recommendations": ["run", "jumps1_subject1", "dance2_subject4"]
        },
        {
            "name": "Artistic Expression",
            "filter": "Creative, expressive, entertaining", 
            "recommendations": ["dance1_subject1", "dance2_subject2", "dance1_subject3"]
        },
        {
            "name": "Practical Applications",
            "filter": "Useful, functional, real-world",
            "recommendations": ["walk", "run", "fallAndGetUp1_subject1"]
        },
        {
            "name": "Research Challenges",
            "filter": "Complex, cutting-edge, difficult",
            "recommendations": ["fight1_subject2", "jumps1_subject2", "dance2_subject5"]
        }
    ]
    
    for i, search in enumerate(search_criteria, 1):
        print(f"\n{i}. {search['name'].upper()}")
        print(f"   🔍 Filter: {search['filter']}")
        print(f"   💡 Recommendations: {', '.join(search['recommendations'])}")


def demonstrate_motion_sampling():
    """🎬 Quick sampling of different motion types"""
    print("\n🎬 MOTION SAMPLING TOUR")
    print("=" * 40)
    print("Quick preview of different motion categories!")
    print("Each motion plays for ~5 seconds to give you a taste.")
    
    sample_motions = [
        {
            "name": "walk", 
            "type": "default",
            "category": "Basic Locomotion"
        },
        {
            "name": "run",
            "type": "default", 
            "category": "Dynamic Locomotion"
        },
        {
            "name": "dance1_subject1",
            "type": "lafan1",
            "category": "Artistic Expression"
        },
        {
            "name": "jumps1_subject1", 
            "type": "lafan1",
            "category": "Athletic Action"
        }
    ]
    
    for i, motion in enumerate(sample_motions, 1):
        print(f"\n{'='*50}")
        print(f"🎭 SAMPLE {i}/{len(sample_motions)}: {motion['category']}")
        print(f"📋 Motion: {motion['name']} ({motion['type']} dataset)")
        print(f"{'='*50}")
        
        try:
            # Create appropriate environment
            if motion['type'] == 'default':
                env = ImitationFactory.make(
                    "UnitreeG1",
                    default_dataset_conf=DefaultDatasetConf([motion['name']]),
                    n_substeps=20
                )
            else:  # lafan1
                env = ImitationFactory.make(
                    "UnitreeG1", 
                    lafan1_dataset_conf=LAFAN1DatasetConf([motion['name']]),
                    n_substeps=20
                )
            
            print(f"✅ {motion['name']} loaded!")
            print(f"🎬 Playing 5-second sample...")
            
            # Short sample - 150 steps = ~5 seconds
            env.play_trajectory(
                n_episodes=1,
                n_steps_per_episode=150,
                render=True
            )
            
            print(f"✅ {motion['name']} sample complete!")
            del env
            
        except Exception as e:
            print(f"❌ Failed to sample {motion['name']}: {e}")
        
        # Pause between samples
        if i < len(sample_motions):
            print("⏱️  Preparing next sample...")
            time.sleep(1)


def build_custom_collection():
    """🛠️ Demonstrate building custom motion collections"""
    print("\n🛠️ BUILDING CUSTOM COLLECTIONS")
    print("=" * 40)
    print("🎯 How to Combine Multiple Datasets")
    
    collection_examples = [
        {
            "name": "Locomotion Masterclass",
            "purpose": "Complete walking and running training",
            "default_motions": ["walk", "run"],
            "lafan1_motions": ["walk1_subject1", "run1_subject2"],
            "benefit": "Variety of locomotion styles for robust training"
        },
        {
            "name": "Entertainment Package",
            "purpose": "Robot performance and entertainment",
            "default_motions": ["balance"],
            "lafan1_motions": ["dance1_subject1", "dance2_subject4"],
            "benefit": "Expressive motions for public demonstrations"
        },
        {
            "name": "Athletic Training Suite",
            "purpose": "Dynamic and challenging motions",
            "default_motions": ["run", "squat"],
            "lafan1_motions": ["jumps1_subject1", "fight1_subject2"],
            "benefit": "Push robot capabilities to the limit"
        },
        {
            "name": "Safety Research Set",
            "purpose": "Balance and recovery analysis", 
            "default_motions": ["balance", "walk"],
            "lafan1_motions": ["fallAndGetUp1_subject1"],
            "benefit": "Focus on stability and safety mechanisms"
        }
    ]
    
    for i, collection in enumerate(collection_examples, 1):
        print(f"\n{i}. {collection['name'].upper()}")
        print(f"   🎯 Purpose: {collection['purpose']}")
        print(f"   📦 Default motions: {', '.join(collection['default_motions'])}")
        print(f"   🎭 LAFAN1 motions: {', '.join(collection['lafan1_motions'])}")
        print(f"   💡 Benefit: {collection['benefit']}")
    
    # Demonstrate how to create one
    print(f"\n🛠️ CREATING CUSTOM COLLECTION: Entertainment Package")
    print("=" * 60)
    
    try:
        print("📋 Loading combined dataset...")
        env = ImitationFactory.make(
            "UnitreeG1",
            default_dataset_conf=DefaultDatasetConf(["balance"]),
            lafan1_dataset_conf=LAFAN1DatasetConf(["dance1_subject1"]),
            n_substeps=20
        )
        
        print("✅ Combined dataset loaded successfully!")
        print("🎬 This environment now contains multiple motion types")
        print("💡 The robot can switch between balance and dance motions")
        
        # Short demonstration
        env.play_trajectory(
            n_episodes=1,
            n_steps_per_episode=200,
            render=True
        )
        
        del env
        print("✅ Custom collection demonstration complete!")
        
    except Exception as e:
        print(f"❌ Custom collection failed: {e}")
        print("💡 Some combinations may require additional setup")


def dataset_selection_guide():
    """📋 Guide for choosing the right datasets"""
    print("\n📋 DATASET SELECTION GUIDE")
    print("=" * 40)
    print("🎯 How to Choose the Right Motion Data")
    
    selection_criteria = [
        {
            "question": "What is your robot's skill level?",
            "beginner": "Start with: walk, balance, walk1_subject1",
            "intermediate": "Try: run, squat, dance1_subject1",
            "advanced": "Challenge with: jumps1_subject1, fight1_subject2"
        },
        {
            "question": "What is your project goal?",
            "education": "Use: walk, balance (clear, predictable)",
            "research": "Use: LAFAN1 motions (diverse, challenging)",
            "entertainment": "Use: dance motions (expressive, engaging)"
        },
        {
            "question": "What are your hardware constraints?",
            "limited_power": "Choose: balance, walk (low energy)",
            "standard_robot": "Choose: run, squat (moderate energy)",
            "high_performance": "Choose: jumps, fights (high energy)"
        },
        {
            "question": "How much time do you have?",
            "quick_demo": "Use: any single motion (~30 seconds)",
            "full_lesson": "Use: multiple related motions (~5-10 minutes)",
            "deep_research": "Use: comprehensive collections (~hours)"
        }
    ]
    
    for criteria in selection_criteria:
        print(f"\n❓ {criteria['question']}")
        for key, value in criteria.items():
            if key != 'question':
                print(f"   📌 {key.replace('_', ' ').title()}: {value}")


def exploration_best_practices():
    """🎓 Best practices for dataset exploration"""
    print("\n🎓 EXPLORATION BEST PRACTICES")
    print("=" * 40)
    print("🔬 Systematic Approach:")
    print("   • Start with basic motions before advanced")
    print("   • Document what works and what doesn't")
    print("   • Test combinations systematically")
    print("   • Keep notes on motion characteristics")
    print("")
    print("⚖️ Quality Assessment:")
    print("   • Does the motion look natural?")
    print("   • Does the robot maintain balance?")
    print("   • Are there any glitches or artifacts?")
    print("   • How well does it match human motion?")
    print("")
    print("🎯 Practical Considerations:")
    print("   • Consider your robot's physical limits")
    print("   • Match motion complexity to your goals")
    print("   • Think about real-world applications")
    print("   • Plan for failure modes and edge cases")
    print("")
    print("🚀 Advanced Exploration:")
    print("   • Modify motion parameters")
    print("   • Blend different motion types")
    print("   • Create custom motion sequences")
    print("   • Analyze motion data scientifically")


def main():
    """🚀 Main lesson function"""
    print("🗺️ Lesson 1.7: Dataset Explorer")
    print("=" * 50)
    print("🎯 Goal: Become an expert motion dataset explorer")
    print("⏱️  Time: ~15 minutes")
    print("🎓 Difficulty: Intermediate")
    
    # Introduction and catalogs
    introduce_dataset_explorer()
    default_datasets = catalog_default_datasets()
    lafan1_categories = catalog_lafan1_datasets()
    
    # Search and filtering
    demonstrate_dataset_search()
    
    # Motion sampling tour
    demonstrate_motion_sampling()
    
    # Custom collections
    build_custom_collection()
    
    # Selection guidance
    dataset_selection_guide()
    exploration_best_practices()
    
    print(f"\n🎓 LESSON COMPLETE!")
    print("=" * 50)
    print("✅ You've learned:")
    print("   • Complete overview of all available datasets")
    print("   • How to search and filter motion data")
    print("   • Techniques for comparing motions")
    print("   • Building custom motion collections")
    print("")
    print("🚀 Ready for Lesson 1.8: Test Utilities")
    print("")
    print("🏆 EXPERIMENT IDEAS:")
    print("💡 Create your own collections:")
    print("   • Design a 'Robot Training Bootcamp' collection")
    print("   • Build a 'Motion Quality Test Suite'")
    print("   • Create themed collections (sports, dance, etc.)")
    print("💡 Advanced exploration:")
    print("   • Compare motion quality across all datasets")
    print("   • Find the most/least challenging motions")
    print("   • Analyze dataset coverage gaps")
    print("💡 Custom research projects:")
    print("   • Motion complexity classification system")
    print("   • Dataset recommendation engine")
    print("   • Motion quality scoring system")


if __name__ == "__main__":
    main()