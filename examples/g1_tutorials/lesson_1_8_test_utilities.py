#!/usr/bin/env python3
"""
🧪 Lesson 1.8: Test Utilities
============================

GOAL: Learn to test and validate robot systems systematically
WHY: Testing ensures your robots work reliably and helps debug problems

WHAT YOU'LL LEARN:
✅ Essential robot testing concepts
✅ Automated testing for robot systems
✅ Debugging common robot problems
✅ Performance validation techniques

Become a robot testing expert - ensure your robots work flawlessly!
"""

import time
import traceback
import numpy as np
from loco_mujoco.task_factories import RLFactory, ImitationFactory, DefaultDatasetConf, LAFAN1DatasetConf


def get_action_size(env):
    """🔧 Get action size from environment in a robust way"""
    if hasattr(env, 'action_size'):
        return env.action_size
    elif hasattr(env, 'action_space') and hasattr(env.action_space, 'shape'):
        return env.action_space.shape[0]
    else:
        return 23  # Default for G1 robot


def explain_robot_testing():
    """🧪 Explain why testing is crucial for robotics"""
    print("🧪 ROBOT TESTING FUNDAMENTALS")
    print("=" * 40)
    print("🎯 What is Robot Testing?")
    print("   • Systematic verification that robots work correctly")
    print("   • Checking for problems before they cause failures")
    print("   • Ensuring reliable and safe operation")
    print("   • Validating performance meets requirements")
    print("")
    print("⚠️ Why Testing is Critical:")
    print("   • Robots operate in physical world - failures can be dangerous")
    print("   • Complex systems have many failure modes")
    print("   • Early detection saves time and money")
    print("   • Builds confidence in robot reliability")
    print("")
    print("🔬 Types of Robot Testing:")
    print("   • UNIT TESTS: Individual components work correctly")
    print("   • INTEGRATION TESTS: Components work together")
    print("   • SYSTEM TESTS: Complete robot system functions")
    print("   • PERFORMANCE TESTS: Robot meets speed/accuracy requirements")
    print("   • SAFETY TESTS: Robot operates safely under all conditions")


def testing_strategies():
    """📋 Overview of robot testing strategies"""
    print("\n📋 TESTING STRATEGIES")
    print("=" * 40)
    
    strategies = [
        {
            "name": "Smoke Tests",
            "purpose": "Quick verification system works at all",
            "when": "Before any detailed testing",
            "example": "Can robot load? Can it move? Does it render?"
        },
        {
            "name": "Functional Tests",
            "purpose": "Verify specific features work correctly",
            "when": "For each major capability",
            "example": "Walking works, datasets load, controls respond"
        },
        {
            "name": "Performance Tests",
            "purpose": "Check if robot meets speed/quality requirements",
            "when": "After functional tests pass",
            "example": "Maintains 30 FPS, stable for 10 minutes"
        },
        {
            "name": "Stress Tests",
            "purpose": "Find breaking points and edge cases",
            "when": "Before deployment",
            "example": "Extreme motions, long duration, resource limits"
        },
        {
            "name": "Regression Tests",
            "purpose": "Ensure changes don't break existing functionality",
            "when": "After any system modifications",
            "example": "All previous tests still pass after updates"
        }
    ]
    
    print(f"{'Strategy':<18} {'Purpose':<35} {'Example'}")
    print("-" * 80)
    
    for strategy in strategies:
        print(f"{strategy['name']:<18} {strategy['purpose']:<35} {strategy['example']}")
    
    print(f"\n📋 DETAILED EXPLANATIONS:")
    for i, strategy in enumerate(strategies, 1):
        print(f"\n{i}. {strategy['name'].upper()}")
        print(f"   🎯 Purpose: {strategy['purpose']}")
        print(f"   ⏰ When: {strategy['when']}")
        print(f"   💡 Example: {strategy['example']}")


class RobotTester:
    """🧪 Automated robot testing utility"""
    
    def __init__(self):
        self.test_results = []
        self.passed = 0
        self.failed = 0
        
    def run_test(self, test_name, test_function, *args, **kwargs):
        """🔬 Run a single test and record results"""
        print(f"\n🧪 RUNNING: {test_name}")
        print("-" * 50)
        
        start_time = time.time()
        try:
            result = test_function(*args, **kwargs)
            duration = time.time() - start_time
            
            if result:
                print(f"✅ PASSED: {test_name} ({duration:.2f}s)")
                self.passed += 1
                self.test_results.append({
                    'name': test_name,
                    'status': 'PASSED',
                    'duration': duration,
                    'error': None
                })
                return True
            else:
                print(f"❌ FAILED: {test_name} ({duration:.2f}s)")
                self.failed += 1
                self.test_results.append({
                    'name': test_name,
                    'status': 'FAILED',
                    'duration': duration,
                    'error': 'Test returned False'
                })
                return False
                
        except Exception as e:
            duration = time.time() - start_time
            print(f"💥 ERROR: {test_name} ({duration:.2f}s)")
            print(f"   Error: {str(e)}")
            self.failed += 1
            self.test_results.append({
                'name': test_name,
                'status': 'ERROR',
                'duration': duration,
                'error': str(e)
            })
            return False
    
    def print_summary(self):
        """📊 Print test summary"""
        total = self.passed + self.failed
        print(f"\n📊 TEST SUMMARY")
        print("=" * 40)
        print(f"Total Tests: {total}")
        print(f"✅ Passed: {self.passed}")
        print(f"❌ Failed: {self.failed}")
        print(f"📊 Success Rate: {(self.passed/total*100) if total > 0 else 0:.1f}%")
        
        if self.failed > 0:
            print(f"\n❌ FAILED TESTS:")
            for result in self.test_results:
                if result['status'] in ['FAILED', 'ERROR']:
                    print(f"   • {result['name']}: {result['error']}")


def test_basic_robot_creation():
    """🤖 Test basic robot environment creation"""
    print("🎯 Testing basic robot creation...")
    
    try:
        # Test RL environment
        env = RLFactory.make("UnitreeG1", n_substeps=20)
        print("   ✅ RL environment created")
        
        # Test basic properties using robust approach
        action_size = get_action_size(env)
        assert action_size > 0, f"Environment should have valid action_size, got {action_size}"
        print(f"   ✅ Action size: {action_size}")
        
        # Test observation size if available
        if hasattr(env, 'observation_size'):
            assert env.observation_size > 0, "Environment should have valid observation_size"
            print(f"   ✅ Observation size: {env.observation_size}")
        else:
            print("   ℹ️  Observation size not directly available")
            
        print(f"   ✅ Environment created successfully with action size: {action_size}")
        
        del env
        return True
        
    except Exception as e:
        print(f"   ❌ Robot creation failed: {e}")
        return False


def test_environment_reset():
    """🔄 Test environment reset functionality"""
    print("🎯 Testing environment reset...")
    
    try:
        env = RLFactory.make("UnitreeG1", n_substeps=20)
        
        # Test reset returns proper format - handle different return types
        reset_result = env.reset()
        if isinstance(reset_result, tuple):
            state = reset_result[0]
            info = reset_result[1] if len(reset_result) > 1 else {}
        else:
            state = reset_result
            info = {}
        print("   ✅ Reset handled successfully")
        
        # Validate state format
        assert hasattr(state, '__len__'), "State should be array-like"
        assert len(state) > 0, f"State should have positive length, got {len(state)}"
        print(f"   ✅ State format valid (size: {len(state)})")
        
        # Test multiple resets
        for i in range(3):
            reset_result2 = env.reset()
            if isinstance(reset_result2, tuple):
                state2 = reset_result2[0]
            else:
                state2 = reset_result2
            assert len(state2) == len(state), "Reset should return consistent state size"
        print("   ✅ Multiple resets work consistently")
        
        del env
        return True
        
    except Exception as e:
        print(f"   ❌ Reset test failed: {e}")
        return False


def test_environment_step():
    """👣 Test environment step functionality"""
    print("🎯 Testing environment stepping...")
    
    try:
        env = RLFactory.make("UnitreeG1", n_substeps=20)
        
        # Robust reset handling
        reset_result = env.reset()
        if isinstance(reset_result, tuple):
            state = reset_result[0]
        else:
            state = reset_result
        
        # Create valid action using helper function
        action_size = get_action_size(env)
        action = np.zeros(action_size)
        print(f"   ✅ Created action with size {len(action)}")
        
        # Test step function with robust handling
        step_result = env.step(action)
        if len(step_result) == 5:
            next_state, reward, terminated, truncated, info = step_result
        elif len(step_result) == 4:
            next_state, reward, terminated, info = step_result
            truncated = False
        else:
            next_state, reward, terminated = step_result[:3]
            truncated = False
            info = {}
        print("   ✅ Step handled successfully")
        
        # Validate returns
        assert len(next_state) > 0, "Next state should have positive length"
        assert isinstance(reward, (int, float, np.floating)), "Reward should be numeric"
        assert isinstance(terminated, (bool, np.bool_)), "Terminated should be boolean"
        assert isinstance(truncated, (bool, np.bool_)), "Truncated should be boolean"
        print("   ✅ Return values have correct types")
        
        # Test multiple steps
        for i in range(5):
            step_result = env.step(action)
            if len(step_result) == 5:
                state, reward, terminated, truncated, info = step_result
            elif len(step_result) == 4:
                state, reward, terminated, info = step_result
                truncated = False
            else:
                state, reward, terminated = step_result[:3]
                truncated = False
                info = {}
            
            if terminated or truncated:
                reset_result = env.reset()
                if isinstance(reset_result, tuple):
                    state = reset_result[0]
                else:
                    state = reset_result
                print("   ✅ Environment handles episode termination")
        
        del env
        return True
        
    except Exception as e:
        print(f"   ❌ Step test failed: {e}")
        return False


def test_dataset_loading():
    """📦 Test dataset loading functionality"""
    print("🎯 Testing dataset loading...")
    
    try:
        # Test default datasets
        env1 = ImitationFactory.make(
            "UnitreeG1",
            default_dataset_conf=DefaultDatasetConf(["walk"]),
            n_substeps=20
        )
        print("   ✅ Default dataset (walk) loaded")
        del env1
        
        # Test LAFAN1 datasets 
        env2 = ImitationFactory.make(
            "UnitreeG1", 
            lafan1_dataset_conf=LAFAN1DatasetConf(["dance1_subject1"]),
            n_substeps=20
        )
        print("   ✅ LAFAN1 dataset (dance1_subject1) loaded")
        del env2
        
        # Test combined datasets
        env3 = ImitationFactory.make(
            "UnitreeG1",
            default_dataset_conf=DefaultDatasetConf(["walk"]),
            lafan1_dataset_conf=LAFAN1DatasetConf(["dance1_subject1"]),
            n_substeps=20
        )
        print("   ✅ Combined datasets loaded")
        del env3
        
        return True
        
    except Exception as e:
        print(f"   ❌ Dataset loading failed: {e}")
        return False


def test_rendering():
    """🎨 Test rendering functionality"""
    print("🎯 Testing rendering system...")
    
    try:
        env = RLFactory.make("UnitreeG1", n_substeps=20)
        
        # Robust reset handling
        reset_result = env.reset()
        if isinstance(reset_result, tuple):
            state = reset_result[0]
        else:
            state = reset_result
        
        # Test render function exists and works
        env.render()
        print("   ✅ Render function works")
        
        # Test rendering during simulation
        action_size = get_action_size(env)
        action = np.zeros(action_size)
        
        for i in range(5):
            step_result = env.step(action)
            if len(step_result) == 5:
                state, reward, terminated, truncated, info = step_result
            elif len(step_result) == 4:
                state, reward, terminated, info = step_result
                truncated = False
            else:
                state, reward, terminated = step_result[:3]
                truncated = False
                info = {}
                
            env.render()
            if terminated or truncated:
                reset_result = env.reset()
                if isinstance(reset_result, tuple):
                    state = reset_result[0]
                else:
                    state = reset_result
        
        print("   ✅ Rendering during simulation works")
        
        del env
        return True
        
    except Exception as e:
        print(f"   ❌ Rendering test failed: {e}")
        return False


def test_performance_basic():
    """⚡ Test basic performance requirements"""
    print("🎯 Testing basic performance...")
    
    try:
        env = RLFactory.make("UnitreeG1", n_substeps=20)
        
        # Robust reset handling
        reset_result = env.reset()
        if isinstance(reset_result, tuple):
            state = reset_result[0]
        else:
            state = reset_result
        
        action_size = get_action_size(env)
        action = np.zeros(action_size)
        
        # Measure step performance
        start_time = time.time()
        step_count = 0
        
        for i in range(100):  # 100 steps
            step_result = env.step(action)
            if len(step_result) == 5:
                state, reward, terminated, truncated, info = step_result
            elif len(step_result) == 4:
                state, reward, terminated, info = step_result
                truncated = False
            else:
                state, reward, terminated = step_result[:3]
                truncated = False
                info = {}
                
            step_count += 1
            
            if terminated or truncated:
                reset_result = env.reset()
                if isinstance(reset_result, tuple):
                    state = reset_result[0]
                else:
                    state = reset_result
        
        duration = time.time() - start_time
        steps_per_sec = step_count / duration
        
        print(f"   ✅ Performance: {steps_per_sec:.1f} steps/sec")
        
        # Basic performance requirement: should manage at least 10 steps/sec
        if steps_per_sec >= 10:
            print("   ✅ Meets minimum performance requirement (>10 steps/sec)")
            del env
            return True
        else:
            print(f"   ⚠️  Below minimum performance requirement ({steps_per_sec:.1f} < 10 steps/sec)")
            del env
            return False
        
    except Exception as e:
        print(f"   ❌ Performance test failed: {e}")
        return False


def test_stability():
    """🏗️ Test system stability"""
    print("🎯 Testing system stability...")
    
    try:
        env = RLFactory.make("UnitreeG1", n_substeps=20)
        
        action_size = get_action_size(env)
        
        # Test with various action patterns
        test_patterns = [
            ("Zero actions", np.zeros(action_size)),
            ("Small random", np.random.normal(0, 0.1, action_size)),
            ("Medium random", np.random.normal(0, 0.3, action_size)),
        ]
        
        for pattern_name, base_action in test_patterns:
            print(f"   🧪 Testing {pattern_name}...")
            
            # Robust reset handling
            reset_result = env.reset()
            if isinstance(reset_result, tuple):
                state = reset_result[0]
            else:
                state = reset_result
            
            stable_steps = 0
            for i in range(50):  # Test for 50 steps each
                # Add some variation
                action = base_action + np.random.normal(0, 0.05, action_size)
                action = np.clip(action, -1, 1)  # Ensure valid range
                
                step_result = env.step(action)
                if len(step_result) == 5:
                    state, reward, terminated, truncated, info = step_result
                elif len(step_result) == 4:
                    state, reward, terminated, info = step_result
                    truncated = False
                else:
                    state, reward, terminated = step_result[:3]
                    truncated = False
                    info = {}
                
                if not (terminated or truncated):
                    stable_steps += 1
                else:
                    reset_result = env.reset()
                    if isinstance(reset_result, tuple):
                        state = reset_result[0]
                    else:
                        state = reset_result
                    break
            
            print(f"      ✅ Stable for {stable_steps}/50 steps")
        
        del env
        return True
        
    except Exception as e:
        print(f"   ❌ Stability test failed: {e}")
        return False


def run_full_test_suite():
    """🧪 Run complete robot testing suite"""
    print("🧪 ROBOT SYSTEM TEST SUITE")
    print("=" * 50)
    print("Running comprehensive tests to validate robot system...")
    
    tester = RobotTester()
    
    # Core functionality tests
    tester.run_test("Basic Robot Creation", test_basic_robot_creation)
    tester.run_test("Environment Reset", test_environment_reset)
    tester.run_test("Environment Step", test_environment_step)
    
    # Data and rendering tests
    tester.run_test("Dataset Loading", test_dataset_loading)
    tester.run_test("Rendering System", test_rendering)
    
    # Performance and stability tests
    tester.run_test("Basic Performance", test_performance_basic)
    tester.run_test("System Stability", test_stability)
    
    # Print final summary
    tester.print_summary()
    
    return tester


def debugging_guide():
    """🔧 Guide for debugging common robot problems"""
    print("\n🔧 DEBUGGING GUIDE")
    print("=" * 40)
    print("🚨 Common Problems and Solutions:")
    
    problems = [
        {
            "problem": "Robot falls immediately",
            "causes": ["Extreme actions", "Poor initial state", "Unstable control"],
            "solutions": ["Use smaller action values", "Check reset function", "Improve control algorithm"]
        },
        {
            "problem": "Environment won't load",
            "causes": ["Missing dependencies", "Wrong robot name", "Corrupted files"],
            "solutions": ["Check installation", "Verify robot names", "Reinstall package"]
        },
        {
            "problem": "Slow performance", 
            "causes": ["High substeps", "Complex rendering", "Resource constraints"],
            "solutions": ["Reduce n_substeps", "Disable rendering", "Close other programs"]
        },
        {
            "problem": "Datasets won't load",
            "causes": ["Missing dataset files", "Network issues", "Wrong configuration"],
            "solutions": ["Check cache directory", "Try re-download", "Verify dataset names"]
        },
        {
            "problem": "Rendering issues",
            "causes": ["Graphics drivers", "Display settings", "OpenGL problems"],
            "solutions": ["Update drivers", "Check display connection", "Use software rendering"]
        }
    ]
    
    for i, prob in enumerate(problems, 1):
        print(f"\n{i}. {prob['problem'].upper()}")
        print(f"   🔍 Possible causes: {', '.join(prob['causes'])}")
        print(f"   🔧 Solutions: {', '.join(prob['solutions'])}")


def testing_best_practices():
    """📚 Best practices for robot testing"""
    print("\n📚 TESTING BEST PRACTICES")
    print("=" * 40)
    print("🎯 Effective Testing Strategies:")
    print("   • Test early and test often")
    print("   • Start with simple tests, build complexity")
    print("   • Automate repetitive tests")
    print("   • Document test results and patterns")
    print("")
    print("🔧 Debugging Techniques:")
    print("   • Isolate problems to smallest component")
    print("   • Use systematic elimination process")
    print("   • Check logs and error messages carefully")
    print("   • Test one change at a time")
    print("")
    print("📊 Performance Monitoring:")
    print("   • Establish baseline performance metrics")
    print("   • Monitor resource usage (CPU, memory)")
    print("   • Track performance over time")
    print("   • Set performance regression alerts")
    print("")
    print("🛡️ Safety Considerations:")
    print("   • Test edge cases and failure modes")
    print("   • Verify safety limits and constraints")
    print("   • Test recovery from error conditions")
    print("   • Document known limitations and risks")


def main():
    """🚀 Main lesson function"""
    print("🧪 Lesson 1.8: Test Utilities")
    print("=" * 50)
    print("🎯 Goal: Learn systematic robot testing and validation")
    print("⏱️  Time: ~12 minutes")
    print("🎓 Difficulty: Intermediate")
    
    # Theory and concepts
    explain_robot_testing()
    testing_strategies()
    
    # Practical testing
    tester = run_full_test_suite()
    
    # Debugging and best practices
    debugging_guide()
    testing_best_practices()
    
    print(f"\n🎓 LESSON COMPLETE!")
    print("=" * 50)
    print("✅ You've learned:")
    print("   • Essential robot testing concepts")
    print("   • Automated testing techniques")
    print("   • Common debugging approaches")
    print("   • Performance validation methods")
    print("")
    print("🚀 Ready for Lesson 1.9: Slow Motion Viewer")
    print("")
    print("🏆 EXPERIMENT IDEAS:")
    print("💡 Extended testing:")
    print("   • Create custom test suites for your projects")
    print("   • Add stress tests with extreme parameters")
    print("   • Test different robot models")
    print("💡 Performance optimization:")
    print("   • Benchmark different configurations")
    print("   • Profile resource usage patterns")
    print("   • Test scaling with parallel environments")
    print("💡 Reliability analysis:")
    print("   • Long-duration stability tests")
    print("   • Monte Carlo testing with random parameters")
    print("   • Failure mode analysis")


if __name__ == "__main__":
    main()