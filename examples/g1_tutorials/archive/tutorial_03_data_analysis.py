#!/usr/bin/env python3
"""
📊 Tutorial 3: Robot Data Analysis & Visualization

WHAT YOU'LL LEARN:
✅ How to extract and analyze robot motion data
✅ Create beautiful visualizations of robot behavior
✅ Understand joint trajectories and movement patterns
✅ Compare different motion types quantitatively

WHAT TO EXPECT:
📈 Real-time plots of robot joint angles and positions
📊 Comparative analysis of walking vs squatting vs jumping
🎨 Beautiful data visualizations and charts
🔍 Deep dive into what makes good robot motion

EDUCATIONAL PURPOSE:
Learn to analyze robot data like a scientist! Understanding data is crucial
for debugging robot behavior, evaluating performance, and improving AI systems.
"""

import jax
import numpy as np
from loco_mujoco.task_factories import ImitationFactory, DefaultDatasetConf
import time

# Visualization setup
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    from matplotlib.animation import FuncAnimation
    HAS_MATPLOTLIB = True
    print("📊 Matplotlib available - creating beautiful plots!")
except ImportError:
    HAS_MATPLOTLIB = False
    print("📝 Matplotlib not available - using text-based analysis")

def explain_concept(title, explanation):
    """Helper function to clearly explain concepts"""
    print(f"\n💡 CONCEPT: {title}")
    print("─" * 60)
    print(f"   {explanation}")
    print("─" * 60)

def create_ascii_plot(data, title, width=60, height=12):
    """Create ASCII art plots when matplotlib isn't available"""
    if len(data) == 0:
        return f"\n{title}\n[No data available]\n"
    
    # Normalize data to plot dimensions
    min_val, max_val = np.min(data), np.max(data)
    if max_val == min_val:
        max_val = min_val + 1
    
    normalized = ((data - min_val) / (max_val - min_val) * (height - 1)).astype(int)
    
    # Create the plot
    plot_lines = []
    plot_lines.append(f"\n📈 {title}")
    plot_lines.append(f"Range: [{min_val:.3f} to {max_val:.3f}]")
    plot_lines.append("┌" + "─" * (width-2) + "┐")
    
    for row in range(height-1, -1, -1):
        line = "│"
        for col in range(min(width-2, len(normalized))):
            if normalized[col] == row:
                line += "●"
            elif col > 0:
                # Draw connecting lines
                prev_row, curr_row = normalized[col-1], normalized[col]
                if min(prev_row, curr_row) <= row <= max(prev_row, curr_row):
                    line += "─"
                else:
                    line += " "
            else:
                line += " "
        line += "│"
        plot_lines.append(line)
    
    plot_lines.append("└" + "─" * (width-2) + "┘")
    return "\n".join(plot_lines)

def analyze_motion_data(env, motion_name, num_steps=500):
    """Collect and analyze robot motion data"""
    print(f"\n🔍 Analyzing {motion_name} motion...")
    
    # Reset environment and collect data
    key = jax.random.PRNGKey(42)
    obs = env.reset(key)
    
    # Data storage
    joint_positions = []
    body_positions = []
    joint_velocities = []
    rewards = []
    
    for step in range(num_steps):
        # Step the environment (it plays back the dataset)
        step_result = env.step(np.zeros(env.info.action_space.shape[0]))
        if len(step_result) == 5:
            obs, reward, done, truncated, info = step_result
        elif len(step_result) == 4:
            obs, reward, done, info = step_result
        else:
            obs, reward, done = step_result
            info = {}
        
        # Extract meaningful data from observations
        if len(obs) >= 10:
            # Assume first 3 are position, next 4 are orientation, rest are joints
            body_pos = obs[0:3] if len(obs) >= 3 else [0, 0, 1]
            joint_pos = obs[7:] if len(obs) > 7 else []
            
            body_positions.append(body_pos)
            if len(joint_pos) > 0:
                joint_positions.append(joint_pos[:12])  # First 12 joints for analysis
        
        rewards.append(reward)
        
        # Reset if done
        if done:
            obs = env.reset(key)
    
    # Convert to numpy arrays for analysis
    body_positions = np.array(body_positions)
    joint_positions = np.array(joint_positions) if joint_positions else np.array([])
    rewards = np.array(rewards)
    
    # Calculate statistics
    stats = {
        'motion_name': motion_name,
        'avg_height': np.mean(body_positions[:, 2]) if body_positions.size > 0 else 0,
        'height_variation': np.std(body_positions[:, 2]) if body_positions.size > 0 else 0,
        'avg_reward': np.mean(rewards),
        'total_distance': 0,
        'joint_range_of_motion': []
    }
    
    # Calculate distance traveled
    if body_positions.size > 0:
        distances = np.sqrt(np.sum(np.diff(body_positions[:, :2], axis=0)**2, axis=1))
        stats['total_distance'] = np.sum(distances)
    
    # Calculate joint range of motion
    if joint_positions.size > 0:
        for joint_idx in range(min(6, joint_positions.shape[1])):  # First 6 joints
            joint_range = np.max(joint_positions[:, joint_idx]) - np.min(joint_positions[:, joint_idx])
            stats['joint_range_of_motion'].append(joint_range)
    
    return stats, body_positions, joint_positions, rewards

def create_visualizations(motion_data, motion_names):
    """Create beautiful visualizations of the robot data"""
    
    if not HAS_MATPLOTLIB:
        # Text-based visualizations
        print("\n📊 DATA ANALYSIS RESULTS (Text Mode)")
        print("=" * 60)
        
        for i, (stats, body_pos, joint_pos, rewards) in enumerate(motion_data):
            print(f"\n🤖 {motion_names[i].upper()} MOTION ANALYSIS:")
            print(f"   Average Height: {stats['avg_height']:.3f}m")
            print(f"   Height Variation: {stats['height_variation']:.3f}m")
            print(f"   Distance Traveled: {stats['total_distance']:.3f}m") 
            print(f"   Average Reward: {stats['avg_reward']:.3f}")
            
            if len(rewards) > 0:
                print(create_ascii_plot(rewards[-100:], f"{motion_names[i]} Reward Over Time"))
            
            if body_pos.size > 0:
                height_data = body_pos[-100:, 2]  # Last 100 height measurements
                print(create_ascii_plot(height_data, f"{motion_names[i]} Height Over Time"))
                
        return
    
    # Matplotlib visualizations
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle('🤖 Robot Motion Analysis Dashboard', fontsize=16, fontweight='bold')
    
    # Plot 1: Height trajectories
    ax1 = axes[0, 0]
    for i, (stats, body_pos, joint_pos, rewards) in enumerate(motion_data):
        if body_pos.size > 0:
            time_steps = np.arange(len(body_pos)) / 30.0  # Convert to seconds (30 FPS)
            ax1.plot(time_steps, body_pos[:, 2], label=motion_names[i], linewidth=2)
    
    ax1.set_title('🔺 Robot Height Over Time')
    ax1.set_xlabel('Time (seconds)')
    ax1.set_ylabel('Height (meters)')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    
    # Plot 2: Distance traveled comparison
    ax2 = axes[0, 1]
    distances = [stats['total_distance'] for stats, _, _, _ in motion_data]
    colors = ['#FF6B6B', '#4ECDC4', '#45B7D1']
    bars = ax2.bar(motion_names, distances, color=colors)
    ax2.set_title('🏃 Total Distance Traveled')
    ax2.set_ylabel('Distance (meters)')
    
    # Add value labels on bars
    for bar, distance in zip(bars, distances):
        height = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{distance:.2f}m', ha='center', va='bottom')
    
    # Plot 3: Average reward comparison
    ax3 = axes[1, 0] 
    avg_rewards = [stats['avg_reward'] for stats, _, _, _ in motion_data]
    bars = ax3.bar(motion_names, avg_rewards, color=colors)
    ax3.set_title('🏆 Average Reward Score')
    ax3.set_ylabel('Reward')
    
    for bar, reward in zip(bars, avg_rewards):
        height = bar.get_height()
        ax3.text(bar.get_x() + bar.get_width()/2., height + 0.01,
                f'{reward:.3f}', ha='center', va='bottom')
    
    # Plot 4: Joint range of motion heatmap
    ax4 = axes[1, 1]
    joint_data = []
    for stats, _, _, _ in motion_data:
        if stats['joint_range_of_motion']:
            joint_data.append(stats['joint_range_of_motion'][:6])  # First 6 joints
        else:
            joint_data.append([0] * 6)
    
    if joint_data:
        im = ax4.imshow(joint_data, cmap='viridis', aspect='auto')
        ax4.set_title('🦾 Joint Range of Motion')
        ax4.set_xlabel('Joint Index')
        ax4.set_ylabel('Motion Type')
        ax4.set_yticks(range(len(motion_names)))
        ax4.set_yticklabels(motion_names)
        plt.colorbar(im, ax=ax4, label='Range (radians)')
    
    plt.tight_layout()
    plt.show()
    
    print("📊 Visualizations created! Check the plot window.")

def main():
    print("📊 LocoMuJoCo Tutorial 3: Robot Data Analysis & Visualization")
    print("=" * 70)
    
    explain_concept(
        "Why Data Analysis Matters",
        "Understanding robot data helps us:\n"
        "   • Debug movement problems\n"
        "   • Compare different motion strategies\n" 
        "   • Optimize robot performance\n"
        "   • Validate that learning algorithms work correctly"
    )
    
    # Motion types to analyze
    motion_types = ["walk", "squat", "jump"]
    
    print(f"\n🔬 STEP 1: Collecting Motion Data")
    print(f"Analyzing {len(motion_types)} different motion types...")
    
    motion_data = []
    
    for motion in motion_types:
        print(f"\n📋 Loading {motion} motion dataset...")
        
        try:
            # Create environment for this specific motion
            env = ImitationFactory.make(
                "UnitreeG1",
                default_dataset_conf=DefaultDatasetConf([motion]),
                n_substeps=20
            )
            
            # Collect and analyze data
            stats, body_pos, joint_pos, rewards = analyze_motion_data(env, motion, num_steps=300)
            motion_data.append((stats, body_pos, joint_pos, rewards))
            
            print(f"✅ {motion} analysis complete!")
            print(f"   Height: {stats['avg_height']:.2f}±{stats['height_variation']:.2f}m")
            print(f"   Distance: {stats['total_distance']:.2f}m")
            print(f"   Reward: {stats['avg_reward']:.3f}")
            
        except Exception as e:
            print(f"⚠️  Skipping {motion} due to error: {e}")
            continue
    
    if not motion_data:
        print("❌ No motion data collected. Check your installation.")
        return
    
    # Data analysis and comparison
    print(f"\n📈 STEP 2: Comparative Analysis") 
    print("=" * 50)
    
    # Find the motion with highest/lowest metrics
    best_height = max(motion_data, key=lambda x: x[0]['avg_height'])
    most_dynamic = max(motion_data, key=lambda x: x[0]['height_variation']) 
    longest_distance = max(motion_data, key=lambda x: x[0]['total_distance'])
    
    print(f"🏔️  Most upright motion: {best_height[0]['motion_name']} ({best_height[0]['avg_height']:.2f}m)")
    print(f"🎢 Most dynamic motion: {most_dynamic[0]['motion_name']} (variation: {most_dynamic[0]['height_variation']:.3f}m)")
    print(f"🏃 Greatest distance: {longest_distance[0]['motion_name']} ({longest_distance[0]['total_distance']:.2f}m)")
    
    explain_concept(
        "Understanding the Numbers",
        "• HEIGHT: How high the robot's center of mass stays\n"
        "   • VARIATION: How much the height changes (dynamic vs static)\n"
        "   • DISTANCE: How far the robot travels in space\n"
        "   • REWARD: How well the robot follows the reference motion"
    )
    
    # Create visualizations
    print(f"\n🎨 STEP 3: Data Visualization")
    print("Creating beautiful plots and charts...")
    
    motion_names = [stats['motion_name'] for stats, _, _, _ in motion_data]
    create_visualizations(motion_data, motion_names)
    
    # Educational insights
    print(f"\n🧠 STEP 4: Scientific Insights")
    print("=" * 50)
    
    print("📚 What the data tells us:")
    
    # Walking analysis
    walk_data = next((data for data in motion_data if data[0]['motion_name'] == 'walk'), None)
    if walk_data:
        stats = walk_data[0]
        print(f"🚶 WALKING: Steady height ({stats['avg_height']:.2f}m), covers distance ({stats['total_distance']:.2f}m)")
        print("   → This is locomotion - moving while maintaining stability")
    
    # Squatting analysis  
    squat_data = next((data for data in motion_data if data[0]['motion_name'] == 'squat'), None)
    if squat_data:
        stats = squat_data[0]
        print(f"🏋️ SQUATTING: Variable height (±{stats['height_variation']:.3f}m), minimal distance")
        print("   → This is postural control - changing body configuration in place")
    
    # Jumping analysis
    jump_data = next((data for data in motion_data if data[0]['motion_name'] == 'jump'), None) 
    if jump_data:
        stats = jump_data[0]
        print(f"🦘 JUMPING: Dynamic height changes, explosive motion patterns")
        print("   → This demonstrates ballistic movement - brief contact with ground")
    
    # Educational summary
    print("\n🎓 TUTORIAL COMPLETE - What You Just Learned:")
    print("=" * 60)
    print("✅ How to extract quantitative data from robot simulations")
    print("✅ Different motion types have distinct statistical signatures") 
    print("✅ Data visualization reveals patterns not obvious from watching")
    print("✅ Scientific analysis helps understand robot behavior deeply")
    print("✅ This approach scales to evaluating learning algorithms")
    
    explain_concept(
        "Real Research Applications",
        "Scientists use these exact techniques to:\n"
        "   • Evaluate new robot learning algorithms\n"
        "   • Compare different robot designs\n"
        "   • Validate that robots move human-like\n" 
        "   • Debug when robots behave unexpectedly"
    )
    
    print("\n🏆 EXPERIMENT TIME!")
    print("Try modifying this tutorial:")
    print("💡 Add more motion types: 'run', 'dance', 'crawl'")
    print("💡 Analyze different robots: 'UnitreeH1', 'Atlas'")
    print("💡 Extend data collection time for more statistics")
    print("💡 Add your own analysis metrics (energy, smoothness, etc.)")
    
    explain_concept(
        "What's Next?",
        "Now you can analyze robot behavior scientifically! Next learn:\n"
        "   • How to design reward functions for learning\n"
        "   • Training robots with reinforcement learning\n"
        "   • Advanced motion analysis and biomechanics"
    )

if __name__ == "__main__":
    main()