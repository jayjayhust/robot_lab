# Training Pipeline Architecture

<cite>
**Referenced Files in This Document**
- [scripts/reinforcement_learning/rsl_rl/train.py](file://scripts/reinforcement_learning/rsl_rl/train.py)
- [scripts/reinforcement_learning/rsl_rl/cli_args.py](file://scripts/reinforcement_learning/rsl_rl/cli_args.py)
- [scripts/reinforcement_learning/rsl_rl/play.py](file://scripts/reinforcement_learning/rsl_rl/play.py)
- [scripts/reinforcement_learning/rsl_rl/play_cs.py](file://scripts/reinforcement_learning/rsl_rl/play_cs.py)
- [scripts/reinforcement_learning/cusrl/train.py](file://scripts/reinforcement_learning/cusrl/train.py)
- [scripts/reinforcement_learning/cusrl/play.py](file://scripts/reinforcement_learning/cusrl/play.py)
- [scripts/reinforcement_learning/skrl/train.py](file://scripts/reinforcement_learning/skrl/train.py)
- [scripts/reinforcement_learning/skrl/play.py](file://scripts/reinforcement_learning/skrl/play.py)
- [scripts/reinforcement_learning/rl_utils.py](file://scripts/reinforcement_learning/rl_utils.py)
- [logs/rsl_rl/opendoge_apx_flat/2026-01-20_11-11-30/params/agent.yaml](file://logs/rsl_rl/opendoge_apx_flat/2026-01-20_11-11-30/params/agent.yaml)
</cite>

## Table of Contents
1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Core Components](#core-components)
4. [Architecture Overview](#architecture-overview)
5. [Detailed Component Analysis](#detailed-component-analysis)
6. [Dependency Analysis](#dependency-analysis)
7. [Performance Considerations](#performance-considerations)
8. [Troubleshooting Guide](#troubleshooting-guide)
9. [Conclusion](#conclusion)
10. [Appendices](#appendices)

## Introduction
This document explains the training pipeline architecture across three RL systems integrated in the repository: RSL-RL, CusRL, and SKRL. It covers:
- Multiple RL algorithm implementations and distributed training support
- RSL-RL PPO implementation, hyperparameters, and training optimization techniques
- CusRL experimental training system and its custom algorithm implementations
- SKRL training system for advanced RL algorithms including AMP (Associative Memory Paradigm)
- Concrete examples from the codebase showing training script usage, CLI argument configuration, and experiment tracking
- Distributed training architecture supporting multi-GPU and multi-node scenarios
- Training pipeline components including environment interaction, policy execution, gradient computation, and model updates
- Training optimization techniques such as curriculum learning, symmetry data augmentation, and model distillation
- Troubleshooting guidance for common training issues and performance optimization strategies

## Project Structure
The repository organizes RL training under scripts/reinforcement_learning with three subsystems:
- rsl_rl: RSL-RL training and playback scripts, plus CLI argument parsing and configuration overrides
- cusrl: CusRL training and playback scripts with distributed and optimization flags
- skrl: SKRL training and playback scripts supporting multiple algorithms (PPO, IPPO, MAPPO, AMP)

```mermaid
graph TB
subgraph "RL Systems"
RSL["RSL-RL<br/>train.py, play.py, play_cs.py, cli_args.py"]
CUS["CusRL<br/>train.py, play.py"]
SKR["SKRL<br/>train.py, play.py"]
end
subgraph "Environment Layer"
ENV["IsaacLab Environments<br/>ManagerBased/Direct/MARL"]
WRAP["Vectorized Env Wrappers<br/>RslRlVecEnvWrapper / SkrlVecEnvWrapper"]
end
subgraph "Logging & Artifacts"
LOGS["logs/<system>/<experiment>/<timestamp>"]
PARAMS["params/env.yaml, agent.yaml"]
CHECK["checkpoints/*.pt"]
VIDS["videos/train|play"]
end
RSL --> ENV
CUS --> ENV
SKR --> ENV
ENV --> WRAP
WRAP --> RSL
WRAP --> SKR
RSL --> LOGS
CUS --> LOGS
SKR --> LOGS
LOGS --> PARAMS
LOGS --> CHECK
LOGS --> VIDS
```

**Diagram sources**
- [scripts/reinforcement_learning/rsl_rl/train.py](file://scripts/reinforcement_learning/rsl_rl/train.py#L117-L225)
- [scripts/reinforcement_learning/cusrl/train.py](file://scripts/reinforcement_learning/cusrl/train.py#L79-L135)
- [scripts/reinforcement_learning/skrl/train.py](file://scripts/reinforcement_learning/skrl/train.py#L135-L237)

**Section sources**
- [scripts/reinforcement_learning/rsl_rl/train.py](file://scripts/reinforcement_learning/rsl_rl/train.py#L1-L232)
- [scripts/reinforcement_learning/cusrl/train.py](file://scripts/reinforcement_learning/cusrl/train.py#L1-L146)
- [scripts/reinforcement_learning/skrl/train.py](file://scripts/reinforcement_learning/skrl/train.py#L1-L250)

## Core Components
- Environment orchestration via gym.make with configurable num_envs, device, and render modes
- Vectorized environment wrappers tailored to each RL library
- Runner/Trainer abstractions that encapsulate policy execution, gradient computation, and model updates
- CLI-driven configuration overrides for seeds, logging, resume, and distributed training
- Experiment logging with YAML parameter dumps, checkpoints, and optional video recording
- Optional camera-follow utility for interactive playback

Key implementation references:
- RSL-RL training runner selection and checkpoint loading
- CusRL trainer creation with agent factory overrides and logger factory
- SKRL runner instantiation with algorithm-specific agent configuration entry points

**Section sources**
- [scripts/reinforcement_learning/rsl_rl/train.py](file://scripts/reinforcement_learning/rsl_rl/train.py#L196-L213)
- [scripts/reinforcement_learning/cusrl/train.py](file://scripts/reinforcement_learning/cusrl/train.py#L122-L132)
- [scripts/reinforcement_learning/skrl/train.py](file://scripts/reinforcement_learning/skrl/train.py#L224-L237)

## Architecture Overview
The training pipeline follows a consistent flow across systems:
- Parse CLI arguments and apply overrides
- Initialize IsaacLab AppLauncher and environment
- Wrap environment for vectorized execution
- Instantiate runner/trainer and optionally load checkpoints
- Run training loop with logging and optional video capture
- Export policy artifacts (ONNX/JIT) for deployment

```mermaid
sequenceDiagram
participant CLI as "CLI Args"
participant App as "AppLauncher"
participant Env as "IsaacLab Env"
participant Wrap as "VecEnv Wrapper"
participant Runner as "Runner/Trainer"
participant Log as "Logs/Checkpoints"
CLI->>App : Launch with device/distributed flags
App->>Env : gym.make(task, cfg)
Env->>Wrap : Wrap for vectorized execution
Wrap->>Runner : Initialize with agent config
Runner->>Log : Dump params/env.yaml, agent.yaml
Runner->>Runner : Load checkpoint (optional)
Runner->>Env : Interact (obs->actions->rew, dones)
Runner->>Log : Save checkpoints, videos
```

**Diagram sources**
- [scripts/reinforcement_learning/rsl_rl/train.py](file://scripts/reinforcement_learning/rsl_rl/train.py#L117-L225)
- [scripts/reinforcement_learning/cusrl/train.py](file://scripts/reinforcement_learning/cusrl/train.py#L79-L135)
- [scripts/reinforcement_learning/skrl/train.py](file://scripts/reinforcement_learning/skrl/train.py#L135-L237)

## Detailed Component Analysis

### RSL-RL Training System
RSL-RL provides OnPolicyRunner and DistillationRunner with PPO algorithm support. The training script:
- Accepts CLI arguments for video, num_envs, task, agent entry point, seed, max_iterations, distributed, and IO descriptor export
- Applies AppLauncher arguments and validates RSL-RL version
- Wraps the environment with RslRlVecEnvWrapper and selects runner based on configuration
- Supports resuming from checkpoints and exporting policy artifacts
- Records videos during training when enabled

```mermaid
sequenceDiagram
participant Main as "train.py main()"
participant CLIFunc as "cli_args.update_rsl_rl_cfg()"
participant Env as "gym.make(...)"
participant Wrap as "RslRlVecEnvWrapper"
participant Runner as "OnPolicyRunner/DistillationRunner"
participant Log as "logs/rsl_rl/<exp>/<ts>"
Main->>CLIFunc : Override agent_cfg with CLI
Main->>Env : gym.make(task, cfg)
Env->>Wrap : Wrap vectorized env
Wrap->>Runner : Initialize runner with env and agent_cfg
Runner->>Log : Add git repo, dump params, load checkpoint (optional)
Runner->>Runner : learn(max_iterations)
Runner->>Log : Save checkpoints/videos
```

**Diagram sources**
- [scripts/reinforcement_learning/rsl_rl/train.py](file://scripts/reinforcement_learning/rsl_rl/train.py#L117-L225)
- [scripts/reinforcement_learning/rsl_rl/cli_args.py](file://scripts/reinforcement_learning/rsl_rl/cli_args.py#L63-L94)

Key configuration highlights (example from logs):
- Seed, device, num_steps_per_env, max_iterations, save_interval
- Policy architecture (hidden dims, activation)
- PPO algorithm parameters (learning rate, schedule, gamma, lam, entropy_coef, clipping, normalization)

**Section sources**
- [scripts/reinforcement_learning/rsl_rl/train.py](file://scripts/reinforcement_learning/rsl_rl/train.py#L21-L44)
- [scripts/reinforcement_learning/rsl_rl/train.py](file://scripts/reinforcement_learning/rsl_rl/train.py#L117-L225)
- [scripts/reinforcement_learning/rsl_rl/cli_args.py](file://scripts/reinforcement_learning/rsl_rl/cli_args.py#L19-L94)
- [logs/rsl_rl/opendoge_apx_flat/2026-01-20_11-11-30/params/agent.yaml](file://logs/rsl_rl/opendoge_apx_flat/2026-01-20_11-11-30/params/agent.yaml#L1-L50)

### RSL-RL Playback and Camera Utilities
Playback scripts load checkpoints and run inference loops:
- Select OnPolicyRunner or DistillationRunner based on configuration
- Export policy to ONNX/JIT for deployment
- Optional keyboard control hook and camera-follow behavior for interactive sessions

```mermaid
sequenceDiagram
participant Play as "play.py main()"
participant Env as "gym.make(...)"
participant Wrap as "RslRlVecEnvWrapper"
participant Runner as "OnPolicyRunner/DistillationRunner"
participant Policy as "runner.get_inference_policy()"
participant Utils as "rl_utils.camera_follow"
Play->>Env : gym.make(task, cfg)
Env->>Wrap : Wrap vectorized env
Wrap->>Runner : Initialize runner and load checkpoint
Runner->>Policy : Get inference policy
loop Inference Loop
Policy->>Env : actions = policy(obs)
Env-->>Policy : obs, rew, dones, _
Policy->>Utils : camera_follow(env) (optional)
end
```

**Diagram sources**
- [scripts/reinforcement_learning/rsl_rl/play.py](file://scripts/reinforcement_learning/rsl_rl/play.py#L94-L246)
- [scripts/reinforcement_learning/rl_utils.py](file://scripts/reinforcement_learning/rl_utils.py#L9-L27)

**Section sources**
- [scripts/reinforcement_learning/rsl_rl/play.py](file://scripts/reinforcement_learning/rsl_rl/play.py#L94-L246)
- [scripts/reinforcement_learning/rsl_rl/play_cs.py](file://scripts/reinforcement_learning/rsl_rl/play_cs.py#L95-L285)
- [scripts/reinforcement_learning/rl_utils.py](file://scripts/reinforcement_learning/rl_utils.py#L9-L27)

### CusRL Experimental Training System
CusRL provides a Trainer abstraction with:
- Agent factory overrides for device, autocast, and torch.compile
- Logger factory for TensorBoard-style logging
- Distributed world-size scaling of num_envs
- Optional video recording per process

```mermaid
sequenceDiagram
participant Train as "cusrl/train.py main()"
participant Env as "gym.make(...)"
participant Wrap as "IsaacLabEnvAdapter"
participant Trainer as "cusrl.Trainer"
participant Log as "logs/cusrl/<exp>/<ts>"
Train->>Env : gym.make(task, cfg)
Env->>Wrap : Adapter(env)
Wrap->>Trainer : Initialize Trainer with agent_factory, logger_factory
Trainer->>Log : Save params, checkpoints, videos (main process)
Trainer->>Trainer : run_training_loop()
```

**Diagram sources**
- [scripts/reinforcement_learning/cusrl/train.py](file://scripts/reinforcement_learning/cusrl/train.py#L79-L135)

**Section sources**
- [scripts/reinforcement_learning/cusrl/train.py](file://scripts/reinforcement_learning/cusrl/train.py#L79-L135)
- [scripts/reinforcement_learning/cusrl/play.py](file://scripts/reinforcement_learning/cusrl/play.py#L80-L170)

### SKRL Training System (AMP, PPO, IPPO, MAPPO)
SKRL supports multiple algorithms and ML frameworks:
- Algorithm selection via --algorithm or explicit --agent entry point
- ML framework selection (torch, jax, jax-numpy)
- Runner instantiation with environment wrapper and optional checkpoint loading
- Configurable trainer timesteps derived from max_iterations and rollouts

```mermaid
sequenceDiagram
participant Train as "skrl/train.py main()"
participant Env as "gym.make(...)"
participant Wrap as "SkrlVecEnvWrapper"
participant Runner as "skrl Runner"
participant Log as "logs/skrl/<exp>/<ts>"
Train->>Env : gym.make(task, cfg)
Env->>Wrap : Wrap for skrl
Wrap->>Runner : Initialize Runner with agent_cfg
Runner->>Log : Dump params/env.yaml, agent.yaml
Runner->>Runner : Load checkpoint (optional)
Runner->>Runner : run()
```

**Diagram sources**
- [scripts/reinforcement_learning/skrl/train.py](file://scripts/reinforcement_learning/skrl/train.py#L135-L237)

**Section sources**
- [scripts/reinforcement_learning/skrl/train.py](file://scripts/reinforcement_learning/skrl/train.py#L24-L62)
- [scripts/reinforcement_learning/skrl/train.py](file://scripts/reinforcement_learning/skrl/train.py#L135-L237)
- [scripts/reinforcement_learning/skrl/play.py](file://scripts/reinforcement_learning/skrl/play.py#L131-L245)

### Distributed Training Architecture
All three systems support multi-GPU training:
- RSL-RL: Uses AppLauncher.local_rank to set device per process and adjusts seed per rank
- SKRL: Resolves device to cuda:<local_rank> when distributed is enabled
- CusRL: Reads LOCAL_RANK from environment to set device and scale num_envs by world_size()

```mermaid
flowchart TD
Start(["Start Training"]) --> CheckDist{"--distributed or LOCAL_RANK?"}
CheckDist --> |Yes| SetDevice["Set device to cuda:<local_rank>"]
CheckDist --> |No| CPUWarn["CPU device not supported for distributed"]
SetDevice --> SeedAdj["Adjust seed per rank"]
SeedAdj --> RunLoop["Run training loop per process"]
CPUWarn --> End(["Exit"])
RunLoop --> End
```

**Diagram sources**
- [scripts/reinforcement_learning/rsl_rl/train.py](file://scripts/reinforcement_learning/rsl_rl/train.py#L138-L146)
- [scripts/reinforcement_learning/skrl/train.py](file://scripts/reinforcement_learning/skrl/train.py#L149-L155)
- [scripts/reinforcement_learning/cusrl/train.py](file://scripts/reinforcement_learning/cusrl/train.py#L46-L50)

**Section sources**
- [scripts/reinforcement_learning/rsl_rl/train.py](file://scripts/reinforcement_learning/rsl_rl/train.py#L131-L146)
- [scripts/reinforcement_learning/skrl/train.py](file://scripts/reinforcement_learning/skrl/train.py#L142-L155)
- [scripts/reinforcement_learning/cusrl/train.py](file://scripts/reinforcement_learning/cusrl/train.py#L46-L50)

### Training Pipeline Components
- Environment interaction: Reset, step, and observation collection
- Policy execution: Deterministic/stochastic actions from policy or runner agent
- Gradient computation and updates: Encapsulated within runner/trainer (e.g., OnPolicyRunner, DistillationRunner, SKRL Runner)
- Model updates: Checkpoint saving at intervals and optional export to ONNX/JIT

```mermaid
flowchart TD
Reset["Reset environment"] --> Observe["Collect observations"]
Observe --> Act["Compute actions via policy/runner"]
Act --> Step["Step environment"]
Step --> Store["Store transitions"]
Store --> Update["Update policy (gradient steps)"]
Update --> Save["Save checkpoint"]
Save --> Observe
```

[No sources needed since this diagram shows conceptual workflow, not actual code structure]

## Dependency Analysis
The training scripts depend on:
- AppLauncher for initializing the IsaacSim application
- Environment wrappers specific to each RL library
- Runner/trainer abstractions from each RL library
- Logging utilities for YAML dumping and checkpoint retrieval
- Optional camera-follow utility for interactive playback

```mermaid
graph LR
RSL_TRAIN["rsl_rl/train.py"] --> APP["AppLauncher"]
RSL_TRAIN --> ENV["IsaacLab Env"]
RSL_TRAIN --> WRAP_RSL["RslRlVecEnvWrapper"]
RSL_TRAIN --> RUN_RSL["OnPolicyRunner/DistillationRunner"]
CUS_TRAIN["cusrl/train.py"] --> APP
CUS_TRAIN --> ENV
CUS_TRAIN --> ADAPTER["IsaacLabEnvAdapter"]
CUS_TRAIN --> TRAINER["cusrl.Trainer"]
SKR_TRAIN["skrl/train.py"] --> APP
SKR_TRAIN --> ENV
SKR_TRAIN --> WRAP_SKR["SkrlVecEnvWrapper"]
SKR_TRAIN --> RUN_SKR["skrl Runner"]
```

**Diagram sources**
- [scripts/reinforcement_learning/rsl_rl/train.py](file://scripts/reinforcement_learning/rsl_rl/train.py#L89-L99)
- [scripts/reinforcement_learning/cusrl/train.py](file://scripts/reinforcement_learning/cusrl/train.py#L63-L63)
- [scripts/reinforcement_learning/skrl/train.py](file://scripts/reinforcement_learning/skrl/train.py#L115-L115)

**Section sources**
- [scripts/reinforcement_learning/rsl_rl/train.py](file://scripts/reinforcement_learning/rsl_rl/train.py#L89-L99)
- [scripts/reinforcement_learning/cusrl/train.py](file://scripts/reinforcement_learning/cusrl/train.py#L63-L63)
- [scripts/reinforcement_learning/skrl/train.py](file://scripts/reinforcement_learning/skrl/train.py#L115-L115)

## Performance Considerations
- Mixed precision and compilation:
  - RSL-RL: TF32 allowances and deterministic/benchmark toggles set early
  - CusRL: --autocast and --compile flags passed to agent factory
- Distributed scaling:
  - RSL-RL: Device assignment per rank and seed offset per rank
  - SKRL: Device resolution to cuda:<local_rank>
  - CusRL: num_envs scaled by world_size()
- Curriculum and augmentation:
  - Environment configs demonstrate disabling curriculum and randomization for stable evaluation
  - Symmetry configuration fields present in RSL-RL agent.yaml indicate potential for symmetry data augmentation
- Logging overhead:
  - SKRL/RSL-RL export YAML params and optionally IO descriptors for reproducibility

[No sources needed since this section provides general guidance]

## Troubleshooting Guide
Common issues and resolutions:
- Unsupported RSL-RL version:
  - The script checks installed version and prints installation command for the required version
- CPU device with distributed training:
  - Distributed training requires GPU devices; the script raises an error for CPU device when distributed is enabled
- Video recording:
  - Enable cameras via CLI to record videos; ensure video kwargs are configured properly
- Checkpoint loading:
  - Use resume flags or explicit checkpoint paths; ensure log directories match expected patterns
- Keyboard control:
  - Keyboard mode sets num_envs to 1 and disables certain terminations for interactive control
- Camera follow:
  - Use the camera-follow utility during interactive sessions to track the robot

**Section sources**
- [scripts/reinforcement_learning/rsl_rl/train.py](file://scripts/reinforcement_learning/rsl_rl/train.py#L57-L76)
- [scripts/reinforcement_learning/rsl_rl/train.py](file://scripts/reinforcement_learning/rsl_rl/train.py#L131-L136)
- [scripts/reinforcement_learning/rsl_rl/play.py](file://scripts/reinforcement_learning/rsl_rl/play.py#L125-L137)
- [scripts/reinforcement_learning/rl_utils.py](file://scripts/reinforcement_learning/rl_utils.py#L9-L27)

## Conclusion
The repository integrates three complementary RL training systems:
- RSL-RL offers mature PPO support with robust configuration, distributed training, and checkpointing
- CusRL provides an experimental, flexible trainer with distributed and optimization flags
- SKRL enables advanced algorithms (including AMP) and multiple ML frameworks with unified runner APIs

Together, they form a comprehensive training pipeline supporting diverse research and deployment needs, with strong emphasis on reproducibility, distributed scalability, and practical evaluation workflows.

## Appendices

### Example CLI Argument Configuration
- RSL-RL training:
  - --video, --video_length, --video_interval, --num_envs, --task, --agent, --seed, --max_iterations, --distributed, --export_io_descriptors
- CusRL training:
  - --video, --video_length, --video_interval, --num_envs, --task, --agent, --seed, --run_name, --checkpoint, --logger, --max_iterations, --autocast, --compile
- SKRL training:
  - --video, --video_length, --video_interval, --num_envs, --task, --agent, --seed, --distributed, --checkpoint, --max_iterations, --export_io_descriptors, --ml_framework, --algorithm

**Section sources**
- [scripts/reinforcement_learning/rsl_rl/train.py](file://scripts/reinforcement_learning/rsl_rl/train.py#L22-L44)
- [scripts/reinforcement_learning/cusrl/train.py](file://scripts/reinforcement_learning/cusrl/train.py#L17-L36)
- [scripts/reinforcement_learning/skrl/train.py](file://scripts/reinforcement_learning/skrl/train.py#L24-L62)

### Hyperparameter Configuration Examples
- RSL-RL PPO configuration (example from logs):
  - Seed, device, num_steps_per_env, max_iterations, save_interval
  - Policy hidden dimensions and activation
  - PPO parameters: learning rate, schedule, gamma, lam, entropy_coef, clipping, normalization

**Section sources**
- [logs/rsl_rl/opendoge_apx_flat/2026-01-20_11-11-30/params/agent.yaml](file://logs/rsl_rl/opendoge_apx_flat/2026-01-20_11-11-30/params/agent.yaml#L1-L50)