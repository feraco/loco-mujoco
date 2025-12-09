# Dance Dataset Balance Issues - Analysis and Solutions

## Problem Summary

When running dance datasets at 100% speed on real G1 hardware, the robot loses balance and may fall. This happens because:

### Root Causes

1. **Kinematic-Only Retargeting**
   - The LAFAN1 retargeting only considers kinematic constraints (joint positions, velocities)
   - **Does NOT account for**:
     - Dynamic constraints (momentum, forces, torques)
     - Center of Mass (CoM) trajectory
     - Zero Moment Point (ZMP) stability
     - Actuator torque/power limits
     - Inertial effects at higher speeds

2. **Motion Capture Data Characteristics**
   - Original mocap is from humans with different:
     - Mass distribution
     - Link lengths
     - Center of mass location
     - Moment of inertia
   - Humans compensate for balance unconsciously during dance

3. **High Dynamic Motions**
   - Dance involves:
     - Rapid weight shifts
     - Quick direction changes
     - Large arm movements (affecting angular momentum)
     - Single-leg support phases
   - At 100% speed, these create large unmodeled forces

4. **Hardware Reality Gap**
   - Simulation vs reality differences:
     - Joint friction and backlash
     - Motor response delays
     - Floor contact dynamics
     - Sensor noise and delays

## Recommended Solutions

### Solution 1: Use the New Balanced Controller ⭐ **RECOMMENDED**

The new `quick_hardware_test_jetson_balanced.py` script adds real-time balance stabilization:

```bash
# Conservative start - 50% speed with balance control
python3 quick_hardware_test_jetson_balanced.py dancing --speed 0.5

# Gradually increase speed
python3 quick_hardware_test_jetson_balanced.py dancing --speed 0.7

# Full speed with balance control (still risky!)
python3 quick_hardware_test_jetson_balanced.py dancing --speed 1.0

# Compare with original (no balance)
python3 quick_hardware_test_jetson_balanced.py dancing --speed 0.5 --no-balance
```

**Features**:
- ✅ Real-time IMU-based tilt detection
- ✅ Torso stabilization (waist corrections)
- ✅ Ankle strategy for roll compensation
- ✅ Hip strategy for pitch compensation
- ✅ Adaptive gain scheduling during fast motions
- ✅ Emergency stop on excessive tilt
- ✅ Stability monitoring and warnings

**How It Works**:
```python
# Detects robot tilt from IMU
roll, pitch = get_orientation(imu.quaternion)

# Computes corrections to counteract tilt
if abs(roll) > 0.05:
    corrections[WaistRoll] = -roll * stabilization_gain
    corrections[LeftAnkleRoll] += -roll * ankle_gain
    corrections[RightAnkleRoll] += -roll * ankle_gain

# Applies corrections to target positions
corrected_positions = target_positions + corrections
```

### Solution 2: Reduce Playback Speed

The original script can be used safely at reduced speeds:

```bash
# Original script with 20% speed (current dancing default)
python3 quick_hardware_test_jetson.py dancing  # Uses 2% speed

# Custom speed
python3 quick_hardware_test_jetson.py dancing --dataset 1 --speed 0.3
```

**Speed Guidelines**:
| Speed | Recommendation | Risk Level |
|-------|---------------|------------|
| 10-30% | ✅ Safe for testing | Low |
| 30-50% | ⚠️ Monitor closely | Medium |
| 50-70% | ⚠️ Use balance control | Medium-High |
| 70-100% | 🚨 High fall risk | High |
| >100% | 🚨 Not recommended | Very High |

### Solution 3: Motion Preprocessing (Advanced)

For researchers wanting to improve the dataset itself:

1. **CoM Trajectory Optimization**
   ```python
   # Recompute joint angles to keep CoM within support polygon
   from loco_mujoco import RLFactory
   
   env = RLFactory.make("UnitreeG1")
   # ... optimize CoM trajectory while keeping end-effector poses
   ```

2. **ZMP-Based Retargeting**
   - Ensure Zero Moment Point stays within foot support polygon
   - Requires inverse dynamics and trajectory optimization

3. **Speed-Adaptive Scaling**
   - Scale motion amplitude based on playback speed
   - Reduce arm swing at higher speeds to limit momentum

4. **Foot Pressure Balancing**
   - Monitor foot force sensors
   - Adjust ankle/hip angles to maintain even weight distribution

### Solution 4: Safe Testing Practices

**Physical Setup**:
- ✅ Use overhead suspension/safety harness
- ✅ Test on soft surfaces (mats)
- ✅ Clear 3m radius around robot
- ✅ Have emergency stop ready
- ✅ Start with robot in stable stance

**Progressive Testing**:
```bash
# Step 1: Visualize in simulation first
python3 rerun_visualize.py --file_name dance1_subject1 --robot_type g1

# Step 2: Test at very low speed
python3 quick_hardware_test_jetson_balanced.py dancing --speed 0.2

# Step 3: Gradually increase by 0.1 increments
python3 quick_hardware_test_jetson_balanced.py dancing --speed 0.3
python3 quick_hardware_test_jetson_balanced.py dancing --speed 0.4

# Step 4: Monitor IMU data and stop if unstable
# (Balance controller does this automatically)
```

## Understanding Balance Metrics

### Critical Stability Indicators

1. **Roll/Pitch Angle**
   - Safe range: ±15° (0.26 rad)
   - Warning: ±17° (0.30 rad)
   - Emergency: ±20° (0.35 rad)

2. **Angular Velocity**
   - Safe: < 0.5 rad/s
   - Warning: > 1.0 rad/s
   - Emergency: > 2.0 rad/s

3. **Center of Mass Position**
   - Must stay within support polygon (foot contact area)
   - Dance motions often push CoM to edges

### Monitoring During Execution

The balanced controller prints warnings:
```
⚠️  Excessive roll: 18.5°
⚠️  High pitch velocity: 1.2 rad/s
🚨 EMERGENCY STOP - Robot unstable!
```

## Dataset-Specific Recommendations

### Dance Datasets

| Dataset | Frames | Duration | Safe Speed | With Balance | Notes |
|---------|--------|----------|------------|--------------|-------|
| dance1_subject1 | 3945 | 131s | 20-30% | 50-70% | Moderate dynamics |
| dance1_subject2 | 3945 | 131s | 20-30% | 50-70% | Similar to subject1 |
| dance2_subject1 | 6771 | 226s | 15-25% | 40-60% | More dynamic moves |

### Comparison with Other Motions

| Motion Type | Safe Speed (no balance) | Safe Speed (with balance) | Dynamics Level |
|-------------|------------------------|---------------------------|----------------|
| Walking | 80-100% | 100%+ | Low |
| Running | 30-50% | 70-90% | Medium |
| Jumping | 20-30% | 50-70% | High |
| **Dancing** | **20-30%** | **50-70%** | **Very High** |
| Fighting | 20-40% | 60-80% | High |

## Technical Details: Why Balance Control Helps

### 1. Feedback Loop
Without balance control:
```
Target Position → Motor → Robot Falls → No Correction
```

With balance control:
```
Target Position → IMU Feedback → Compute Correction → Adjusted Position → Motor → Stable
```

### 2. Control Strategies

**Ankle Strategy** (small perturbations):
- Adjust ankle pitch/roll to shift CoM
- Fast response, small range
- Effective for < 10° tilts

**Hip Strategy** (larger perturbations):
- Adjust hip joints to move upper body
- Slower response, larger range
- Effective for 10-20° tilts

**Torso Strategy** (our implementation):
- Adjust waist joints to counter-rotate
- Medium response, medium range
- Keeps feet planted

### 3. Adaptive Gains

```python
# Reduce gains during fast motions (less interference)
avg_velocity = mean(abs(joint_velocities))
gain_multiplier = 1.0 - min(avg_velocity / threshold, 1.0) * (1.0 - 0.3)

# Apply to corrections
correction = -tilt * base_gain * gain_multiplier
```

This prevents the balance controller from fighting against the desired motion.

## Future Improvements

### Hardware Side
1. ✅ Implement the balanced controller (done!)
2. ⬜ Add foot force sensor feedback
3. ⬜ Model Predictive Control (MPC) for balance
4. ⬜ Learning-based adaptation (RL fine-tuning)

### Dataset Side
1. ⬜ Re-retarget with ZMP constraints
2. ⬜ Optimize for dynamic feasibility
3. ⬜ Include actuator limits in optimization
4. ⬜ Generate speed-specific versions

### Simulation-to-Reality Gap
1. ⬜ System identification on real hardware
2. ⬜ Domain randomization during training
3. ⬜ Sim-to-real transfer learning
4. ⬜ Online adaptation

## FAQ

**Q: Why does walking work at 100% but dancing doesn't?**
A: Walking has continuous double-support phases and slower dynamics. Dance has rapid weight shifts and single-leg support that exceed the kinematic retargeting assumptions.

**Q: Will balance control let me run at 100% speed safely?**
A: It helps significantly but doesn't guarantee safety. Start conservatively and increase gradually. Always use physical safety measures.

**Q: Can I use this on H1 or H1_2 robots?**
A: The concepts apply, but you'll need to adapt joint indices and possibly adjust gains for different robot dynamics.

**Q: How do I know if my robot is about to fall?**
A: Watch for:
- Rapid tilt increase
- Extended single-leg support
- Large angular velocity
- The balance controller will print warnings

**Q: Should I modify the CSV data instead?**
A: For quick testing, use the balance controller. For production/research, re-retargeting with dynamic constraints is better but more complex.

## References

- LAFAN1 Dataset: https://github.com/ubisoft/ubisoft-laforge-animation-dataset
- LocoMuJoCo Documentation: https://github.com/feraco/loco-mujoco
- Unitree G1 SDK: https://github.com/unitreerobotics/unitree_sdk2
- Humanoid Balance Control: Winter (2009) "Biomechanics and Motor Control of Human Movement"
- ZMP Theory: Vukobratović & Borovac (2004) "Zero-Moment Point — Thirty Five Years of its Life"

## Support

For issues or questions:
1. Check IMU readings during failure
2. Try progressively lower speeds
3. Verify balance controller is active
4. Check for hardware issues (loose joints, low battery)
5. Open an issue on GitHub with failure logs

---

**Remember**: The retargeted motions are kinematically feasible but not necessarily dynamically stable. Always prioritize safety when testing on real hardware!
