# RSL-RL Training System

<cite>
**Referenced Files in This Document**
- [README.md](file://README.md)
- [train.py](file://scripts/reinforcement_learning/rsl_rl/train.py)
- [play.py](file://scripts/reinforcement_learning/rsl_rl/play.py)
- [cli_args.py](file://scripts/reinforcement_learning/rsl_rl/cli_args.py)
- [rsl_rl_ppo_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/anymal_d/agents/rsl_rl_ppo_cfg.py)
- [rsl_rl_distillation_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/anymal_d/agents/rsl_rl_distillation_cfg.py)
- [flat_env_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/anymal_d/flat_env_cfg.py)
- [rsl_rl_ppo_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/agents/rsl_rl_ppo_cfg.py)
- [stair_env_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/stair_env_cfg.py)
- [velocity_env_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py)
- [rl_utils.py](file://scripts/reinforcement_learning/rl_utils.py)
- [__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/__init__.py)
</cite>

## Update Summary
**Changes Made**
- Enhanced with explicit class name declarations in RSL-RL policy configuration files
- Documented that the default policy class is ActorCritic for clarity in customization
- Added comprehensive stair-specific PPO runner configuration (ZsibotZSL1StairPPORunnerCfg)
- Added comprehensive debugging improvements for height scanner visualization
- Updated environment variants section to include stair climbing scenarios
- Enhanced reward system documentation with stair-specific optimizations
- Added concrete examples for stair climbing training configurations
- Removed documentation for temporarily removed height scanner debug visualization feature

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
This document explains the RSL-RL training system implemented in the repository. It covers the Proximal Policy Optimization (PPO) algorithm configuration, the training pipeline, and the CLI argument system. It also documents the OnPolicyRunner and DistillationRunner classes, their differences and use cases, the environment wrapper system, action clipping, and video recording. Finally, it provides guidance on distributed training, experiment logging, checkpoint management, and common training issues.

**Updated** Enhanced with explicit class name declarations in policy configuration files, documenting that the default policy class is ActorCritic, providing clarity for users customizing policy architecture.

## Project Structure
The RSL-RL training system is organized around three primary scripts and configuration modules:
- Training entry point: scripts/reinforcement_learning/rsl_rl/train.py
- Playback/inference entry point: scripts/reinforcement_learning/rsl_rl/play.py
- CLI argument helpers: scripts/reinforcement_learning/rsl_rl/cli_args.py
- Agent configuration templates: source/robot_lab/robot_lab/tasks/.../agents/rsl_rl_ppo_cfg.py and rsl_rl_distillation_cfg.py
- Environment configuration templates: source/robot_lab/robot_lab/tasks/.../flat_env_cfg.py, rough_env_cfg.py, and stair_env_cfg.py

```mermaid
graph TB
A["CLI (train.py)"] --> B["Environment Creation<br/>gym.make(...)"]
B --> C["RslRlVecEnvWrapper<br/>(clip_actions)"]
C --> D["Runner Selection<br/>OnPolicyRunner vs DistillationRunner"]
D --> E["Algorithm: PPO / Distillation"]
E --> F["Logging & Checkpoints<br/>TensorBoard/W&B/Neptune"]
E --> G["Video Recording (optional)"]
A2["CLI (play.py)"] --> B2["Environment Creation"]
B2 --> C2["RslRlVecEnvWrapper"]
C2 --> D2["Runner Load Checkpoint"]
D2 --> H["Policy Export (JIT/ONNX)"]
```

**Diagram sources**
- [train.py:171-224](file://scripts/reinforcement_learning/rsl_rl/train.py#L171-L224)
- [play.py:158-214](file://scripts/reinforcement_learning/rsl_rl/play.py#L158-L214)

**Section sources**
- [README.md:193-348](file://README.md#L193-L348)
- [train.py:1-232](file://scripts/reinforcement_learning/rsl_rl/train.py#L1-L232)
- [play.py:1-254](file://scripts/reinforcement_learning/rsl_rl/play.py#L1-L254)

## Core Components
- PPO Algorithm Configuration: The PPO configuration defines policy architecture, value loss coefficient, clipping parameters, entropy bonus, learning rate schedule, discount factor, GAE lambda, KL target, and gradient norm clipping. See [rsl_rl_ppo_cfg.py:12-38](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/anymal_d/agents/rsl_rl_ppo_cfg.py#L12-L38).
- Distillation Configuration: Distillation runner configuration sets up a student-teacher architecture with shared observation groups and a distillation-specific algorithm configuration. See [rsl_rl_distillation_cfg.py:18-38](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/anymal_d/agents/rsl_rl_distillation_cfg.py#L18-L38).
- Environment Wrapping and Action Clipping: The environment is wrapped with RslRlVecEnvWrapper and actions are clipped according to agent configuration. See [train.py:196-197](file://scripts/reinforcement_learning/rsl_rl/train.py#L196-L197) and [play.py:177-178](file://scripts/reinforcement_learning/rsl_rl/play.py#L177-L178).
- Video Recording: Optional video capture during training and playback using gym.wrappers.RecordVideo with configurable intervals and lengths. See [train.py:182-192](file://scripts/reinforcement_learning/rsl_rl/train.py#L182-L192) and [play.py:165-175](file://scripts/reinforcement_learning/rsl_rl/play.py#L165-L175).

**Section sources**
- [rsl_rl_ppo_cfg.py:12-38](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/anymal_d/agents/rsl_rl_ppo_cfg.py#L12-L38)
- [rsl_rl_distillation_cfg.py:18-38](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/anymal_d/agents/rsl_rl_distillation_cfg.py#L18-L38)
- [train.py:182-197](file://scripts/reinforcement_learning/rsl_rl/train.py#L182-L197)
- [play.py:165-178](file://scripts/reinforcement_learning/rsl_rl/play.py#L165-L178)

## Architecture Overview
The training pipeline integrates environment creation, optional video recording, environment wrapping, runner instantiation, checkpoint loading, and algorithm learning loops. The playback pipeline mirrors this with checkpoint loading and policy export.

```mermaid
sequenceDiagram
participant CLI as "CLI (train.py)"
participant Env as "IsaacLab Env"
participant Wrap as "RslRlVecEnvWrapper"
participant Runner as "OnPolicyRunner/DistillationRunner"
participant Log as "Logs/Checkpoints"
CLI->>Env : gym.make(task, cfg)
CLI->>Wrap : wrap(env, clip_actions)
CLI->>Runner : instantiate runner with agent_cfg
CLI->>Runner : load(checkpoint if resume/distillation)
CLI->>Log : dump env.yaml and agent.yaml
Runner->>Runner : learn(max_iterations)
Runner-->>Log : periodic checkpoints
```

**Diagram sources**
- [train.py:171-224](file://scripts/reinforcement_learning/rsl_rl/train.py#L171-L224)

## Detailed Component Analysis

### PPO Algorithm Implementation and Hyperparameters
- Policy architecture: Hidden layers and activation are configured per environment variant. See [rsl_rl_ppo_cfg.py:17-24](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/anymal_d/agents/rsl_rl_ppo_cfg.py#L17-L24).
- Algorithm hyperparameters: Includes value loss coefficient, clipped value loss, clipping parameter, entropy coefficient, epochs, mini-batches, learning rate schedule, discount factor gamma, GAE lambda, desired KL divergence, and max gradient norm. See [rsl_rl_ppo_cfg.py:25-38](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/anymal_d/agents/rsl_rl_ppo_cfg.py#L25-L38).
- Environment variants: Flat and Rough variants adjust terrain and reward terms. See [flat_env_cfg.py:9-29](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/anymal_d/flat_env_cfg.py#L9-L29).

**Updated** Enhanced with explicit class name declarations in policy configuration files, documenting that the default policy class is ActorCritic for clarity in customization.

```mermaid
flowchart TD
Start(["Load PPO Config"]) --> Class["Set Policy Class Name<br/>Default: ActorCritic"]
Class --> Arch["Set Actor/Critic Hidden Dims<br/>Activation"]
Arch --> Algo["Configure PPO Algorithm<br/>Clip Param, Entropy, LR Schedule"]
Algo --> Env["Select Env Variant<br/>Flat/Rough/Stair"]
Env --> Train["Run Training Loop"]
Train --> Save["Save Periodic Checkpoints"]
```

**Diagram sources**
- [rsl_rl_ppo_cfg.py:12-38](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/anymal_d/agents/rsl_rl_ppo_cfg.py#L12-L38)
- [flat_env_cfg.py:9-29](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/anymal_d/flat_env_cfg.py#L9-L29)

**Section sources**
- [rsl_rl_ppo_cfg.py:12-38](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/anymal_d/agents/rsl_rl_ppo_cfg.py#L12-L38)
- [flat_env_cfg.py:9-29](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/anymal_d/flat_env_cfg.py#L9-L29)

### OnPolicyRunner vs DistillationRunner
- OnPolicyRunner: Standard PPO training loop with policy and value networks, configured via PPO algorithm settings. Instantiated in [train.py:200-205](file://scripts/reinforcement_learning/rsl_rl/train.py#L200-L205).
- DistillationRunner: Student-teacher distillation training with separate student and teacher policies, specialized algorithm configuration, and observation groups. Defined in [rsl_rl_distillation_cfg.py:18-38](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/anymal_d/agents/rsl_rl_distillation_cfg.py#L18-L38) and instantiated in [train.py:202-203](file://scripts/reinforcement_learning/rsl_rl/train.py#L202-L203).

**Updated** Enhanced with stair-specific runner configuration featuring identical hyperparameters optimized for stair climbing scenarios.

```mermaid
classDiagram
class OnPolicyRunner {
+learn(num_learning_iterations)
+load(path)
+add_git_repo_to_log(file)
}
class DistillationRunner {
+learn(num_learning_iterations)
+load(path)
+add_git_repo_to_log(file)
}
class RslRlPpoAlgorithmCfg {
+learning_rate
+clip_param
+entropy_coef
+num_learning_epochs
+num_mini_batches
+gamma
+lam
+desired_kl
+max_grad_norm
}
class RslRlDistillationAlgorithmCfg {
+num_learning_epochs
+learning_rate
+gradient_length
}
class ZsibotZSL1StairPPORunnerCfg {
+num_steps_per_env : 24
+max_iterations : 50000
+save_interval : 100
+experiment_name : "zsibot_zsl1_stair"
}
OnPolicyRunner --> RslRlPpoAlgorithmCfg : "uses"
DistillationRunner --> RslRlDistillationAlgorithmCfg : "uses"
ZsibotZSL1StairPPORunnerCfg --> RslRlPpoAlgorithmCfg : "uses"
```

**Diagram sources**
- [train.py:200-205](file://scripts/reinforcement_learning/rsl_rl/train.py#L200-L205)
- [rsl_rl_ppo_cfg.py:25-38](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/anymal_d/agents/rsl_rl_ppo_cfg.py#L25-L38)
- [rsl_rl_distillation_cfg.py:34-38](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/anymal_d/agents/rsl_rl_distillation_cfg.py#L34-L38)
- [rsl_rl_ppo_cfg.py:39-65](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/agents/rsl_rl_ppo_cfg.py#L39-L65)

**Section sources**
- [train.py:200-205](file://scripts/reinforcement_learning/rsl_rl/train.py#L200-L205)
- [rsl_rl_distillation_cfg.py:18-38](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/anymal_d/agents/rsl_rl_distillation_cfg.py#L18-L38)

### CLI Argument System
Key CLI arguments for training and playback:
- Video recording: --video, --video_length, --video_interval
- Environment scaling: --num_envs
- Task selection: --task, --agent
- Seed and iterations: --seed, --max_iterations
- Distributed training: --distributed
- Export I/O descriptors: --export_io_descriptors
- RSL-RL specific: --experiment_name, --run_name, --resume, --load_run, --checkpoint, --logger, --log_project_name

See argument parsing and updates in [train.py:22-44](file://scripts/reinforcement_learning/rsl_rl/train.py#L22-L44) and [cli_args.py:19-94](file://scripts/reinforcement_learning/rsl_rl/cli_args.py#L19-L94).

```mermaid
flowchart TD
Parse["Parse CLI Args"] --> Override["Override Config via CLI"]
Override --> Distributed{"--distributed?"}
Distributed --> |Yes| MultiGPU["Set device per rank<br/>seed += rank"]
Distributed --> |No| SingleGPU["Use provided device/seed"]
Parse --> Video{"--video?"}
Video --> |Yes| Record["Enable RecordVideo<br/>interval/length"]
Video --> |No| Skip["Skip video"]
```

**Diagram sources**
- [train.py:120-146](file://scripts/reinforcement_learning/rsl_rl/train.py#L120-L146)
- [train.py:182-192](file://scripts/reinforcement_learning/rsl_rl/train.py#L182-L192)
- [cli_args.py:19-94](file://scripts/reinforcement_learning/rsl_rl/cli_args.py#L19-L94)

**Section sources**
- [train.py:22-44](file://scripts/reinforcement_learning/rsl_rl/train.py#L22-L44)
- [cli_args.py:19-94](file://scripts/reinforcement_learning/rsl_rl/cli_args.py#L19-L94)

### Environment Wrapper and Action Clipping
- The environment is wrapped with RslRlVecEnvWrapper to adapt observations/actions for RSL-RL. See [train.py:196-197](file://scripts/reinforcement_learning/rsl_rl/train.py#L196-L197) and [play.py:177-178](file://scripts/reinforcement_learning/rsl_rl/play.py#L177-L178).
- Action clipping is controlled by agent_cfg.clip_actions and applied by the wrapper.

**Section sources**
- [train.py:196-197](file://scripts/reinforcement_learning/rsl_rl/train.py#L196-L197)
- [play.py:177-178](file://scripts/reinforcement_learning/rsl_rl/play.py#L177-L178)

### Video Recording Capabilities
- Training: Optional video recording with configurable interval and length. See [train.py:182-192](file://scripts/reinforcement_learning/rsl_rl/train.py#L182-L192).
- Playback: Single-frame trigger at episode start. See [play.py:165-175](file://scripts/reinforcement_learning/rsl_rl/play.py#L165-L175).

**Section sources**
- [train.py:182-192](file://scripts/reinforcement_learning/rsl_rl/train.py#L182-L192)
- [play.py:165-175](file://scripts/reinforcement_learning/rsl_rl/play.py#L165-L175)

### Distributed Training
- Single-node multi-GPU: Use torch.distributed.run with --nproc_per_node equal to the number of GPUs. See [README.md:333-347](file://README.md#L333-L347).
- Multi-node: Launch a process per node with --nnodes and --node_rank, and specify rendezvous endpoint and backend. See [README.md:339-347](file://README.md#L339-L347).
- Per-rank device assignment and seed increment are handled in the training script. See [train.py:138-146](file://scripts/reinforcement_learning/rsl_rl/train.py#L138-L146).

**Section sources**
- [README.md:333-347](file://README.md#L333-L347)
- [train.py:138-146](file://scripts/reinforcement_learning/rsl_rl/train.py#L138-L146)

### Experiment Logging and Checkpoint Management
- Logging directory: logs/rsl_rl/{experiment_name}/{timestamp}_{run_name}. See [train.py:148-158](file://scripts/reinforcement_learning/rsl_rl/train.py#L148-L158).
- Configuration dumps: env.yaml and agent.yaml saved under logs. See [train.py:214-216](file://scripts/reinforcement_learning/rsl_rl/train.py#L214-L216).
- Checkpoint loading: get_checkpoint_path resolves run/checkpoint; loaded by runner.load. See [train.py:178-212](file://scripts/reinforcement_learning/rsl_rl/train.py#L178-L212).
- Playback checkpoint resolution and export: JIT/ONNX export of policy and optional normalizer. See [play.py:140-213](file://scripts/reinforcement_learning/rsl_rl/play.py#L140-L213).

**Section sources**
- [train.py:148-216](file://scripts/reinforcement_learning/rsl_rl/train.py#L148-L216)
- [play.py:140-213](file://scripts/reinforcement_learning/rsl_rl/play.py#L140-L213)

### Debugging Improvements and Height Scanner Visualization
**Updated** Enhanced debugging capabilities with improved height scanner visualization support:

- **Height Scanner Debug Visualization**: The system now supports dynamic height scanner debug visualization that can be toggled based on headless mode. See [play.py:158-161](file://scripts/reinforcement_learning/rsl_rl/play.py#L158-L161).
- **Camera Following**: Enhanced camera control with smoothing for better visualization during playback. See [rl_utils.py:9-27](file://scripts/reinforcement_learning/rl_utils.py#L9-L27).
- **Debug Mode Integration**: Height scanner debug visualization is automatically disabled in headless mode for cleaner simulations.

**Section sources**
- [play.py:158-161](file://scripts/reinforcement_learning/rsl_rl/play.py#L158-L161)
- [rl_utils.py:9-27](file://scripts/reinforcement_learning/rl_utils.py#L9-L27)

### Concrete Examples
- Configure training runs: Select task and agent entry point, set seed and iterations, choose environment variant (Flat/Rough/Stair). See [README.md:197-216](file://README.md#L197-L216).
- Multi-GPU training: Use torch.distributed.run with --nproc_per_node=N for multi-GPU on a single node; extend to multiple nodes with --nnodes and --node_rank. See [README.md:333-347](file://README.md#L333-L347).
- Export model checkpoints: After loading a checkpoint in playback, the policy is exported to JIT and ONNX under the checkpoint's exported/ directory. See [play.py:210-213](file://scripts/reinforcement_learning/rsl_rl/play.py#L210-L213).

**Updated** Enhanced with stair-specific training examples featuring optimized configurations and debugging capabilities.

**Section sources**
- [README.md:197-216](file://README.md#L197-L216)
- [README.md:333-347](file://README.md#L333-L347)
- [play.py:210-213](file://scripts/reinforcement_learning/rsl_rl/play.py#L210-L213)

## Dependency Analysis
The training and playback scripts depend on:
- Environment registration and configuration via task entry points
- RSL-RL runners (OnPolicyRunner, DistillationRunner)
- Environment wrapper (RslRlVecEnvWrapper)
- Logging and checkpoint utilities

```mermaid
graph TB
Train["train.py"] --> EnvMake["gym.make(task, cfg)"]
Train --> Wrap["RslRlVecEnvWrapper"]
Train --> RunnerSel["Runner Selection"]
RunnerSel --> OnPolicy["OnPolicyRunner"]
RunnerSel --> Distill["DistillationRunner"]
Train --> Logger["dump_yaml(env, agent)"]
Play["play.py"] --> Wrap2["RslRlVecEnvWrapper"]
Play --> Load["runner.load(checkpoint)"]
Play --> Export["Export JIT/ONNX"]
```

**Diagram sources**
- [train.py:171-224](file://scripts/reinforcement_learning/rsl_rl/train.py#L171-L224)
- [play.py:158-213](file://scripts/reinforcement_learning/rsl_rl/play.py#L158-L213)

**Section sources**
- [train.py:171-224](file://scripts/reinforcement_learning/rsl_rl/train.py#L171-L224)
- [play.py:158-213](file://scripts/reinforcement_learning/rsl_rl/play.py#L158-L213)

## Performance Considerations
- Enable TF32 and disable deterministic CUDNN for speed on supported GPUs. See [train.py:111-114](file://scripts/reinforcement_learning/rsl_rl/train.py#L111-L114).
- Adjust num_envs to saturate devices; tune num_steps_per_env and num_mini_batches for throughput. See [rsl_rl_ppo_cfg.py:12-15](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/anymal_d/agents/rsl_rl_ppo_cfg.py#L12-L15).
- Use --distributed for multi-GPU scaling; ensure seeds are offset per rank to avoid identical randomization. See [train.py:138-146](file://scripts/reinforcement_learning/rsl_rl/train.py#L138-L146).
- Reduce environment randomness during playback to stabilize evaluation. See [play.py:117-123](file://scripts/reinforcement_learning/rsl_rl/play.py#L117-L123).

## Troubleshooting Guide
- Unsupported runner class: Ensure agent_cfg.class_name is OnPolicyRunner or DistillationRunner. See [train.py:204-205](file://scripts/reinforcement_learning/rsl_rl/train.py#L204-L205).
- Distributed training on CPU: Distributed training requires CUDA devices; the script raises an error if device is CPU with --distributed. See [train.py:131-136](file://scripts/reinforcement_learning/rsl_rl/train.py#L131-L136).
- Video recording not appearing: Ensure --video is enabled and enable_cameras is set; verify video_folder permissions. See [train.py:46-48](file://scripts/reinforcement_learning/rsl_rl/train.py#L46-L48) and [train.py:182-192](file://scripts/reinforcement_learning/rsl_rl/train.py#L182-L192).
- Pre-trained checkpoint availability: Playback supports retrieving published pretrained checkpoints; if unavailable, the script informs and exits gracefully. See [play.py:143-147](file://scripts/reinforcement_learning/rsl_rl/play.py#L143-L147).

**Section sources**
- [train.py:131-136](file://scripts/reinforcement_learning/rsl_rl/train.py#L131-L136)
- [train.py:182-192](file://scripts/reinforcement_learning/rsl_rl/train.py#L182-L192)
- [play.py:143-147](file://scripts/reinforcement_learning/rsl_rl/play.py#L143-L147)

## Conclusion
The RSL-RL training system integrates environment creation, optional video recording, environment wrapping, runner selection, and robust logging and checkpointing. PPO and distillation configurations are cleanly separated and templated per environment variant. The CLI system supports distributed training, experiment naming, and exporting trained policies. Following the examples and guidance herein enables efficient multi-GPU training, reproducible experiments, and reliable deployment of policies.

**Updated** The system now includes dedicated stair-specific PPO runner configuration with optimized hyperparameters for stair climbing scenarios, enhanced debugging capabilities with improved height scanner visualization, comprehensive debugging improvements for better development experience, and explicit class name declarations in policy configuration files documenting that the default policy class is ActorCritic for clarity in customization.

## Appendices

### Appendix A: Environment Variants and Reward Adjustments
- Flat environments remove terrain height scanning and curriculum, simplifying reward computation. See [flat_env_cfg.py:10-29](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/anymal_d/flat_env_cfg.py#L10-L29).
- **Stair environments** utilize specialized inverted pyramid stair terrains with optimized reward systems for stair climbing. See [stair_env_cfg.py:20-47](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/stair_env_cfg.py#L20-L47).

**Updated** Enhanced with comprehensive stair-specific environment configuration featuring specialized terrain generation and reward optimization.

**Section sources**
- [flat_env_cfg.py:10-29](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/anymal_d/flat_env_cfg.py#L10-L29)
- [stair_env_cfg.py:20-47](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/stair_env_cfg.py#L20-L47)

### Appendix B: Stair-Specific PPO Runner Configuration
The ZsibotZSL1StairPPORunnerCfg provides optimized hyperparameters specifically tuned for stair climbing scenarios:

- **Training Parameters**: 
  - num_steps_per_env: 24 (balanced rollout length for stair navigation)
  - max_iterations: 50000 (extended training for stair mastery)
  - save_interval: 100 (frequent checkpointing for stair learning progress)
  - experiment_name: "zsibot_zsl1_stair" (clear identification)

- **Policy Architecture**: 
  - init_noise_std: 1.0 (standard exploration for stair learning)
  - actor_hidden_dims: [512, 256, 128] (deeper network for complex stair patterns)
  - critic_hidden_dims: [512, 256, 128] (symmetric critic architecture)
  - activation: "elu" (smooth activation for stair dynamics)
  - **class_name: "ActorCritic"** (explicitly declared default policy class)

- **Algorithm Hyperparameters**:
  - value_loss_coef: 1.0 (balanced value function learning)
  - clip_param: 0.2 (standard clipping for stable updates)
  - entropy_coef: 0.01 (minimal entropy bonus for stair focus)
  - num_learning_epochs: 5 (efficient policy updates)
  - num_mini_batches: 4 (balanced batch processing)
  - learning_rate: 1.0e-3 (standard learning rate)
  - schedule: "adaptive" (dynamic learning rate adjustment)
  - gamma: 0.99 (high temporal discount for stair rewards)
  - lam: 0.95 (GAE lambda for stair trajectory planning)
  - desired_kl: 0.01 (target KL divergence)
  - max_grad_norm: 1.0 (gradient clipping)

**Updated** Enhanced with explicit class name declaration for clarity in policy customization.

**Section sources**
- [rsl_rl_ppo_cfg.py:39-65](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/agents/rsl_rl_ppo_cfg.py#L39-L65)

### Appendix C: Policy Class Name Declarations and Customization
**Updated** Enhanced with explicit class name declarations for policy customization clarity:

The RSL-RL policy configuration system now includes explicit class name declarations to clarify the default policy architecture:

- **Default Policy Class**: All PPO configurations inherit from RslRlPpoActorCriticCfg, which uses the default class_name "ActorCritic"
- **Explicit Declaration**: Some configurations explicitly declare class_name="ActorCritic" for clarity and future customization
- **Custom Policy Classes**: Users can specify alternative policy classes by setting the class_name field in the policy configuration
- **Backward Compatibility**: Omitting class_name preserves the default ActorCritic behavior

**Section sources**
- [rsl_rl_ppo_cfg.py:54-57](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/agents/rsl_rl_ppo_cfg.py#L54-L57)
- [rsl_rl_ppo_cfg.py:86-89](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/agents/rsl_rl_ppo_cfg.py#L86-L89)

### Appendix D: Stair Environment Reward System Optimizations
The stair environment implements specialized reward functions optimized for stair climbing:

- **Action Scaling**: Increased joint position scaling with reduced ABAD joint influence and enhanced HIP/KNEE power for stair ascent
- **Contact Rewards**: Enhanced contact force rewards for stair gripping and reduced undesired contact penalties
- **Air Time Rewards**: Higher air time thresholds to encourage long strides for stair navigation
- **Feet Height Rewards**: Specialized foot height targets for stair clearance
- **Gait Rewards**: Synced foot pairs for stable stair climbing
- **Termination Handling**: Disabled illegal contact termination for stair climbing safety

**Section sources**
- [stair_env_cfg.py:86-204](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/stair_env_cfg.py#L86-L204)

### Appendix E: Enhanced Debugging and Visualization Features
**Updated** Comprehensive debugging improvements for enhanced development experience:

- **Height Scanner Debug Visualization**: Dynamic toggle based on headless mode for better terrain perception debugging
- **Camera Following System**: Smooth camera tracking with adjustable smoothing window for better visualization
- **Debug Mode Integration**: Automatic debug visualization management across different environment modes
- **Visualization Markers**: Enhanced marker-based debugging for commands and anchors in various MDP components

**Section sources**
- [play.py:158-161](file://scripts/reinforcement_learning/rsl_rl/play.py#L158-L161)
- [rl_utils.py:9-27](file://scripts/reinforcement_learning/rl_utils.py#L9-L27)