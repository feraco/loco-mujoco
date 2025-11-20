# Lesson 1.1: Quick System Test

## Learning Objectives

By the end of this lesson, you will:
- Verify your LocoMuJoCo installation works correctly
- Understand how to create robot environments
- Learn basic robot observation and action concepts
- See your first G1 robot simulation
- Confirm your system is ready for advanced tutorials

## What You'll Do

1. **Run system verification tests**
2. **Create your first G1 robot environment**
3. **Watch the robot perform basic movements**
4. **Learn about robot observations and actions**
5. **Confirm everything works for next lessons**

## Prerequisites

- LocoMuJoCo installed and working
- Python 3.8+ environment
- Graphics support for visualization

## Step-by-Step Instructions

### Step 1: Run the Lesson
```bash
cd /path/to/loco-mujoco/examples/g1_tutorials
python lesson_1_1_quick_test.py
```

**What happens**: The script automatically runs system verification tests.

### Step 2: Understanding the Output

#### System Verification Tests
You'll see tests like:
```
LocoMuJoCo import successful
Task factories available  
G1 robot model found
```

**What this means**: 
- **LocoMuJoCo import**: Core library is installed correctly
- **Task factories**: Robot creation tools are working
- **G1 robot model**: The UnitreeG1 robot files are available

#### Robot Environment Creation
You'll see:
```
Creating UnitreeG1 environment...
Environment created successfully
Action size: 23
Observation size: 60
```

**What this means**:
- **Action size 23**: The G1 robot has 23 controllable joints/motors
- **Observation size 60**: The robot provides 60 pieces of information (joint positions, velocities, etc.)

#### Visual Verification
A 3D window opens showing:
- **G1 humanoid robot**: Standing upright in simulation
- **Physics environment**: Ground plane and lighting
- **Real-time rendering**: Smooth 30+ FPS visualization

**What this means**: Your graphics and physics are working correctly.

#### Basic Movement Test
The robot performs:
```
Testing basic robot movement...
Step 1/10: Small random actions
Step 5/10: Robot responding to commands
Step 10/10: Movement test complete
```

**What this means**:
- **Small random actions**: Safe, tiny movements to test responsiveness
- **Robot responding**: Motors are working and physics is realistic
- **Movement test complete**: Basic control loop is functional

### Step 3: Understanding Robot Concepts

#### What are "Observations"?
Observations are sensor data the robot "sees":
- **Joint positions**: Where each joint currently is (in radians)
- **Joint velocities**: How fast each joint is moving
- **Body orientation**: Which way the robot is facing
- **Contact forces**: What the robot is touching

**Real example**: `obs[0]` might be -0.1 (left hip bent 0.1 radians backward)

#### What are "Actions"?
Actions are commands you send to the robot:
- **Joint torques**: How much force to apply to each motor
- **Target positions**: Where you want joints to move
- **Motor commands**: Direct electrical signals to actuators

**Real example**: `action[0] = 0.5` means "apply moderate force to first joint"

### Step 4: Interpreting Success
If you see:
```
SYSTEM VERIFICATION COMPLETE!
All systems operational
Ready for tutorials 1.2-1.10
```

**You're ready!** Your installation is perfect for all tutorials.

### Step 5: What If Something Fails?

#### Import Errors
```
ImportError: No module named 'loco_mujoco'
```
**Solution**: Reinstall LocoMuJoCo:
```bash
pip install loco-mujoco
```

#### Graphics Issues
```
Error: Could not create OpenGL context
```
**Solution**: Update graphics drivers or use software rendering:
```bash
export MUJOCO_GL=osmesa
python lesson_1_1_quick_test.py
```

#### Robot Model Missing
```
Error: UnitreeG1 model not found
```
**Solution**: Reinstall with complete models:
```bash
pip install --upgrade --force-reinstall loco-mujoco
```

## What You Learned

### Technical Concepts
- **Environment creation**: How to instantiate robot simulations
- **Observation space**: What information robots provide
- **Action space**: How to control robot movements
- **Physics simulation**: Real-time robot dynamics

### LocoMuJoCo Basics
- **RLFactory**: Creates reinforcement learning environments
- **UnitreeG1**: Specific humanoid robot model
- **Rendering**: 3D visualization system
- **Step function**: Core simulation update loop

### System Validation
- **Installation verification**: Confirming setup correctness
- **Hardware compatibility**: Graphics and processing capability
- **Model availability**: Robot assets and configurations
- **Performance baseline**: Simulation speed expectations

## Next Steps

### Ready for Lesson 1.2: Simple Walk Demo
- Watch pre-programmed walking motions
- Learn about trajectory playback
- See realistic humanoid locomotion

### Troubleshooting Resources
- Check `VIEWER_SOLUTIONS.md` for common issues
- Verify system requirements in main `README.md`
- Test graphics with: `python -c "import mujoco; print('MuJoCo OK')"`

### Experiment Ideas
1. **Try different robots**: Change "UnitreeG1" to "Atlas" or "UnitreeH1"
2. **Modify parameters**: Add `n_substeps=40` for smoother physics
3. **Observe details**: Print `env.observation_space` to see sensor details

## Key Takeaways
- **System verification is crucial** - always test first!
- **Robots are complex** - 23 joints, 60 observations is normal
- **Graphics matter** - visualization helps understand robot behavior
- **Small steps work** - gradual movement prevents instability

**You've successfully verified your robotics system!** Ready for more advanced lessons.