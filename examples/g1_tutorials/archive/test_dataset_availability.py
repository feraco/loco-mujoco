#!/usr/bin/env python3
"""
G1 Dataset Availability Test - Check which datasets actually work
"""

from loco_mujoco.task_factories import ImitationFactory, DefaultDatasetConf

def test_dataset(dataset_name):
    """Test if a single dataset works"""
    print(f"🧪 Testing dataset: {dataset_name}")
    try:
        env = ImitationFactory.make("UnitreeG1",
                                   default_dataset_conf=DefaultDatasetConf([dataset_name]),
                                   n_substeps=10)
        print(f"✅ {dataset_name} - WORKS")
        return True
    except Exception as e:
        if "404" in str(e) or "Entry Not Found" in str(e):
            print(f"❌ {dataset_name} - NOT AVAILABLE (404 error)")
        else:
            print(f"❌ {dataset_name} - ERROR: {str(e)[:100]}")
        return False

def main():
    print("🤖 G1 Dataset Availability Test")
    print("=" * 50)
    print("🎯 Testing which datasets are actually available on the server")
    
    # List of datasets to test
    datasets_to_test = [
        "walk",
        "squat", 
        "stand",
        "stepinplace",
        "walk_fast",
        "walk_slow", 
        "jump",
        "run",
        "sit",
        "lie",
    ]
    
    working_datasets = []
    failed_datasets = []
    
    for dataset in datasets_to_test:
        if test_dataset(dataset):
            working_datasets.append(dataset)
        else:
            failed_datasets.append(dataset)
        print()  # Empty line for readability
    
    print("\n📊 RESULTS:")
    print("=" * 30)
    print(f"✅ Working datasets ({len(working_datasets)}):")
    for dataset in working_datasets:
        print(f"   • {dataset}")
    
    print(f"\n❌ Failed datasets ({len(failed_datasets)}):")
    for dataset in failed_datasets:
        print(f"   • {dataset}")
    
    print(f"\n💡 Use only the working datasets in your tutorials!")
    print(f"   Recommended: {working_datasets[:3] if len(working_datasets) >= 3 else working_datasets}")

if __name__ == "__main__":
    main()