# G1 Hardware Setup Instructions

Complete guide to running motion capture playback on the Unitree G1 humanoid robot.

## Requirements

- Unitree G1 robot with Jetson
- Unitree SDK2 Python v1.0.1+ installed at `/home/unitree/unitree_sdk2_python`
- CycloneDDS installed at `/home/unitree/Documents/GitHub/cyclonedds/install`
- Network connection to robot (default: 192.168.30.129)

## Quick Start on Jetson

### 1. SSH to Jetson
```bash
ssh unitree@192.168.30.129
# Password: usually 123 or ask your admin
```

### 2. Set Environment Variables (REQUIRED every session)
```bash
export CYCLONEDDS_HOME=/home/unitree/Documents/GitHub/cyclonedds/install
export LD_LIBRARY_PATH=$CYCLONEDDS_HOME/lib:$LD_LIBRARY_PATH
export PYTHONPATH=/home/unitree/unitree_sdk2_python:$PYTHONPATH
```

Or add to `~/.bashrc` for persistence:
```bash
echo 'export CYCLONEDDS_HOME=/home/unitree/Documents/GitHub/cyclonedds/install' >> ~/.bashrc
echo 'export LD_LIBRARY_PATH=$CYCLONEDDS_HOME/lib:$LD_LIBRARY_PATH' >> ~/.bashrc
echo 'export PYTHONPATH=/home/unitree/unitree_sdk2_python:$PYTHONPATH' >> ~/.bashrc
source ~/.bashrc
```

### 3. Get the Files

**Option A: Download from GitHub**
```bash
# On Jetson
cd ~
wget https://raw.githubusercontent.com/feraco/loco-mujoco/master/LAFAN1_Retargeting_Dataset/quick_hardware_test_jetson.py

# Get motion data
mkdir -p ~/LAFAN1_Retargeting_Dataset
cd ~/LAFAN1_Retargeting_Dataset
git clone https://github.com/feraco/loco-mujoco.git temp
mv temp/LAFAN1_Retargeting_Dataset/g1 .
rm -rf temp
```

**Option B: Copy from your Mac**
```bash
# On your Mac
scp LAFAN1_Retargeting_Dataset/quick_hardware_test_jetson.py unitree@192.168.30.129:~/
scp -r LAFAN1_Retargeting_Dataset/g1/ unitree@192.168.30.129:~/LAFAN1_Retargeting_Dataset/
```

### 4. Run Motion Test
```bash
# On Jetson
python3 ~/quick_hardware_test_jetson.py walking    # Safest - 10% speed
python3 ~/quick_hardware_test_jetson.py running    # 5% speed
python3 ~/quick_hardware_test_jetson.py jumping    # 3% speed
python3 ~/quick_hardware_test_jetson.py dancing    # 2% speed - most dynamic
```

## Troubleshooting

### Error: "No module named 'unitree_sdk2py.g1.low_level'"
This means you have an **old version** of the script. The correct imports are:
```python
from unitree_sdk2py.core.channel import ChannelPublisher, ChannelSubscriber, ChannelFactoryInitialize
from unitree_sdk2py.idl.unitree_hg.msg.dds_ import LowCmd_ as hg_LowCmd, LowState_ as hg_LowState
from unitree_sdk2py.idl.default import unitree_hg_msg_dds__LowCmd_
from unitree_sdk2py.utils.crc import CRC
from unitree_sdk2py.comm.motion_switcher.motion_switcher_client import MotionSwitcherClient
```

**Fix:** Re-download the latest script:
```bash
rm ~/quick_hardware_test_jetson.py
wget https://raw.githubusercontent.com/feraco/loco-mujoco/master/LAFAN1_Retargeting_Dataset/quick_hardware_test_jetson.py -O ~/quick_hardware_test_jetson.py
```

### Error: "Cannot find SDK" or ImportError
Set the PYTHONPATH:
```bash
export PYTHONPATH=/home/unitree/unitree_sdk2_python:$PYTHONPATH
```

### Error: "ChannelFactory" or DDS errors
Set CycloneDDS paths:
```bash
export CYCLONEDDS_HOME=/home/unitree/Documents/GitHub/cyclonedds/install
export LD_LIBRARY_PATH=$CYCLONEDDS_HOME/lib:$LD_LIBRARY_PATH
```

If CycloneDDS isn't installed:
```bash
pip install cyclonedds==0.10.2
```

### Robot not moving
1. **Check mode**: Robot might be in "ai" mode. The script auto-releases this.
2. **Check state**: Robot should be standing upright
3. **Check E-stop**: Physical emergency stop button not pressed
4. **Arms only moving**: Currently arms respond; full body control requires additional mode setup

### Motion data not found
Make sure motion CSV files are in the right location:
```bash
ls ~/LAFAN1_Retargeting_Dataset/g1/
# Should show: walk1_subject1.csv, dance1_subject1.csv, etc.
```

## Safety Features

- **Emergency Stop**: Press `Ctrl+C` at any time to stop robot
- **Smooth Transitions**: Robot interpolates smoothly between poses
- **Speed Limiting**: All motions run at reduced speed (2-10%)
- **Mode Release**: Automatically releases high-level control modes

## Joint Mapping

G1 has 29 controllable joints:
| Index | Joint | Index | Joint |
|-------|-------|-------|-------|
| 0-5 | Left leg | 6-11 | Right leg |
| 12-14 | Waist | 15-21 | Left arm |
| 22-28 | Right arm | | |

## Motion Data Format

CSV files have 36 columns:
- Columns 0-2: Root position (x, y, z)
- Columns 3-6: Root orientation (quaternion)
- Columns 7-35: Joint angles (29 DOF)

## Available Motions

| Type | Files | Description |
|------|-------|-------------|
| Walking | walk1_subject*.csv, walk2_*, walk3_*, walk4_* | Various walking styles |
| Running | run1_subject*.csv, run2_*, sprint1_* | Running and sprinting |
| Jumping | jumps1_subject*.csv | Jump sequences |
| Dancing | dance1_subject*.csv, dance2_* | Dance movements |
| Fighting | fight1_*, fightAndSports1_* | Combat motions |
| Fall/GetUp | fallAndGetUp1_*, fallAndGetUp2_*, fallAndGetUp3_* | Fall and recovery |

## SDK Version Info

Tested with:
- **Unitree SDK2 Python**: v1.0.1
- **CycloneDDS**: v0.10.2
- **Python**: 3.8+

## Credits

- Original LAFAN1 dataset: Ubisoft La Forge Animation Dataset
- Retargeting: lvhaidong
- Hardware integration: feraco
