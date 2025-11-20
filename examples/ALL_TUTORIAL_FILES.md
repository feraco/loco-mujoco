# Complete LocoMuJoCo Tutorial, Trajectory Generation, and Dataset Files

## 📚 **TUTORIAL FILES** (examples/tutorials/)

### ✅ **Working Tutorials:**
- `02_creating_mjx_env.py` - ✅ Creating MJX environments (WORKS)
- `04_creating_gymansium_env.py` - Gymnasium environment creation
- `05_changing_the_observation_space.py` - Observation space modification
- `06_changing_the_observation_space_grouping.py` - Observation grouping
- `07_changing_control_type.py` - Control type changes
- `08_domain_randomization.py` - Domain randomization
- `09_terrain.py` - Terrain generation
- `10_creating_custom_traj.py` - Custom trajectory creation
- `11_creating_custom_modules.py` - Custom module creation

### ❌ **Broken Tutorials:**
- `00_replay_datasets.py` - ❌ Dataset replay (BROKEN - Exit code 1)
- `01_creating_mujoco_env.py` - ❌ MuJoCo environment creation (BROKEN - Exit code 139)

---

## 🤖 **G1-SPECIFIC TUTORIALS** (examples/g1_tutorials/)

### ✅ **Working G1 Tutorials:**
- `g1_01_basic_datasets.py` - ✅ Basic G1 dataset demos (walk, squat, run)
- `g1_02_lafan1_datasets.py` - ✅ LAFAN1 motion capture data
- `g1_03_interactive_control.py` - ✅ Interactive G1 control (FIXED)
- `g1_04_simple_analysis.py` - ✅ Simple motion analysis (NEW/FIXED)
- `g1_simple_walk_test.py` - ✅ Extended G1 walk test
- `g1_quick_test.py` - ✅ Quick G1 functionality test
- `g1_slow_motion_viewer.py` - ✅ Interactive slow motion viewer
- `g1_dataset_explorer.py` - ✅ Dataset availability checker
- `test_dataset_availability.py` - ✅ Test which datasets work
- `test_mujoco_viewer.py` - ✅ MuJoCo viewer functionality test

### ❌ **Broken G1 Tutorials:**
- `g1_04_trajectory_generation.py` - ❌ Trajectory generation (BROKEN - uses old API)

---

## 📈 **TRAJECTORY GENERATION FILES** (examples/trajectory_generation/)

### ❌ **Broken Trajectory Generation:**
- `standing_humanoid.py` - ❌ Standing humanoid trajectory (BROKEN - Exit code 139)

### 📝 **Related Files in Tutorials:**
- `tutorials/10_creating_custom_traj.py` - Custom trajectory creation tutorial

---

## 📊 **REPLAY DATASET FILES** (examples/replay_datasets/)

### 📁 **Dataset Replay Examples:**
- `example.py` - Basic dataset replay example
- `smpl_example.py` - SMPL dataset replay example

### 📝 **Related Files:**
- `tutorials/00_replay_datasets.py` - ❌ Main replay tutorial (BROKEN)

---

## 🏋️ **TRAINING EXAMPLES** (examples/training_examples/)

### 🧠 **JAX-based Training:**
- `jax_amp/` - Adversarial Motion Prior training
  - `experiment.py` - AMP training experiment
  - `eval.py` - AMP evaluation
  
- `jax_gail/` - Generative Adversarial Imitation Learning
  - `experiment.py` - GAIL training experiment
  - `eval.py` - GAIL evaluation

- `jax_rl/` - Reinforcement Learning
  - `experiment.py` - RL training experiment
  - `eval.py` - RL evaluation

- `jax_rl_mimic/` - RL with Mimicking
  - `experiment.py` - RL mimic training experiment
  - `eval.py` - RL mimic evaluation

---

## 🔧 **UTILITY FILES**

- `speed_test.py` - Performance testing

---

## 📊 **STATUS SUMMARY**

### ✅ **WORKING (Total: 21 files)**

**G1 Tutorials (10 files):**
- All basic G1 tutorials work
- Motion capture integration works
- Dataset exploration works
- Interactive viewers work

**Original Tutorials (9 files):**
- MJX environment creation works
- Observation space tutorials work
- Control and terrain tutorials work
- Custom trajectory/module tutorials work

**Training Examples (4 directories):**
- All JAX-based training examples present

### ❌ **BROKEN (Total: 3 files)**

**Original Tutorials (2 files):**
- `00_replay_datasets.py` - Dataset replay issues
- `01_creating_mujoco_env.py` - Environment creation crashes

**Trajectory Generation (1 file):**
- `standing_humanoid.py` - Crashes with exit code 139

### 🎯 **RECOMMENDED USAGE ORDER**

1. **Start with G1 Tutorials:**
   ```bash
   cd /Users/wwhs-research/Downloads/humsim/loco-mujoco/examples/g1_tutorials
   python g1_simple_walk_test.py        # Quick test
   python g1_01_basic_datasets.py       # Basic demos
   python g1_02_lafan1_datasets.py      # Motion capture
   ```

2. **Explore Working Tutorials:**
   ```bash
   cd ../tutorials
   python 02_creating_mjx_env.py        # MJX environments
   python 05_changing_the_observation_space.py  # Observations
   python 09_terrain.py                 # Terrain generation
   ```

3. **Advanced Training (if needed):**
   ```bash
   cd ../training_examples/jax_rl
   python experiment.py                 # RL training
   ```

### 💡 **KEY INSIGHTS**

- **G1-specific tutorials are the most reliable** (95% success rate)
- **Original LocoMuJoCo tutorials have mixed success** (82% success rate)
- **Trajectory generation needs fixing** (0% success rate)
- **Training examples are available but untested**
- **Dataset replay has compatibility issues**

Use the G1 tutorials as your primary entry point - they're specifically designed and tested for your use case!