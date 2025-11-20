# G1 MuJoCo Viewer Solutions - Extended Viewing Time

## Problem Summary
The original issue was: **"WHEN I RUN G1_01 AND G1_02 MUJOCO OPENS AND THEN CLOSES RIGHT AWAY"**

## Root Causes Identified
1. **Short Episode Duration**: Original tutorials used 200-400 steps (~6-12 seconds)
2. **Missing Datasets**: `stepinplace` dataset was not available on server (404 error) 
3. **Unsupported Parameters**: `render_mode="human"` parameter not supported in this LocoMuJoCo version
4. **Quick Sequential Execution**: No pauses between different motion demonstrations

## Solutions Implemented

### ✅ 1. Extended Episode Duration
- **Before**: 200-400 steps per episode (~6-12 seconds)
- **After**: 1000-2000 steps per episode (30-60+ seconds)
- **Result**: Much longer viewing time for each motion

### ✅ 2. Fixed Dataset Issues  
- **Before**: Used unavailable `stepinplace` dataset
- **After**: Replaced with available `squat` dataset
- **Result**: No more 404 dataset errors

### ✅ 3. Removed Unsupported Parameters
- **Before**: `render_mode="human"` caused errors
- **After**: Simple `render=True` parameter only
- **Result**: No more parameter errors

### ✅ 4. Individual Dataset Demonstrations
- **Before**: Multiple datasets played quickly in sequence
- **After**: Each dataset demonstrated separately with descriptions
- **Result**: Better focus on each motion type

### ✅ 5. Interactive Viewer Instructions
Added clear instructions for MuJoCo viewer controls:
- **SPACE**: Pause/Resume simulation  
- **ESC**: Exit viewer
- **R**: Reset simulation
- **Mouse drag**: Rotate camera view
- **Mouse wheel**: Zoom in/out

## Updated Tutorial Files

### 📁 g1_01_basic_datasets.py (FIXED)
- Extended viewing time: 30+ seconds per motion
- Demonstrates: `walk` and `squat` motions individually
- 3 episodes per motion type for variety
- Clear instructions and progress indicators

### 📁 g1_02_lafan1_datasets.py (FIXED) 
- Extended viewing time: 45+ seconds per motion capture
- Demonstrates: `walk1_subject1` and `dance2_subject4` 
- High-quality human motion capture data
- Individual motion demonstrations with pauses

### 📁 g1_simple_walk_test.py (NEW)
- **Purpose**: Maximum viewing time test script
- **Duration**: 60+ seconds per episode, 3+ minutes total
- **Focus**: Only G1 walking motion for detailed observation
- **Best for**: Initial testing and troubleshooting

### 📁 g1_slow_motion_viewer.py (NEW)
- **Purpose**: Interactive menu-driven viewer
- **Features**: Choose specific motions to view
- **Duration**: 60-120 seconds per motion
- **Controls**: User can select individual datasets or view all

### 📁 g1_dataset_explorer.py (HELPER)
- Lists all available G1 datasets
- Shows dataset locations and descriptions
- Tests import capabilities
- Troubleshooting information

## Usage Instructions

### Quick Test (Recommended First)
```bash
cd /Users/wwhs-research/Downloads/humsim/loco-mujoco/examples/g1_tutorials
conda activate unitree_mujoco
python g1_simple_walk_test.py
```

### Full Basic Tutorial
```bash
python g1_01_basic_datasets.py
```

### Motion Capture Tutorial  
```bash
python g1_02_lafan1_datasets.py
```

### Interactive Viewer
```bash
python g1_slow_motion_viewer.py
```

## Expected Behavior Now

1. **MuJoCo viewer opens** and displays G1 humanoid robot
2. **Viewer stays open** for 30-60+ seconds per motion
3. **Multiple episodes** show variations of each motion
4. **Clear progress indicators** show which motion is playing
5. **Interactive controls** work (SPACE to pause, etc.)
6. **Proper transitions** between different motion types

## Troubleshooting

If viewer still closes quickly:
1. **Check conda environment**: Must use `unitree_mujoco` environment
2. **Verify LocoMuJoCo installation**: `pip install -e .` in loco-mujoco directory  
3. **Test basic MuJoCo**: Try `test_mujoco_viewer.py` first
4. **Check system graphics**: MuJoCo requires OpenGL support
5. **Run from correct directory**: Must be in `g1_tutorials` folder

## Success Indicators

✅ **Datasets download successfully** (progress bars reach 100%)  
✅ **"UnitreeG1 environment created successfully!" message appears**  
✅ **MuJoCo viewer window opens and displays 3D robot**  
✅ **G1 robot performs walking/squatting motions**  
✅ **Viewer stays open for 30+ seconds per episode**  
✅ **Multiple episodes show motion variations**  
✅ **Interactive controls respond (SPACE, ESC, mouse)**

The tutorials should now provide ample viewing time to observe G1 humanoid robot movements in detail!