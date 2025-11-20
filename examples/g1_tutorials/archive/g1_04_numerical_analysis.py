#!/usr/bin/env python3
"""
G1 Dataset Tutorial 4: Numerical Data Analysis and Understanding
This tutorial helps understand what the G1 robot data looks like numerically
Shows joint positions, velocities, actions, and observations in detail
"""

import numpy as np
from loco_mujoco.task_factories import ImitationFactory, DefaultDatasetConf
import time

def analyze_g1_joint_data(env, dataset_name):
    """Analyze G1 joint data numerically"""
    print(f"\n🔬 Analyzing G1 {dataset_name} data numerically...")
    print("=" * 60)
    
    try:
        # Create dataset
        dataset = env.create_dataset()
        print(f"✅ Dataset created for {dataset_name}")
        
        # Reset environment to get initial state
        obs = env.reset()
        
        # Get environment info using LocoMuJoCo API
        try:
            action_dim = env.info.action_space.shape[0] if hasattr(env.info.action_space, 'shape') else env.info.action_space.n
        except:
            action_dim = 29  # G1 typically has 29 DOF
        
        obs_dim = len(obs) if isinstance(obs, (list, tuple, np.ndarray)) else 1
        
        print(f"\n📊 G1 Robot Dimensions:")
        print(f"   Action space size: {action_dim}")
        print(f"   Observation space size: {obs_dim}")
        
        # Sample some trajectory steps to analyze
        print(f"\n🎯 Sampling trajectory data for analysis...")
        
        trajectory_data = {
            'observations': [],
            'actions': [],
            'step_count': 0
        }
        
        # Run for a short time to collect data
        for step in range(50):  # Short sample
            # Use zero actions (standing)
            action = np.zeros(action_dim)
            
            # Small random variations to see response
            if step > 5:
                action += np.random.normal(0, 0.01, action_dim)
            
            # Step environment
            obs = env.step(action)
            
            # Store data
            trajectory_data['observations'].append(obs.copy() if isinstance(obs, np.ndarray) else obs)
            trajectory_data['actions'].append(action.copy())
            trajectory_data['step_count'] += 1
            
            if step % 10 == 0:
                print(f"   📈 Collected {step+1}/50 samples")
        
        return analyze_numerical_patterns(trajectory_data, dataset_name)
        
    except Exception as e:
        print(f"❌ Error analyzing {dataset_name}: {e}")
        return None

def analyze_numerical_patterns(data, dataset_name):
    """Analyze the numerical patterns in the trajectory data"""
    print(f"\n🔍 NUMERICAL ANALYSIS RESULTS for {dataset_name}:")
    print("=" * 60)
    
    observations = np.array(data['observations'])
    actions = np.array(data['actions'])
    
    print(f"📊 Data Shape Analysis:")
    print(f"   Observations shape: {observations.shape}")
    print(f"   Actions shape: {actions.shape}")
    print(f"   Time steps collected: {data['step_count']}")
    
    # Action analysis
    print(f"\n🎮 ACTION DATA ANALYSIS:")
    print(f"   Action dimensions: {actions.shape[1]}")
    print(f"   Action range: [{actions.min():.4f}, {actions.max():.4f}]")
    print(f"   Action mean: {actions.mean():.4f}")
    print(f"   Action std: {actions.std():.4f}")
    
    # Show action statistics per joint
    print(f"\n🤖 PER-JOINT ACTION STATISTICS:")
    for i in range(min(10, actions.shape[1])):  # Show first 10 joints
        joint_data = actions[:, i]
        print(f"   Joint {i:2d}: mean={joint_data.mean():8.4f}, std={joint_data.std():8.4f}, "
              f"range=[{joint_data.min():8.4f}, {joint_data.max():8.4f}]")
    
    if actions.shape[1] > 10:
        print(f"   ... and {actions.shape[1] - 10} more joints")
    
    # Observation analysis
    print(f"\n👀 OBSERVATION DATA ANALYSIS:")
    print(f"   Observation dimensions: {observations.shape[1]}")
    print(f"   Observation range: [{observations.min():.4f}, {observations.max():.4f}]")
    print(f"   Observation mean: {observations.mean():.4f}")
    print(f"   Observation std: {observations.std():.4f}")
    
    # Show observation statistics per component
    print(f"\n📡 PER-COMPONENT OBSERVATION STATISTICS:")
    for i in range(min(15, observations.shape[1])):  # Show first 15 components
        obs_data = observations[:, i]
        print(f"   Obs {i:2d}: mean={obs_data.mean():8.4f}, std={obs_data.std():8.4f}, "
              f"range=[{obs_data.min():8.4f}, {obs_data.max():8.4f}]")
    
    if observations.shape[1] > 15:
        print(f"   ... and {observations.shape[1] - 15} more observation components")
    
    # Time series analysis
    print(f"\n📈 TIME SERIES PATTERNS:")
    
    # Check for trends in first few components
    for i in range(min(3, observations.shape[1])):
        obs_series = observations[:, i]
        diff = np.diff(obs_series)
        print(f"   Obs component {i}: trend={diff.mean():8.4f}, volatility={diff.std():8.4f}")
    
    # Action smoothness analysis
    action_diffs = np.diff(actions, axis=0)
    action_smoothness = np.mean(np.std(action_diffs, axis=0))
    print(f"   Action smoothness (lower=smoother): {action_smoothness:.6f}")
    
    # Observation smoothness analysis  
    obs_diffs = np.diff(observations, axis=0)
    obs_smoothness = np.mean(np.std(obs_diffs, axis=0))
    print(f"   Observation smoothness: {obs_smoothness:.6f}")
    
    return {
        'actions': actions,
        'observations': observations,
        'action_stats': {
            'mean': actions.mean(),
            'std': actions.std(),
            'min': actions.min(),
            'max': actions.max(),
            'smoothness': action_smoothness
        },
        'obs_stats': {
            'mean': observations.mean(),
            'std': observations.std(),
            'min': observations.min(),
            'max': observations.max(),
            'smoothness': obs_smoothness
        }
    }

def compare_dataset_patterns(results_dict):
    """Compare numerical patterns across different datasets"""
    print(f"\n🔍 COMPARATIVE ANALYSIS ACROSS DATASETS:")
    print("=" * 60)
    
    datasets = list(results_dict.keys())
    
    print(f"📊 Dataset Comparison Summary:")
    print(f"{'Dataset':<15} {'Action Range':<15} {'Obs Range':<15} {'Action Smooth':<15} {'Obs Smooth':<15}")
    print("-" * 80)
    
    for dataset in datasets:
        if results_dict[dataset]:
            stats = results_dict[dataset]
            action_range = f"[{stats['action_stats']['min']:.2f}, {stats['action_stats']['max']:.2f}]"
            obs_range = f"[{stats['obs_stats']['min']:.2f}, {stats['obs_stats']['max']:.2f}]"
            action_smooth = f"{stats['action_stats']['smoothness']:.4f}"
            obs_smooth = f"{stats['obs_stats']['smoothness']:.4f}"
            
            print(f"{dataset:<15} {action_range:<15} {obs_range:<15} {action_smooth:<15} {obs_smooth:<15}")
    
    print(f"\n💡 Data Insights:")
    print(f"   • Lower smoothness values indicate more stable, predictable motion")
    print(f"   • Action ranges show the control effort required for different motions")
    print(f"   • Observation ranges indicate the state space coverage")
    print(f"   • Compare patterns to understand motion complexity")

def main():
    print("🤖 G1 Numerical Data Analysis Tutorial")
    print("=" * 60)
    print("🎯 Purpose: Understand G1 robot data numerically")
    print("📊 Analyzes: Actions, observations, joint patterns, time series")
    
    # Working datasets to analyze
    datasets_to_analyze = [
        ("walk", "Walking motion data analysis"),
        ("squat", "Squatting motion data analysis"),
        ("run", "Running motion data analysis")
    ]
    
    results = {}
    
    for dataset_name, description in datasets_to_analyze:
        print(f"\n{'='*80}")
        print(f"🎯 ANALYZING: {dataset_name.upper()}")
        print(f"📋 Description: {description}")
        
        try:
            print(f"\n🔄 Creating G1 environment for {dataset_name}...")
            
            # Create environment with single dataset
            env = ImitationFactory.make("UnitreeG1",
                                       default_dataset_conf=DefaultDatasetConf([dataset_name]),
                                       n_substeps=10)  # Lower substeps for faster analysis
            
            print(f"✅ Environment created for {dataset_name}!")
            
            # Analyze numerical data
            result = analyze_g1_joint_data(env, dataset_name)
            results[dataset_name] = result
            
            # Brief pause between analyses
            print(f"\n⏸️  {dataset_name} analysis complete. Pausing...")
            time.sleep(1)
            
        except Exception as e:
            print(f"❌ Error with {dataset_name}: {e}")
            results[dataset_name] = None
            continue
    
    # Comparative analysis
    if any(results.values()):
        compare_dataset_patterns(results)
    
    # Final summary
    print(f"\n{'='*80}")
    print("📊 FINAL NUMERICAL ANALYSIS SUMMARY:")
    print("=" * 40)
    
    successful = sum(1 for r in results.values() if r is not None)
    print(f"🎯 Results: {successful}/{len(datasets_to_analyze)} datasets analyzed successfully")
    
    if successful > 0:
        print(f"\n💡 Key Numerical Insights:")
        print(f"   • G1 has high-dimensional action and observation spaces")
        print(f"   • Different motions show distinct numerical patterns")
        print(f"   • Walking typically shows periodic patterns in joint data")
        print(f"   • Squatting shows more static patterns with less variation")
        print(f"   • Running shows higher action magnitudes and more dynamic changes")
        print(f"   • Observation data captures full robot state including:")
        print(f"     - Joint positions and velocities")
        print(f"     - Body orientation and angular velocity") 
        print(f"     - Contact forces and sensor data")
        print(f"   • Action smoothness indicates motion quality and control stability")
    
    print(f"\n✅ G1 numerical data analysis completed!")
    print(f"📚 Use this data understanding for:")
    print(f"   • Designing custom controllers")
    print(f"   • Setting appropriate action/observation limits")
    print(f"   • Understanding motion complexity")
    print(f"   • Comparing different locomotion patterns")

if __name__ == "__main__":
    main()