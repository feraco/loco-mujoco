<p align="center">
  <img width="70%" src="https://github.com/robfiras/loco-mujoco/assets/69359729/bd2a219e-ddfd-4355-8024-d9af921fb92a">
</p>

![continous integration](https://github.com/robfiras/loco-mujoco/actions/workflows/continuous_integration.yml/badge.svg?branch=dev)
[![Documentation Status](https://readthedocs.org/projects/loco-mujoco/badge/?version=latest)](https://loco-mujoco.readthedocs.io/en/latest/?badge=latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Join our Discord](https://img.shields.io/badge/Discord-Join%20Us-7289DA?style=flat&logo=discord&logoColor=white)](https://discord.gg/gEqR3xCVdn)

[//]: # ([![PyPI]&#40;https://img.shields.io/pypi/v/loco-mujoco&#41;]&#40;https://pypi.org/project/loco-mujoco/&#41;)

> 🚀 **Latest News:**
> A **major release (v1.0)** just dropped! 🎉  
> LocoMuJoCo now supports MJX and comes with new Jax algorithms. We also added many new environments and +22k datasets! 🚀   

> 🎓 **RoboUniversity Edition:**
> This fork includes enhanced teaching visualizations and tools for learning Unitree G1 programming with MuJoCo.
> Perfect for educational use and understanding humanoid robot locomotion!

## About This Project

**LocoMuJoCo** is an **imitation learning benchmark** specifically designed for **whole-body control**.  
It features a diverse set of environments, including **quadrupeds**, **humanoids**, and **(musculo-)skeletal human models**,
each provided with comprehensive datasets (over 22,000 samples per humanoid).

Although primarily focused on imitation learning, LocoMuJoCo also supports custom reward function classes,  
making it suitable for pure reinforcement learning as well.

### RoboUniversity: Learning Unitree G1 Programming

This repository is used at **RoboUniversity** to teach students how to program the **Unitree G1 humanoid robot** using MuJoCo simulation. Students learn to:

- 🤖 **Understand robot kinematics**: Visualize joint movements and body dynamics in real-time
- 🎭 **Explore motion capture data**: Learn from retargeted human motion datasets (LAFAN1, AMASS)
- 📊 **Analyze robot behavior**: Use interactive visualizations with Rerun and web interfaces
- 🧪 **Develop control algorithms**: Test locomotion strategies in a safe simulation environment
- 🎯 **Master imitation learning**: Train robots to replicate complex human movements

The included teaching tools provide professional visualizations perfect for classroom demonstrations and research presentations.

<div align="center">
  <img src="imgs/main_lmj.gif"/>
</div>

### Key Advantages 
✅ Supports **MuJoCo** (single environment) and **MJX** (parallel environments) \
✅ Includes **12 humanoid and 4 quadruped environments**, featuring 4 **biomechanical human models** \
✅ Clean single-file JAX algorithms for quick benchmarking (**PPO**, **GAIL**, **AMP**, **DeepMimic**)\
✅ Combined training and environment into one JIT‑compiled function for lightning‑fast training 🚀 \
✅ **Over 22,000 motion capture datasets** (AMASS, LAFAN1, native LocoMuJoCo) retargeted for each humanoid \
✅ **Robot-to-robot retargeting** allows to retarget any existing dataset from one robot to another \
✅ Powerful **trajectory comparison metrics** including dynamic time warping and discrete Fréchet distance, all in JAX \
✅ Interface for Gymnasium \
✅ Built-in **domain and terrain randomization** \
✅ Modular design: define, swap, and reuse components like observation types, reward functions, terminal state handlers, and domain randomization \
✅ [Documentation](https://loco-mujoco.readthedocs.io/)

---

## Installation

### Prerequisites

Before installing LocoMuJoCo, ensure you have:
- **Python 3.8+** (Python 3.10 or 3.11 recommended)
- **pip** package manager
- **Git** for cloning the repository

### Platform-Specific Requirements

#### macOS (Apple Silicon M1/M2/M3)
```bash
# Install Conda (if not already installed)
brew install --cask miniconda

# Create a Python environment
conda create -n loco-mujoco python=3.11
conda activate loco-mujoco

# Install required system dependencies
conda install -c conda-forge pinocchio
```

#### macOS (Intel)
```bash
# Create a Python environment
python3 -m venv loco-mujoco-env
source loco-mujoco-env/bin/activate

# You may need to install additional build tools
xcode-select --install
```

#### Linux (Ubuntu/Debian)
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install python3-dev python3-pip git build-essential

# Create a Python environment
python3 -m venv loco-mujoco-env
source loco-mujoco-env/bin/activate

# For Pinocchio support (optional, for advanced visualization)
sudo apt-get install robotpkg-py311-pinocchio
```

#### Windows
```bash
# Install via Anaconda (recommended for Windows)
conda create -n loco-mujoco python=3.11
conda activate loco-mujoco

# Install Visual Studio Build Tools if needed
# Download from: https://visualstudio.microsoft.com/downloads/
```

### Core Installation

Once prerequisites are met, install LocoMuJoCo:

```bash
# Clone the repository
git clone https://github.com/feraco/loco-mujoco.git
cd loco-mujoco

# Install in editable mode
pip install -e .
```

### GPU Support (Optional but Recommended)

For GPU-accelerated training with JAX:

```bash
# CUDA 12.x (NVIDIA GPUs)
pip install "jax[cuda12]"

# CUDA 11.x (older NVIDIA GPUs)
pip install "jax[cuda11]"
```

### Visualization Tools (For RoboUniversity Teaching)

Install additional packages for enhanced visualizations:

```bash
# For Rerun 3D visualization with actual robot meshes
conda install -c conda-forge pinocchio
pip install rerun-sdk trimesh

# For web-based interactive visualizations
pip install matplotlib numpy

# Verify installation
python -c "import loco_mujoco; print('LocoMuJoCo installed successfully!')"
```

### Advanced Features

> [!NOTE]
> If you want to run the **MyoSkeleton** environment, you need to additionally run:
> ```bash
> loco-mujoco-myomodel-init
> ```
> This accepts the license and downloads the musculoskeletal model.

### Troubleshooting

**Issue: Import errors for `mujoco` or `mujoco-mjx`**
```bash
pip install mujoco mujoco-mjx
```

**Issue: `pinocchio` not found (macOS)**
```bash
conda install -c conda-forge pinocchio
```

**Issue: NumPy version conflicts**
```bash
pip install "numpy<2.0"  # LocoMuJoCo works best with numpy 1.x
```

**Issue: Permission denied on Linux**
```bash
# Add user to render group for GPU access
sudo usermod -a -G render $USER
# Log out and back in for changes to take effect
```


### Datasets

LocoMuJoCo provides three sources of motion capture (mocap) data for humanoid environments: default (provided by us), LAFAN1, and AMASS. The first two datasets
are available on the [LocoMujoCo HuggingFace dataset repository](https://huggingface.co/datasets/robfiras/loco-mujoco-datasets)
and will be downloaded and cached automatically. AMASS needs to be downloaded and installed separately due to
licensing requirements. See [here](loco_mujoco/smpl) for more information about AMASS installation.

#### Quick Dataset Example

```python
from loco_mujoco.task_factories import ImitationFactory, LAFAN1DatasetConf, DefaultDatasetConf, AMASSDatasetConf

# Create environment with multiple datasets
env = ImitationFactory.make("UnitreeG1",
                            default_dataset_conf=DefaultDatasetConf(["walk", "squat"]),
                            lafan1_dataset_conf=LAFAN1DatasetConf(["dance2_subject4", "walk1_subject1"]),
                            # If SMPL and AMASS are installed:
                            #amass_dataset_conf=AMASSDatasetConf(["DanceDB/DanceDB/20120911_TheodorosSourmelis/Capoeira_Theodoros_v2_C3D_poses"])
                            )

# Visualize the loaded trajectories
env.play_trajectory(n_episodes=3, n_steps_per_episode=500, render=True)
```

#### RoboUniversity Teaching Visualizations

For educational purposes, we provide enhanced visualization tools:

**1. Complete Rerun Visualizer (3D Robot + Joint Data)**
```bash
cd LAFAN1_Retargeting_Dataset
python complete_g1_visualizer.py --file_name dance1_subject2 --robot_type g1 --playback_speed 0.01
```
This shows the actual G1 robot with meshes and joint angle time series in separate panels.

**2. Interactive Web Visualizer**
```bash
cd LAFAN1_Retargeting_Dataset
python web_teaching_interface.py --file_name dance1_subject2 --robot_type g1 --output robouniversity_visualizer.html
open robouniversity_visualizer.html
```
Click any joint value to see detailed time-series plots - perfect for teaching!

**3. Simple Joint Analysis**
```bash
cd LAFAN1_Retargeting_Dataset
python simple_rerun_visualizer.py --file_name dance1_subject2 --robot_type g1
```
Creates comprehensive matplotlib plots showing joint patterns and motion analysis.

#### Speeding up Dataset Loading
#### Speeding up Dataset Loading

LocoMuJoCo stores datasets with only joint positions and velocities to save memory. All other attributes are calculated 
using forward kinematics upon loading. To speed up dataset loading, you can define caches that store the forward kinematics results: 

```bash
loco-mujoco-set-all-caches --path "$HOME/.loco-mujoco-caches"
```

This significantly reduces loading time on subsequent runs, especially useful when working with large datasets like AMASS.

---

## Quick Start for Unitree G1 Programming

Perfect for students learning humanoid robot control:

### 1. Test Your Installation
```python
import loco_mujoco

# Create a simple G1 environment
env = loco_mujoco.LocoEnv.make("UnitreeG1")

# Reset and take random actions
obs = env.reset()
for _ in range(1000):
    action = env.action_space.sample()
    obs, reward, done, info = env.step(action)
    env.render()
```

### 2. Load and Visualize Motion Data
```python
from loco_mujoco.task_factories import ImitationFactory, LAFAN1DatasetConf

# Load G1 with dance dataset
env = ImitationFactory.make("UnitreeG1",
                            lafan1_dataset_conf=LAFAN1DatasetConf(["dance1_subject2"]))

# Watch the robot perform the motion
env.play_trajectory(n_episodes=1, n_steps_per_episode=500, render=True)
```

### 3. Analyze Robot Movements
```bash
# Navigate to the teaching dataset folder
cd LAFAN1_Retargeting_Dataset

# Launch the complete visualizer with actual robot meshes
python complete_g1_visualizer.py --file_name dance1_subject2 --robot_type g1 --playback_speed 0.01
```

This opens Rerun with:
- 🤖 Full 3D G1 robot with actual meshes
- 📊 Real-time joint angle graphs
- 🎯 Grouped analysis (legs, arms, torso)
- 📈 Motion analysis and velocity data

### 4. Interactive Web Teaching Tool
```bash
# Generate interactive HTML visualization
python web_teaching_interface.py --file_name dance1_subject2 --robot_type g1 --output my_visualization.html

# Open in browser
open my_visualization.html
```

Perfect for presentations - click any joint to see its detailed behavior over time!

---

## Environments 
You want a quick overview of all **environments** available? You can find it 
[here](/loco_mujoco/environments) and more detailed in the [Documentation](https://loco-mujoco.readthedocs.io/).

<div align="center">
  <img src="imgs/lmj_envs.gif"/>
</div>

And stay tuned! There are many more to come ...

---

## Tutorials

We provide a set of tutorials to help you get started with LocoMuJoCo. You can find them in the [tutorials folder](./examples/tutorials)
or with more explanation in the [documentation](https://loco-mujoco.readthedocs.io/).

If you want to check out training examples of a PPO, GAIL, AMP, or DeepMimic agent, you can find them 
in the [training examples folder](./examples/training_examples). For instance, [here](./examples/training_examples/jax_rl_mimic) is an example of a DeepMimic agent
you can train to achieve a human-like walking in all directions, which was trained in 36 min on an RTX 3080 Ti:

<div align="center">
  <img src="imgs/unitree_h1_walk_anydir.gif"/>
</div>

---
## Citation
```
@inproceedings{alhafez2023b,
title={LocoMuJoCo: A Comprehensive Imitation Learning Benchmark for Locomotion},
author={Firas Al-Hafez and Guoping Zhao and Jan Peters and Davide Tateo},
booktitle={6th Robot Learning Workshop, NeurIPS},
year={2023}
}
```




