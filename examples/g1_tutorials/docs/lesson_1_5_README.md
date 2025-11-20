# Lesson 1.5: Interactive Control

## Learning Objectives

By the end of this lesson, you will:
- Control the G1 robot in real-time with keyboard input
- Understand direct robot manipulation techniques
- Learn joint-level control and coordination
- Experience immediate feedback from robot actions
- Master safe robot control practices

## What You'll Do

1. **Launch persistent interactive robot control**
2. **Control individual joints with keyboard commands**
3. **Reset robot to safe poses when needed**
4. **Learn real-time robot response characteristics**
5. **Practice coordinated multi-joint movements**

## Prerequisites

- Completed Lessons 1.1 through 1.4
- Understanding of robot joint structure
- Familiarity with robot observation/action concepts

## Step-by-Step Instructions

### Step 1: Launch Interactive Control
```bash
cd /path/to/loco-mujoco/examples/g1_tutorials
python lesson_1_5_interactive_control.py
```

**Important**: This lesson runs continuously until you quit - no auto-closing!

### Step 2: Control Interface

When the lesson starts, you'll see:

1. **Console Instructions**:
   ```
   G1 Robot Interactive Control
   ============================
   Controls:
     w/s: Hip flexion/extension
     a/d: Hip abduction/adduction  
     q/e: Knee flexion/extension
     r/f: Ankle dorsi/plantar flexion
     t/g: Shoulder flexion/extension
     +/-: Increase/decrease action magnitude
     0: Reset robot to standing pose
     quit: Exit program
   
   Robot initialized. Use keyboard to control!
   Press keys to move the robot...
   ```

2. **3D Visualization**:
   - G1 robot in standing position
   - Real-time response to your keyboard inputs
   - Smooth joint movements
   - Immediate visual feedback

### Step 3: Control Commands

#### Basic Joint Controls

**Hip Controls**:
- **w**: Hip flexion (bend forward)
- **s**: Hip extension (lean backward)
- **a**: Hip abduction (legs apart)
- **d**: Hip adduction (legs together)

**Leg Controls**:
- **q**: Knee flexion (bend knees)
- **e**: Knee extension (straighten knees)
- **r**: Ankle dorsiflexion (toes up)
- **f**: Ankle plantarflexion (point toes)

**Arm Controls**:
- **t**: Shoulder flexion (arms forward)
- **g**: Shoulder extension (arms backward)

#### Control Modifiers

**Action Strength**:
- **+**: Increase action magnitude (stronger movements)
- **-**: Decrease action magnitude (gentler movements)

**Safety Commands**:
- **0**: Reset to neutral standing pose
- **quit**: Exit the program safely

### Step 4: Understanding Real-Time Control

#### Robot Response Characteristics

**Immediate Feedback**:
- Actions apply instantly when keys are pressed
- Robot responds within 20ms of input
- Visual feedback shows joint movement clearly
- Physics simulation maintains balance and stability

**Joint Behavior**:
- Each keypress applies torque to specific joints
- Multiple keys can be pressed simultaneously
- Actions accumulate for coordinated movement
- Robot attempts to maintain balance automatically

#### Control Strategy Tips

**Effective Techniques**:
1. **Start gentle**: Use low action magnitudes first (press '-' several times)
2. **Single joints**: Try one joint at a time initially
3. **Observe response**: Watch how robot reacts before next input
4. **Use reset**: Press '0' to return to safe pose when needed
5. **Gradual building**: Combine simple movements into complex ones

**Common Challenges**:
- Robot may become unstable with large actions
- Multiple simultaneous inputs can cause confusion
- Balance may be lost if actions are too aggressive
- Some joint combinations may conflict

### Step 5: Understanding the Code

#### Interactive Control System
```python
class InteractiveController:
    def __init__(self, env):
        self.env = env
        self.action_magnitude = 0.1  # Start with gentle actions
        self.joint_mapping = {
            'w': [0, 6],      # Hip flexion (left, right)
            's': [0, 6],      # Hip extension  
            'a': [1, 7],      # Hip abduction
            'd': [1, 7],      # Hip adduction
            # ... more mappings
        }
    
    def process_input(self, key):
        action = np.zeros(23)  # 23 joint actions
        if key in self.joint_mapping:
            joints = self.joint_mapping[key]
            for joint in joints:
                action[joint] = self.get_action_value(key)
        return action
```

#### Real-Time Control Loop
```python
def run_interactive_control():
    env = RLFactory.make("UnitreeG1")
    controller = InteractiveController(env)
    
    obs = env.reset()
    
    while True:  # Persistent control loop
        key = get_keyboard_input()  # Non-blocking input
        
        if key == 'quit':
            break
        elif key == '0':
            obs = env.reset()  # Reset to standing
        else:
            action = controller.process_input(key)
            obs, reward, done, info = env.step(action)
        
        env.render()  # Show current state
        time.sleep(1/50)  # 50 FPS control rate
```

#### Key Input Handling
```python
def get_keyboard_input():
    """Non-blocking keyboard input for real-time control"""
    if sys.platform == "win32":
        if msvcrt.kbhit():
            return msvcrt.getch().decode('utf-8')
    else:
        # Unix/Linux/macOS implementation
        import select, sys, tty, termios
        if select.select([sys.stdin], [], [], 0)[0]:
            return sys.stdin.read(1)
    return None
```

## Technical Details

### Control System Architecture

**Real-Time Requirements**:
- **Input latency**: <20ms from keypress to action
- **Control frequency**: 50 Hz action updates
- **Rendering rate**: 30-60 FPS visual feedback
- **Response time**: Immediate visual confirmation

**Safety Mechanisms**:
- **Action limiting**: Maximum torque values capped
- **Reset capability**: Instant return to safe pose
- **Graceful exit**: Clean program termination
- **Balance assistance**: Automatic stability corrections

### Joint Control Mapping

**G1 Robot Joint Layout**:
```
Joints [0-22]: 23 total actuated joints
├── Legs [0-11]: Hip, knee, ankle for both legs
├── Torso [12-14]: Waist and spine joints
├── Arms [15-22]: Shoulders, elbows, wrists
└── Head [not actuated]: Fixed orientation
```

**Control Mapping Strategy**:
- Symmetric control: Same key affects both left/right joints
- Logical grouping: Related joints controlled together
- Progressive magnitude: Adjustable action strength
- Safety priority: Easy reset and gentle defaults

### Performance Characteristics

**Responsiveness Metrics**:
- **Key detection**: <5ms input recognition
- **Action computation**: <1ms command generation
- **Physics update**: <10ms simulation step
- **Rendering**: <20ms visual update
- **Total latency**: <40ms keypress to visual feedback

## Troubleshooting

### Common Issues

**Problem**: Robot becomes unstable and falls
**Solution**: Reset immediately and use gentler actions
```
1. Press '0' to reset to standing pose
2. Press '-' multiple times to reduce action magnitude
3. Try single joint movements first
4. Build up complexity gradually
```

**Problem**: No response to keyboard input
**Solution**: Check console focus and input method
```
1. Click on the console window to ensure focus
2. Verify the 3D window doesn't have input focus
3. Try pressing keys multiple times
4. Restart if input system becomes unresponsive
```

**Problem**: Robot moves too fast/aggressively
**Solution**: Adjust action magnitude
```
1. Press '-' repeatedly to reduce action strength
2. Start with magnitude around 0.01-0.05
3. Gradually increase only after testing
4. Use '0' reset frequently for safety
```

**Problem**: Cannot exit the program
**Solution**: Use proper exit commands
```
1. Type 'quit' in the console
2. If unresponsive, press Ctrl+C
3. Close console window as last resort
```

### Input System Debugging

**Verify Keyboard Input**:
```python
# Test keyboard input detection
def test_keyboard():
    print("Press keys (type 'quit' to exit):")
    while True:
        key = get_keyboard_input()
        if key:
            print(f"Detected key: {key}")
            if key == 'quit':
                break
        time.sleep(0.1)
```

## What You Learned

### Direct Robot Control
- Real-time human-robot interaction techniques
- Joint-level control and coordination
- Safety practices for robot manipulation
- Understanding of robot response characteristics

### Technical Skills
- Keyboard input handling for robotics applications
- Real-time control system implementation
- Action mapping from human commands to joint torques
- Robot state management and reset procedures

### Control Theory Concepts
- Feedback control loops in robotics
- Human-in-the-loop control systems
- Real-time constraints and latency management
- Safety mechanisms in interactive robotics

## What's Next

With interactive control mastery:
- **Lesson 1.6**: Motion analysis with live data visualization
- **Lesson 1.7**: Dataset explorer with advanced interaction
- **Advanced topics**: Custom control interfaces and automation

## Key Takeaways

- Real-time robot control requires careful system design
- Human feedback is essential for effective robot interaction
- Safety mechanisms are critical in interactive systems
- Direct manipulation provides intuitive understanding of robot behavior
- Persistent control enables extended exploration and learning

**Hands-on control transforms theoretical knowledge into practical understanding!**

This lesson provides direct experience with robot control, building intuition for how robots respond to commands and developing skills for more advanced robotics applications.