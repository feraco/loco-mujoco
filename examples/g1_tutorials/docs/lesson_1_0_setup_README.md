# 🛠️ Lesson 1.0: Installation and Setup

## 🎯 **Learning Objectives**
By the end of this setup lesson, you will have:
- ✅ A proper Python environment (3.8-3.11) with conda or uv
- ✅ LocoMuJoCo installed and working correctly
- ✅ All dependencies configured properly
- ✅ Graphics and visualization working
- ✅ A clean environment ready for all tutorials

## 📋 **What You'll Set Up**
1. **Python environment management** (conda or uv)
2. **LocoMuJoCo framework installation**
3. **Graphics and visualization dependencies**
4. **Verify installation with quick tests**
5. **Troubleshoot common installation issues**

## 🔧 **System Requirements**

### **Operating System Support**
- ✅ **Linux** (Ubuntu 18.04+, recommended)
- ✅ **macOS** (10.14+, Intel or Apple Silicon)
- ✅ **Windows** (10/11 with WSL2 recommended)

### **Hardware Requirements**
- **CPU**: Modern multi-core processor (Intel i5+ or AMD equivalent)
- **RAM**: 8GB minimum, 16GB recommended
- **GPU**: Any modern graphics card (NVIDIA, AMD, or integrated)
- **Storage**: 10GB free space (5GB for environments + 5GB for datasets)
- **Internet**: Required for initial dataset downloads

### **Python Version Requirements**
- **Python 3.8, 3.9, 3.10, or 3.11** (3.12+ not yet supported)
- **NOT Python 3.7 or earlier** (missing required features)
- **NOT Python 3.12+** (dependency compatibility issues)

## 📖 **Installation Methods**

Choose **ONE** of these methods based on your preference:

---

## **Method 1: Conda Environment (Recommended for Beginners)**

### **Step 1: Install Conda**
If you don't have conda installed:

**On Linux/macOS:**
```bash
# Download and install Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh
# Follow installation prompts, restart terminal when done
```

**On Windows:**
1. Download Miniconda from: https://docs.conda.io/en/latest/miniconda.html
2. Run the installer and follow prompts
3. Use "Anaconda Prompt" for all commands below

**Verify conda installation:**
```bash
conda --version
# Should show: conda 23.x.x or similar
```

### **Step 2: Create LocoMuJoCo Environment**
```bash
# Create new environment with Python 3.10
conda create -n locomujoco python=3.10 -y

# Activate the environment
conda activate locomujoco

# Verify Python version
python --version
# Should show: Python 3.10.x
```

### **Step 3: Install LocoMuJoCo**
```bash
# Make sure you're in the locomujoco environment
conda activate locomujoco

# Install LocoMuJoCo with all dependencies
pip install loco-mujoco

# Install additional visualization dependencies
pip install matplotlib imageio imageio-ffmpeg
```

### **Step 4: Verify Installation**
```bash
# Test basic import
python -c "import loco_mujoco; print('✅ LocoMuJoCo installed successfully!')"

# Test MuJoCo physics engine
python -c "import mujoco; print('✅ MuJoCo physics engine working!')"

# Test robot models
python -c "from loco_mujoco.task_factories import RLFactory; print('✅ Task factories available!')"
```

---

## **Method 2: UV Environment (Advanced Users)**

### **Step 1: Install UV**
UV is a fast Python package manager:

**On Linux/macOS:**
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
# Restart terminal or run: source ~/.bashrc
```

**On Windows:**
```powershell
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
```

**Verify UV installation:**
```bash
uv --version
# Should show: uv 0.x.x or similar
```

### **Step 2: Create Project Environment**
```bash
# Create project directory
mkdir locomujoco-tutorials
cd locomujoco-tutorials

# Initialize UV project with Python 3.10
uv init --python 3.10

# Activate the environment
source .venv/bin/activate  # On Linux/macOS
# OR
.venv\Scripts\activate     # On Windows
```

### **Step 3: Install Dependencies**
```bash
# Install LocoMuJoCo and dependencies
uv add loco-mujoco matplotlib imageio imageio-ffmpeg

# Verify installation
uv run python -c "import loco_mujoco; print('✅ LocoMuJoCo ready!')"
```

---

## **Method 3: System Python with venv (Not Recommended)**

⚠️ **Warning**: Only use if you can't install conda or uv.

### **Step 1: Check Python Version**
```bash
python3 --version
# Must be 3.8-3.11, if not, install correct version first
```

### **Step 2: Create Virtual Environment**
```bash
# Create virtual environment
python3 -m venv locomujoco-env

# Activate environment
source locomujoco-env/bin/activate  # Linux/macOS
# OR
locomujoco-env\Scripts\activate     # Windows

# Upgrade pip
pip install --upgrade pip
```

### **Step 3: Install LocoMuJoCo**
```bash
# Install with all dependencies
pip install loco-mujoco matplotlib imageio imageio-ffmpeg

# Verify installation
python -c "import loco_mujoco; print('✅ Installation complete!')"
```

---

## **Graphics Setup**

### **Linux Graphics Setup**
```bash
# Install OpenGL dependencies
sudo apt-get update
sudo apt-get install -y libgl1-mesa-glx libgl1-mesa-dri

# For headless servers (optional)
sudo apt-get install -y xvfb
export DISPLAY=:99
Xvfb :99 -screen 0 1024x768x24 &
```

### **macOS Graphics Setup**
Usually works out-of-the-box, but if you have issues:
```bash
# Install XQuartz if needed
brew install --cask xquartz
# Restart terminal after installation
```

### **Windows Graphics Setup**
- Ensure graphics drivers are up to date
- Windows 10/11 usually work without additional setup
- For WSL2: Install VcXsrv or similar X server

---

## **Verification Tests**

### **Test 1: Basic Import Test**
```bash
python -c "
import loco_mujoco
import mujoco
import numpy as np
import matplotlib.pyplot as plt
print('✅ All basic imports successful!')
"
```

### **Test 2: Robot Creation Test**
```bash
python -c "
from loco_mujoco.task_factories import RLFactory
try:
    env = RLFactory.make('UnitreeG1', n_substeps=10)
    print('✅ Robot environment created successfully!')
    print(f'✅ Action size: {getattr(env, \"action_size\", \"Unknown\")}')
except Exception as e:
    print(f'❌ Robot creation failed: {e}')
"
```

### **Test 3: Graphics Test**
```bash
python -c "
from loco_mujoco.task_factories import RLFactory
import time
try:
    env = RLFactory.make('UnitreeG1', n_substeps=10)
    env.reset()
    env.render()  # This should open a 3D window
    print('✅ Graphics rendering working!')
    time.sleep(2)  # Keep window open briefly
except Exception as e:
    print(f'❌ Graphics test failed: {e}')
    print('Try: export MUJOCO_GL=osmesa')
"
```

---

## **Troubleshooting Common Issues**

### **❌ Python Version Problems**
```
ERROR: Python 3.7 is not supported
```
**Solution**: Install Python 3.8-3.11
```bash
# With conda
conda install python=3.10

# With uv
uv python install 3.10
```

### **❌ Package Installation Fails**
```
ERROR: Could not install loco-mujoco
```
**Solutions**:
```bash
# Update pip first
pip install --upgrade pip

# Install with no cache
pip install --no-cache-dir loco-mujoco

# Install specific version
pip install loco-mujoco==1.0.1
```

### **❌ Graphics/OpenGL Issues**
```
ERROR: Could not create OpenGL context
```
**Solutions**:
```bash
# Try software rendering
export MUJOCO_GL=osmesa
python your_script.py

# On Linux, install graphics libraries
sudo apt-get install libgl1-mesa-glx libgl1-mesa-dri

# Update graphics drivers (system-specific)
```

### **❌ MuJoCo License Issues** (Older Versions)
```
ERROR: MuJoCo license not found
```
**Solution**: MuJoCo is now free! Update to latest version:
```bash
pip install --upgrade mujoco
```

### **❌ Import Errors**
```
ModuleNotFoundError: No module named 'loco_mujoco'
```
**Solutions**:
```bash
# Make sure environment is activated
conda activate locomujoco
# OR
source .venv/bin/activate

# Verify installation
pip list | grep loco-mujoco

# Reinstall if needed
pip uninstall loco-mujoco
pip install loco-mujoco
```

---

## **Environment Activation Quick Reference**

### **Every Time You Start Working**

**With Conda:**
```bash
conda activate locomujoco
cd /path/to/loco-mujoco/examples/g1_tutorials
```

**With UV:**
```bash
cd locomujoco-tutorials
source .venv/bin/activate  # Linux/macOS
# OR
.venv\Scripts\activate     # Windows
```

**With venv:**
```bash
source locomujoco-env/bin/activate  # Linux/macOS
# OR
locomujoco-env\Scripts\activate     # Windows
```

---

## **Dataset Cache Setup** (Optional but Recommended)

### **Pre-download Datasets**
Speed up first tutorial runs:
```bash
python -c "
from loco_mujoco.task_factories import ImitationFactory, DefaultDatasetConf
print('📦 Pre-downloading datasets...')
env = ImitationFactory.make('UnitreeG1', 
    default_dataset_conf=DefaultDatasetConf(['walk']))
print('✅ Walk dataset cached!')
"
```

### **Set Cache Location**
```bash
# Optional: Set custom cache directory
export LOCO_MUJOCO_CACHE_DIR="/path/to/your/cache"
```

---

## **Final Verification**

Run this complete test to ensure everything is ready:

```bash
python -c "
print('🧪 Running complete installation verification...')

# Test 1: Imports
try:
    import loco_mujoco
    import mujoco
    import numpy as np
    import matplotlib.pyplot as plt
    print('✅ All imports successful')
except Exception as e:
    print(f'❌ Import failed: {e}')
    exit(1)

# Test 2: Environment creation
try:
    from loco_mujoco.task_factories import RLFactory
    env = RLFactory.make('UnitreeG1', n_substeps=10)
    print('✅ Robot environment created')
except Exception as e:
    print(f'❌ Environment creation failed: {e}')
    exit(1)

# Test 3: Basic simulation
try:
    import numpy as np
    state = env.reset()
    if isinstance(state, tuple):
        state = state[0]
    action = np.zeros(23)  # G1 has 23 joints
    result = env.step(action)
    print('✅ Simulation step successful')
except Exception as e:
    print(f'❌ Simulation failed: {e}')
    exit(1)

print('🎉 INSTALLATION VERIFICATION COMPLETE!')
print('✅ Ready for Lesson 1.1!')
"
```

---

## **What's Next?**

### **🚀 Ready for Lesson 1.1: Quick System Test**
Now that everything is installed:
```bash
cd /path/to/loco-mujoco/examples/g1_tutorials
python lesson_1_1_quick_test.py
```

### **📚 Learning Path**
1. **Lesson 1.1**: Verify your setup works
2. **Lesson 1.2**: Watch robot walking
3. **Lesson 1.5**: Interactive robot control
4. **Continue through Lessons 1.3-1.10**

### **🔧 Development Setup** (Optional)
For advanced users who want to modify LocoMuJoCo:
```bash
# Install in development mode
git clone https://github.com/robfiras/loco-mujoco.git
cd loco-mujoco
pip install -e .
```

---

## 💡 **Key Takeaways**
- ✅ **Environment isolation is crucial** - always use conda/uv/venv
- ✅ **Python 3.8-3.11 only** - newer versions have compatibility issues  
- ✅ **Graphics setup varies by system** - test early and troubleshoot
- ✅ **Verification tests catch problems early** - run them all

**🎯 You now have a professional LocoMuJoCo development environment!** Ready to start learning robotics.