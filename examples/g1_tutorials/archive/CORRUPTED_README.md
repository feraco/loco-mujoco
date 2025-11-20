# 🤖 G1 Robot Learning Tutorials# 🤖 G1 Robot Learning Tutorials



A comprehensive tutorial series for learning robot control and motion analysis with the UnitreeG1 humanoid robot using LocoMuJoCo.A comprehensive tutorial series for learning robot control and motion analysis with the UnitreeG1 humanoid robot using LocoMuJoCo.



## 🎯 Tutorial Series Overview## 📋 Tutorial Overview



### **Unit 1: Fundamentals (Lessons 1.1-1.10)**### Tutorial 1: Basic Motion Datasets (`g1_01_basic_datasets.py`)

*Learn the basics of robot operation, datasets, and analysis***Focus: Default LocoMuJoCo Datasets**

- Learn how to use built-in motion datasets with G1

| Lesson | Title | Focus | Duration |- Available datasets: `walk`, `squat`, `stand`, `stepinplace`, `jump`, etc.

|--------|-------|--------|----------|- Play motion capture data on the G1 robot

| **1.1** | [Quick System Test](lesson_1_1_quick_test.py) | Verify installation and basic functionality | 5 min |- Understand dataset configuration and replay

| **1.2** | [Simple Walk Demo](lesson_1_2_simple_walk_test.py) | Watch robot walk with built-in motions | 8 min |

| **1.3** | [Basic Datasets](lesson_1_3_basic_datasets.py) | Explore default motion datasets | 10 min |### Tutorial 2: LAFAN1 Motion Capture (`g1_02_lafan1_datasets.py`) 

| **1.4** | [LAFAN1 Datasets](lesson_1_4_lafan1_datasets.py) | Advanced human motion capture data | 12 min |**Focus: High-Quality Human Motion Data**

| **1.5** | [Interactive Control](lesson_1_5_interactive_control.py) | **Control robot with keyboard** | 15 min |- Use LAFAN1 datasets with real human motion capture

| **1.6** | [Motion Analysis](lesson_1_6_motion_analysis.py) | **Live graphs and motion science** | 15 min |- Available motions: walking, dancing, running, obstacle navigation

| **1.7** | [Dataset Explorer](lesson_1_7_dataset_explorer.py) | Browse and analyze motion collections | 12 min |- Compare different human subjects' movement patterns

| **1.8** | [Test Utilities](lesson_1_8_test_utilities.py) | Automated testing and validation | 12 min |- Advanced motion retargeting to G1 skeleton

| **1.9** | [Slow Motion Viewer](lesson_1_9_slow_motion_viewer.py) | Detailed motion frame analysis | 10 min |

| **1.10** | [Complete Summary](lesson_1_10_complete_summary.py) | Review and next steps | 8 min |### Tutorial 3: Interactive Control (`g1_03_interactive_control.py`)

**Focus: Manual G1 Control with Dataset Reference**

## 🌟 **Featured Lessons**- Control G1 manually while using datasets as reference

- Test different control strategies and their stability

### 🎮 **Lesson 1.5 - Interactive Control** - Compare minimal movement vs. walking-like motions

- **Real-time robot control** with keyboard- Real-time control with visual feedback

- Control individual joints (w/s/a/d/q/e)

- Reset poses and quit safely### Tutorial 4: Trajectory Generation (`g1_04_trajectory_generation.py`)

- **No auto-closing** - control until you quit!**Focus: Custom Trajectory Creation and Analysis**

- Generate custom trajectories for G1 (standing, walking)

### 📊 **Lesson 1.6 - Live Motion Analysis**- Analyze trajectory statistics and smoothness

- **Real-time data visualization** with graphs- Create walking patterns with sinusoidal joint movements

- Joint positions, velocities, energy metrics- Export and replay custom trajectories

- **Live plotting** that updates during motion

- Scientific motion analysis and interpretation## 🗃️ Dataset Information



### 🧪 **Lesson 1.8 - Test Utilities**### Default Datasets (Built-in)

- **100% automated testing suite**These are automatically downloaded when first used:

- Validates robot creation, datasets, performance

- Comprehensive debugging guides| Dataset Name | Description | Use Case |

- Professional robot validation techniques|--------------|-------------|----------|

| `walk` | Standard walking gait | Basic locomotion |

## 🚀 **Quick Start**| `squat` | Squatting motion | Strength poses |

| `stand` | Standing still | Balance reference |

```bash| `stepinplace` | Step-in-place motion | Stationary gait |

# Start with the fundamentals| `walk_fast` | Fast walking | Dynamic locomotion |

python lesson_1_1_quick_test.py| `walk_slow` | Slow walking | Stable locomotion |

| `jump` | Jumping motion | Dynamic movements |

# Try interactive control (most popular!)

python lesson_1_5_interactive_control.py### LAFAN1 Datasets (Motion Capture)

High-quality human motion capture data:

# See live motion analysis

python lesson_1_6_motion_analysis.py| Dataset Name | Description | Complexity |

```|--------------|-------------|------------|

| `walk1_subject1` | Walking from subject 1 | ⭐⭐ |

## 📁 **Directory Structure**| `walk1_subject2` | Walking from subject 2 | ⭐⭐ |

| `dance1_subject1` | Dance choreography 1 | ⭐⭐⭐⭐ |

```| `dance2_subject4` | Dance choreography 2 | ⭐⭐⭐⭐⭐ |

g1_tutorials/| `run1_subject1` | Running pattern 1 | ⭐⭐⭐ |

├── lesson_1_*.py          # Main tutorial lessons| `obstacles_subject2` | Obstacle navigation | ⭐⭐⭐⭐ |

├── README.md             # This overview

├── DATASET_LOCATIONS.md  # Dataset information## 🚀 Quick Start

├── VIEWER_SOLUTIONS.md   # Troubleshooting guide

├── archive/              # Old experimental files1. **Prerequisites**:

├── development/          # Development notes   ```bash

├── media/               # Videos and recordings   conda activate unitree_mujoco

└── tools/               # Utility scripts   cd /path/to/loco-mujoco/examples/g1_tutorials

```   ```



## 🎓 **Learning Path**2. **Run Basic Dataset Tutorial**:

   ```bash

### **Beginner**: Start with lessons 1.1 → 1.3   python g1_01_basic_datasets.py

- Learn basic robot operation   ```

- Understand datasets and motions

- Get comfortable with the system3. **Try LAFAN1 Motion Capture**:

   ```bash

### **Intermediate**: Continue with lessons 1.4 → 1.7     python g1_02_lafan1_datasets.py

- Advanced motion datasets   ```

- Interactive robot control

- Scientific motion analysis## 📊 Dataset Storage Locations

- Data exploration techniques

When you run the tutorials, datasets are automatically downloaded to:

### **Advanced**: Complete with lessons 1.8 → 1.10

- Professional testing methods- **Default Datasets**: `~/.loco_mujoco/DefaultDatasets/mocap/UnitreeG1/`

- Detailed motion analysis- **LAFAN1 Datasets**: `~/.loco_mujoco/LAFAN1/UnitreeG1/`

- System validation- **Custom Trajectories**: Generated in memory or saved to specified paths

- Ready for advanced projects

## 🛠️ Troubleshooting

## 🔧 **System Requirements**

### Common Issues

- **Python 3.8+** with LocoMuJoCo installed

- **Graphics support** for visualization1. **ImportError: No module named 'jax'**

- **Keyboard input** for interactive lessons   ```bash

- **~2GB storage** for datasets (auto-downloaded)   pip install jax jaxlib

   ```

## 💡 **Tips for Success**

2. **Dataset download fails**

1. **Follow in order** - lessons build on each other   - Check internet connection

2. **Try interactive lessons** - 1.5 and 1.6 are highlights   - Manually download from LocoMuJoCo repository

3. **Read error messages** - lesson 1.8 has debugging guides   - Use single dataset instead of multiple

4. **Experiment** - each lesson has experiment ideas

5. **Ask questions** - check VIEWER_SOLUTIONS.md for help3. **G1 falls or unstable**

   - Reduce action magnitudes in tutorials

## 🏆 **What You'll Learn**   - Increase `n_substeps` parameter for smoother simulation

   - Check joint limits and model constraints

- ✅ **Robot Control**: Direct robot manipulation and control

- ✅ **Motion Analysis**: Scientific analysis of robot movement  ### Performance Tips

- ✅ **Dataset Usage**: Working with motion capture data

- ✅ **Visualization**: Real-time graphs and motion plotting- **For better stability**: Increase `n_substeps=25` or higher

- ✅ **Testing**: Professional robot validation techniques- **For faster simulation**: Reduce number of episodes or steps

- ✅ **Debugging**: Systematic problem-solving approaches- **For smoother motion**: Use LAFAN1 datasets instead of synthetic ones



## 🚀 **Ready for More?**## 🎯 Expected Outcomes



After completing Unit 1, you'll be ready for:After completing these tutorials, you should be able to:

- **Unit 2**: Custom environments and advanced control

- **Research Projects**: Motion learning and optimization1. ✅ Load and replay motion datasets on UnitreeG1

- **Real Robot Control**: Transfer to physical robots2. ✅ Use human motion capture data (LAFAN1) with G1

- **AI Development**: Reinforcement learning applications3. ✅ Control G1 interactively with different strategies  

4. ✅ Generate and analyze custom trajectories

---5. ✅ Understand dataset formats and storage locations

6. ✅ Troubleshoot common G1 simulation issues

**🎯 Start your robotics journey today!** Begin with `python lesson_1_1_quick_test.py`
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