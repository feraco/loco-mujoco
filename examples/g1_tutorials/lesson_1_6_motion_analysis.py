#!/usr/bin/env python3
"""
📊 Lesson 1.6: Motion Analysis
=============================

GOAL: Learn to analyze and understand robot motion scientifically  
WHY: Motion analysis helps us improve robots and understand movement

WHAT YOU'LL LEARN:
✅ How to measure and analyze motion
✅ Key metrics for evaluating robot performance
✅ Visualization techniques for understanding data
✅ Scientific approach to motion evaluation

Become a motion scientist - analyze how robots really move!
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from loco_mujoco.task_factories import RLFactory, ImitationFactory, DefaultDatasetConf
import time
import threading
from collections import deque


def get_action_size(env):
    """🔧 Get action size from environment in a robust way"""
    if hasattr(env, 'action_size'):
        return env.action_size
    elif hasattr(env, 'action_space') and hasattr(env.action_space, 'shape'):
        return env.action_space.shape[0]
    else:
        return 23  # Default for G1 robot


def explain_motion_analysis():
    """📊 Introduce the science of motion analysis"""
    print("📊 MOTION ANALYSIS FUNDAMENTALS")
    print("=" * 40)
    print("🔬 What is Motion Analysis?")
    print("   • Scientific study of how things move")
    print("   • Measuring motion with numbers and data")
    print("   • Finding patterns and problems in movement")
    print("   • Using data to improve performance")
    print("")
    print("🎯 Why Analyze Robot Motion?")
    print("   • Understand what the robot is actually doing")
    print("   • Find problems before they cause failures")
    print("   • Optimize motion for efficiency or speed")
    print("   • Compare different control strategies")
    print("   • Validate that robots match human motion")
    print("")
    print("📏 Key Motion Metrics:")
    print("   • POSITION: Where is the robot/joint?")
    print("   • VELOCITY: How fast is it moving?")
    print("   • ACCELERATION: How quickly is speed changing?")
    print("   • FORCES: What forces are being applied?")
    print("   • STABILITY: How well does it maintain balance?")
    print("   • EFFICIENCY: How much energy is being used?")


def motion_metrics_explained():
    """📐 Detailed explanation of motion metrics"""
    print("\n📐 MOTION METRICS DEEP DIVE")
    print("=" * 40)
    
    metrics = [
        {
            "name": "Position Tracking",
            "description": "Where each joint/body part is in space",
            "units": "meters, radians (for joints)",
            "why_important": "Ensures robot follows desired path",
            "normal_range": "Depends on task and robot limits"
        },
        {
            "name": "Velocity Profile", 
            "description": "How fast each part is moving",
            "units": "meters/second, radians/second",
            "why_important": "Smooth motion, energy efficiency",
            "normal_range": "Walking: 0.1-2 m/s, Running: 2-6 m/s"
        },
        {
            "name": "Acceleration",
            "description": "How quickly velocity changes",
            "units": "meters/second², radians/second²", 
            "why_important": "Comfort, stability, motor limits",
            "normal_range": "Human-like: < 3 m/s² for walking"
        },
        {
            "name": "Ground Forces",
            "description": "Forces between feet and ground",
            "units": "Newtons (N)",
            "why_important": "Balance, efficiency, impact safety",
            "normal_range": "Walking: 0.8-1.2x body weight"
        },
        {
            "name": "Center of Mass",
            "description": "Balance point of entire robot",
            "units": "meters from reference point",
            "why_important": "Stability, falling prevention",
            "normal_range": "Must stay over support polygon"
        }
    ]
    
    for metric in metrics:
        print(f"\n📊 {metric['name'].upper()}")
        print(f"   📝 What: {metric['description']}")
        print(f"   📏 Units: {metric['units']}")
        print(f"   🎯 Why Important: {metric['why_important']}")
        print(f"   ✅ Normal Range: {metric['normal_range']}")


def collect_live_motion_data(env, motion_name, n_steps=300):
    """🎬 Collect live motion data with real-time visualization"""
    print(f"\n🎬 LIVE MOTION ANALYSIS: {motion_name}")
    print("=" * 40)
    print("📊 Collecting real-time motion data...")
    print("📈 Watch the graphs update as the robot moves!")
    
    # Data storage for live plotting
    joint_positions = deque(maxlen=n_steps)
    joint_velocities = deque(maxlen=n_steps) 
    center_of_mass = deque(maxlen=n_steps)
    energy_metrics = deque(maxlen=n_steps)
    time_steps = deque(maxlen=n_steps)
    
    # Setup live plotting
    plt.ion()  # Interactive mode
    fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(12, 8))
    fig.suptitle(f'Live Motion Analysis: {motion_name}', fontsize=14)
    
    # Initialize plots
    line1, = ax1.plot([], [], 'b-', label='Hip Joint')
    line2, = ax1.plot([], [], 'r-', label='Knee Joint')
    ax1.set_title('Joint Positions (rad)')
    ax1.set_ylabel('Position')
    ax1.legend()
    ax1.grid(True)
    
    line3, = ax2.plot([], [], 'g-', label='Velocity')
    ax2.set_title('Joint Velocities (rad/s)')
    ax2.set_ylabel('Velocity') 
    ax2.grid(True)
    
    line4, = ax3.plot([], [], 'm-', label='CoM Height')
    ax3.set_title('Center of Mass Movement')
    ax3.set_ylabel('Height (m)')
    ax3.set_xlabel('Time (s)')
    ax3.grid(True)
    
    line5, = ax4.plot([], [], 'c-', label='Motion Energy')
    ax4.set_title('Movement Energy')
    ax4.set_ylabel('Energy')
    ax4.set_xlabel('Time (s)')
    ax4.grid(True)
    
    try:
        # Reset environment
        reset_result = env.reset()
        if isinstance(reset_result, tuple):
            state = reset_result[0]
        else:
            state = reset_result
        
        print("🎯 Starting live data collection...")
        
        for step in range(n_steps):
            # Get current observation
            obs = state
            
            # Let the trajectory play naturally (no action needed for imitation)
            action_size = get_action_size(env)
            action = np.zeros(action_size)  # Let imitation environment handle motion
            
            # Step the environment
            step_result = env.step(action)
            if len(step_result) == 5:
                state, reward, terminated, truncated, info = step_result
            elif len(step_result) == 4:
                state, reward, terminated, info = step_result
                truncated = False
            else:
                state, reward, terminated = step_result[:3]
                truncated = False
                info = {}
            
            # Extract meaningful data from observations
            current_time = step * 0.033  # ~30 FPS
            time_steps.append(current_time)
            
            # Joint positions (first few joints)
            if len(obs) >= 6:
                hip_pos = obs[0] if len(obs) > 0 else 0
                knee_pos = obs[3] if len(obs) > 3 else 0
                joint_positions.append([hip_pos, knee_pos])
            else:
                joint_positions.append([0, 0])
            
            # Joint velocities (estimate from position changes)
            if len(obs) >= 12:
                vel1 = obs[6] if len(obs) > 6 else 0
                vel2 = obs[9] if len(obs) > 9 else 0
                avg_vel = np.mean([abs(vel1), abs(vel2)])
                joint_velocities.append(avg_vel)
            else:
                joint_velocities.append(0)
            
            # Center of mass approximation (from root position if available)
            if len(obs) >= 3:
                com_height = obs[2] if len(obs) > 2 else 0  # Z position usually
                center_of_mass.append(com_height)
            else:
                center_of_mass.append(0)
            
            # Energy metric (velocity squared approximation)
            if len(joint_velocities) > 0:
                energy = joint_velocities[-1] ** 2
                energy_metrics.append(energy)
            else:
                energy_metrics.append(0)
            
            # Update plots every 10 steps for performance
            if step % 10 == 0 and len(time_steps) > 1:
                time_array = list(time_steps)
                
                # Update joint positions
                if len(joint_positions) > 0:
                    joint_array = list(joint_positions)
                    hip_data = [jp[0] for jp in joint_array]
                    knee_data = [jp[1] for jp in joint_array]
                    
                    line1.set_data(time_array, hip_data)
                    line2.set_data(time_array, knee_data)
                    ax1.relim()
                    ax1.autoscale_view()
                
                # Update velocities
                line3.set_data(time_array, list(joint_velocities))
                ax2.relim()
                ax2.autoscale_view()
                
                # Update center of mass
                line4.set_data(time_array, list(center_of_mass))
                ax3.relim()
                ax3.autoscale_view()
                
                # Update energy
                line5.set_data(time_array, list(energy_metrics))
                ax4.relim()
                ax4.autoscale_view()
                
                plt.pause(0.01)  # Small pause for plot update
            
            # Render the simulation
            env.render()
            
            if terminated or truncated:
                print("🔄 Episode ended, resetting...")
                reset_result = env.reset()
                if isinstance(reset_result, tuple):
                    state = reset_result[0]
                else:
                    state = reset_result
            
            # Small delay to control playback speed
            time.sleep(0.02)
        
        print("✅ Live data collection complete!")
        print("📊 Final plot shows complete motion analysis")
        
        # Calculate summary statistics
        if len(joint_positions) > 0:
            joint_array = list(joint_positions)
            position_range = np.max([jp[0] for jp in joint_array]) - np.min([jp[0] for jp in joint_array])
            avg_velocity = np.mean(list(joint_velocities))
            max_energy = np.max(list(energy_metrics))
            
            print(f"\n📈 MOTION SUMMARY:")
            print(f"   🎯 Joint Range of Motion: {position_range:.3f} radians")
            print(f"   ⚡ Average Velocity: {avg_velocity:.3f} rad/s")
            print(f"   🔋 Peak Energy: {max_energy:.3f}")
            print(f"   📊 Data Points Collected: {len(joint_positions)}")
        
        # Keep the final plot open for a moment
        plt.ioff()
        plt.show(block=False)
        time.sleep(3)  # Show final results for 3 seconds
        plt.close(fig)
        
        # Create comprehensive dataset
        data = {
            'joint_positions': np.array(list(joint_positions)),
            'joint_velocities': np.array(list(joint_velocities)),
            'center_of_mass': np.array(list(center_of_mass)),
            'energy_metrics': np.array(list(energy_metrics)),
            'time_steps': np.array(list(time_steps)),
            'motion_name': motion_name,
            'summary': {
                'position_range': position_range if len(joint_positions) > 0 else 0,
                'avg_velocity': avg_velocity if len(joint_velocities) > 0 else 0,
                'max_energy': max_energy if len(energy_metrics) > 0 else 0
            }
        }
        
        print(f"✅ Live analysis data collected for {motion_name}")
        return data
        
    except Exception as e:
        print(f"❌ Live data collection failed: {e}")
        plt.close('all')  # Clean up plots on error
        return None


def collect_motion_data(env, motion_name, n_steps=300):
    """📈 Collect motion data for analysis"""
    print(f"\n📈 COLLECTING MOTION DATA: {motion_name}")
    print("=" * 50)
    
    # Data storage
    positions = []
    velocities = []
    actions = []
    rewards = []
    com_positions = []
    
    try:
        # Robust environment reset handling
        reset_result = env.reset()
        if isinstance(reset_result, tuple):
            state = reset_result[0]
        else:
            state = reset_result
            
        print(f"📊 Recording {n_steps} steps (~10 seconds)...")
        print("🎬 Watch the motion while we collect data!")
        
        for step in range(n_steps):
            # Get current state information
            obs = state
            
            # Simple walking action (if no dataset)
            action_size = get_action_size(env)
            if hasattr(env, 'play_trajectory'):
                # For imitation environments, let trajectory play
                action = np.zeros(action_size)
            else:
                # Simple oscillating walking pattern for RL environments
                t = step * 0.033
                action = np.array([
                    0.3 * np.sin(2 * t),       # Hip motion
                    0.2 * np.cos(2 * t + 0.5), # Leg coordination
                    0.1 * np.sin(3 * t),       # Arm swing
                    0.15 * np.cos(1.5 * t),    # Knee bend
                    0.1 * np.sin(2.5 * t + 1)  # Balance
                ])[:action_size]
            
            # Robust step execution - handle different return tuple sizes
            step_result = env.step(action)
            if len(step_result) == 5:
                state, reward, terminated, truncated, info = step_result
            elif len(step_result) == 4:
                state, reward, terminated, info = step_result
                truncated = False
            else:
                state, reward, terminated = step_result[:3]
                truncated = False
                info = {}
            
            env.render()
            
            # Store data
            positions.append(obs[:10] if len(obs) >= 10 else obs)  # First 10 obs (usually joint positions)
            velocities.append(obs[10:20] if len(obs) >= 20 else np.zeros(10))  # Next 10 (usually velocities)
            actions.append(action.copy())
            rewards.append(reward)
            
            # Calculate center of mass (simplified)
            try:
                # This would need proper calculation from robot model
                com_pos = np.mean(obs[:3]) if len(obs) >= 3 else 0
                com_positions.append(com_pos)
            except:
                com_positions.append(0)
            
            if terminated or truncated:
                print("🔄 Episode ended, resetting...")
                reset_result = env.reset()
                if isinstance(reset_result, tuple):
                    state = reset_result[0]
                else:
                    state = reset_result
            
            time.sleep(0.02)  # Small delay for visualization
        
        print("✅ Data collection complete!")
        
        # Convert to numpy arrays for analysis
        data = {
            'positions': np.array(positions),
            'velocities': np.array(velocities), 
            'actions': np.array(actions),
            'rewards': np.array(rewards),
            'com_positions': np.array(com_positions),
            'time': np.arange(n_steps) * 0.033  # Assuming 30 FPS
        }
        
        return data
        
    except Exception as e:
        print(f"❌ Data collection failed: {e}")
        return None


def analyze_motion_data(data, motion_name):
    """🔍 Analyze the collected motion data"""
    if data is None:
        print("❌ No data to analyze")
        return
        
    print(f"\n🔍 LIVE MOTION ANALYSIS RESULTS: {motion_name}")
    print("=" * 50)
    
    # Handle both detailed and simplified data
    if 'time' in data:
        # Detailed analysis
        print("📊 DETAILED STATISTICS:")
        print(f"   ⏱️  Duration: {data['time'][-1]:.1f} seconds")
        print(f"   📈 Samples: {len(data['time'])}")
        print(f"   🎯 Average reward: {np.mean(data['rewards']):.3f}")
        print(f"   📊 Reward range: {np.min(data['rewards']):.3f} to {np.max(data['rewards']):.3f}")
        
        # Additional detailed analysis would go here
        if 'positions' in data and data['positions'].size > 0:
            pos_data = data['positions']
            print(f"\n📍 POSITION ANALYSIS:")
            print(f"   📏 Position dimensions: {pos_data.shape}")
            print(f"   📊 Position range: {np.min(pos_data):.3f} to {np.max(pos_data):.3f}")
    
    
    # Analyze live motion data
    if 'summary' in data:
        summary = data['summary']
        print("📊 REAL-TIME MOTION ANALYSIS:")
        print(f"   🎯 Joint Range of Motion: {summary['position_range']:.3f} radians")
        print(f"   ⚡ Average Joint Velocity: {summary['avg_velocity']:.3f} rad/s")
        print(f"   � Peak Movement Energy: {summary['max_energy']:.3f}")
        print(f"   📈 Data Points Collected: {len(data['time_steps'])}")
        
        # Motion quality assessment
        if summary['position_range'] > 0.5:
            print("   ✅ High range of motion - dynamic movement")
        elif summary['position_range'] > 0.2:
            print("   📊 Moderate range of motion - normal movement")
        else:
            print("   ⚠️  Limited range of motion - restricted movement")
            
        if summary['avg_velocity'] > 1.0:
            print("   🚀 High velocity movement - energetic")
        elif summary['avg_velocity'] > 0.3:
            print("   🎯 Moderate velocity - controlled movement")
        else:
            print("   🐢 Low velocity - slow/careful movement")
            
        if summary['max_energy'] > 2.0:
            print("   🔥 High energy motion - explosive movements")
        elif summary['max_energy'] > 0.5:
            print("   ⚡ Moderate energy - balanced motion")
        else:
            print("   🌊 Low energy - smooth, gentle motion")
    else:
        print("📊 LIVE DATA ANALYSIS:")
        print("   ❌ Summary data not available - check data collection")


def visualize_motion_data(data, motion_name):
    """📊 Create visualizations of motion data"""
    if data is None:
        print("❌ No data to visualize")
        return
        
    print(f"\n📊 CREATING MOTION VISUALIZATIONS: {motion_name}")
    print("=" * 50)
    
    try:
        # Create figure with subplots
        fig, axes = plt.subplots(2, 2, figsize=(12, 8))
        fig.suptitle(f'Motion Analysis: {motion_name}', fontsize=16)
        
        # 1. Reward over time
        axes[0,0].plot(data['time'], data['rewards'])
        axes[0,0].set_title('Reward Over Time')
        axes[0,0].set_xlabel('Time (s)')
        axes[0,0].set_ylabel('Reward')
        axes[0,0].grid(True)
        
        # 2. Position trajectories (first few joints)
        pos_data = data['positions']
        if pos_data.size > 0:
            n_joints = min(5, pos_data.shape[1])  # Show first 5 joints
            for i in range(n_joints):
                axes[0,1].plot(data['time'], pos_data[:, i], label=f'Joint {i}')
            axes[0,1].set_title('Joint Positions')
            axes[0,1].set_xlabel('Time (s)')
            axes[0,1].set_ylabel('Position (rad)')
            axes[0,1].legend()
            axes[0,1].grid(True)
        
        # 3. Velocity profiles
        vel_data = data['velocities']
        if vel_data.size > 0:
            vel_magnitude = np.sqrt(np.sum(vel_data**2, axis=1))
            axes[1,0].plot(data['time'], vel_magnitude)
            axes[1,0].set_title('Velocity Magnitude')
            axes[1,0].set_xlabel('Time (s)')
            axes[1,0].set_ylabel('Velocity (rad/s)')
            axes[1,0].grid(True)
        
        # 4. Action patterns
        action_data = data['actions']
        if action_data.size > 0:
            n_actions = min(5, action_data.shape[1])  # Show first 5 actions
            for i in range(n_actions):
                axes[1,1].plot(data['time'], action_data[:, i], label=f'Action {i}')
            axes[1,1].set_title('Control Actions')
            axes[1,1].set_xlabel('Time (s)')
            axes[1,1].set_ylabel('Action Value')
            axes[1,1].legend()
            axes[1,1].grid(True)
        
        plt.tight_layout()
        
        # Save the plot
        plot_filename = f'motion_analysis_{motion_name.lower().replace(" ", "_")}.png'
        plt.savefig(plot_filename, dpi=150, bbox_inches='tight')
        print(f"📊 Visualization saved as: {plot_filename}")
        
        # Show plot
        plt.show(block=False)
        plt.pause(3)  # Display for 3 seconds
        plt.close()
        
        print("✅ Visualization complete!")
        
    except Exception as e:
        print(f"❌ Visualization failed: {e}")
        print("💡 This may be due to display/plotting library issues")


def motion_comparison_demo():
    """⚖️ Compare different types of motion"""
    print("\n⚖️ MOTION COMPARISON STUDY")
    print("=" * 50)
    print("We'll analyze and compare different motion types!")
    
    motion_tests = [
        {
            "name": "Basic Walking Motion",
            "type": "Imitation",
            "dataset": DefaultDatasetConf(["walk"]),
            "description": "Human-recorded walking motion data"
        },
        {
            "name": "Running Motion", 
            "type": "Imitation",
            "dataset": DefaultDatasetConf(["run"]),
            "description": "Fast running motion with dynamics"
        }
    ]
    
    motion_data_collection = {}
    
    for test in motion_tests:
        print(f"\n{'='*60}")
        print(f"🎬 ANALYZING: {test['name']}")
        print(f"📝 Type: {test['type']}")
        print(f"📋 Description: {test['description']}")
        print(f"{'='*60}")
        
        try:
            # Create environment with dataset
            env = ImitationFactory.make(
                "UnitreeG1",
                default_dataset_conf=test['dataset'],
                n_substeps=20
            )
            
            print(f"✅ Environment loaded for {test['name']}")
            print(f"🎬 Playing motion for analysis (10 seconds)...")
            
            # Play the motion for visual analysis
            env.play_trajectory(
                n_episodes=1,
                n_steps_per_episode=300,  # ~10 seconds
                render=True
            )
            
            # Collect live motion data with real-time visualization
            try:
                data = collect_live_motion_data(env, test['name'], n_steps=200)
                
                if data is not None:
                    analyze_motion_data(data, test['name'])
                    motion_data_collection[test['name']] = data
            except Exception as e:
                print(f"❌ Data collection failed: {e}")
                data = None
            
            del env
            
        except Exception as e:
            print(f"❌ Failed to test {test['name']}: {e}")
        
        time.sleep(2)  # Pause between tests
    
    # Compare results if we have multiple datasets
    if len(motion_data_collection) > 1:
        print(f"\n📊 COMPARATIVE ANALYSIS")
        print("=" * 50)
        
        for name, data in motion_data_collection.items():
            print(f"\n{name}:")
            
            # Show live motion analysis summary
            if 'summary' in data:
                summary = data['summary']
                print(f"   � Joint Range: {summary['position_range']:.3f} rad")
                print(f"   ⚡ Avg Velocity: {summary['avg_velocity']:.3f} rad/s")
                print(f"   🔋 Peak Energy: {summary['max_energy']:.3f}")
            else:
                print(f"   📊 [Live data not available]")


def analysis_best_practices():
    """📚 Share best practices for motion analysis"""
    print("\n📚 MOTION ANALYSIS BEST PRACTICES")
    print("=" * 50)
    print("🔬 Scientific Approach:")
    print("   • Always record what you're measuring")
    print("   • Use consistent time periods for comparison")
    print("   • Consider multiple trials to check repeatability")
    print("   • Document environmental conditions")
    print("")
    print("📊 Data Quality:")
    print("   • Check for sensor noise or glitches")
    print("   • Ensure sufficient sampling rate (>30 Hz)")
    print("   • Validate data ranges make physical sense")
    print("   • Look for unexpected patterns or anomalies")
    print("")
    print("📈 Analysis Techniques:")
    print("   • Use appropriate statistical measures")
    print("   • Consider both time and frequency domain")
    print("   • Compare against known baselines")
    print("   • Visualize data to spot patterns")
    print("")
    print("🎯 Key Questions to Ask:")
    print("   • Is the motion achieving its intended goal?")
    print("   • How does it compare to human motion?")
    print("   • Where are the inefficiencies or problems?")
    print("   • What improvements could be made?")


def main():
    """🚀 Main lesson function"""
    print("📊 Lesson 1.6: Motion Analysis")
    print("=" * 50)
    print("🎯 Goal: Learn to analyze robot motion scientifically")
    print("⏱️  Time: ~15 minutes") 
    print("🎓 Difficulty: Intermediate")
    
    # Theory and concepts
    explain_motion_analysis()
    motion_metrics_explained()
    
    # Practical analysis
    motion_comparison_demo()
    
    # Best practices
    analysis_best_practices()
    
    print(f"\n🎓 LESSON COMPLETE!")
    print("=" * 50)
    print("✅ You've learned:")
    print("   • How to scientifically analyze robot motion")
    print("   • Key metrics for evaluating performance")
    print("   • Visualization techniques for motion data")
    print("   • How to compare different motion strategies")
    print("")
    print("🚀 Ready for Lesson 1.7: Dataset Explorer")
    print("")
    print("🏆 EXPERIMENT IDEAS:")
    print("💡 Extended analysis:")
    print("   • Compare walking vs running motion patterns")
    print("   • Analyze dance motions for complexity")
    print("   • Study balance recovery strategies")
    print("💡 Advanced metrics:")
    print("   • Calculate energy efficiency")
    print("   • Measure motion naturalness scores")
    print("   • Analyze frequency content of motions")
    print("💡 Comparison studies:")
    print("   • Human vs robot motion differences")
    print("   • Different robots performing same task")
    print("   • Effect of control parameters on motion quality")


if __name__ == "__main__":
    main()