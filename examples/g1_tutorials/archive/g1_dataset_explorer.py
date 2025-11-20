#!/usr/bin/env python3
"""
G1 Dataset Explorer - Find and list all available datasets for UnitreeG1
"""

import os
from pathlib import Path

def find_dataset_locations():
    """Find where LocoMuJoCo stores datasets"""
    print("🔍 Searching for LocoMuJoCo dataset locations...")
    
    # Common dataset locations
    possible_locations = [
        Path.home() / ".loco_mujoco",
        Path("/tmp/loco_mujoco"),
        Path("/Users/wwhs-research/Downloads/humsim/loco-mujoco/data"),
        Path("/Users/wwhs-research/.cache/loco_mujoco"),
        Path(os.getcwd()) / "datasets",
    ]
    
    found_locations = []
    
    for location in possible_locations:
        if location.exists():
            print(f"✅ Found: {location}")
            found_locations.append(location)
            
            # List contents
            try:
                for item in location.rglob("*"):
                    if item.is_file() and item.suffix in ['.npz', '.csv', '.json']:
                        rel_path = item.relative_to(location)
                        print(f"   📄 {rel_path}")
                    elif item.is_dir() and 'UnitreeG1' in item.name:
                        print(f"   📁 {item.name}")
            except Exception as e:
                print(f"   ❌ Error reading {location}: {e}")
        else:
            print(f"❌ Not found: {location}")
    
    return found_locations

def list_available_datasets():
    """List datasets that can be used with UnitreeG1"""
    print("\n📋 Available Datasets for UnitreeG1")
    print("=" * 50)
    
    # Default datasets (these should be available)
    default_datasets = {
        "walk": "Standard walking motion",
        "squat": "Squatting exercise motion", 
        "stand": "Standing still pose",
        "stepinplace": "Stepping in place motion",
        "walk_fast": "Fast walking gait",
        "walk_slow": "Slow walking gait", 
        "jump": "Jumping motion pattern",
    }
    
    print("🎯 Default Datasets (Built-in):")
    for dataset, description in default_datasets.items():
        print(f"  • {dataset:<12} - {description}")
    
    # LAFAN1 datasets (motion capture)
    lafan1_datasets = {
        "walk1_subject1": "Walking motion from subject 1",
        "walk1_subject2": "Walking motion from subject 2", 
        "walk1_subject5": "Walking motion from subject 5",
        "dance1_subject1": "Dance choreography 1",
        "dance2_subject4": "Dance choreography 2",
        "dance3_subject2": "Dance choreography 3",
        "run1_subject1": "Running pattern 1",
        "run1_subject3": "Running pattern 3",
        "obstacles_subject2": "Obstacle navigation",
        "aiming1_subject3": "Aiming and pointing motions",
    }
    
    print("\n🎭 LAFAN1 Datasets (Motion Capture):")
    for dataset, description in lafan1_datasets.items():
        print(f"  • {dataset:<18} - {description}")

def test_dataset_import():
    """Test if we can import dataset configuration classes"""
    print("\n🧪 Testing Dataset Import Capabilities")
    print("-" * 40)
    
    try:
        from loco_mujoco.task_factories import DefaultDatasetConf
        print("✅ DefaultDatasetConf imported successfully")
        
        # Test creating a config
        config = DefaultDatasetConf(["walk"])
        print(f"✅ Created DefaultDatasetConf with walk dataset")
        
    except Exception as e:
        print(f"❌ DefaultDatasetConf import failed: {e}")
    
    try:
        from loco_mujoco.task_factories import LAFAN1DatasetConf
        print("✅ LAFAN1DatasetConf imported successfully")
        
        # Test creating a config
        config = LAFAN1DatasetConf(["walk1_subject1"])
        print(f"✅ Created LAFAN1DatasetConf with walk1_subject1 dataset")
        
    except Exception as e:
        print(f"❌ LAFAN1DatasetConf import failed: {e}")
    
    try:
        from loco_mujoco.task_factories import ImitationFactory
        print("✅ ImitationFactory imported successfully")
        
    except Exception as e:
        print(f"❌ ImitationFactory import failed: {e}")

def main():
    print("🤖 UnitreeG1 Dataset Explorer")
    print("=" * 50)
    
    # Find where datasets are stored
    dataset_locations = find_dataset_locations()
    
    # List available datasets
    list_available_datasets()
    
    # Test imports
    test_dataset_import()
    
    print("\n💡 Usage Tips:")
    print("  1. Datasets are downloaded automatically on first use")
    print("  2. Check ~/.loco_mujoco/ for cached datasets")
    print("  3. Use multiple datasets for variety: ['walk', 'stepinplace']")
    print("  4. LAFAN1 datasets provide higher quality human motion")
    print("  5. Increase n_substeps for smoother G1 motion")
    
    print("\n🚀 Try running the G1 tutorials:")
    print("  python g1_01_basic_datasets.py")
    print("  python g1_02_lafan1_datasets.py") 
    print("  python g1_03_interactive_control.py")
    print("  python g1_04_trajectory_generation.py")

if __name__ == "__main__":
    main()