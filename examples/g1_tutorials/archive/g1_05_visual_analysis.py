#!/usr/bin/env python3
"""
G1 Visual Data Analysis Tutorial
This tutorial creates visual plots and charts to understand G1 robot data
Shows joint trajectories, action patterns, and motion analysis with graphs
"""

import numpy as np
from loco_mujoco.task_factories import ImitationFactory, DefaultDatasetConf
import time
import os

# Check if matplotlib is available, if not provide text-based alternatives
try:
    import matplotlib.pyplot as plt
    import matplotlib.patches as patches
    HAS_MATPLOTLIB = True
    print("📊 Matplotlib available - will create visual plots")
except ImportError:
    HAS_MATPLOTLIB = False
    print("📝 Matplotlib not available - will create text-based visualizations")

def create_text_plot(data, title, width=60, height=15):
    """Create a simple ASCII plot when matplotlib isn't available"""
    if len(data) == 0:
        return f"{title}\n[No data to plot]\n"
    
    # Normalize data to plot height
    min_val, max_val = np.min(data), np.max(data)
    if max_val == min_val:
        max_val = min_val + 1
    
    normalized = ((data - min_val) / (max_val - min_val) * (height - 1)).astype(int)
    
    # Create plot grid
    plot = []
    plot.append(f"{title}")
    plot.append(f"Range: [{min_val:.3f}, {max_val:.3f}]")
    plot.append("─" * width)
    
    for row in range(height-1, -1, -1):
        line = "|"
        for col in range(min(width-2, len(normalized))):
            if normalized[col] == row:
                line += "●"
            elif col > 0 and min(normalized[col-1], normalized[col]) <= row <= max(normalized[col-1], normalized[col]):
                line += "─"
            else:
                line += " "
        line += "|"
        plot.append(line)
    
    plot.append("─" * width)
    plot.append(f"Time steps: 0 → {len(data)}")
    return "\n".join(plot) + "\n"

def analyze_and_visualize_dataset(dataset_name, max_samples=200):
    """Analyze a dataset and create visual representations"""
    print(f"\n{'='*80}")
    print(f"🎯 VISUAL ANALYSIS: {dataset_name.upper()}")
    print(f"📊 Creating plots and visualizations...")
    
    try:
        # Create environment
        env = ImitationFactory.make("UnitreeG1",
                                   default_dataset_conf=DefaultDatasetConf([dataset_name]),
                                   n_substeps=10)
        
        print(f"✅ Environment created for {dataset_name}")
        
        # Collect data samples
        actions_list = []
        observations_list = []
        
        print(f"   📈 Collecting {max_samples} samples...")
        for i in range(max_samples):
            obs, _ = env.reset()
            action = env.action_space.sample()
            obs, reward, terminated, truncated, info = env.step(action)
            
            # Handle different observation types
            if hasattr(obs, 'shape'):
                # If obs is already a numpy array
                obs_flat = obs.flatten() if len(obs.shape) > 1 else obs
            elif isinstance(obs, (list, tuple)):
                # If obs is a list/tuple, convert to flat array
                obs_flat = np.array(obs).flatten()
            else:
                # If obs is a single value
                obs_flat = np.array([obs])
            
            # Handle different action types
            if hasattr(action, 'shape'):
                action_flat = action.flatten() if len(action.shape) > 1 else action
            elif isinstance(action, (list, tuple)):
                action_flat = np.array(action).flatten()
            else:
                action_flat = np.array([action])
            
            actions_list.append(action_flat)
            observations_list.append(obs_flat)
            
            if (i + 1) % 50 == 0:
                print(f"   📈 Collected {i+1}/{max_samples} samples")
        
        # Convert to numpy arrays with proper handling
        try:
            # Try to stack arrays directly
            actions = np.vstack(actions_list)
            observations = np.vstack(observations_list)
        except ValueError:
            # If shapes are inconsistent, pad to max size
            max_action_len = max(len(a) for a in actions_list)
            max_obs_len = max(len(o) for o in observations_list)
            
            # Pad actions
            padded_actions = []
            for action in actions_list:
                if len(action) < max_action_len:
                    padded_action = np.pad(action, (0, max_action_len - len(action)), 'constant')
                else:
                    padded_action = action
                padded_actions.append(padded_action)
            actions = np.array(padded_actions)
            
            # Pad observations
            padded_observations = []
            for obs in observations_list:
                if len(obs) < max_obs_len:
                    padded_obs = np.pad(obs, (0, max_obs_len - len(obs)), 'constant')
                else:
                    padded_obs = obs
                padded_observations.append(padded_obs)
            observations = np.array(padded_observations)
        
        print(f"✅ Data collection complete: {observations.shape[0]} samples")
        
        # Create visualizations
        return create_visualizations(dataset_name, observations, actions)
        
    except Exception as e:
        print(f"❌ Error analyzing {dataset_name}: {e}")
        return None

def create_visualizations(dataset_name, observations, actions):
    """Create visual plots for the trajectory data"""
    print(f"\n📊 Creating visualizations for {dataset_name}...")
    
    results = {
        'dataset_name': dataset_name,
        'obs_shape': observations.shape,
        'action_shape': actions.shape,
        'visualizations': []
    }
    
    if HAS_MATPLOTLIB:
        # Create matplotlib plots
        fig, axes = plt.subplots(2, 3, figsize=(15, 10))
        fig.suptitle(f'G1 Robot Data Analysis: {dataset_name.upper()}', fontsize=16)
        
        # Plot 1: First 6 joint actions over time
        axes[0, 0].plot(actions[:, :6])
        axes[0, 0].set_title('First 6 Joint Actions')
        axes[0, 0].set_xlabel('Time Steps')
        axes[0, 0].set_ylabel('Action Value')
        axes[0, 0].legend([f'Joint {i}' for i in range(6)], fontsize=8)
        axes[0, 0].grid(True)
        
        # Plot 2: Action magnitude distribution
        action_magnitudes = np.linalg.norm(actions, axis=1)
        axes[0, 1].hist(action_magnitudes, bins=20, alpha=0.7, color='blue')
        axes[0, 1].set_title('Action Magnitude Distribution')
        axes[0, 1].set_xlabel('Action Magnitude')
        axes[0, 1].set_ylabel('Frequency')
        axes[0, 1].grid(True)
        
        # Plot 3: Joint action heatmap (first 10 joints)
        im1 = axes[0, 2].imshow(actions[:50, :10].T, aspect='auto', cmap='viridis')
        axes[0, 2].set_title('Action Heatmap (First 10 Joints)')
        axes[0, 2].set_xlabel('Time Steps')
        axes[0, 2].set_ylabel('Joint Index')
        plt.colorbar(im1, ax=axes[0, 2])
        
        # Plot 4: First 6 observations over time
        axes[1, 0].plot(observations[:, :6])
        axes[1, 0].set_title('First 6 Observations')
        axes[1, 0].set_xlabel('Time Steps')
        axes[1, 0].set_ylabel('Observation Value')
        axes[1, 0].legend([f'Obs {i}' for i in range(6)], fontsize=8)
        axes[1, 0].grid(True)
        
        # Plot 5: Observation variance across components
        obs_var = np.var(observations, axis=0)
        axes[1, 1].bar(range(min(20, len(obs_var))), obs_var[:20])
        axes[1, 1].set_title('Observation Variance (First 20 Components)')
        axes[1, 1].set_xlabel('Observation Component')
        axes[1, 1].set_ylabel('Variance')
        axes[1, 1].grid(True)
        
        # Plot 6: Phase plot (obs[0] vs obs[1])
        if observations.shape[1] >= 2:
            axes[1, 2].scatter(observations[:, 0], observations[:, 1], alpha=0.6, s=10)
            axes[1, 2].set_title('Phase Plot: Obs[0] vs Obs[1]')
            axes[1, 2].set_xlabel('Observation Component 0')
            axes[1, 2].set_ylabel('Observation Component 1')
            axes[1, 2].grid(True)
        
        plt.tight_layout()
        
        # Save plot
        plot_filename = f'g1_{dataset_name}_analysis.png'
        plt.savefig(plot_filename, dpi=150, bbox_inches='tight')
        print(f"📊 Saved matplotlib plot: {plot_filename}")
        
        # Show plot
        plt.show()
        
        results['visualizations'].append(f"Matplotlib plot saved as {plot_filename}")
        
    else:
        # Create text-based visualizations
        print(f"\n📊 TEXT-BASED VISUALIZATIONS for {dataset_name}:")
        print("=" * 60)
        
        # Joint action plot
        if actions.shape[1] >= 1:
            joint_0_plot = create_text_plot(actions[:50, 0], f"Joint 0 Action Trajectory ({dataset_name})")
            print(joint_0_plot)
            results['visualizations'].append("Joint 0 text plot")
        
        # Action magnitude plot
        action_magnitudes = np.linalg.norm(actions, axis=1)
        magnitude_plot = create_text_plot(action_magnitudes[:50], f"Action Magnitudes ({dataset_name})")
        print(magnitude_plot)
        results['visualizations'].append("Action magnitude text plot")
        
        # Observation plot
        if observations.shape[1] >= 1:
            obs_0_plot = create_text_plot(observations[:50, 0], f"Observation 0 Trajectory ({dataset_name})")
            print(obs_0_plot)
            results['visualizations'].append("Observation 0 text plot")
    
    # Statistical summary
    print(f"\n📈 VISUAL DATA SUMMARY for {dataset_name}:")
    print("-" * 40)
    print(f"📊 Data Shape:")
    print(f"   Actions: {actions.shape}")
    print(f"   Observations: {observations.shape}")
    
    print(f"\n🎮 Action Statistics:")
    print(f"   Mean magnitude: {np.mean(np.linalg.norm(actions, axis=1)):.4f}")
    print(f"   Max magnitude: {np.max(np.linalg.norm(actions, axis=1)):.4f}")
    print(f"   Action smoothness: {np.mean(np.std(np.diff(actions, axis=0), axis=0)):.6f}")
    
    print(f"\n👀 Observation Statistics:")
    print(f"   Mean: {np.mean(observations):.4f}")
    print(f"   Std: {np.std(observations):.4f}")
    print(f"   Range: [{np.min(observations):.4f}, {np.max(observations):.4f}]")
    
    # Movement pattern analysis
    if actions.shape[1] >= 6:
        print(f"\n🤖 Movement Pattern Analysis:")
        leg_joints = actions[:, :6]  # First 6 joints (legs)
        leg_activity = np.std(leg_joints, axis=0)
        most_active_joint = np.argmax(leg_activity)
        print(f"   Most active leg joint: Joint {most_active_joint} (std: {leg_activity[most_active_joint]:.4f})")
        print(f"   Leg joint activity pattern: {leg_activity[:6]}")
    
    return results

def compare_visual_patterns(all_results):
    """Compare visual patterns across datasets"""
    print(f"\n{'='*80}")
    print("📊 COMPARATIVE VISUAL ANALYSIS")
    print("=" * 40)
    
    if not all_results or not any(all_results.values()):
        print("❌ No results to compare")
        return
    
    print(f"📈 Dataset Comparison:")
    for dataset, result in all_results.items():
        if result:
            print(f"\n🎯 {dataset.upper()}:")
            print(f"   Data size: {result['obs_shape'][0]} samples")
            print(f"   Action dims: {result['action_shape'][1]}")
            print(f"   Obs dims: {result['obs_shape'][1]}")
            print(f"   Visualizations: {len(result['visualizations'])}")
    
    print(f"\n💡 Visual Analysis Insights:")
    print(f"   • Different motions show distinct visual patterns")
    print(f"   • Joint trajectories reveal periodic vs static motions")
    print(f"   • Action heatmaps show which joints are most active")
    print(f"   • Phase plots reveal state space structure")
    print(f"   • Variance analysis shows information content")

def main():
    print("🤖 G1 Visual Data Analysis Tutorial")
    print("=" * 60)
    print("🎯 Purpose: Create visual plots and charts for G1 robot data")
    print("📊 Creates: Joint trajectories, heatmaps, distributions, phase plots")
    
    if HAS_MATPLOTLIB:
        print("✅ Matplotlib available - will create high-quality plots")
    else:
        print("📝 Using text-based visualizations (install matplotlib for better plots)")
        print("   pip install matplotlib")
    
    # Datasets to analyze visually
    datasets_to_analyze = ["walk", "squat", "run"]
    
    all_results = {}
    
    for dataset in datasets_to_analyze:
        try:
            result = analyze_and_visualize_dataset(dataset, max_samples=150)
            all_results[dataset] = result
            time.sleep(1)  # Brief pause
        except Exception as e:
            print(f"❌ Error with {dataset}: {e}")
            all_results[dataset] = None
    
    # Compare patterns
    compare_visual_patterns(all_results)
    
    # Final summary
    print(f"\n{'='*80}")
    print("🎨 VISUAL ANALYSIS COMPLETE!")
    print("=" * 30)
    
    successful = sum(1 for r in all_results.values() if r is not None)
    print(f"🎯 Analyzed: {successful}/{len(datasets_to_analyze)} datasets")
    
    if HAS_MATPLOTLIB:
        print(f"📊 Created matplotlib plots in current directory")
        print(f"   Look for: g1_walk_analysis.png, g1_squat_analysis.png, g1_run_analysis.png")
    
    print(f"\n💡 Use Visual Analysis For:")
    print(f"   • Understanding motion patterns graphically")
    print(f"   • Identifying periodic vs static behaviors")
    print(f"   • Comparing joint activity across motions")
    print(f"   • Detecting outliers and anomalies")
    print(f"   • Validating controller performance")

if __name__ == "__main__":
    main()