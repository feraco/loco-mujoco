# 🤖 G1 Robot Learning Tutorials

A comprehensive tutorial series for learning robot control and motion analysis with the UnitreeG1 humanoid robot using LocoMuJoCo.

## 📋 Tutorial Overview

### Tutorial 1: Basic Motion Datasets (`g1_01_basic_datasets.py`)
**Focus: Default LocoMuJoCo Datasets**
- Learn how to use built-in motion datasets with G1
- Available datasets: `walk`, `squat`, `stand`, `stepinplace`, `jump`, etc.
- Play motion capture data on the G1 robot
- Understand dataset configuration and replay

### Tutorial 2: LAFAN1 Motion Capture (`g1_02_lafan1_datasets.py`) 
**Focus: High-Quality Human Motion Data**
- Use LAFAN1 datasets with real human motion capture
- Available motions: walking, dancing, running, obstacle navigation
- Compare different human subjects' movement patterns
- Advanced motion retargeting to G1 skeleton

### Tutorial 3: Interactive Control (`g1_03_interactive_control.py`)
**Focus: Manual G1 Control with Dataset Reference**
- Control G1 manually while using datasets as reference
- Test different control strategies and their stability
- Compare minimal movement vs. walking-like motions
- Real-time control with visual feedback

### Tutorial 4: Trajectory Generation (`g1_04_trajectory_generation.py`)
**Focus: Custom Trajectory Creation and Analysis**
- Generate custom trajectories for G1 (standing, walking)
- Analyze trajectory statistics and smoothness
- Create walking patterns with sinusoidal joint movements
- Export and replay custom trajectories

## 🗃️ Dataset Information

### Default Datasets (Built-in)
These are automatically downloaded when first used:

| Dataset Name | Description | Use Case |
|--------------|-------------|----------|
| `walk` | Standard walking gait | Basic locomotion |
| `squat` | Squatting motion | Strength poses |
| `stand` | Standing still | Balance reference |
| `stepinplace` | Step-in-place motion | Stationary gait |
| `walk_fast` | Fast walking | Dynamic locomotion |
| `walk_slow` | Slow walking | Stable locomotion |
| `jump` | Jumping motion | Dynamic movements |

### LAFAN1 Datasets (Motion Capture)
High-quality human motion capture data:

| Dataset Name | Description | Complexity |
|--------------|-------------|------------|
| `walk1_subject1` | Walking from subject 1 | ⭐⭐ |
| `walk1_subject2` | Walking from subject 2 | ⭐⭐ |
| `dance1_subject1` | Dance choreography 1 | ⭐⭐⭐⭐ |
| `dance2_subject4` | Dance choreography 2 | ⭐⭐⭐⭐⭐ |
| `run1_subject1` | Running pattern 1 | ⭐⭐⭐ |
| `obstacles_subject2` | Obstacle navigation | ⭐⭐⭐⭐ |

## 🚀 Quick Start

1. **Prerequisites**:
   ```bash
   conda activate unitree_mujoco
   cd /path/to/loco-mujoco/examples/g1_tutorials
   ```

2. **Run Basic Dataset Tutorial**:
   ```bash
   python g1_01_basic_datasets.py
   ```

3. **Try LAFAN1 Motion Capture**:
   ```bash
   python g1_02_lafan1_datasets.py
   ```

## 📊 Dataset Storage Locations

When you run the tutorials, datasets are automatically downloaded to:

- **Default Datasets**: `~/.loco_mujoco/DefaultDatasets/mocap/UnitreeG1/`
- **LAFAN1 Datasets**: `~/.loco_mujoco/LAFAN1/UnitreeG1/`
- **Custom Trajectories**: Generated in memory or saved to specified paths

## 🛠️ Troubleshooting

### Common Issues

1. **ImportError: No module named 'jax'**
   ```bash
   pip install jax jaxlib
   ```

2. **Dataset download fails**
   - Check internet connection
   - Manually download from LocoMuJoCo repository
   - Use single dataset instead of multiple

3. **G1 falls or unstable**
   - Reduce action magnitudes in tutorials
   - Increase `n_substeps` parameter for smoother simulation
   - Check joint limits and model constraints

### Performance Tips

- **For better stability**: Increase `n_substeps=25` or higher
- **For faster simulation**: Reduce number of episodes or steps
- **For smoother motion**: Use LAFAN1 datasets instead of synthetic ones

## 🎯 Expected Outcomes

After completing these tutorials, you should be able to:

1. ✅ Load and replay motion datasets on UnitreeG1
2. ✅ Use human motion capture data (LAFAN1) with G1
3. ✅ Control G1 interactively with different strategies  
4. ✅ Generate and analyze custom trajectories
5. ✅ Understand dataset formats and storage locations
6. ✅ Troubleshoot common G1 simulation issues

## 🔗 Additional Resources

- **LocoMuJoCo Documentation**: [loco-mujoco.readthedocs.io](https://loco-mujoco.readthedocs.io)
- **UnitreeG1 Model**: `loco_mujoco/models/unitree_g1/`
- **Dataset Tools**: `loco_mujoco/datasets/data_generation/`
- **Original Tutorials**: `../tutorials/` (generic humanoid examples)

## 📝 Next Steps

1. **Modify trajectories** in Tutorial 4 to create custom G1 behaviors
2. **Combine datasets** from Tutorials 1 and 2 for rich motion libraries
3. **Export trajectories** for use in other applications or training
4. **Create your own datasets** using the data generation tools

---

**Note**: These tutorials are specifically optimized for the UnitreeG1 robot. For other humanoids (H1, Atlas, etc.), see the generic tutorials in `../tutorials/`.