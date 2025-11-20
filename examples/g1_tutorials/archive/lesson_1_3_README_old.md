# 📦 Lesson 1.3: Basic Datasets

## 🎯 **Learning Objectives**
By the end of this lesson, you will:
- ✅ Explore all built-in LocoMuJoCo motion datasets
- ✅ Understand different types of robot movements
- ✅ Learn dataset configuration and selection
- ✅ Compare locomotion vs. manipulation motions
- ✅ Master dataset loading and switching techniques

## 📋 **What You'll Do**
1. **Load multiple motion datasets**
2. **Watch different types of robot behaviors**
3. **Learn about motion categories and purposes**
4. **Configure dataset parameters**
5. **Compare movement quality and characteristics**

## 🔧 **Prerequisites**
- Completed Lessons 1.1-1.2
- Understanding of imitation learning
- Familiarity with basic robot concepts

## 📖 **Step-by-Step Instructions**

### **Step 1: Run the Lesson**
```bash
cd /path/to/loco-mujoco/examples/g1_tutorials
python lesson_1_3_basic_datasets.py
```

**What happens**: The script demonstrates 6 different motion types with detailed analysis.

### **Step 2: Understanding Motion Categories**

#### **🏃 Locomotion Motions**
These move the robot from place to place:

**1. Walking (`walk`)**
```
🚶 WALKING MOTION
📝 Purpose: Basic forward locomotion
⏱️ Duration: ~20 minutes of data
🎯 Use case: Navigation, exploration
```
- **Speed**: Moderate (1-2 m/s)
- **Stability**: High - very stable gait
- **Energy**: Low - efficient movement
- **Complexity**: Medium - coordinated limbs

**2. Running (`run`)**  
```
🏃 RUNNING MOTION  
📝 Purpose: Fast locomotion with flight phases
⏱️ Duration: ~5 minutes of data
🎯 Use case: Rapid movement, sports
```
- **Speed**: High (3-6 m/s)
- **Stability**: Medium - dynamic balance required
- **Energy**: High - intensive movement
- **Complexity**: High - precise timing needed

**3. Step in Place (`stepinplace`)**
```
🦶 STEP IN PLACE
📝 Purpose: Maintain gait without forward motion
⏱️ Duration: ~3 minutes of data  
🎯 Use case: Waiting, preparation, transitions
```
- **Speed**: Zero - no forward movement
- **Stability**: Very high - minimal risk
- **Energy**: Low - minimal effort
- **Complexity**: Low - simple pattern

#### **🤸 Athletic/Exercise Motions**

**4. Jumping (`jump`)**
```
🦘 JUMPING MOTION
📝 Purpose: Vertical movement and landing
⏱️ Duration: ~2 minutes of data
🎯 Use case: Obstacle clearing, sports
```
- **Speed**: Variable - explosive then controlled
- **Stability**: Low during flight, high on landing
- **Energy**: Very high - explosive movement
- **Complexity**: Very high - ballistic motion

**5. Squatting (`squat`)**
```
🏋️ SQUATTING MOTION
📝 Purpose: Up-down exercise movement
⏱️ Duration: ~4 minutes of data
🎯 Use case: Exercise, strength training
```
- **Speed**: Slow - controlled movement
- **Stability**: High - grounded throughout
- **Energy**: Medium - strength-focused
- **Complexity**: Medium - balance + strength

#### **🧘 Static/Maintenance Motions**

**6. Standing (`stand`)**
```
🧍 STANDING MOTION
📝 Purpose: Stable upright posture
⏱️ Duration: ~10 minutes of data
🎯 Use case: Idle state, observation
```
- **Speed**: Zero - no movement
- **Stability**: Very high - designed for stability  
- **Energy**: Very low - minimal effort
- **Complexity**: Low - balance only

### **Step 3: Dataset Loading Process**

#### **📊 Dataset Information Display**
For each motion, you'll see:
```
============================================================
🚶 ANALYZING: Walking Motion
📝 Type: Locomotion
📋 Description: Natural forward walking gait
============================================================
📦 Loading dataset: walk
100%|████████████| 35198/35198 [00:08<00:00, 4000.00it/s]
✅ Dataset loaded: 35,198 frames
⏱️ Duration: 19.5 minutes
🎬 Frame rate: 30 FPS
```

**Understanding the numbers**:
- **Frame count**: Total number of robot positions recorded
- **Duration**: Real-time length if played at normal speed
- **Frame rate**: Positions per second (30 FPS = smooth motion)
- **Data size**: Larger = more variety and examples

#### **🔄 Motion Demonstration**
```
🎬 Playing motion preview (10 seconds)...
Progress: 100%|███████| 300/300 [00:10<00:00, 30.0it/s]
✅ Motion preview complete
```

**What's happening**:
- **10-second preview**: Short sample to show motion character
- **300 frames**: 10 seconds × 30 FPS = 300 positions
- **Real-time playback**: Natural speed demonstration

### **Step 4: Motion Analysis and Comparison**

#### **🔍 Movement Characteristics**
Watch for these differences between motions:

**Walking vs. Running**:
- **Walking**: Always one foot on ground, smooth rhythm
- **Running**: Flight phases (both feet off ground), bouncy rhythm

**Athletic vs. Locomotion**:
- **Athletic** (jump, squat): Explosive power, specific patterns
- **Locomotion** (walk, run): Continuous, cyclical patterns

**Dynamic vs. Static**:
- **Dynamic** (run, jump): Rapid changes, high accelerations
- **Static** (stand, stepinplace): Minimal movement, stability focus

#### **⚖️ Quality Assessment**
For each motion, evaluate:

**Technical Quality**:
- **Smoothness**: No jerky or unnatural movements
- **Realism**: Matches human/robot capabilities
- **Stability**: Doesn't fall or lose balance
- **Repeatability**: Consistent when replayed

**Functional Quality**:
- **Purpose achievement**: Accomplishes intended goal
- **Efficiency**: Reasonable energy expenditure  
- **Naturalness**: Looks like real human/robot motion
- **Adaptability**: Could work in different contexts

### **Step 5: Dataset Configuration**

#### **🛠️ Basic Configuration**
```python
# How the datasets are loaded:
env = ImitationFactory.make(
    "UnitreeG1",
    default_dataset_conf=DefaultDatasetConf(["walk"]),  # Single motion
    n_substeps=20
)
```

**Configuration options**:
- **Single motion**: `["walk"]` - just walking
- **Multiple motions**: `["walk", "run", "jump"]` - random selection
- **All motions**: `["walk", "run", "jump", "squat", "stand", "stepinplace"]`

#### **🎛️ Advanced Parameters**
```python
# More detailed configuration:
dataset_conf = DefaultDatasetConf(
    motions=["walk", "run"],     # Which motions to include
    min_length=100,              # Minimum episode length
    max_length=2000,             # Maximum episode length  
    shuffle=True                 # Random order selection
)
```

**Parameter meanings**:
- **motions**: List of motion types to use
- **min_length**: Shortest sequence (frames)
- **max_length**: Longest sequence (frames)
- **shuffle**: Random vs. sequential selection

### **Step 6: Practical Applications**

#### **🎯 When to Use Each Motion**

**Walking**: 
- ✅ **Navigation tasks**: Moving between locations
- ✅ **Exploration**: Searching environments
- ✅ **Daily activities**: Most common locomotion need

**Running**:
- ✅ **Emergency response**: Rapid movement required  
- ✅ **Sports/games**: Athletic activities
- ✅ **Time-critical tasks**: Speed over efficiency

**Jumping**:
- ✅ **Obstacle avoidance**: Getting over barriers
- ✅ **Terrain navigation**: Uneven surfaces
- ✅ **Athletic performance**: Sports applications

**Squatting**:
- ✅ **Object manipulation**: Picking up low items
- ✅ **Strength training**: Exercise routines
- ✅ **Height adjustment**: Accessing different levels

**Standing**:
- ✅ **Observation tasks**: Watching/monitoring
- ✅ **Idle state**: Default position when not active
- ✅ **Preparation**: Before starting other motions

**Step in Place**:
- ✅ **Waiting**: Maintaining readiness without movement
- ✅ **Transitions**: Between different motion types
- ✅ **Balance practice**: Maintaining coordination

## 🎓 **What You Learned**

### **Motion Classification**
- **Locomotion**: Walking, running, step-in-place
- **Athletic**: Jumping, squatting
- **Static**: Standing
- **Quality metrics**: Smoothness, stability, naturalness

### **Dataset Management**  
- **Loading process**: How motion data is accessed
- **Configuration options**: Selecting and combining motions
- **Performance considerations**: Data size vs. variety trade-offs
- **Quality assessment**: Evaluating motion effectiveness

### **Practical Applications**
- **Task matching**: Choosing appropriate motions for goals
- **Behavior sequencing**: Combining different motion types
- **Performance optimization**: Balancing speed vs. stability
- **System integration**: Using motions in larger applications

## 🚀 **Next Steps**

### **Ready for Lesson 1.4**: LAFAN1 Datasets
- Explore advanced human motion capture data
- Learn about retargeting human motions to robots
- Access professional dance and complex movements

### **Experiment Ideas**
1. **Motion mixing**: Try combining multiple dataset types
2. **Performance comparison**: Time each motion type
3. **Stability analysis**: Which motions are most/least stable
4. **Energy estimation**: Observe which require most effort

### **Troubleshooting**

#### **❌ Dataset Loading Fails**
```
Error: Could not load dataset 'walk'
```
**Solutions**:
1. Check internet connection for initial download
2. Clear cache: `rm -rf ~/.loco-mujoco-caches`
3. Retry: `python lesson_1_3_basic_datasets.py`

#### **❌ Motion Looks Unnatural**
```
Robot movement seems robotic or jerky
```
**Possible causes**:
- Graphics performance issues
- Dataset corruption
- Physics timestep problems

**Solutions**:
- Reduce graphics quality: `export MUJOCO_GL=osmesa`
- Re-download datasets
- Check system performance

#### **❌ Slow Playback**
```
Motion preview takes too long
```
**Solutions**:
- Close other applications
- Reduce preview duration in code
- Use faster hardware if available

## 💡 **Key Takeaways**
- ✅ **Different motions serve different purposes** - choose wisely
- ✅ **Dataset quality varies** - some motions are more polished
- ✅ **Configuration matters** - parameters affect behavior significantly
- ✅ **Observation skills develop** - you're learning to evaluate robot motion

**🎯 You now understand the full range of basic robot motions!** Ready for advanced human motion data.