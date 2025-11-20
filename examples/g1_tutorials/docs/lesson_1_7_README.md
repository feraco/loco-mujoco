# Lesson 1.7: Dataset Explorer

## Learning Objectives

By the end of this lesson, you will:
- Navigate large motion dataset collections systematically
- Filter and search motion data by categories and characteristics
- Compare multiple motion types simultaneously
- Understand dataset metadata and organization systems
- Master advanced dataset exploration techniques

## What You'll Do

1. **Launch comprehensive dataset browser interface**
2. **Filter motions by category, difficulty, and duration**
3. **Preview and compare multiple motion sequences**
4. **Search datasets using metadata and characteristics**
5. **Bookmark and organize favorite motion sequences**

## Prerequisites

- Completed Lessons 1.1 through 1.6
- Understanding of motion datasets and categories
- Familiarity with motion analysis concepts

## Step-by-Step Instructions

### Step 1: Launch Dataset Explorer
```bash
cd /path/to/loco-mujoco/examples/g1_tutorials
python lesson_1_7_dataset_explorer.py
```

### Step 2: Explorer Interface

When you run the lesson, you will see:

1. **Console Menu**:
   ```
   G1 Robot Dataset Explorer
   =========================
   
   Available Commands:
   1. list - Show all available datasets
   2. filter <category> - Filter by motion category
   3. search <keyword> - Search motion descriptions
   4. preview <motion_id> - Quick motion preview
   5. compare <motion1> <motion2> - Compare two motions
   6. info <motion_id> - Detailed motion information
   7. play <motion_id> - Full motion playback
   8. bookmark <motion_id> - Save to favorites
   9. help - Show this menu
   10. quit - Exit explorer
   
   Total datasets loaded: 47 motions
   Categories: locomotion, stationary, transitions, dance, sports
   ```

2. **Interactive Navigation**:
   - Type commands to explore datasets
   - Real-time filtering and search results
   - Quick preview capabilities
   - Detailed motion information display

### Step 3: Dataset Navigation Commands

#### Basic Exploration

**List All Datasets**:
```bash
> list
Available Datasets (47 total):
├── locomotion (12 motions)
│   ├── walk_slow, walk_normal, walk_fast
│   ├── run_light, run_moderate, run_sprint
│   ├── jog_steady, jog_interval
│   └── march_military, march_parade
├── stationary (8 motions)
│   ├── stand_relaxed, stand_attention
│   ├── sit_chair, sit_ground, sit_cross_legged
│   └── squat_deep, squat_partial, squat_hold
├── transitions (15 motions)
│   ├── walk_to_run, run_to_walk
│   ├── sit_to_stand, stand_to_sit
│   └── ... (11 more)
├── dance (7 motions)
│   ├── dance_contemporary, dance_jazz
│   └── ... (5 more)
└── sports (5 motions)
    ├── tennis_serve, basketball_dribble
    └── ... (3 more)
```

**Filter by Category**:
```bash
> filter locomotion
Filtered Results: 12 locomotion motions
├── walk_slow (8.2s, easy, 0.8 m/s)
├── walk_normal (10.1s, easy, 1.2 m/s)
├── walk_fast (7.8s, medium, 1.8 m/s)
├── run_light (6.5s, medium, 2.2 m/s)
├── run_moderate (8.0s, medium, 3.1 m/s)
├── run_sprint (4.2s, hard, 4.5 m/s)
└── ... (6 more)
```

#### Advanced Search

**Search by Keywords**:
```bash
> search dance
Search Results for "dance":
├── dance_contemporary (24.1s, expert, artistic)
├── dance_jazz (18.7s, hard, rhythmic)
├── dance_ballet_basic (15.2s, medium, classical)
├── lafan1_dance1_subject4 (20.8s, expert, professional)
└── lafan1_dance2_subject2 (25.3s, expert, choreographed)

> search fast
Search Results for "fast":
├── walk_fast (7.8s, medium, 1.8 m/s)
├── run_sprint (4.2s, hard, 4.5 m/s)
├── transition_quick_turn (2.1s, medium, agile)
└── sports_tennis_serve (3.5s, hard, explosive)
```

#### Motion Information

**Detailed Motion Info**:
```bash
> info walk_normal
Motion: walk_normal
====================
Category: locomotion
Duration: 10.1 seconds
Difficulty: easy
Speed: 1.2 m/s average
Quality: 95% biomechanical accuracy
Source: motion_capture_studio
Joints: 23 (full body)
Frames: 505 (50 Hz)
File size: 2.1 MB

Description:
Natural walking gait at comfortable pace. Suitable for
general locomotion tasks and baseline comparisons.
Features symmetric gait cycle with heel-toe contact
pattern and coordinated arm swing.

Characteristics:
- Step length: 0.65 ± 0.08 meters
- Cadence: 110 ± 5 steps/minute
- Ground contact: 62% duty cycle
- Energy efficiency: 0.28 J/kg/m
- Stability margin: 0.12 meters

Applications:
- Basic locomotion demonstration
- Gait analysis baseline
- Imitation learning training data
- Biomechanical validation
```

#### Motion Preview and Comparison

**Quick Preview**:
```bash
> preview walk_fast
Previewing: walk_fast (3 seconds)
[3D visualization shows 3-second clip]
Preview complete. Use 'play walk_fast' for full motion.

> preview dance_jazz
Previewing: dance_jazz (3 seconds)  
[3D visualization shows dance sequence clip]
Preview complete. Complex motion with artistic elements.
```

**Motion Comparison**:
```bash
> compare walk_normal run_light
Comparing: walk_normal vs run_light
=====================================

Speed Comparison:
├── walk_normal: 1.2 m/s (comfortable pace)
└── run_light: 2.2 m/s (83% faster)

Energy Comparison:
├── walk_normal: 0.28 J/kg/m (efficient)
└── run_light: 0.45 J/kg/m (61% higher cost)

Gait Characteristics:
├── walk_normal: 62% duty cycle (always ground contact)
└── run_light: 45% duty cycle (flight phase present)

Joint Range:
├── walk_normal: ±35° hip flexion
└── run_light: ±55° hip flexion (57% greater range)

Stability:
├── walk_normal: 0.12m stability margin (very stable)
└── run_light: 0.08m stability margin (dynamically stable)
```

### Step 4: Understanding Dataset Organization

#### Motion Categories

**Locomotion Motions**:
- **Basic**: walk_slow, walk_normal, walk_fast
- **Running**: run_light, run_moderate, run_sprint
- **Specialized**: march_military, march_parade
- **Variations**: jog_steady, jog_interval

**Stationary Motions**:
- **Standing**: stand_relaxed, stand_attention, stand_balance
- **Sitting**: sit_chair, sit_ground, sit_cross_legged
- **Squatting**: squat_deep, squat_partial, squat_hold

**Transition Motions**:
- **Locomotion changes**: walk_to_run, run_to_walk
- **Posture changes**: sit_to_stand, stand_to_sit
- **Direction changes**: turn_left, turn_right, turn_around

**Artistic Motions**:
- **Dance**: contemporary, jazz, ballet basics
- **Expressive**: gesture sequences, emotional poses
- **LAFAN1**: Professional motion capture data

#### Metadata Structure

**Motion Properties**:
```python
motion_metadata = {
    'id': 'walk_normal',
    'category': 'locomotion',
    'subcategory': 'walking',
    'difficulty': 'easy',           # easy, medium, hard, expert
    'duration': 10.1,               # seconds
    'speed': 1.2,                   # m/s average
    'energy_cost': 0.28,            # J/kg/m
    'quality_score': 0.95,          # 0-1 biomechanical accuracy
    'source': 'motion_capture',     # capture method
    'validated': True,              # physics validation
    'tags': ['natural', 'baseline', 'symmetric']
}
```

### Step 5: Understanding the Code

#### Dataset Management System
```python
class DatasetExplorer:
    def __init__(self):
        self.datasets = self.load_all_datasets()
        self.bookmarks = []
        self.current_filter = None
        
    def load_all_datasets(self):
        """Load and index all available motion datasets"""
        datasets = {}
        
        # Load default datasets
        for motion_type in DEFAULT_MOTIONS:
            datasets[motion_type] = self.load_motion_metadata(motion_type)
            
        # Load LAFAN1 datasets if available
        for lafan_motion in LAFAN1_MOTIONS:
            datasets[lafan_motion] = self.load_lafan_metadata(lafan_motion)
            
        return datasets
    
    def filter_datasets(self, category=None, difficulty=None, duration_range=None):
        """Filter datasets by multiple criteria"""
        filtered = self.datasets.copy()
        
        if category:
            filtered = {k: v for k, v in filtered.items() 
                       if v['category'] == category}
        if difficulty:
            filtered = {k: v for k, v in filtered.items()
                       if v['difficulty'] == difficulty}
        if duration_range:
            min_dur, max_dur = duration_range
            filtered = {k: v for k, v in filtered.items()
                       if min_dur <= v['duration'] <= max_dur}
                       
        return filtered
```

#### Search and Comparison System
```python
def search_motions(self, query):
    """Search motion descriptions and metadata"""
    query_lower = query.lower()
    results = {}
    
    for motion_id, metadata in self.datasets.items():
        # Search in motion ID
        if query_lower in motion_id.lower():
            results[motion_id] = metadata
            continue
            
        # Search in description
        if 'description' in metadata and query_lower in metadata['description'].lower():
            results[motion_id] = metadata
            continue
            
        # Search in tags
        if 'tags' in metadata:
            for tag in metadata['tags']:
                if query_lower in tag.lower():
                    results[motion_id] = metadata
                    break
    
    return results

def compare_motions(self, motion1_id, motion2_id):
    """Generate detailed comparison between two motions"""
    m1 = self.datasets[motion1_id]
    m2 = self.datasets[motion2_id]
    
    comparison = {
        'speed_ratio': m2['speed'] / m1['speed'],
        'duration_diff': m2['duration'] - m1['duration'],
        'energy_ratio': m2['energy_cost'] / m1['energy_cost'],
        'difficulty_comparison': self.compare_difficulty(m1['difficulty'], m2['difficulty'])
    }
    
    return comparison
```

#### Interactive Console Interface
```python
def run_interactive_explorer(self):
    """Main interactive loop for dataset exploration"""
    print("G1 Robot Dataset Explorer")
    print("=" * 25)
    self.show_help()
    
    while True:
        try:
            command = input("> ").strip().split()
            if not command:
                continue
                
            cmd = command[0].lower()
            args = command[1:] if len(command) > 1 else []
            
            if cmd == 'quit':
                break
            elif cmd == 'list':
                self.list_datasets()
            elif cmd == 'filter':
                category = args[0] if args else None
                self.filter_and_display(category)
            elif cmd == 'search':
                query = ' '.join(args) if args else ''
                self.search_and_display(query)
            elif cmd == 'info':
                motion_id = args[0] if args else ''
                self.show_motion_info(motion_id)
            # ... handle other commands
            
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")
```

## Technical Details

### Dataset Loading Performance

**Optimization Strategies**:
- **Lazy loading**: Load metadata first, motion data on demand
- **Caching**: Store frequently accessed motions in memory
- **Indexing**: Pre-build search indices for fast queries
- **Compression**: Use efficient storage formats

**Performance Metrics**:
- **Metadata loading**: <500ms for 50+ motions
- **Search operations**: <100ms for text queries
- **Motion preview**: <2s for 3-second clips
- **Full motion loading**: <5s for 30-second sequences

### Search Algorithm Implementation

**Multi-Field Search**:
```python
def build_search_index(self):
    """Create searchable index of all motion data"""
    self.search_index = {}
    
    for motion_id, metadata in self.datasets.items():
        # Index motion ID
        words = motion_id.lower().split('_')
        for word in words:
            if word not in self.search_index:
                self.search_index[word] = []
            self.search_index[word].append(motion_id)
        
        # Index tags
        if 'tags' in metadata:
            for tag in metadata['tags']:
                tag_lower = tag.lower()
                if tag_lower not in self.search_index:
                    self.search_index[tag_lower] = []
                self.search_index[tag_lower].append(motion_id)
```

## Troubleshooting

### Common Issues

**Problem**: Some datasets not appearing in listings
**Solution**: Check dataset installation and permissions
```python
# Verify dataset availability
import os
cache_dir = os.path.expanduser("~/.loco-mujoco-caches")
print(f"Cache directory: {cache_dir}")
print(f"Cache exists: {os.path.exists(cache_dir)}")

# List available dataset files
if os.path.exists(cache_dir):
    for root, dirs, files in os.walk(cache_dir):
        print(f"Directory: {root}")
        for file in files[:5]:  # Show first 5 files
            print(f"  File: {file}")
```

**Problem**: Search returns no results for known motions
**Solution**: Check search index and motion metadata
```python
# Debug search functionality
explorer = DatasetExplorer()
print(f"Total datasets loaded: {len(explorer.datasets)}")
print(f"Sample motion IDs: {list(explorer.datasets.keys())[:5]}")

# Test specific search
results = explorer.search_motions("walk")
print(f"Search results for 'walk': {len(results)}")
```

**Problem**: Motion previews not working
**Solution**: Verify environment creation and rendering
```python
# Test motion loading
try:
    from loco_mujoco import ImitationFactory
    from loco_mujoco.datasets import DefaultDatasetConf
    
    env = ImitationFactory.make("UnitreeG1", 
                               default_dataset_conf=DefaultDatasetConf(["walk"]))
    trajectory = env.sample_trajectory()
    print(f"Motion loaded successfully: {len(trajectory)} frames")
except Exception as e:
    print(f"Motion loading failed: {e}")
```

## What You Learned

### Dataset Management
- Systematic exploration of large motion collections
- Filtering and searching techniques for motion data
- Understanding dataset organization and metadata systems
- Comparison methods for motion characteristics

### Technical Skills
- Interactive console interface development
- Search algorithm implementation for motion data
- Dataset indexing and caching strategies
- Motion metadata analysis and interpretation

### Research Methods
- Systematic approach to motion dataset analysis
- Quantitative comparison of movement characteristics
- Understanding motion quality metrics and validation
- Organization techniques for research datasets

## What's Next

With dataset exploration mastery:
- **Lesson 1.8**: Automated testing and validation systems
- **Lesson 1.9**: Detailed frame-by-frame motion analysis
- **Advanced projects**: Custom dataset curation and analysis

## Key Takeaways

- Systematic exploration reveals hidden patterns in motion data
- Metadata organization enables efficient dataset navigation
- Comparison tools provide objective motion analysis
- Search capabilities accelerate research workflows
- Interactive exploration builds intuitive understanding

**Organized exploration transforms large datasets into accessible knowledge!**

This lesson provides essential skills for working with large motion datasets, enabling systematic research and efficient discovery of relevant motion data.