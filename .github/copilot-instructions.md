# LocoMuJoCo AI Development Guide

## Project Overview
LocoMuJoCo is an imitation learning benchmark for whole-body locomotion control supporting both **MuJoCo CPU** and **MJX GPU** environments. The codebase emphasizes JAX-based algorithms, modular architecture through task factories, and extensive humanoid/quadruped robot datasets.

## Core Architecture

### Factory Pattern System
- **TaskFactory** (`loco_mujoco/task_factories/`): Central registry for creating environments
  - `RLFactory.make("UnitreeG1")` - RL environments with custom rewards
  - `ImitationFactory.make("UnitreeG1", default_dataset_conf=DefaultDatasetConf(["walk"]))` - Imitation with datasets
- All factories auto-register via `factory.register()` calls in `__init__.py`

### Dual Simulation Engines
- **Mujoco** (`loco_mujoco/core/Mujoco`): CPU simulation, good for debugging/visualization
- **Mjx** (`loco_mujoco/core/Mjx`): GPU-accelerated via JAX, optimized for training
  - MJX requires XML modifications (simplified contacts, primitive shapes) - see `_modify_spec_for_mjx()` pattern
  - Use `mjx_step()`/`mjx_reset()` for GPU, `step()`/`reset()` for CPU fallback

### Observation/Action Specification
```python
# Define what you want to observe from the XML
observation_spec = [
    ObservationType.JointPos("joint_pos", "knee_angle_l"),
    ObservationType.BodyVel("body_vel", "torso")
]
# Specify actuator names from XML
action_spec = ["hip_actuator", "knee_actuator"]
```

## JAX Training Pattern

### Standard Training Flow
1. **Environment**: Create via factory with MJX for performance
2. **Agent Config**: `PPOJax.init_agent_conf(env, config)`
3. **Training Function**: `PPOJax.build_train_fn(env, agent_conf)`
4. **JIT Compilation**: `jax.jit(jax.vmap(train_fn))` for multi-seed training
5. **Execution**: Pass JAX PRNG keys, get jitted results

### Configuration via Hydra
- Use `@hydra.main(config_path="./", config_name="conf")` pattern
- YAML configs specify env_params, task_factory, hyperparameters
- Environment names: `MjxUnitreeG1`, `UnitreeH1`, `Atlas`, etc.

## Dataset System

### Dataset Configuration
```python
# Multiple dataset sources supported
env = ImitationFactory.make("UnitreeG1",
    default_dataset_conf=DefaultDatasetConf(["walk", "squat"]),
    lafan1_dataset_conf=LAFAN1DatasetConf(["dance2_subject4"]),
    amass_dataset_conf=AMASSDatasetConf(["DanceDB/..."])  # Requires SMPL setup
)
```

### Dataset Caching
- Datasets store only joint pos/vel, compute FK on load
- Speed up with: `loco-mujoco-set-all-caches --path "$HOME/.loco-mujoco-caches"`
- Auto-download from HuggingFace for default/LAFAN1 datasets

## Development Workflows

### Environment Testing
```python
# Quick environment validation
env = RLFactory.make("UnitreeG1")
env.reset(jax.random.key(0))
env.render()  # Visual debugging
```

### Training Experiments
- Use `examples/training_examples/jax_rl/experiment.py` as template
- Hydra configs in same directory define hyperparameters
- WandB integration for logging metrics

### GPU vs CPU Development
- **Development/Debugging**: Use `Mujoco` class for step-through debugging
- **Training**: Switch to `Mjx` with `n_envs=2048+` for performance
- **Rendering**: Both support `render()`, MJX has `mjx_render(state)`

## Key File Patterns

### Models Directory
- Robot XMLs in `loco_mujoco/models/` (unitree_h1, unitree_g1, atlas, etc.)
- Environment classes auto-discover models by name matching

### Algorithm Structure
- JAX algorithms in `loco_mujoco/algorithms/` (PPOJax, GAILJax, AMPJax)
- Each has `init_agent_conf()`, `build_train_fn()`, `save_agent()` methods
- Pure JAX implementation for JIT compilation

### Environment Registration
- Environments auto-register via `LocoEnv.register()` decorators
- Check available: `loco_mujoco.get_registered_envs()`

## Common Pitfalls

1. **MJX Performance**: Ensure `n_envs >= 1000` for GPU efficiency
2. **Dataset Loading**: Cache datasets to avoid repeated FK computation
3. **XML Compatibility**: MJX requires simplified contact models (see core/README.md examples)
4. **SMPL Setup**: MyoSkeleton requires `loco-mujoco-myomodel-init` license acceptance
5. **JAX Compilation**: Use `jax.jit()` on training functions, not individual steps

## Testing
- Run `python test_locomujoco_examples.py` for basic functionality
- Individual algorithm tests in `tests/` directory
- Environment-specific examples in `examples/g1_tutorials/`