#!/usr/bin/env python3
"""
🕹️ Lesson 1.5: Interactive Control 
=================================

GOAL: Take direct control of the robot and learn how control works
WHY: Understanding control is key to robotics - you become the "brain"

WHAT YOU'LL LEARN:
✅ What robot control means
✅ Different types of robot control
✅ How to manually control joints
✅ Challenges of real-time control

Experience what it's like to BE the robot's control system!
"""

import numpy as np
from loco_mujoco.task_factories import RLFactory
import time
import os

# 🎨 Visual customization options
def set_background_color(color_name="black"):
    """🎨 Set MuJoCo background color"""
    colors = {
        "black": "0 0 0",
        "dark_blue": "0.1 0.1 0.2", 
        "dark_gray": "0.2 0.2 0.2",
        "white": "1 1 1",
        "default": "0.2 0.3 0.4"  # MuJoCo default-ish
    }
    
    bg_color = colors.get(color_name, colors["black"])
    os.environ['MUJOCO_GL_BACKGROUND'] = bg_color
    print(f"🎨 Background set to {color_name} ({bg_color})")


def get_action_size(env):
    """🔧 Get action size from environment in a robust way"""
    if hasattr(env, 'action_size'):
        return env.action_size
    elif hasattr(env, 'action_space') and hasattr(env.action_space, 'shape'):
        return env.action_space.shape[0]
    else:
        return 23  # Default for G1 robot


class InteractiveController:
    """🕹️ Simple interactive robot controller"""
    
    def __init__(self, env):
        self.env = env
        self.action_size = get_action_size(env)
        self.current_action = np.zeros(self.action_size)
        self.control_mode = "individual"  # individual, group, preset
        self.control_speed = 0.1  # How fast actions change
        
    def show_controls(self):
        """📋 Display available controls"""
        print("\n🕹️ INTERACTIVE CONTROLS")
        print("=" * 40)
        print("JOINT CONTROL:")
        print("  w/s - Joint 0 (up/down)")
        print("  a/d - Joint 1 (left/right)")
        print("  q/e - Joint 2 (rotate)")
        print("  r/f - Joint 3 (bend)")
        print("  t/g - Joint 4 (flex)")
        print("")
        print("MODES:")
        print("  1 - Individual joint mode")
        print("  2 - Upper body group") 
        print("  3 - Lower body group")
        print("  4 - Preset motions")
        print("")
        print("SPEED:")
        print("  + - Increase control speed")
        print("  - - Decrease control speed")
        print("")
        print("EXIT:")
        print("  x - Exit control mode")
        print("  h - Show this help again")
        
    def update_action(self, key):
        """🎮 Update robot action based on key press"""
        speed = self.control_speed
        
        # Individual joint control
        if key == 'w':
            self.current_action[0] = min(1.0, self.current_action[0] + speed)
            return True
        elif key == 's':
            self.current_action[0] = max(-1.0, self.current_action[0] - speed)
            return True
        elif key == 'a':
            self.current_action[1] = min(1.0, self.current_action[1] + speed)
            return True
        elif key == 'd':
            self.current_action[1] = max(-1.0, self.current_action[1] - speed)
            return True
        elif key == 'q':
            self.current_action[2] = min(1.0, self.current_action[2] + speed)
            return True
        elif key == 'e':
            self.current_action[2] = max(-1.0, self.current_action[2] - speed)
            return True
        elif key == 'r':
            if len(self.current_action) > 3:
                self.current_action[3] = min(1.0, self.current_action[3] + speed)
                return True
        elif key == 'f':
            if len(self.current_action) > 3:
                self.current_action[3] = max(-1.0, self.current_action[3] - speed)
                return True
        elif key == 't':
            if len(self.current_action) > 4:
                self.current_action[4] = min(1.0, self.current_action[4] + speed)
                return True
        elif key == 'g':
            if len(self.current_action) > 4:
                self.current_action[4] = max(-1.0, self.current_action[4] - speed)
                return True
                
        # Speed control
        elif key == '+':
            self.control_speed = min(0.5, self.control_speed + 0.02)
            print(f"🎚️ Control speed: {self.control_speed:.2f}")
            return True
        elif key == '-':
            self.control_speed = max(0.01, self.control_speed - 0.02)
            print(f"🎚️ Control speed: {self.control_speed:.2f}")
            return True
            
        # Reset
        elif key == '0':
            self.current_action = np.zeros_like(self.current_action)
            print("🔄 Actions reset to zero")
            return True
            
        # Help
        elif key == 'h':
            self.show_controls()
            return True
            
        return False  # Unknown command


def explain_robot_control():
    """🧠 Explain the concepts of robot control"""
    print("🧠 UNDERSTANDING ROBOT CONTROL")
    print("=" * 40)
    print("🤖 What is Robot Control?")
    print("   Control = telling the robot's joints what to do")
    print("   Every fraction of a second, we send commands")
    print("   Robot receives commands → moves joints → creates motion")
    print("")
    print("🔗 The Control Chain:")
    print("   1. BRAIN (You/AI) - decides what to do")
    print("   2. CONTROLLER - translates decisions to commands")  
    print("   3. ACTUATORS - motors that move joints")
    print("   4. SENSORS - tell us what happened")
    print("   5. FEEDBACK - adjust for next time")
    print("")
    print("⚡ Types of Control:")
    print("   • POSITION: Move joint to exact angle")
    print("   • VELOCITY: Move joint at certain speed")  
    print("   • TORQUE: Apply specific force to joint")
    print("   • IMPEDANCE: Balance position and compliance")


def explain_control_challenges():
    """⚠️ Explain why robot control is challenging"""
    print("\n⚠️ WHY CONTROL IS CHALLENGING")
    print("=" * 40)
    print("🎯 Real-time Constraints:")
    print("   • Must make decisions quickly (30-1000 Hz)")
    print("   • No time to 'think' - immediate responses needed")
    print("   • Miss a deadline = robot falls or fails")
    print("")
    print("🤹 Coordination Challenge:")
    print("   • G1 robot has 23 joints to coordinate")
    print("   • All joints affect each other")
    print("   • Moving arm changes balance for legs")
    print("   • Like playing 23-key piano... with physics!")
    print("")
    print("⚖️ Balance and Dynamics:")
    print("   • Robot must fight gravity constantly")
    print("   • Every action has reaction forces")
    print("   • Ground contact creates complex forces")
    print("   • Balance is dynamic, not static")
    print("")
    print("🎛️ Precision vs Compliance:")
    print("   • Too stiff = robot breaks or falls")
    print("   • Too loose = robot can't control motion")
    print("   • Must adapt to different situations")
    print("   • Human-like flexibility is very hard")


def demonstrate_control_types():
    """🎮 Demonstrate different control approaches"""
    print("\n🎮 CONTROL TYPE DEMONSTRATIONS")
    print("=" * 40)
    
    control_types = [
        {
            "name": "Individual Joint Control",
            "description": "Control each joint separately",
            "pros": "Precise, predictable",
            "cons": "Hard to coordinate, unnatural"
        },
        {
            "name": "Coordinated Motion",
            "description": "Multiple joints work together",
            "pros": "More natural, better coordination", 
            "cons": "Complex to program, harder to debug"
        },
        {
            "name": "Oscillatory Control",
            "description": "Rhythmic, repeating patterns",
            "pros": "Good for locomotion, stable",
            "cons": "Limited behaviors, robotic"
        }
    ]
    
    # Show conceptual demonstration using imitation data
    try:
        from loco_mujoco.task_factories import ImitationFactory, DefaultDatasetConf
        
        print("🎬 VISUAL CONTROL DEMONSTRATIONS")
        print("We'll show how different control approaches look:")
        
        # Use walking data to show coordinated control
        env = ImitationFactory.make(
            "UnitreeG1",
            default_dataset_conf=DefaultDatasetConf(["walk"]),
            n_substeps=20
        )
        
        for i, ctrl_type in enumerate(control_types, 1):
            print(f"\n{i}. {ctrl_type['name'].upper()}")
            print(f"   📝 {ctrl_type['description']}")
            print(f"   ✅ Pros: {ctrl_type['pros']}")
            print(f"   ❌ Cons: {ctrl_type['cons']}")
            print(f"   🎬 Showing example motion...")
            
            # Play short demonstration
            env.play_trajectory(
                n_episodes=1,
                n_steps_per_episode=90,  # ~3 seconds
                render=True
            )
            
            print(f"   ✅ {ctrl_type['name']} example complete!")
            time.sleep(1)
            
        del env
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        print("💡 Concepts explained - visual demo not available")


def interactive_control_session():
    """🕹️ Run interactive control session"""
    print("\n🕹️ INTERACTIVE CONTROL SESSION")
    print("=" * 40)
    print("🎯 Now YOU control the robot with keyboard!")
    print("This gives you real-time control - the robot responds to your inputs!")
    
    try:
        env = RLFactory.make("UnitreeG1", n_substeps=20)
        controller = InteractiveController(env)
        action_size = get_action_size(env)
        
        print(f"\n✅ Robot loaded! Action size: {action_size}")
        controller.show_controls()
        
        # Handle different reset return formats
        reset_result = env.reset()
        if isinstance(reset_result, tuple):
            state = reset_result[0]
        else:
            state = reset_result
        
        print(f"\n🎮 KEYBOARD CONTROL ACTIVE!")
        print("Type commands and press Enter:")
        print("- 'w'/'s' = Joint 0 up/down")
        print("- 'a'/'d' = Joint 1 left/right") 
        print("- 'q'/'e' = Joint 2 rotate")
        print("- '0' = Reset all to zero")
        print("- 'help' = Show controls again")
        print("- 'quit' = Exit")
        print(f"Current actions: {controller.current_action[:5]}")
        
        step_count = 0
        max_steps = 50000  # Very high limit so you can control as long as you want
        
        while step_count < max_steps:
            try:
                # Get user input
                user_input = input(f"\nStep {step_count} > ").strip().lower()
                
                # Handle commands
                if user_input in ['quit', 'exit', 'q']:
                    print("🛑 Exiting control session...")
                    break
                elif user_input == 'help' or user_input == 'h':
                    controller.show_controls()
                    continue
                elif user_input == '0' or user_input == 'reset':
                    controller.current_action = np.zeros(controller.action_size)
                    print(f"🔄 Reset! Actions: {controller.current_action[:5]}")
                elif user_input in ['w', 's', 'a', 'd', 'q', 'e', 'r', 'f', 't', 'g', '+', '-']:
                    # Update action based on key
                    controller.update_action(user_input)
                    print(f"� Updated! Actions: {controller.current_action[:5]}")
                elif user_input == '':
                    # Just step with current action
                    pass
                else:
                    print("❓ Unknown command. Type 'help' for controls or 'quit' to exit")
                    continue
                
                # Apply action and step simulation for 30 frames (~1 second)
                for i in range(30):
                    state, reward, terminated, truncated, info = env.step(controller.current_action)
                    env.render()
                    
                    if terminated or truncated:
                        reset_result = env.reset()
                        if isinstance(reset_result, tuple):
                            state = reset_result[0]
                        else:
                            state = reset_result
                        if i == 0:  # Only print if reset immediately
                            print("🔄 Robot reset!")
                        break
                    
                    time.sleep(0.033)  # ~30 FPS
                    step_count += 1
                
                # Show status
                if step_count % 300 == 0:  # Every ~10 seconds
                    print(f"📊 Status: {step_count} steps, Reward: {reward:.3f}")
                    
            except (EOFError, KeyboardInterrupt):
                print("\n🛑 Control interrupted by user")
                break
            except Exception as e:
                print(f"⚠️ Error: {e} - continuing...")
        
        print(f"\n🎮 INTERACTIVE SESSION COMPLETE!")
        print(f"Total steps controlled: {step_count}")
        print("Thanks for trying robot control!")
        del env
        
    except Exception as e:
        print(f"❌ Interactive control failed: {e}")
        print("💡 The robot control concepts are still valid!")


def control_insights():
    """💡 Share insights about robot control"""
    print("\n💡 CONTROL INSIGHTS")
    print("=" * 40)
    print("🧠 What You Just Experienced:")
    print("   • How small actions create big movements")
    print("   • Why coordination between joints matters")  
    print("   • How hard it is to maintain balance")
    print("   • The challenge of real-time decision making")
    print("")
    print("🎯 Key Takeaways:")
    print("   • Control is the 'brain' of robotics")
    print("   • Small changes can have big effects")
    print("   • Coordination is harder than individual control")
    print("   • Real-time performance is critical")
    print("")
    print("🚀 Advanced Control Concepts:")
    print("   • MODEL PREDICTIVE CONTROL: Plan ahead")
    print("   • REINFORCEMENT LEARNING: Learn by trial")
    print("   • ADAPTIVE CONTROL: Adjust to changes")
    print("   • ROBUST CONTROL: Handle uncertainties")
    print("")
    print("🔮 The Future:")
    print("   • AI will make robots smarter controllers")
    print("   • Better sensors will improve feedback")
    print("   • New materials will enable better actuation")
    print("   • Brain-computer interfaces may allow direct control")


def main():
    """🚀 Main lesson function"""
    print("🕹️ Lesson 1.5: Interactive Control")
    print("=" * 50)
    print("🎯 Goal: Learn robot control by taking direct control")
    print("⏱️  Time: ~12 minutes")
    print("🎓 Difficulty: Intermediate")
    
    # 🎨 Visual customization
    print("\n🎨 Setting up visual environment...")
    set_background_color("black")  # Cool black background for better focus
    
    # Theory
    explain_robot_control()
    explain_control_challenges()
    
    # Demonstrations
    demonstrate_control_types()
    
    # Interactive experience
    interactive_control_session()
    
    # Analysis and insights
    control_insights()
    
    print(f"\n🎓 LESSON COMPLETE!")
    print("=" * 50)
    print("✅ You've learned:")
    print("   • What robot control means")
    print("   • Different types of control approaches")
    print("   • Why coordination is challenging")
    print("   • How real-time constraints affect robots")
    print("")
    print("🚀 Ready for Lesson 1.6: Motion Analysis")
    print("")
    print("🏆 EXPERIMENT IDEAS:")
    print("💡 Try different control strategies:")
    print("   • Pure position control vs mixed control")
    print("   • Fast vs slow control updates")
    print("   • Single joint vs coordinated motion")
    print("💡 Analyze control stability:")
    print("   • Which actions lead to falling?")
    print("   • How does speed affect stability?")
    print("   • What makes 'good' vs 'bad' control?")
    print("💡 Advanced experiments:")
    print("   • Compare human vs robot control capabilities")
    print("   • Design a simple walking controller")
    print("   • Test control under different conditions")


if __name__ == "__main__":
    main()