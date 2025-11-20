#!/usr/bin/env python3
"""
🎬 Lesson 1.9: Slow Motion Viewer
=================================

GOAL: Study robot motion in slow motion for detailed analysis
WHY: Slow motion reveals details invisible at normal speed

WHAT YOU'LL LEARN:
✅ How to control simulation speed
✅ Frame-by-frame motion analysis
✅ Identifying motion problems and solutions
✅ Advanced visualization techniques

See every detail of robot motion - become a motion detective!
"""

import time
from loco_mujoco.task_factories import ImitationFactory, DefaultDatasetConf, LAFAN1DatasetConf


def explain_slow_motion_analysis():
    """🎬 Explain the value of slow motion analysis"""
    print("🎬 SLOW MOTION ANALYSIS FUNDAMENTALS")
    print("=" * 40)
    print("🎯 What is Slow Motion Analysis?")
    print("   • Deliberately slowing down robot motion for study")
    print("   • Frame-by-frame examination of movement")
    print("   • Detailed observation of motion characteristics")
    print("   • Scientific analysis of robot behavior")
    print("")
    print("🔍 Why Use Slow Motion?")
    print("   • Human eye can't catch fast motion details")
    print("   • Reveals subtle problems and inefficiencies")
    print("   • Helps understand motion mechanics")
    print("   • Makes learning more effective")
    print("")
    print("🎥 What Slow Motion Reveals:")
    print("   • Joint coordination patterns")
    print("   • Balance strategies and corrections")
    print("   • Impact and force distribution")
    print("   • Timing relationships between body parts")
    print("   • Transition phases in motion cycles")


def slow_motion_techniques():
    """⚙️ Different techniques for slow motion analysis"""
    print("\n⚙️ SLOW MOTION TECHNIQUES")
    print("=" * 40)
    
    techniques = [
        {
            "name": "Time Dilation",
            "description": "Slow down entire simulation time",
            "method": "Add delays between simulation steps",
            "best_for": "Overall motion pattern analysis",
            "pros": "Simple, maintains motion relationships",
            "cons": "Takes longer to analyze full sequences"
        },
        {
            "name": "Step-by-Step",
            "description": "Manual frame advancement",
            "method": "User controls when to advance frames",
            "best_for": "Detailed examination of specific moments",
            "pros": "Complete control, can focus on problems",
            "cons": "More complex interaction required"
        },
        {
            "name": "Speed Scaling",
            "description": "Variable playback speeds", 
            "method": "Dynamically adjust playback rate",
            "best_for": "Comparing different motion phases",
            "pros": "Flexible, can emphasize key moments",
            "cons": "Requires more sophisticated controls"
        },
        {
            "name": "Motion Isolation",
            "description": "Study individual joints/body parts",
            "method": "Highlight specific components",
            "best_for": "Understanding joint-level behavior",
            "pros": "Reduces visual complexity",
            "cons": "May miss system-level interactions"
        }
    ]
    
    for i, tech in enumerate(techniques, 1):
        print(f"\n{i}. {tech['name'].upper()}")
        print(f"   📝 Description: {tech['description']}")
        print(f"   🔧 Method: {tech['method']}")
        print(f"   🎯 Best for: {tech['best_for']}")
        print(f"   ✅ Pros: {tech['pros']}")
        print(f"   ❌ Cons: {tech['cons']}")


class SlowMotionViewer:
    """🎬 Slow motion viewing utility"""
    
    def __init__(self, env, base_delay=0.033):
        self.env = env
        self.base_delay = base_delay  # ~30 FPS
        self.speed_multipliers = {
            'ultra_slow': 10.0,    # 10x slower = ~3 FPS
            'very_slow': 5.0,      # 5x slower = ~6 FPS  
            'slow': 2.0,           # 2x slower = ~15 FPS
            'normal': 1.0,         # Normal speed = ~30 FPS
            'fast': 0.5,           # 2x faster = ~60 FPS
        }
        self.current_speed = 'normal'
        
    def set_speed(self, speed_name):
        """🎚️ Set playback speed"""
        if speed_name in self.speed_multipliers:
            self.current_speed = speed_name
            print(f"🎬 Speed set to: {speed_name} ({self.speed_multipliers[speed_name]:.1f}x)")
        else:
            print(f"❌ Unknown speed: {speed_name}")
            print(f"Available speeds: {list(self.speed_multipliers.keys())}")
    
    def get_current_delay(self):
        """⏱️ Get current frame delay"""
        return self.base_delay * self.speed_multipliers[self.current_speed]
    
    def play_with_analysis(self, n_steps=300, analysis_points=None):
        """🎬 Play motion with slow motion analysis"""
        print(f"\n🎬 SLOW MOTION PLAYBACK")
        print("=" * 40)
        print(f"🎚️ Current speed: {self.current_speed}")
        print(f"⏱️ Frame delay: {self.get_current_delay():.3f}s")
        print(f"📊 Total steps: {n_steps}")
        
        if analysis_points is None:
            analysis_points = [n_steps//4, n_steps//2, 3*n_steps//4]
        
        state, _ = self.env.reset()
        
        for step in range(n_steps):
            # Step simulation
            import numpy as np
            action = np.zeros(self.env.action_size)
            state, reward, terminated, truncated, info = self.env.step(action)
            self.env.render()
            
            # Analysis points
            if step in analysis_points:
                self.analyze_current_frame(step, state, reward)
                input("📋 Press Enter to continue...")
            
            # Handle termination
            if terminated or truncated:
                state, _ = self.env.reset()
                print(f"🔄 Episode reset at step {step}")
            
            # Apply slow motion delay
            time.sleep(self.get_current_delay())
        
        print(f"✅ Slow motion playback complete!")
    
    def analyze_current_frame(self, step, state, reward):
        """🔍 Analyze current frame in detail"""
        print(f"\n🔍 FRAME ANALYSIS - Step {step}")
        print("-" * 30)
        print(f"📊 Reward: {reward:.3f}")
        print(f"📏 State size: {len(state) if hasattr(state, '__len__') else 'unknown'}")
        
        # Basic state analysis
        if hasattr(state, '__len__') and len(state) > 0:
            import numpy as np
            state_array = np.array(state)
            print(f"📈 State range: {np.min(state_array):.3f} to {np.max(state_array):.3f}")
            print(f"📊 State magnitude: {np.mean(np.abs(state_array)):.3f}")
        
        # Motion phase detection (simplified)
        motion_phase = self.detect_motion_phase(step)
        print(f"🎭 Motion phase: {motion_phase}")
    
    def detect_motion_phase(self, step):
        """🎭 Simple motion phase detection"""
        cycle_length = 60  # Assume 60-step motion cycles
        phase_position = (step % cycle_length) / cycle_length
        
        if phase_position < 0.25:
            return "Preparation"
        elif phase_position < 0.5:
            return "Execution"
        elif phase_position < 0.75:
            return "Follow-through"
        else:
            return "Recovery"


def demonstrate_speed_comparison():
    """⚖️ Demonstrate different playback speeds"""
    print("\n⚖️ SPEED COMPARISON DEMONSTRATION")
    print("=" * 50)
    print("We'll show the same motion at different speeds.")
    print("Notice how different details become visible!")
    
    speeds_to_demo = ['normal', 'slow', 'very_slow']
    
    try:
        # Create environment with interesting motion
        env = ImitationFactory.make(
            "UnitreeG1",
            default_dataset_conf=DefaultDatasetConf(["walk"]),
            n_substeps=20
        )
        
        viewer = SlowMotionViewer(env)
        
        for i, speed in enumerate(speeds_to_demo, 1):
            print(f"\n{'='*60}")
            print(f"🎬 DEMO {i}/{len(speeds_to_demo)}: {speed.upper()} SPEED")
            print(f"{'='*60}")
            
            viewer.set_speed(speed)
            
            print(f"🎯 Watch carefully - observe:")
            if speed == 'normal':
                print("   • Overall motion flow and rhythm")
                print("   • General balance and coordination")
            elif speed == 'slow':
                print("   • Joint coordination details")
                print("   • Weight transfer patterns")
            elif speed == 'very_slow':
                print("   • Individual joint movements")
                print("   • Balance corrections and micro-adjustments")
            
            # Play short sequence
            viewer.play_with_analysis(n_steps=120, analysis_points=[])  # ~4 seconds at normal speed
            
            print(f"✅ {speed} speed demonstration complete!")
            time.sleep(2)
        
        del env
        
    except Exception as e:
        print(f"❌ Speed comparison failed: {e}")


def analyze_motion_details():
    """🔍 Detailed motion analysis techniques"""
    print("\n🔍 DETAILED MOTION ANALYSIS")
    print("=" * 40)
    print("🎯 What to Look For in Slow Motion:")
    
    analysis_aspects = [
        {
            "aspect": "Joint Coordination",
            "what_to_watch": "How joints move relative to each other",
            "good_signs": "Smooth, synchronized movement",
            "bad_signs": "Jerky, disconnected motions",
            "insights": "Reveals control algorithm quality"
        },
        {
            "aspect": "Balance Strategies",
            "what_to_watch": "How robot maintains upright posture",
            "good_signs": "Small, proactive adjustments",
            "bad_signs": "Large, reactive corrections",
            "insights": "Shows stability control effectiveness"
        },
        {
            "aspect": "Energy Efficiency",
            "what_to_watch": "Smoothness of motion trajectories",
            "good_signs": "Fluid, minimal wasted motion",
            "bad_signs": "Oscillations, overshooting",
            "insights": "Indicates optimization quality"
        },
        {
            "aspect": "Ground Contact",
            "what_to_watch": "Foot placement and impact patterns",
            "good_signs": "Controlled, stable contacts",
            "bad_signs": "Sliding, unstable landings",
            "insights": "Shows interaction dynamics"
        },
        {
            "aspect": "Motion Transitions",
            "what_to_watch": "Changes between motion phases",
            "good_signs": "Smooth, natural transitions",
            "bad_signs": "Abrupt, unnatural changes",
            "insights": "Reveals motion planning quality"
        }
    ]
    
    for i, aspect in enumerate(analysis_aspects, 1):
        print(f"\n{i}. {aspect['aspect'].upper()}")
        print(f"   👁️  What to watch: {aspect['what_to_watch']}")
        print(f"   ✅ Good signs: {aspect['good_signs']}")
        print(f"   ❌ Bad signs: {aspect['bad_signs']}")
        print(f"   💡 Insights: {aspect['insights']}")


def interactive_slow_motion_session():
    """🎮 Interactive slow motion analysis session"""
    print("\n🎮 INTERACTIVE SLOW MOTION SESSION")
    print("=" * 50)
    print("🎯 Now you control the slow motion analysis!")
    print("We'll load a complex motion and analyze it together.")
    
    try:
        # Load an interesting motion for analysis
        env = ImitationFactory.make(
            "UnitreeG1",
            lafan1_dataset_conf=LAFAN1DatasetConf(["dance2_subject4"]),
            n_substeps=20
        )
        
        viewer = SlowMotionViewer(env)
        
        print(f"\n✅ Dance motion loaded for analysis!")
        print("🎭 This is a complex, expressive motion with many details.")
        
        # Guided analysis session
        analysis_sessions = [
            {
                "name": "Overview Pass",
                "speed": "normal", 
                "focus": "Get familiar with the overall motion pattern",
                "duration": 150
            },
            {
                "name": "Coordination Analysis",
                "speed": "slow",
                "focus": "Watch how upper and lower body coordinate",
                "duration": 100
            },
            {
                "name": "Detail Examination", 
                "speed": "very_slow",
                "focus": "Examine individual joint movements and timing",
                "duration": 80
            }
        ]
        
        for i, session in enumerate(analysis_sessions, 1):
            print(f"\n{'='*60}")
            print(f"🔍 SESSION {i}/{len(analysis_sessions)}: {session['name']}")
            print(f"📋 Focus: {session['focus']}")
            print(f"🎚️ Speed: {session['speed']}")
            print(f"{'='*60}")
            
            viewer.set_speed(session['speed'])
            
            print(f"🎬 Starting analysis session...")
            viewer.play_with_analysis(
                n_steps=session['duration'],
                analysis_points=[session['duration']//3, 2*session['duration']//3]
            )
            
            print(f"✅ {session['name']} complete!")
            time.sleep(2)
        
        del env
        print(f"\n🎓 Interactive session complete!")
        
    except Exception as e:
        print(f"❌ Interactive session failed: {e}")
        print("💡 Try with a simpler motion if dance datasets aren't available")


def slow_motion_applications():
    """🚀 Applications of slow motion analysis"""
    print("\n🚀 SLOW MOTION APPLICATIONS")
    print("=" * 40)
    print("🎯 How Professionals Use Slow Motion:")
    
    applications = [
        {
            "field": "Robot Development",
            "uses": ["Debug control algorithms", "Optimize motion quality", "Validate safety systems"],
            "example": "Finding why robot falls during fast turns"
        },
        {
            "field": "Sports Science",
            "uses": ["Analyze athlete technique", "Prevent injuries", "Improve performance"],
            "example": "Studying running form to reduce impact stress"
        },
        {
            "field": "Animation/Entertainment", 
            "uses": ["Create realistic motion", "Perfect timing", "Study natural movement"],
            "example": "Making animated characters move more naturally"
        },
        {
            "field": "Medical Rehabilitation",
            "uses": ["Analyze patient movement", "Track progress", "Design therapy"],
            "example": "Studying walking patterns after injury"
        },
        {
            "field": "Research/Education",
            "uses": ["Understand biomechanics", "Teach motion principles", "Publish findings"],
            "example": "Teaching students how walking actually works"
        }
    ]
    
    for i, app in enumerate(applications, 1):
        print(f"\n{i}. {app['field'].upper()}")
        print(f"   🔧 Uses: {', '.join(app['uses'])}")
        print(f"   💡 Example: {app['example']}")


def slow_motion_best_practices():
    """📚 Best practices for slow motion analysis"""
    print("\n📚 SLOW MOTION ANALYSIS BEST PRACTICES")
    print("=" * 40)
    print("🎯 Effective Analysis Techniques:")
    print("   • Start with normal speed for context")
    print("   • Use progressive slowdown (normal → slow → very slow)")
    print("   • Focus on one aspect at a time")
    print("   • Take notes on observations")
    print("   • Compare multiple cycles/repetitions")
    print("")
    print("🔍 What to Document:")
    print("   • Timing of key events")
    print("   • Coordination patterns between joints")
    print("   • Problem areas and failure modes")
    print("   • Differences from expected behavior")
    print("   • Ideas for improvements")
    print("")
    print("⚠️ Common Pitfalls:")
    print("   • Getting lost in details - keep big picture")
    print("   • Analyzing too much at once")
    print("   • Not comparing with reference motions")
    print("   • Forgetting to document insights")
    print("")
    print("🚀 Advanced Techniques:")
    print("   • Side-by-side comparisons")
    print("   • Overlay multiple motion attempts")
    print("   • Quantitative measurement integration")
    print("   • Video recording for later review")


def main():
    """🚀 Main lesson function"""
    print("🎬 Lesson 1.9: Slow Motion Viewer")
    print("=" * 50)
    print("🎯 Goal: Master slow motion analysis for detailed motion study")
    print("⏱️  Time: ~15 minutes")
    print("🎓 Difficulty: Intermediate")
    
    # Theory and techniques
    explain_slow_motion_analysis()
    slow_motion_techniques()
    
    # Practical demonstrations
    demonstrate_speed_comparison()
    analyze_motion_details()
    
    # Interactive session
    interactive_slow_motion_session()
    
    # Applications and best practices
    slow_motion_applications()
    slow_motion_best_practices()
    
    print(f"\n🎓 LESSON COMPLETE!")
    print("=" * 50)
    print("✅ You've learned:")
    print("   • How to control simulation speed for analysis")
    print("   • Frame-by-frame motion examination techniques")
    print("   • What details to look for in slow motion")
    print("   • Professional applications of slow motion analysis")
    print("")
    print("🚀 Ready for Lesson 1.10: Complete Beginner Summary")
    print("")
    print("🏆 EXPERIMENT IDEAS:")
    print("💡 Motion comparison studies:")
    print("   • Compare human vs robot motion in slow motion")
    print("   • Analyze different walking speeds")
    print("   • Study balance recovery strategies")
    print("💡 Technical analysis:")
    print("   • Measure timing patterns in motions")
    print("   • Identify efficiency improvements")
    print("   • Document motion quality metrics")
    print("💡 Creative applications:")
    print("   • Create motion quality scoring system")
    print("   • Develop motion debugging toolkit")
    print("   • Design educational slow motion demos")


if __name__ == "__main__":
    main()