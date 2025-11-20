# 🤖 LocoMuJoCo Simplified Tutorials

**Learn humanoid robotics and AI through hands-on interactive tutorials!**

## 🎯 What These Tutorials Teach

These tutorials are designed to be **educational**, **interactive**, and **visually stunning**. Each one builds your understanding step-by-step:

1. **🚀 Tutorial 1: Your First Robot** - Create and watch humanoid robots perform human motions
2. **🎮 Tutorial 2: Interactive Control** - Learn how robots are controlled and why good control matters  
3. **📊 Tutorial 3: Data Analysis** - Analyze robot behavior scientifically with beautiful visualizations

## 🎬 What to Expect

✅ **Beautiful 3D robot simulations** with realistic physics  
✅ **Clear explanations** of every concept as you go  
✅ **Interactive demonstrations** you can modify and experiment with  
✅ **Visual data analysis** with plots and charts  
✅ **Practical learning** about AI, robotics, and machine learning  

## 🚀 Quick Start

### Prerequisites
Make sure you have LocoMuJoCo properly installed:

```bash
# Install LocoMuJoCo with correct dependencies
cd /path/to/loco-mujoco
pip install mujoco==3.2.7 mujoco-mjx==3.2.7
pip install -e .
pip install matplotlib seaborn wandb imageio imageio-ffmpeg
```

### Run Your First Tutorial

```bash
cd examples/g1_tutorials
python tutorial_01_your_first_robot.py
```

**What you'll see:**
- A beautiful 3D UnitreeG1 humanoid robot
- Realistic walking, squatting, and jumping motions
- Clear explanations of how imitation learning works

## 📚 Tutorial Details

### 🤖 Tutorial 1: Your First Robot
**File:** `tutorial_01_your_first_robot.py`  
**Duration:** ~3 minutes  
**Concepts:** Robot creation, imitation learning, motion capture data  

**You'll Learn:**
- What LocoMuJoCo is and why it's useful
- How robots learn from human motion data  
- Different types of locomotion (walking, squatting, jumping)
- Basic robotics concepts (joints, sensors, physics)

**Visual Highlights:**
- UnitreeG1 robot performing human-like motions
- Real-time 3D physics simulation
- Interactive viewer controls (pause, restart, camera)

---

### 🎮 Tutorial 2: Interactive Control  
**File:** `tutorial_02_interactive_control.py`  
**Duration:** ~4 minutes  
**Concepts:** Robot control, feedback loops, control strategies  

**You'll Learn:**
- How robots are controlled with motor commands
- The difference between observations (sensors) and actions (motors)
- Why random control fails and smart control succeeds
- How feedback from sensors enables good control

**Visual Highlights:**
- Side-by-side comparison of control strategies
- Real-time performance metrics and robot state analysis
- Dramatic demonstration of good vs bad control

---

### 📊 Tutorial 3: Data Analysis & Visualization
**File:** `tutorial_03_data_analysis.py`  
**Duration:** ~5 minutes  
**Concepts:** Data science, motion analysis, scientific evaluation  

**You'll Learn:**
- How to extract quantitative data from robot simulations
- Statistical analysis of different motion types
- Creating beautiful data visualizations and plots
- Scientific methods for evaluating robot performance

**Visual Highlights:**
- Real-time plots of joint angles, positions, and performance metrics
- Comparative analysis dashboard with multiple charts
- Beautiful matplotlib visualizations (or ASCII art if no matplotlib)

## 🎮 Interactive Features

### Viewer Controls
All tutorials include an interactive 3D viewer:
- **SPACEBAR** - Pause/Resume simulation
- **R** - Restart current demonstration  
- **ESC** - Exit viewer
- **Mouse** - Rotate camera, zoom in/out

### Customization Options
Each tutorial includes suggestions for modifications:
- Try different robots (UnitreeH1, Atlas, etc.)
- Experiment with different motion datasets
- Adjust simulation parameters for different effects
- Add your own analysis and visualizations

## 🔧 Troubleshooting

### Common Issues

**Error: "Need at least one array to concatenate"**
- Solution: Make sure you have internet connection for dataset downloads
- Try running the tutorial again - datasets are cached after first download

**Error: Import issues with matplotlib/numpy/jax**
- Solution: Reinstall dependencies: `pip install matplotlib numpy jax`
- These are linting errors - the code will still run

**Error: Robot falls immediately** 
- This is expected in Tutorial 2 with random control!
- The tutorial explains why this happens and shows better strategies

**Slow performance or lag**
- Reduce `n_substeps` parameter for faster simulation
- Close other applications to free up system resources

### Getting Help

1. **Check the console output** - tutorials provide detailed error messages and suggestions
2. **Try the fallback modes** - most tutorials have backup strategies if primary methods fail  
3. **Modify parameters** - experiment with different settings to see what works
4. **Check the original examples** - reference the existing `g1_*.py` files for comparison

## 🎓 Educational Philosophy

These tutorials follow **learning by doing** principles:

1. **Show, Don't Just Tell** - Every concept is demonstrated visually
2. **Build Intuition First** - Understand the "why" before diving into technical details  
3. **Encourage Experimentation** - Suggestions for modifications and explorations
4. **Real-World Context** - Connect concepts to actual robotics research and applications
5. **Progressive Complexity** - Each tutorial builds on the previous ones

## 🏆 Next Steps

After completing these tutorials, you'll be ready to:

- Explore advanced LocoMuJoCo features (LAFAN1, AMASS datasets)
- Learn about reinforcement learning and policy optimization
- Train your own robot controllers from scratch
- Dive into research papers on locomotion and imitation learning
- Contribute to open-source robotics projects

## 📖 Additional Resources

- **[LocoMuJoCo Documentation](https://loco-mujoco.readthedocs.io/)** - Complete API reference
- **[Original Examples](.)** - More advanced examples and use cases
- **[MuJoCo Documentation](https://mujoco.readthedocs.io/)** - Physics simulation details  
- **[JAX Documentation](https://jax.readthedocs.io/)** - Machine learning framework

---

*Made with ❤️ for the robotics and AI community. Happy learning!* 🤖✨