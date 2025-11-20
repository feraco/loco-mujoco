# G1 Dataset Locations and Availability Guide

## 🎯 **CONFIRMED WORKING G1 DATASETS**

Based on testing, only **3 datasets** are currently available for UnitreeG1:

### ✅ **Available Default Datasets:**
1. **`walk`** - Natural walking motion (35,198 trajectories)
2. **`squat`** - Squatting exercise motion (2,398 trajectories) 
3. **`run`** - Running motion pattern (8,718 trajectories)

### ❌ **Unavailable Datasets (404 Errors):**
- `stand` - Standing posture
- `stepinplace` - Stepping in place
- `walk_fast` - Fast walking
- `walk_slow` - Slow walking  
- `jump` - Jumping motion
- `sit` - Sitting motion
- `lie` - Lying down motion

## 📍 **Dataset Storage Locations**

### **Online Source:**
- **HuggingFace Repository**: https://huggingface.co/datasets/robfiras/loco-mujoco-datasets
- **Direct URLs**:
  - Walk: `https://huggingface.co/datasets/robfiras/loco-mujoco-datasets/resolve/main/DefaultDatasets/mocap/UnitreeG1/walk.npz`
  - Squat: `https://huggingface.co/datasets/robfiras/loco-mujoco-datasets/resolve/main/DefaultDatasets/mocap/UnitreeG1/squat.npz`
  - Run: `https://huggingface.co/datasets/robfiras/loco-mujoco-datasets/resolve/main/DefaultDatasets/mocap/UnitreeG1/run.npz`

### **Local Cache (After Download):**
```bash
# Main cache directory
~/.cache/huggingface/hub/datasets--robfiras--loco-mujoco-datasets/

# Alternative locations to check:
~/.loco_mujoco/
/tmp/loco_mujoco_cache/
```

### **In Your Project:**
```bash
/Users/wwhs-research/Downloads/humsim/loco-mujoco/examples/g1_tutorials/
```

## 🎭 **LAFAN1 Datasets (Motion Capture)**

LAFAN1 datasets are separate and may have better availability:

### **Working LAFAN1 Datasets:**
- `walk1_subject1` - Human walking capture 1
- `walk1_subject2` - Human walking capture 2  
- `walk1_subject5` - Human walking capture 5
- `dance1_subject1` - Dance choreography 1
- `dance2_subject4` - Dance choreography 2
- `run1_subject1` - Running motion 1

### **LAFAN1 Source:**
- **Original**: https://github.com/ubisoft/ubisoft-laforge-animation-dataset
- **LocoMuJoCo Version**: Processed for humanoid robots

## 🔧 **How to Use Available Datasets**

### **Safe Tutorial Code:**
```python
from loco_mujoco.task_factories import ImitationFactory, DefaultDatasetConf

# Use ONLY confirmed working datasets
env = ImitationFactory.make("UnitreeG1",
                           default_dataset_conf=DefaultDatasetConf([
                               "walk",   # ✅ Works
                               "squat",  # ✅ Works  
                               "run"     # ✅ Works
                           ]))
```

### **Individual Dataset Testing:**
```python
# Test one dataset at a time
datasets_to_try = ["walk", "squat", "run"]

for dataset in datasets_to_try:
    try:
        env = ImitationFactory.make("UnitreeG1",
                                   default_dataset_conf=DefaultDatasetConf([dataset]))
        print(f"✅ {dataset} works!")
    except Exception as e:
        print(f"❌ {dataset} failed: {e}")
```

## 🔍 **Finding Additional Datasets**

### **Option 1: Check Other Robots**
```bash
# Go through different robot types in LocoMuJoCo
cd /Users/wwhs-research/Downloads/humsim/loco-mujoco/loco_mujoco/environments/
ls -la  # Look for other humanoid robots
```

### **Option 2: Browse HuggingFace Repository**
1. Visit: https://huggingface.co/datasets/robfiras/loco-mujoco-datasets/tree/main
2. Navigate to: `DefaultDatasets/mocap/`
3. Check available robot folders
4. Look for `.npz` files

### **Option 3: Create Custom Datasets**
```python
# You can record your own motions
env = ImitationFactory.make("UnitreeG1")
# Record trajectories using env.reset(), env.step(), etc.
```

## 🚀 **Recommended Usage**

### **For Stable Demos:**
```python
# Most reliable combination
DefaultDatasetConf(["walk", "squat"])  # 2 different motion types
```

### **For Variety:**
```python  
# All available datasets
DefaultDatasetConf(["walk", "squat", "run"])  # 3 motion types
```

### **For Specific Motions:**
```python
# Just walking (most stable)
DefaultDatasetConf(["walk"])

# Just dynamic motion
DefaultDatasetConf(["run"])
```

## 📊 **Dataset Statistics**

| Dataset | Trajectories | Motion Type | Stability |
|---------|-------------|-------------|-----------|
| `walk`  | 35,198      | Locomotion  | High      |
| `squat` | 2,398       | Exercise    | High      |
| `run`   | 8,718       | Dynamic     | Medium    |

## 💡 **Pro Tips**

1. **Always use `["walk"]` for initial testing** - most reliable
2. **Combine `["walk", "squat"]` for variety** - both very stable  
3. **Add `["run"]` for dynamic motion** - more challenging but works
4. **Avoid the unavailable datasets** - they cause 404 errors
5. **Check dataset cache** in `~/.cache/huggingface/` after downloads