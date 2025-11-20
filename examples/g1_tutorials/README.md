# G1 Robot Learning Tutorials# 🤖 G1 Robot Learning Tutorials# 🤖 G1 Robot Learning Tutorials# 🤖 G1 Robot Learning Tutorials



A comprehensive tutorial series for learning robot control and motion analysis with the UnitreeG1 humanoid robot using LocoMuJoCo.



## Tutorial Series OverviewA comprehensive tutorial series for learning robot control and motion analysis with the UnitreeG1 humanoid robot using LocoMuJoCo.



### Unit 1: Fundamentals (Lessons 1.0-1.10)

*Learn the basics of robot operation, datasets, and analysis*

## 🎯 Tutorial Series OverviewA comprehensive tutorial series for learning robot control and motion analysis with the UnitreeG1 humanoid robot using LocoMuJoCo.A comprehensive tutorial series for learning robot control and motion analysis with the UnitreeG1 humanoid robot using LocoMuJoCo.

| Lesson | Title | Focus | Duration |

|--------|-------|--------|----------|

| **1.0** | [Setup & Installation Guide](lesson_1_0_setup_README.md) | **Install LocoMuJoCo with conda/uv** | 15-30 min |

| **1.1** | [Quick System Test](lesson_1_1_quick_test.py) | Verify installation and basic functionality | 5 min |### **Unit 1: Fundamentals (Lessons 1.0-1.10)**

| **1.2** | [Simple Walk Demo](lesson_1_2_simple_walk_test.py) | Watch robot walk with built-in motions | 8 min |

| **1.3** | [Basic Datasets](lesson_1_3_basic_datasets.py) | Explore default motion datasets | 10 min |*Learn the basics of robot operation, datasets, and analysis*

| **1.4** | [LAFAN1 Datasets](lesson_1_4_lafan1_datasets.py) | Advanced human motion capture data | 12 min |

| **1.5** | [Interactive Control](lesson_1_5_interactive_control.py) | **Control robot with keyboard** | 15 min |## 🎯 Tutorial Series Overview## 📋 Tutorial Overview

| **1.6** | [Motion Analysis](lesson_1_6_motion_analysis.py) | **Live graphs and motion science** | 15 min |

| **1.7** | [Dataset Explorer](lesson_1_7_dataset_explorer.py) | Browse and analyze motion collections | 12 min || Lesson | Title | Focus | Duration |

| **1.8** | [Test Utilities](lesson_1_8_test_utilities.py) | Automated testing and validation | 12 min |

| **1.9** | [Slow Motion Viewer](lesson_1_9_slow_motion_viewer.py) | Detailed motion frame analysis | 10 min ||--------|-------|--------|----------|

| **1.10** | [Complete Summary](lesson_1_10_complete_summary.py) | Review and next steps | 8 min |

| **1.0** | [📖 Setup & Installation Guide](lesson_1_0_setup_README.md) | **Install LocoMuJoCo with conda/uv** | 15-30 min |

## Featured Lessons

| **1.1** | [Quick System Test](lesson_1_1_quick_test.py) | Verify installation and basic functionality | 5 min |### **Unit 1: Fundamentals (Lessons 1.1-1.10)**### Tutorial 1: Basic Motion Datasets (`g1_01_basic_datasets.py`)

### Lesson 1.0 - Setup & Installation

- **Complete installation guide** with conda, uv, or pip| **1.2** | [Simple Walk Demo](lesson_1_2_simple_walk_test.py) | Watch robot walk with built-in motions | 8 min |

- **Environment management** best practices  

- **Graphics setup** for all operating systems| **1.3** | [Basic Datasets](lesson_1_3_basic_datasets.py) | Explore default motion datasets | 10 min |*Learn the basics of robot operation, datasets, and analysis***Focus: Default LocoMuJoCo Datasets**

- **Comprehensive troubleshooting** for common issues

| **1.4** | [LAFAN1 Datasets](lesson_1_4_lafan1_datasets.py) | Advanced human motion capture data | 12 min |

### Lesson 1.5 - Interactive Control

- **Real-time robot control** with keyboard| **1.5** | [Interactive Control](lesson_1_5_interactive_control.py) | **Control robot with keyboard** | 15 min |- Learn how to use built-in motion datasets with G1

- Control individual joints (w/s/a/d/q/e)

- Reset poses and quit safely| **1.6** | [Motion Analysis](lesson_1_6_motion_analysis.py) | **Live graphs and motion science** | 15 min |

- **No auto-closing** - control until you quit!

| **1.7** | [Dataset Explorer](lesson_1_7_dataset_explorer.py) | Browse and analyze motion collections | 12 min || Lesson | Title | Focus | Duration |- Available datasets: `walk`, `squat`, `stand`, `stepinplace`, `jump`, etc.

### Lesson 1.6 - Live Motion Analysis

- **Real-time data visualization** with graphs| **1.8** | [Test Utilities](lesson_1_8_test_utilities.py) | Automated testing and validation | 12 min |

- Joint positions, velocities, energy metrics

- **Live plotting** that updates during motion| **1.9** | [Slow Motion Viewer](lesson_1_9_slow_motion_viewer.py) | Detailed motion frame analysis | 10 min ||--------|-------|--------|----------|- Play motion capture data on the G1 robot

- Scientific motion analysis and interpretation

| **1.10** | [Complete Summary](lesson_1_10_complete_summary.py) | Review and next steps | 8 min |

### Lesson 1.8 - Test Utilities

- **100% automated testing suite**| **1.1** | [Quick System Test](lesson_1_1_quick_test.py) | Verify installation and basic functionality | 5 min |- Understand dataset configuration and replay

- Validates robot creation, datasets, performance

- Comprehensive debugging guides## 🌟 **Featured Lessons**

- Professional robot validation techniques

| **1.2** | [Simple Walk Demo](lesson_1_2_simple_walk_test.py) | Watch robot walk with built-in motions | 8 min |

## Quick Start

### 📖 **Lesson 1.0 - Setup & Installation** 

### First Time Setup

```bash- **Complete installation guide** with conda, uv, or pip| **1.3** | [Basic Datasets](lesson_1_3_basic_datasets.py) | Explore default motion datasets | 10 min |### Tutorial 2: LAFAN1 Motion Capture (`g1_02_lafan1_datasets.py`) 

# 1. Follow the complete setup guide

# Read: lesson_1_0_setup_README.md- **Environment management** best practices  



# 2. Install with conda (recommended)- **Graphics setup** for all operating systems| **1.4** | [LAFAN1 Datasets](lesson_1_4_lafan1_datasets.py) | Advanced human motion capture data | 12 min |**Focus: High-Quality Human Motion Data**

conda create -n locomujoco python=3.10 -y

conda activate locomujoco- **Comprehensive troubleshooting** for common issues

pip install loco-mujoco

| **1.5** | [Interactive Control](lesson_1_5_interactive_control.py) | **Control robot with keyboard** | 15 min |- Use LAFAN1 datasets with real human motion capture

# 3. Verify installation

python -c "import loco_mujoco; print('Ready!')"### 🎮 **Lesson 1.5 - Interactive Control** 

```

- **Real-time robot control** with keyboard| **1.6** | [Motion Analysis](lesson_1_6_motion_analysis.py) | **Live graphs and motion science** | 15 min |- Available motions: walking, dancing, running, obstacle navigation

### Start Learning

```bash- Control individual joints (w/s/a/d/q/e)

# Always activate environment first

conda activate locomujoco- Reset poses and quit safely| **1.7** | [Dataset Explorer](lesson_1_7_dataset_explorer.py) | Browse and analyze motion collections | 12 min |- Compare different human subjects' movement patterns



# Start with system verification- **No auto-closing** - control until you quit!

python lesson_1_1_quick_test.py

| **1.8** | [Test Utilities](lesson_1_8_test_utilities.py) | Automated testing and validation | 12 min |- Advanced motion retargeting to G1 skeleton

# Try interactive control (most popular!)

python lesson_1_5_interactive_control.py### 📊 **Lesson 1.6 - Live Motion Analysis**



# See live motion analysis- **Real-time data visualization** with graphs| **1.9** | [Slow Motion Viewer](lesson_1_9_slow_motion_viewer.py) | Detailed motion frame analysis | 10 min |

python lesson_1_6_motion_analysis.py

```- Joint positions, velocities, energy metrics



## Directory Structure- **Live plotting** that updates during motion| **1.10** | [Complete Summary](lesson_1_10_complete_summary.py) | Review and next steps | 8 min |### Tutorial 3: Interactive Control (`g1_03_interactive_control.py`)



```- Scientific motion analysis and interpretation

g1_tutorials/

├── lesson_1_0_setup_README.md    # Installation guide (START HERE!)**Focus: Manual G1 Control with Dataset Reference**

├── lesson_1_*_README.md          # Detailed guides for each lesson

├── lesson_1_*.py                 # Main tutorial lessons### 🧪 **Lesson 1.8 - Test Utilities**

├── README.md                     # This overview

├── DATASET_LOCATIONS.md          # Dataset information- **100% automated testing suite**## 🌟 **Featured Lessons**- Control G1 manually while using datasets as reference

├── VIEWER_SOLUTIONS.md           # Troubleshooting guide

├── archive/                      # Old experimental files- Validates robot creation, datasets, performance

├── development/                  # Development notes

├── media/                        # Videos and recordings- Comprehensive debugging guides- Test different control strategies and their stability

└── tools/                        # Utility scripts

```- Professional robot validation techniques



## Learning Path### 🎮 **Lesson 1.5 - Interactive Control** - Compare minimal movement vs. walking-like motions



### Prerequisites: Start with Setup (Lesson 1.0)## 🚀 **Quick Start**

- Read the complete installation guide

- Set up conda or uv environment  - **Real-time robot control** with keyboard- Real-time control with visual feedback

- Install LocoMuJoCo and dependencies

- Verify graphics and visualization### **First Time Setup**



### Beginner: Learn Basics (Lessons 1.1 → 1.3)```bash- Control individual joints (w/s/a/d/q/e)

- Verify your installation works

- Watch robot walking demonstrations# 1. Follow the complete setup guide

- Explore different motion datasets

- Understand imitation learning concepts# Read: lesson_1_0_setup_README.md- Reset poses and quit safely### Tutorial 4: Trajectory Generation (`g1_04_trajectory_generation.py`)



### Intermediate: Get Hands-On (Lessons 1.4 → 1.7)  

- Advanced human motion datasets

- **Interactive robot control with keyboard**# 2. Install with conda (recommended)- **No auto-closing** - control until you quit!**Focus: Custom Trajectory Creation and Analysis**

- **Scientific motion analysis with live graphs**

- Professional data exploration techniquesconda create -n locomujoco python=3.10 -y



### Advanced: Master the System (Lessons 1.8 → 1.10)conda activate locomujoco- Generate custom trajectories for G1 (standing, walking)

- Automated testing and validation

- Detailed frame-by-frame analysispip install loco-mujoco

- System debugging and optimization

- Ready for custom research projects### 📊 **Lesson 1.6 - Live Motion Analysis**- Analyze trajectory statistics and smoothness



## System Requirements# 3. Verify installation



- **Python**: 3.8, 3.9, 3.10, or 3.11 (NOT 3.12+)python -c "import loco_mujoco; print('✅ Ready!')"- **Real-time data visualization** with graphs- Create walking patterns with sinusoidal joint movements

- **OS**: Linux (recommended), macOS, Windows 10/11

- **RAM**: 8GB minimum, 16GB recommended```

- **Storage**: 10GB free space for datasets

- **Graphics**: Any modern GPU or integrated graphics- Joint positions, velocities, energy metrics- Export and replay custom trajectories

- **Internet**: Required for initial dataset downloads

### **Start Learning**

## Tips for Success

```bash- **Live plotting** that updates during motion

1. **Start with Setup** - Read `lesson_1_0_setup_README.md` first

2. **Follow in order** - Lessons build on each other# Always activate environment first

3. **Read the READMEs** - Each lesson has detailed instructions

4. **Try interactive lessons** - 1.5 and 1.6 are highlights  conda activate locomujoco- Scientific motion analysis and interpretation## 🗃️ Dataset Information

5. **Use the testing** - Lesson 1.8 has debugging guides

6. **Experiment** - Each lesson has experiment ideas

7. **Ask for help** - Check `VIEWER_SOLUTIONS.md`

# Start with system verification

## What You'll Learn

python lesson_1_1_quick_test.py

- **Environment Setup**: Professional Python development with conda/uv

- **Robot Control**: Direct robot manipulation and real-time control### 🧪 **Lesson 1.8 - Test Utilities**### Default Datasets (Built-in)

- **Motion Analysis**: Scientific analysis with live data visualization  

- **Dataset Usage**: Working with motion capture and trajectory data# Try interactive control (most popular!)

- **Visualization**: Real-time graphs, 3D rendering, and motion plotting

- **Testing**: Professional robot validation and debugging techniquespython lesson_1_5_interactive_control.py- **100% automated testing suite**These are automatically downloaded when first used:

- **System Integration**: Combining all components for research projects



## Ready for More?

# See live motion analysis- Validates robot creation, datasets, performance

After completing Unit 1, you'll be ready for:

- **Unit 2**: Custom environments and advanced control systemspython lesson_1_6_motion_analysis.py

- **Research Projects**: Motion learning and optimization algorithms

- **Real Robot Control**: Transfer learned skills to physical robots```- Comprehensive debugging guides| Dataset Name | Description | Use Case |

- **AI Development**: Reinforcement learning and neural network applications



## Important Notes

## 📁 **Directory Structure**- Professional robot validation techniques|--------------|-------------|----------|

### Python Version Compatibility

- **Supported**: Python 3.8, 3.9, 3.10, 3.11

- **Not Supported**: Python 3.7 and earlier, Python 3.12+

- **Recommended**: Python 3.10 for best compatibility```| `walk` | Standard walking gait | Basic locomotion |



### Environment Managementg1_tutorials/

- **Always use virtual environments** (conda, uv, or venv)

- **Never install globally** - causes dependency conflicts├── lesson_1_0_setup_README.md    # 📖 Installation guide (START HERE!)## 🚀 **Quick Start**| `squat` | Squatting motion | Strength poses |

- **Activate environment** before every session

├── lesson_1_*_README.md          # 📚 Detailed guides for each lesson

### Graphics Requirements

- OpenGL support required for 3D visualization├── lesson_1_*.py                 # 🤖 Main tutorial lessons| `stand` | Standing still | Balance reference |

- Update graphics drivers if you have rendering issues

- Software rendering available as fallback (`MUJOCO_GL=osmesa`)├── README.md                     # 📋 This overview



---├── DATASET_LOCATIONS.md          # 📦 Dataset information```bash| `stepinplace` | Step-in-place motion | Stationary gait |



**Start your robotics journey today!** ├── VIEWER_SOLUTIONS.md           # 🔧 Troubleshooting guide



1. **Read**: `lesson_1_0_setup_README.md` for installation├── archive/                      # 🗃️ Old experimental files# Start with the fundamentals| `walk_fast` | Fast walking | Dynamic locomotion |

2. **Begin**: `python lesson_1_1_quick_test.py` for first steps

3. **Enjoy**: Interactive robot control and live motion analysis!├── development/                  # 🛠️ Development notes

├── media/                        # 🎬 Videos and recordingspython lesson_1_1_quick_test.py| `walk_slow` | Slow walking | Stable locomotion |

└── tools/                        # ⚙️ Utility scripts

```| `jump` | Jumping motion | Dynamic movements |



## 🎓 **Learning Path**# Try interactive control (most popular!)



### **📖 Prerequisites**: Start with Setup (Lesson 1.0)python lesson_1_5_interactive_control.py### LAFAN1 Datasets (Motion Capture)

- Read the complete installation guide

- Set up conda or uv environment  High-quality human motion capture data:

- Install LocoMuJoCo and dependencies

- Verify graphics and visualization# See live motion analysis



### **🥾 Beginner**: Learn Basics (Lessons 1.1 → 1.3)python lesson_1_6_motion_analysis.py| Dataset Name | Description | Complexity |

- Verify your installation works

- Watch robot walking demonstrations```|--------------|-------------|------------|

- Explore different motion datasets

- Understand imitation learning concepts| `walk1_subject1` | Walking from subject 1 | ⭐⭐ |



### **🏃 Intermediate**: Get Hands-On (Lessons 1.4 → 1.7)  ## 📁 **Directory Structure**| `walk1_subject2` | Walking from subject 2 | ⭐⭐ |

- Advanced human motion datasets

- **Interactive robot control with keyboard**| `dance1_subject1` | Dance choreography 1 | ⭐⭐⭐⭐ |

- **Scientific motion analysis with live graphs**

- Professional data exploration techniques```| `dance2_subject4` | Dance choreography 2 | ⭐⭐⭐⭐⭐ |



### **🧪 Advanced**: Master the System (Lessons 1.8 → 1.10)g1_tutorials/| `run1_subject1` | Running pattern 1 | ⭐⭐⭐ |

- Automated testing and validation

- Detailed frame-by-frame analysis├── lesson_1_*.py          # Main tutorial lessons| `obstacles_subject2` | Obstacle navigation | ⭐⭐⭐⭐ |

- System debugging and optimization

- Ready for custom research projects├── README.md             # This overview



## 🔧 **System Requirements**├── DATASET_LOCATIONS.md  # Dataset information## 🚀 Quick Start



- **Python**: 3.8, 3.9, 3.10, or 3.11 (NOT 3.12+)├── VIEWER_SOLUTIONS.md   # Troubleshooting guide

- **OS**: Linux (recommended), macOS, Windows 10/11

- **RAM**: 8GB minimum, 16GB recommended├── archive/              # Old experimental files1. **Prerequisites**:

- **Storage**: 10GB free space for datasets

- **Graphics**: Any modern GPU or integrated graphics├── development/          # Development notes   ```bash

- **Internet**: Required for initial dataset downloads

├── media/               # Videos and recordings   conda activate unitree_mujoco

## 💡 **Tips for Success**

└── tools/               # Utility scripts   cd /path/to/loco-mujoco/examples/g1_tutorials

1. **📖 Start with Setup** - Read `lesson_1_0_setup_README.md` first

2. **🔄 Follow in order** - Lessons build on each other```   ```

3. **📚 Read the READMEs** - Each lesson has detailed instructions

4. **🎮 Try interactive lessons** - 1.5 and 1.6 are highlights  

5. **🧪 Use the testing** - Lesson 1.8 has debugging guides

6. **🔍 Experiment** - Each lesson has experiment ideas## 🎓 **Learning Path**2. **Run Basic Dataset Tutorial**:

7. **❓ Ask for help** - Check `VIEWER_SOLUTIONS.md`

   ```bash

## 🏆 **What You'll Learn**

### **Beginner**: Start with lessons 1.1 → 1.3   python g1_01_basic_datasets.py

- ✅ **Environment Setup**: Professional Python development with conda/uv

- ✅ **Robot Control**: Direct robot manipulation and real-time control- Learn basic robot operation   ```

- ✅ **Motion Analysis**: Scientific analysis with live data visualization  

- ✅ **Dataset Usage**: Working with motion capture and trajectory data- Understand datasets and motions

- ✅ **Visualization**: Real-time graphs, 3D rendering, and motion plotting

- ✅ **Testing**: Professional robot validation and debugging techniques- Get comfortable with the system3. **Try LAFAN1 Motion Capture**:

- ✅ **System Integration**: Combining all components for research projects

   ```bash

## 🚀 **Ready for More?**

### **Intermediate**: Continue with lessons 1.4 → 1.7     python g1_02_lafan1_datasets.py

After completing Unit 1, you'll be ready for:

- **Unit 2**: Custom environments and advanced control systems- Advanced motion datasets   ```

- **Research Projects**: Motion learning and optimization algorithms

- **Real Robot Control**: Transfer learned skills to physical robots- Interactive robot control

- **AI Development**: Reinforcement learning and neural network applications

- Scientific motion analysis## 📊 Dataset Storage Locations

## ⚠️ **Important Notes**

- Data exploration techniques

### **Python Version Compatibility**

- ✅ **Supported**: Python 3.8, 3.9, 3.10, 3.11When you run the tutorials, datasets are automatically downloaded to:

- ❌ **Not Supported**: Python 3.7 and earlier, Python 3.12+

- 🔧 **Recommended**: Python 3.10 for best compatibility### **Advanced**: Complete with lessons 1.8 → 1.10



### **Environment Management**- Professional testing methods- **Default Datasets**: `~/.loco_mujoco/DefaultDatasets/mocap/UnitreeG1/`

- **Always use virtual environments** (conda, uv, or venv)

- **Never install globally** - causes dependency conflicts- Detailed motion analysis- **LAFAN1 Datasets**: `~/.loco_mujoco/LAFAN1/UnitreeG1/`

- **Activate environment** before every session

- System validation- **Custom Trajectories**: Generated in memory or saved to specified paths

### **Graphics Requirements**

- OpenGL support required for 3D visualization- Ready for advanced projects

- Update graphics drivers if you have rendering issues

- Software rendering available as fallback (`MUJOCO_GL=osmesa`)## 🛠️ Troubleshooting



---## 🔧 **System Requirements**



**🎯 Start your robotics journey today!** ### Common Issues



1. **📖 Read**: `lesson_1_0_setup_README.md` for installation- **Python 3.8+** with LocoMuJoCo installed

2. **🚀 Begin**: `python lesson_1_1_quick_test.py` for first steps

3. **🎮 Enjoy**: Interactive robot control and live motion analysis!- **Graphics support** for visualization1. **ImportError: No module named 'jax'**

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