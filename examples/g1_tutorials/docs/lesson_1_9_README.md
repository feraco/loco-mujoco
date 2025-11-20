# Lesson 1.9: Slow Motion Viewer

## Learning Objectives

By the end of this lesson, you will:
- Analyze robot motion frame-by-frame in slow motion
- Understand detailed biomechanical movement patterns
- Learn precision motion analysis techniques
- Master frame-level motion debugging and inspection
- Develop skills for detailed movement quality assessment

## What You'll Do

1. **Launch slow motion analysis viewer with frame control**
2. **Step through motion sequences frame by frame**
3. **Analyze joint movements at microscopic time scales**
4. **Compare normal speed vs. slow motion observations**
5. **Generate detailed frame-by-frame motion reports**

## Prerequisites

- Completed Lessons 1.1 through 1.8
- Understanding of motion analysis and data visualization
- Familiarity with robot kinematics and joint mechanics

## Step-by-Step Instructions

### Step 1: Launch Slow Motion Viewer
```bash
cd /path/to/loco-mujoco/examples/g1_tutorials
python lesson_1_9_slow_motion_viewer.py
```

### Step 2: Viewer Interface Controls

When you run the lesson, you will see:

1. **Console Controls**:
   ```
   G1 Robot Slow Motion Analysis Viewer
   ===================================
   
   Playback Controls:
   - SPACE: Play/Pause motion
   - RIGHT ARROW: Next frame (step forward)
   - LEFT ARROW: Previous frame (step backward)
   - UP ARROW: Increase playback speed
   - DOWN ARROW: Decrease playback speed
   - R: Reset to first frame
   - S: Save current frame analysis
   - Q: Quit viewer
   
   Current Status:
   - Motion: walk_normal (500 frames)
   - Speed: 0.1x (1/10 normal speed)
   - Frame: 1/500 (0.02 seconds)
   - Mode: PAUSED
   ```

2. **Real-Time Information Display**:
   ```
   Frame Analysis (Frame 45/500):
   =============================
   Time: 0.90 seconds
   
   Joint Angles (degrees):
   ├── Left Hip: -12.3° (flexion)
   ├── Right Hip: +18.7° (extension)
   ├── Left Knee: +35.2° (flexion)
   ├── Right Knee: +8.1° (slight flexion)
   ├── Left Ankle: -5.4° (plantarflexion)
   └── Right Ankle: +12.8° (dorsiflexion)
   
   Gait Phase: Right heel strike
   Balance: Stable (CoM within support)
   Ground Contact: Right foot only
   ```

### Step 3: Slow Motion Analysis Techniques

#### Frame-by-Frame Stepping

**Detailed Motion Inspection**:
- Use RIGHT/LEFT arrows to step through individual frames
- Each frame represents 0.02 seconds (50Hz data)
- Observe subtle joint angle changes between frames
- Identify precise timing of gait events

**Key Observations in Walking**:
```
Frame-by-Frame Walking Analysis:

Frames 1-25: Right leg swing phase
├── Frame 1: Toe-off initiation
├── Frame 8: Maximum knee flexion
├── Frame 15: Forward leg swing
├── Frame 22: Heel strike preparation
└── Frame 25: Right heel strike

Frames 26-50: Left leg swing phase  
├── Frame 26: Left toe-off
├── Frame 33: Double support phase
├── Frame 40: Left leg forward swing
├── Frame 47: Left heel strike preparation
└── Frame 50: Left heel strike (cycle complete)
```

#### Speed Control Analysis

**Multiple Playback Speeds**:
- **0.01x speed**: Ultra-slow for joint angle precision
- **0.1x speed**: Detailed gait phase analysis  
- **0.5x speed**: Comfortable detailed observation
- **1.0x speed**: Normal walking speed reference
- **2.0x speed**: Quick overview mode

**Speed-Dependent Observations**:
```
Ultra-Slow (0.01x):
├── Individual joint rotations clearly visible
├── Muscle activation timing apparent
├── Balance adjustments observable
└── Sub-frame movement details

Normal Speed (1.0x):
├── Overall gait pattern assessment
├── Natural movement flow
├── Coordination between limbs
└── General stability evaluation
```

#### Gait Event Detection

**Critical Gait Events Identified**:
```
Heel Strike Events (Right Leg):
├── Frame 25: Initial ground contact
├── Frame 26: Weight acceptance begins
├── Frame 27: Full foot contact
├── Frame 28: Load response phase
└── Frame 30: Single support begins

Toe-Off Events (Right Leg):
├── Frame 48: Heel lift initiation
├── Frame 49: Toe contact only
├── Frame 50: Push-off phase
├── Frame 51: Foot clears ground
└── Frame 52: Swing phase begins
```

### Step 4: Biomechanical Analysis Features

#### Joint Angle Precision Measurement

**Real-Time Joint Analysis**:
```python
# Displayed for each frame
Joint Measurements (Frame 127):
================================

Hip Joints:
├── Left Hip Flexion: -15.7° ± 0.1°
├── Left Hip Abduction: +2.3° ± 0.1°
├── Right Hip Flexion: +22.4° ± 0.1°
└── Right Hip Abduction: -1.8° ± 0.1°

Knee Joints:
├── Left Knee Flexion: +42.1° ± 0.2°
└── Right Knee Flexion: +6.7° ± 0.2°

Ankle Joints:
├── Left Ankle Dorsiflexion: -8.3° ± 0.3°
└── Right Ankle Dorsiflexion: +15.2° ± 0.3°
```

#### Center of Mass Tracking

**Precise CoM Analysis**:
```python
Center of Mass (Frame 200):
===========================
Position: (1.24m, 0.02m, 0.87m)
Velocity: (1.18 m/s, 0.05 m/s, 0.12 m/s)
Acceleration: (0.23 m/s², -0.31 m/s², -0.87 m/s²)

Stability Metrics:
├── Support polygon: 0.24m × 0.12m
├── CoM within polygon: YES (safe)
├── Stability margin: 0.08m (good)
└── Fall risk: NONE (stable)
```

#### Energy Analysis Per Frame

**Detailed Energy Breakdown**:
```python
Energy Analysis (Frame 156):
============================
Kinetic Energy: 245.7 Joules
├── Translational KE: 178.3 J (72.5%)
├── Rotational KE: 67.4 J (27.5%)
└── Joint motion KE: 45.2 J (18.4%)

Potential Energy: 423.8 Joules
├── Gravitational PE: 423.8 J
├── Height above ground: 0.87m
└── Energy efficiency: 82.4%

Total Energy: 669.5 Joules
Energy change from previous frame: +2.1 J
```

### Step 5: Understanding the Code

#### Slow Motion Control System
```python
class SlowMotionViewer:
    def __init__(self, trajectory):
        self.trajectory = trajectory
        self.current_frame = 0
        self.playback_speed = 0.1  # Start at 1/10 speed
        self.is_playing = False
        self.frame_time = 1/50     # 50 Hz original data
        self.setup_environment()
        
    def handle_keyboard_input(self):
        """Process real-time keyboard commands"""
        key = self.get_key_input()
        
        if key == ' ':  # Spacebar
            self.is_playing = not self.is_playing
        elif key == 'right':
            self.step_forward()
        elif key == 'left':
            self.step_backward()
        elif key == 'up':
            self.increase_speed()
        elif key == 'down':
            self.decrease_speed()
        elif key == 'r':
            self.reset_to_start()
        elif key == 's':
            self.save_frame_analysis()
        elif key == 'q':
            return False  # Quit
        return True
    
    def step_forward(self):
        """Advance one frame with analysis"""
        if self.current_frame < len(self.trajectory) - 1:
            self.current_frame += 1
            self.update_display()
            self.analyze_current_frame()
    
    def step_backward(self):
        """Go back one frame with analysis"""
        if self.current_frame > 0:
            self.current_frame -= 1
            self.update_display()
            self.analyze_current_frame()
```

#### Frame Analysis System
```python
def analyze_current_frame(self):
    """Comprehensive analysis of current frame"""
    frame_data = self.trajectory[self.current_frame]
    
    # Extract joint information
    joint_angles = self.extract_joint_angles(frame_data)
    joint_velocities = self.compute_joint_velocities()
    
    # Compute center of mass
    com_position = self.compute_center_of_mass(frame_data)
    com_velocity = self.compute_com_velocity()
    
    # Energy calculations
    energy_metrics = self.compute_energy_metrics(frame_data)
    
    # Gait phase detection
    gait_phase = self.detect_gait_phase(frame_data)
    
    # Display analysis
    self.display_frame_analysis({
        'frame': self.current_frame,
        'time': self.current_frame * self.frame_time,
        'joints': joint_angles,
        'velocities': joint_velocities,
        'com': com_position,
        'energy': energy_metrics,
        'gait_phase': gait_phase
    })

def compute_joint_velocities(self):
    """Calculate joint velocities using numerical differentiation"""
    if self.current_frame == 0:
        # Forward difference for first frame
        next_frame = self.trajectory[1]
        current_frame = self.trajectory[0]
        velocities = (next_frame - current_frame) / self.frame_time
    elif self.current_frame == len(self.trajectory) - 1:
        # Backward difference for last frame  
        current_frame = self.trajectory[-1]
        prev_frame = self.trajectory[-2]
        velocities = (current_frame - prev_frame) / self.frame_time
    else:
        # Central difference for middle frames
        next_frame = self.trajectory[self.current_frame + 1]
        prev_frame = self.trajectory[self.current_frame - 1]
        velocities = (next_frame - prev_frame) / (2 * self.frame_time)
    
    return velocities
```

#### Gait Phase Detection
```python
def detect_gait_phase(self, frame_data):
    """Identify current phase of walking gait"""
    # Extract foot positions and contact forces
    left_foot_height = self.get_foot_height(frame_data, 'left')
    right_foot_height = self.get_foot_height(frame_data, 'right')
    
    # Ground contact detection (simplified)
    left_contact = left_foot_height < 0.05  # 5cm threshold
    right_contact = right_foot_height < 0.05
    
    # Determine gait phase
    if left_contact and right_contact:
        return "Double support"
    elif left_contact and not right_contact:
        return "Left stance / Right swing"
    elif not left_contact and right_contact:
        return "Right stance / Left swing"
    else:
        return "Double swing (running)"

def get_foot_height(self, frame_data, foot_side):
    """Calculate foot height above ground"""
    # Forward kinematics to compute foot position
    joint_angles = frame_data[:23]  # First 23 elements are joint angles
    
    if foot_side == 'left':
        foot_joints = [0, 1, 2]  # Left hip, knee, ankle indices
    else:
        foot_joints = [6, 7, 8]  # Right hip, knee, ankle indices
    
    # Simplified foot height calculation
    ankle_angle = joint_angles[foot_joints[2]]
    knee_angle = joint_angles[foot_joints[1]]
    
    # Estimate foot height from joint configuration
    estimated_height = 0.1 * np.sin(ankle_angle) + 0.05 * np.sin(knee_angle)
    return max(0, estimated_height)
```

## Technical Details

### Frame Analysis Precision

**Temporal Resolution**:
- **Data frequency**: 50 Hz (0.02 second intervals)
- **Frame precision**: Sub-degree joint angle accuracy
- **Time stamps**: Millisecond precision timing
- **Interpolation**: Optional sub-frame analysis capability

**Measurement Accuracy**:
```python
MEASUREMENT_PRECISION = {
    'joint_angles': 0.1,      # degrees
    'joint_velocities': 0.5,   # degrees/second  
    'positions': 0.001,        # meters
    'velocities': 0.01,        # meters/second
    'energy': 1.0,             # joules
    'timing': 0.001            # seconds
}
```

### Advanced Analysis Features

**Gait Event Detection**:
```python
GAIT_EVENTS = {
    'heel_strike': 'Initial ground contact',
    'foot_flat': 'Full foot ground contact', 
    'mid_stance': 'Single limb support peak',
    'heel_off': 'Heel lift initiation',
    'toe_off': 'Final ground contact loss',
    'mid_swing': 'Maximum limb flexion',
    'terminal_swing': 'Limb extension for contact'
}
```

**Biomechanical Metrics**:
```python
def calculate_biomechanical_metrics(frame_data):
    """Advanced biomechanical analysis"""
    return {
        'joint_power': joint_torque * joint_velocity,
        'mechanical_work': integrate(joint_power, time),
        'muscle_activation': estimate_muscle_forces(joint_angles),
        'balance_stability': compute_stability_margin(com, support_polygon),
        'energy_efficiency': mechanical_work / total_energy,
        'coordination_index': measure_joint_coordination(joint_velocities)
    }
```

## Troubleshooting

### Common Issues

**Problem**: Frame stepping too fast or unresponsive
**Solution**: Adjust keyboard input timing
```python
# Add input delays for better control
import time
def get_key_input_with_delay():
    key = get_raw_key_input()
    if key:
        time.sleep(0.1)  # Prevent rapid repeated inputs
    return key
```

**Problem**: Analysis data appears incorrect
**Solution**: Verify frame data interpretation
```python
# Debug frame data structure
frame = trajectory[current_frame]
print(f"Frame shape: {frame.shape}")
print(f"Joint angles: {frame[:23]}")  # First 23 are joint angles
print(f"Data range: {frame.min():.3f} to {frame.max():.3f}")
```

**Problem**: Slow motion playback is jerky
**Solution**: Optimize rendering performance
```python
# Reduce rendering complexity during slow motion
def optimized_render_for_slow_motion():
    env.render(mode='human', 
               width=640, height=480,  # Lower resolution
               camera_id=0)            # Fixed camera
```

**Problem**: Gait phase detection seems inaccurate
**Solution**: Calibrate ground contact detection
```python
# Adjust ground contact thresholds
GROUND_CONTACT_THRESHOLD = 0.02  # 2cm instead of 5cm
CONTACT_FORCE_THRESHOLD = 10.0   # Newtons minimum force

def improved_contact_detection(frame_data):
    foot_height = get_foot_height(frame_data, 'left')
    contact_force = estimate_contact_force(frame_data, 'left')
    
    return (foot_height < GROUND_CONTACT_THRESHOLD and 
            contact_force > CONTACT_FORCE_THRESHOLD)
```

### Performance Optimization

**Memory Management**:
```python
# Optimize for large trajectory analysis
class MemoryEfficientViewer:
    def __init__(self, trajectory):
        self.trajectory_length = len(trajectory)
        self.load_frame_on_demand = True  # Don't load all frames
        self.frame_cache_size = 100       # Cache recent frames only
        
    def get_frame_data(self, frame_index):
        """Load frame data on demand"""
        if frame_index in self.frame_cache:
            return self.frame_cache[frame_index]
        else:
            frame_data = self.load_frame_from_disk(frame_index)
            self.update_cache(frame_index, frame_data)
            return frame_data
```

## What You Learned

### Detailed Motion Analysis
- Frame-by-frame analysis techniques for precise motion study
- Biomechanical event detection and timing analysis
- Slow motion visualization for detailed observation
- Precision measurement of joint angles and movements

### Technical Skills
- Interactive frame control and navigation systems
- Real-time analysis and display of motion metrics
- Gait phase detection and classification algorithms  
- Performance optimization for smooth slow motion playback

### Research Methods
- Systematic approach to detailed motion analysis
- Understanding temporal dynamics of robot movement
- Quantitative assessment of movement quality
- Professional motion debugging and inspection techniques

## What's Next

With detailed analysis mastery:
- **Lesson 1.10**: Complete tutorial summary and graduation ceremony
- **Advanced projects**: Custom motion analysis tools and research applications
- **Unit 2 preparation**: Advanced robotics and custom environment development

## Key Takeaways

- Frame-by-frame analysis reveals hidden motion details
- Slow motion observation enables precise biomechanical study
- Detailed timing analysis is crucial for understanding gait
- Interactive control enhances motion analysis workflow
- Precision measurement tools enable quantitative motion science

**Microscopic analysis transforms casual observation into scientific understanding!**

This lesson provides advanced motion analysis skills essential for research-level robotics work, enabling detailed study of movement patterns that are invisible at normal speeds.