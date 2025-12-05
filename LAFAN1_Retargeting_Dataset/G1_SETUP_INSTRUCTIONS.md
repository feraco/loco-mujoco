# G1 Hardware Setup Instructions

## Quick Start on Jetson

### 1. SSH to Jetson
```bash
ssh unitree@192.168.30.129
```

### 2. Set Environment Variables
```bash
export CYCLONEDDS_HOME=/home/unitree/Documents/GitHub/cyclonedds/install
export LD_LIBRARY_PATH=$CYCLONEDDS_HOME/lib:$LD_LIBRARY_PATH
export PYTHONPATH=/home/unitree/unitree_sdk2_python:$PYTHONPATH
```

### 3. Copy Motion Data and Script
From your Mac:
```bash
scp -r g1/ unitree@192.168.30.129:~/LAFAN1_Retargeting_Dataset/
scp quick_hardware_test_jetson.py unitree@192.168.30.129:~/
```

### 4. Run Motion Test
```bash
# On Jetson
python3 quick_hardware_test_jetson.py walking    # Safest - 10% speed
python3 quick_hardware_test_jetson.py running    # 5% speed
python3 quick_hardware_test_jetson.py jumping    # 3% speed
python3 quick_hardware_test_jetson.py dancing    # 2% speed - most dynamic
```

## Safety Features

- **Emergency Stop**: Press Ctrl+C at any time to stop robot
- **Smooth Transitions**: Robot interpolates smoothly between poses
- **Speed Limiting**: All motions run at reduced speed for safety

## Joint Mapping

G1 has 29 controllable joints:
- Joints 0-5: Left leg (hip yaw/roll/pitch, knee, ankle pitch/roll)
- Joints 6-11: Right leg
- Joints 12-14: Waist (yaw, roll, pitch)
- Joints 15-21: Left arm (shoulder pitch/roll/yaw, elbow, wrist yaw/roll/pitch)
- Joints 22-28: Right arm

## Motion Data Format

CSV files have 36 columns:
- Columns 0-6: Root position and orientation (unused for now)
- Columns 7-35: Joint angles for 29 DOF

## Troubleshooting

### "Cannot find SDK"
Make sure environment variables are set:
```bash
export PYTHONPATH=/home/unitree/unitree_sdk2_python:$PYTHONPATH
```

### "ChannelFactory error"
Make sure CycloneDDS is installed:
```bash
pip install cyclonedds
export CYCLONEDDS_HOME=/home/unitree/Documents/GitHub/cyclonedds/install
```

### Robot not responding
Release AI mode first - the script does this automatically via MotionSwitcherClient
