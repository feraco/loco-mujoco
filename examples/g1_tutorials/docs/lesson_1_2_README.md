# Lesson 1.2: Simple Walk Demo

## Learning Objectives

By the end of this lesson, you will:
- Understand imitation learning vs. reinforcement learning
- Learn how to load and play motion datasets  
- Watch realistic humanoid walking gaits
- Understand trajectory playback systems
- See the difference between RL and imitation environments

## What You'll Do

1. **Create an imitation learning environment**
2. **Load the default "walk" dataset**
3. **Watch the G1 robot perform natural walking**
4. **Learn about motion capture data**
5. **Compare RL vs. imitation approaches**

## Prerequisites

- Completed Lesson 1.1 (system verification)
- Understanding of basic robot concepts
- Working graphics for 3D visualization

## Step-by-Step Instructions

### Step 1: Run the Lesson
```bash
cd /path/to/loco-mujoco/examples/g1_tutorials
python lesson_1_2_simple_walk_test.py
```

### Step 2: What You Should See

When you run the lesson, you will observe:

1. **Console Output**:
   ```
   Loading imitation environment with walk dataset...
   Walk dataset loaded successfully
   Dataset contains 500 timesteps
   Starting walking demonstration...
   Playing trajectory...
   Demo complete!
   ```

2. **3D Visualization Window**:
   - G1 robot starts in natural standing pose
   - Robot performs smooth, coordinated walking motion
   - Natural arm swinging and leg coordination
   - Stable forward locomotion
   - Realistic human-like gait pattern

### Step 3: Understanding the Concepts

#### Imitation Learning vs. Reinforcement Learning

**Imitation Learning**:
- Goal: Reproduce existing movement patterns
- Method: Learn from demonstrations
- Speed: Fast (no training needed)
- Quality: High (based on expert demonstrations)

**Reinforcement Learning**:
- Goal: Learn through trial and error
- Method: Reward-based optimization
- Speed: Slow (extensive training required)
- Quality: Variable (can be very good or poor)

#### Motion Dataset Structure

**What you're seeing**:
```
Walk Dataset:
- Duration: 10 seconds
- Frequency: 50 Hz (50 frames per second)
- Total frames: 500 timesteps
- Joint data: All 23 joints per timestep
- Format: [timestep, joint_positions[23]]
```

**Key Components**:
- **Joint trajectories**: Precise angles for each joint over time
- **Temporal coordination**: Synchronized movement across all joints  
- **Natural dynamics**: Physics-based realistic motion
- **Cyclic patterns**: Repeating walking cycles

### Step 4: Motion Analysis

#### Natural Walking Features

**Gait Characteristics**:
- Heel-to-toe foot placement
- Coordinated arm and leg swinging
- Stable torso with minimal wobble
- Natural stride length and frequency
- Smooth weight transfer between feet

**Technical Metrics**:
- Walking speed: ~1.2 m/s
- Step length: ~0.65 meters
- Step frequency: ~1.8 Hz
- Joint smoothness: <0.05 rad/s jerk
- Balance stability: Center of mass within support

#### Comparison with Random Actions

**Imitation (this lesson)**:
- Coordinated, purposeful movement
- Natural-looking walking gait
- Stable and balanced
- Predictable forward motion
- Human-like characteristics

**Random Actions (Lesson 1.1)**:
- Chaotic, uncoordinated movement
- No clear direction or purpose
- Often unstable or falling
- Jerky, unrealistic motions
- No resemblance to natural walking

### Step 5: Understanding the Code

#### Environment Creation
```python
from loco_mujoco import ImitationFactory
from loco_mujoco.datasets import DefaultDatasetConf

# Create imitation environment with walking data
env = ImitationFactory.make(
    "UnitreeG1",
    default_dataset_conf=DefaultDatasetConf(["walk"])
)
```

#### Trajectory Playback
```python
# Get a sample trajectory from the dataset
trajectory = env.sample_trajectory()

# Play back the trajectory step by step
for timestep in trajectory:
    obs = env.reset_to_state(timestep)  # Set exact robot pose
    env.render()                        # Display current position
    time.sleep(1/50)                   # Control playback speed
```

## Technical Details

### Dataset Information
- **Source**: High-quality motion capture data
- **Collection**: Professional mocap studio recording
- **Processing**: Retargeted to G1 robot skeleton
- **Validation**: Physics simulation verified
- **Quality**: Smooth, natural human movement

### Imitation Learning Benefits
- **Immediate results**: No training time required
- **High quality**: Based on expert demonstrations
- **Predictable**: Consistent behavior every time
- **Fast setup**: Ready to use in seconds
- **Realistic**: Natural-looking movement

### Imitation Learning Limitations
- **Fixed patterns**: Cannot adapt to new situations
- **No creativity**: Only replays existing motions
- **Dataset dependent**: Quality limited by source data
- **Generalization**: May not work in different environments

### Reinforcement Learning Comparison
**Benefits**:
- **Adaptable**: Can learn new behaviors
- **Creative**: Might discover novel movement patterns
- **Flexible**: Can handle various environments

**Drawbacks**:
- **Training time**: Hours or days to learn basic walking
- **Unstable**: Often falls during learning process
- **Unpredictable**: Results vary between training runs

## Troubleshooting

### Common Issues

**Problem**: Robot doesn't move or moves erratically
**Solution**: Check dataset loading
```python
# Verify trajectory data
traj = env.sample_trajectory()
print(f"Trajectory shape: {traj.shape}")
print(f"Duration: {len(traj)} timesteps")
```

**Problem**: Very slow movement
**Solution**: Adjust playback speed
```python
# Increase playback speed
time.sleep(1/100)  # 10x faster

# Decrease for detailed observation
time.sleep(1/25)   # 2x slower
```

**Problem**: "Dataset not found" error
**Solution**: Check dataset installation
```bash
# Verify dataset cache
ls ~/.loco-mujoco-caches/
# Should show default dataset files

# Re-download if missing
loco-mujoco-set-all-caches --path "$HOME/.loco-mujoco-caches"
```

**Problem**: Window opens but robot doesn't appear
**Solution**: Check model loading
```bash
# Test basic environment creation
python -c "
from loco_mujoco import ImitationFactory
from loco_mujoco.datasets import DefaultDatasetConf
env = ImitationFactory.make('UnitreeG1', default_dataset_conf=DefaultDatasetConf(['walk']))
print('Environment created successfully')
"
```

## What You Learned

### Key Concepts
- **Imitation learning**: Learning from demonstrations
- **Motion datasets**: Collections of recorded movements
- **Trajectory playback**: Replaying recorded motions
- **Natural movement**: Characteristics of realistic walking

### Technical Skills
- Creating imitation learning environments
- Loading and using motion datasets
- Understanding dataset structure and format
- Analyzing motion quality and realism

### Comparative Understanding
- Imitation vs. reinforcement learning tradeoffs
- Advantages of demonstration-based learning
- Limitations of fixed trajectory playback
- Quality differences between approaches

## What's Next

After completing this lesson:
- **Lesson 1.3**: Explore multiple motion types (walk, run, sit, stand)
- **Lesson 1.4**: Advanced LAFAN1 human motion capture datasets  
- **Lesson 1.5**: Interactive robot control with keyboard input
- **Lesson 1.6**: Scientific motion analysis with live data visualization

## Key Takeaways

- Imitation learning provides immediate, high-quality results
- Motion datasets contain rich information about natural movement
- Trajectory playback is fundamental to imitation learning
- Quality of demonstrations directly impacts robot performance
- Both imitation and reinforcement learning have important roles

**Natural walking is remarkably complex - imitation learning makes it accessible immediately!**

This lesson demonstrates how robots can perform sophisticated movements by learning from high-quality demonstrations rather than starting from scratch.