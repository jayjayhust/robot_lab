# Velocity-Based Locomotion Tasks

<cite>
**Referenced Files in This Document**
- [README.md](file://README.md)
- [velocity_env_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py)
- [flat_env_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_a1/flat_env_cfg.py)
- [rough_env_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_a1/rough_env_cfg.py)
- [gap_env_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/gap_env_cfg.py)
- [parkour_env_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/parkour_env_cfg.py)
- [stair_env_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/stair_env_cfg.py)
- [observations.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/observations.py)
- [rewards.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/rewards.py)
- [commands.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/commands.py)
- [curriculums.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/curriculums.py)
- [utils.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/utils.py)
- [events.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/events.py)
- [opendoge_flat_env_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/opendoge_apx/flat_env_cfg.py)
- [fftai_flat_env_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/fftai_gr1t1/flat_env_cfg.py)
- [unitree_h1_flat_env_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/unitree_h1/flat_env_cfg.py)
- [deeprobotics_m20_flat_env_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/wheeled/deeprobotics_m20/flat_env_cfg.py)
- [unitree_go2_parkour_init.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/__init__.py)
- [zsibot_zsl1_parkour_init.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1_parkour/__init__.py)
</cite>

## Update Summary
**Changes Made**
- Enhanced documentation to reflect new terrain-level curriculum functionality with automatic terrain difficulty adjustment
- Updated task naming conventions section to clarify that `-Play` suffixes are no longer used in task naming
- Added detailed explanation of the `terrain_levels_vel` curriculum function and its implementation
- Updated environment registration examples to show current naming conventions
- Enhanced curriculum learning section with terrain-level progression mechanisms

## Table of Contents
1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Core Components](#core-components)
4. [Architecture Overview](#architecture-overview)
5. [Detailed Component Analysis](#detailed-component-analysis)
6. [Advanced Environment Configurations](#advanced-environment-configurations)
7. [Dependency Analysis](#dependency-analysis)
8. [Performance Considerations](#performance-considerations)
9. [Troubleshooting Guide](#troubleshooting-guide)
10. [Conclusion](#conclusion)
11. [Appendices](#appendices)

## Introduction
This document explains the velocity-based locomotion task configurations implemented in the repository. It focuses on the ManagerBasedRLEnv architecture, velocity command generation and tracking, MDP formulation (state representation, action space, rewards, and terminations), terrain configuration options, observation preprocessing and corruption, and practical task parameterization for quadrupeds, wheeled robots, and humanoid variants. The framework now includes enhanced support for specialized locomotion scenarios through improved observation processing that reduces computational overhead and includes sophisticated terrain-level curriculum functionality that automatically adjusts terrain difficulty based on robot performance.

## Project Structure
The velocity-based locomotion tasks are organized under a manager-based RL environment framework with enhanced support for specialized locomotion scenarios. Key elements include:
- Environment configuration templates and robot-specific overrides
- MDP modules for commands, observations, rewards, events, and curriculum
- Advanced terrain generation for gap and parkour environments
- Specialized reward functions for climbing and gap traversal
- Flat vs rough terrain variants per robot family with optimized observation processing
- Terrain-level curriculum functionality for adaptive difficulty progression

```mermaid
graph TB
subgraph "Basic Environment Templates"
BaseCfg["velocity_env_cfg.py<br/>Base environment config"]
FlatCfg["flat_env_cfg.py<br/>Flat override"]
RoughCfg["rough_env_cfg.py<br/>Rough override"]
end
subgraph "Advanced Environment Templates"
GapCfg["gap_env_cfg.py<br/>Gap traversal config"]
ParkourCfg["parkour_env_cfg.py<br/>Parkour navigation config"]
StairCfg["stair_env_cfg.py<br/>Stair climbing config"]
end
subgraph "MDP Modules"
Cmd["commands.py<br/>Velocity command generator"]
Obs["observations.py<br/>Observation helpers"]
Rew["rewards.py<br/>Reward functions"]
Cur["curriculums.py<br/>Curriculum functions"]
Ev["events.py<br/>Randomization and resets"]
Util["utils.py<br/>Terrain-aware utilities"]
end
BaseCfg --> Cmd
BaseCfg --> Obs
BaseCfg --> Rew
BaseCfg --> Cur
BaseCfg --> Ev
FlatCfg --> BaseCfg
RoughCfg --> BaseCfg
GapCfg --> BaseCfg
ParkourCfg --> BaseCfg
StairCfg --> BaseCfg
Cur --> Rew
Ev --> BaseCfg
```

**Diagram sources**
- [velocity_env_cfg.py:696-744](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py#L696-L744)
- [flat_env_cfg.py:1-30](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_a1/flat_env_cfg.py#L1-L30)
- [rough_env_cfg.py:1-162](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_a1/rough_env_cfg.py#L1-L162)
- [gap_env_cfg.py:160-339](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/gap_env_cfg.py#L160-L339)
- [parkour_env_cfg.py:170-349](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/parkour_env_cfg.py#L170-L349)
- [stair_env_cfg.py:56-235](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/stair_env_cfg.py#L56-L235)
- [commands.py:21-85](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/commands.py#L21-L85)
- [observations.py:16-35](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/observations.py#L16-L35)
- [rewards.py:22-681](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/rewards.py#L22-L681)
- [curriculums.py:20-97](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/curriculums.py#L20-L97)
- [events.py:203-270](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/events.py#L203-L270)
- [utils.py:42-127](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/utils.py#L42-L127)

**Section sources**
- [README.md:15-42](file://README.md#L15-L42)
- [velocity_env_cfg.py:42-95](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py#L42-L95)
- [flat_env_cfg.py:1-30](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_a1/flat_env_cfg.py#L1-L30)
- [rough_env_cfg.py:1-162](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_a1/rough_env_cfg.py#L1-L162)

## Core Components
- ManagerBasedRLEnv configuration: Defines scene, commands, observations, actions, rewards, terminations, and curriculum.
- Commands: Velocity command generator with terrain-aware restrictions.
- Observations: Concatenated policy and critic groups with noise and clipping, optimized with selective height_scan disabling for computational efficiency.
- Rewards: Velocity tracking, stability, contact-based, gait-related, and climbing progress terms.
- Events: Physics and kinematic randomization, resets, and perturbations.
- Curriculum: Command range progression and terrain-level difficulty progression based on robot performance.
- Terrain: Generator-based rough terrains and plane-based flat scenes with advanced gap and parkour terrain generation.

**Section sources**
- [velocity_env_cfg.py:102-127](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py#L102-L127)
- [velocity_env_cfg.py:130-255](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py#L130-L255)
- [velocity_env_cfg.py:257-373](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py#L257-L373)
- [velocity_env_cfg.py:374-665](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py#L374-L665)
- [velocity_env_cfg.py:667-688](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py#L667-L688)

## Architecture Overview
The ManagerBasedRLEnv orchestrates the RL loop with enhanced support for specialized locomotion scenarios:
- Scene initializes terrain, robot, sensors, and lighting with advanced terrain generation.
- Commands module generates SE(2) velocity targets with optional heading control.
- Observations module constructs concatenated tensors for policy and critic with optimized processing.
- Rewards module computes shaped feedback for velocity tracking, stability, contact dynamics, and climbing progress.
- Events module injects robustness via parameter randomization and controlled perturbations.
- Curriculum module progressively increases command difficulty and terrain complexity based on performance.

```mermaid
sequenceDiagram
participant Env as "ManagerBasedRLEnv"
participant Scene as "InteractiveSceneCfg"
participant Cmd as "CommandsCfg"
participant Obs as "ObservationsCfg"
participant Rew as "RewardsCfg"
participant Cur as "CurriculumCfg"
participant Ev as "EventCfg"
Env->>Scene : Initialize terrain (basic/advanced)
Env->>Cmd : Sample/resample velocity commands
Env->>Obs : Build policy/critic observations (optimized)
Env->>Env : Step physics and sensors
Env->>Rew : Evaluate reward terms (including climbing progress)
Env->>Cur : Update command ranges and terrain difficulty
Env->>Ev : Apply randomization/reset/perturbations
Env-->>Env : Repeat until termination
```

**Diagram sources**
- [velocity_env_cfg.py:696-744](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py#L696-L744)
- [commands.py:42-85](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/commands.py#L42-L85)
- [rewards.py:22-76](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/rewards.py#L22-L76)
- [curriculums.py:20-97](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/curriculums.py#L20-L97)
- [events.py:203-270](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/events.py#L203-L270)

## Detailed Component Analysis

### ManagerBasedRLEnv Architecture
- Scene: Terrain importer with generator-based rough terrains, robot articulation, height scanners, contact sensors, and sky light.
- Commands: SE(2) velocity command with thresholding, heading control, and periodic resampling.
- Actions: Joint position action with scaling and clipping per joint group.
- Observations: Policy and critic groups with base velocities, gravity projection, commands, joint positions/velocities, actions, and height scans; includes noise injection and corruption toggles with optimized processing.
- Rewards: Comprehensive set covering velocity tracking, stability, joint limits/power, contact dynamics, gait, and climbing progress.
- Terminations: Episode timeouts and terrain bounds; contact-based illegal contact.
- Curriculum: Terrain levels and command range progression with automatic difficulty adjustment.

**Section sources**
- [velocity_env_cfg.py:42-95](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py#L42-L95)
- [velocity_env_cfg.py:102-127](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py#L102-L127)
- [velocity_env_cfg.py:130-255](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py#L130-L255)
- [velocity_env_cfg.py:374-665](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py#L374-L665)
- [velocity_env_cfg.py:667-688](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py#L667-L688)

### Simulation Timing and Decimation Configuration

**Updated** Enhanced documentation clarifies the relationship between simulation timestep, decimation factor, and policy update intervals.

The velocity-based locomotion tasks implement a carefully tuned simulation timing configuration that balances computational efficiency with control precision:

- **Physics timestep (sim.dt)**: Set to 0.005 seconds (200 Hz physics rate)
- **Decimation factor**: Controls how many physics steps occur between policy updates
- **Policy update interval**: Calculated as decimation × sim.dt
- **Render interval**: Directly linked to decimation factor for efficient visualization

```mermaid
flowchart TD
Start(["Environment Initialization"]) --> Config["Configure sim.dt = 0.005s"]
Config --> Decimation["Set decimation = 4"]
Decimation --> Policy["Policy Update Interval = 4 × 0.005s = 0.02s"]
Policy --> Render["Render Interval = decimation = 4"]
Render --> Sensors["Update Sensor Periods"]
Sensors --> Complete(["Ready for Training"])
```

**Diagram sources**
- [velocity_env_cfg.py:804-811](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py#L804-L811)

**Section sources**
- [velocity_env_cfg.py:804-811](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py#L804-L811)
- [velocity_env_cfg.py:753-757](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py#L753-L757)

### Velocity Command Generation and Tracking
- Command specification defines SE(2) velocity ranges and heading control stiffness.
- Terrain-aware restriction: On "pits" terrain, commands are restricted to forward-only movement with lateral and yaw set to zero; heading is forced to zero.
- Thresholding: Small lateral/rotational commands are set to zero to stabilize low-speed behavior.
- Tracking rewards: Exponential kernels penalize deviation from commanded linear and angular velocities in body frame; gravity alignment factor is applied.

```mermaid
flowchart TD
Start(["Step"]) --> CheckPits["Check if robot on 'pits' terrain"]
CheckPits --> |Yes| Restrict["Restrict to forward-only movement<br/>set lateral/yaw to zero"]
CheckPits --> |No| Update["Update commands via parent logic"]
Restrict --> Update
Update --> Threshold["Apply small-command thresholding"]
Threshold --> Track["Compute velocity tracking rewards"]
Track --> End(["Done"])
```

**Diagram sources**
- [commands.py:42-85](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/commands.py#L42-L85)
- [utils.py:72-127](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/utils.py#L72-L127)
- [rewards.py:22-76](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/rewards.py#L22-L76)

**Section sources**
- [velocity_env_cfg.py:102-117](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py#L102-L117)
- [commands.py:21-85](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/commands.py#L21-L85)
- [utils.py:42-127](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/utils.py#L42-L127)
- [rewards.py:22-76](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/rewards.py#L22-L76)

### MDP Formulation

#### State Representation
- Policy group observations include:
  - Base linear/angular velocities (scaled)
  - Projected gravity (scaled)
  - Generated velocity commands (scaled)
  - Joint positions/velocities (relative to defaults, scaled)
  - Last actions (scaled)
  - Height scans from raycasters (scaled) - **Disabled in flat environments for computational efficiency**
- Critic group observations exclude height scans and noise for stability.

**Updated** Enhanced observation processing with systematic height_scan disabling in flat environments to reduce computational overhead and improve training stability.

- Noise injection and clipping:
  - Additive uniform noise applied to selected terms.
  - Clipping applied to prevent outliers.
- Observation concatenation:
  - Policy and critic groups concatenate terms in order.

**Section sources**
- [velocity_env_cfg.py:130-255](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py#L130-L255)
- [observations.py:16-35](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/observations.py#L16-L35)

#### Action Space Configuration
- Joint position control with scaling factors per joint group.
- Optional clipping for safety.
- Preserve joint ordering for deterministic mapping.

**Section sources**
- [velocity_env_cfg.py:121-127](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py#L121-L127)
- [rough_env_cfg.py:49-54](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_a1/rough_env_cfg.py#L49-L54)

#### Reward Functions
- Velocity tracking:
  - Exponential rewards for tracking commanded linear and angular velocities in body frame.
- Stability:
  - Penalize z-velocity, xy angular velocity, base height deviation, and non-flat orientation.
- Joint and power:
  - Torques, accelerations, velocities, power, and position deviation penalties.
- Contact dynamics:
  - Undesired contacts, contact forces, feet air time, contact counts, stumble/sliding detection.
- Gait:
  - Quadruped gait reward enforcing synchronized and anti-synchronized foot contacts.
- Climbing Progress:
  - Specialized reward for forward progress and elevation gain during climbing scenarios.
- Mirrors and sync:
  - Joint/action mirroring and action synchronization across groups.

```mermaid
classDiagram
class RewardsCfg {
+track_lin_vel_xy_exp
+track_ang_vel_z_exp
+flat_orientation_l2
+base_height_l2
+joint_torques_l2
+joint_vel_l2
+joint_acc_l2
+joint_power
+undesired_contacts
+contact_forces
+feet_air_time
+feet_contact
+feet_stumble
+feet_slide
+feet_height
+feet_height_body
+feet_gait
+action_sync
+action_mirror
+joint_mirror
+climbing_progress
+heading_alignment
}
class ClimbingProgress {
+__call__()
+forward_weight : float
+elevation_weight : float
+alignment_threshold : float
}
RewardsCfg --> ClimbingProgress : "uses"
```

**Diagram sources**
- [velocity_env_cfg.py:374-665](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py#L374-L665)
- [rewards.py:670-732](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/rewards.py#L670-L732)

**Section sources**
- [velocity_env_cfg.py:374-665](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py#L374-L665)
- [rewards.py:22-681](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/rewards.py#L22-L681)

#### Termination Conditions
- Episode timeout.
- Terrain out-of-bounds termination.
- Illegal contact termination via contact sensor thresholds.

**Section sources**
- [velocity_env_cfg.py:647-665](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py#L647-L665)

### Terrain Configuration Options
- Rough terrain:
  - Generator-based terrains with physics material and visual materials.
  - Height scanners and base height tracking enabled.
  - Curriculum for terrain levels enabled.
- Flat terrain:
  - Plane terrain with no generator.
  - Height scanner disabled.
  - Base height term disabled.
  - Curriculum for terrain levels disabled.
- Advanced terrains:
  - Custom mesh terrains for gap traversal and parkour navigation.
  - Stair climbing terrains with inverted pyramid designs.

**Updated** Enhanced flat terrain configuration with systematic height_scan disabling for computational efficiency.

**Section sources**
- [velocity_env_cfg.py:42-95](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py#L42-L95)
- [flat_env_cfg.py:11-29](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_a1/flat_env_cfg.py#L11-L29)
- [rough_env_cfg.py:30-80](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_a1/rough_env_cfg.py#L30-L80)

### Observation Preprocessing, Noise Injection, and Corruption
- Noise:
  - Additive uniform noise applied to specific observation terms.
- Clipping:
  - Applied to observations to bound extremes.
- Corruption:
  - Policy group enables corruption; critic group disables it.
- Data corruption:
  - Controlled via observation group flags.

**Updated** Enhanced observation processing with systematic height_scan disabling in flat environments to reduce computational overhead and improve training stability.

**Section sources**
- [velocity_env_cfg.py:138-192](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py#L138-L192)
- [velocity_env_cfg.py:198-250](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py#L198-L250)

### Task Parameterization Examples

#### Quadruped: Unitree A1
- Joint names and base/foot link names defined.
- Reduced action scale for hip vs non-hip joints.
- Base height and body acceleration terms enabled for stability.
- Feet contact and gait terms tuned for quadrupedal gaits.
- Terrain-aware curriculum disabled in this example.

**Section sources**
- [rough_env_cfg.py:18-160](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_a1/rough_env_cfg.py#L18-L160)

#### Advanced Quadruped: ZSIBOT ZSL1 (Gap and Parkour)
- Enhanced joint position scaling for climbing scenarios.
- Specialized reward configurations for gap traversal and parkour navigation.
- Custom terrain generation for gap strips and parkour steps.
- Reduced base height penalties and modified contact sensor configurations.

**Section sources**
- [gap_env_cfg.py:160-339](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/gap_env_cfg.py#L160-L339)
- [parkour_env_cfg.py:170-349](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/parkour_env_cfg.py#L170-L349)
- [stair_env_cfg.py:56-235](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/stair_env_cfg.py#L56-L235)

#### Wheeled Robots
- Wheel velocity penalty term designed for wheeled robots.
- Joint position penalty adapted to wheels (where applicable).
- Example robot families include unitree_b2w, unitree_go2w, deeprobotics_m20, ddtrobot_tita, zsibot_zsl1w, magiclab_magicdogw.

**Section sources**
- [rewards.py:129-150](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/rewards.py#L129-L150)
- [README.md:26-31](file://README.md#L26-L31)

#### Humanoid Variants
- Humanoid families include unitree_g1, unitree_h1, fftai_gr1t1, fftai_gr1t2, booster_t1, robotera_xbot, openloong_loong, roboparty_atom01, magiclab_magicbot_gen1, magiclab_magicbot_z1.

**Section sources**
- [README.md:32-42](file://README.md#L32-L42)

### Curriculum Learning Implementation
- Terrain levels curriculum: **NEW** Automatic difficulty progression based on robot performance using the `terrain_levels_vel` function.
- Command range curriculum:
  - Linear and angular velocity ranges are progressively increased when tracking reward exceeds a threshold.
  - Updates occur at episode boundaries to avoid frequent resampling.

**Updated** Enhanced curriculum learning with terrain-level progression functionality.

The terrain-level curriculum automatically adjusts terrain difficulty based on how far the robot travels when commanded to move at a desired velocity. This provides adaptive difficulty progression that responds to actual robot performance rather than fixed schedules.

```mermaid
flowchart TD
Init["First Episode<br/>Capture original ranges"] --> Loop["Every Episode"]
Loop --> Eval["Accumulate episode sums for tracking reward"]
Eval --> Check{"Avg reward > 80% of max?"}
Check --> |Yes| Expand["Increase command ranges (clamp to final)"]
Check --> |No| Hold["Keep current ranges"]
Expand --> Next["Next Episode"]
Hold --> Next
Next --> Loop
```

**Diagram sources**
- [curriculums.py:20-97](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/curriculums.py#L20-L97)
- [velocity_env_cfg.py:667-688](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py#L667-L688)

**Section sources**
- [velocity_env_cfg.py:667-688](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py#L667-L688)
- [curriculums.py:20-97](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/curriculums.py#L20-L97)

### Training Optimization Strategies
- Disable zero-weight rewards to reduce computation overhead.
- Tune observation scales per domain (e.g., higher base linear velocity scale for quadrupeds).
- Use terrain-aware resets to avoid unstable initial conditions on risky terrains.
- Employ mirrored and synchronized action terms to improve gait consistency for quadrupeds.
- Apply curriculum to gradually increase task difficulty and reward signal strength.
- Optimize simulation timing: Use appropriate decimation factors to balance policy update frequency and computational cost.
- Leverage specialized reward functions for climbing scenarios to improve training efficiency.
- **Systematic height_scan disabling**: Disable height_scan observations in flat environments to reduce computational overhead and improve training stability.
- **Observation processing optimization**: Use optimized observation groups with selective feature inclusion based on terrain complexity.
- **Terrain-level curriculum**: Enable automatic difficulty progression that adapts to robot performance for more efficient training.

**Updated** Enhanced timing optimization strategies based on improved documentation of simulation parameters and systematic height_scan disabling for computational efficiency.

**Section sources**
- [velocity_env_cfg.py:737-744](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py#L737-L744)
- [rough_env_cfg.py:30-160](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_a1/rough_env_cfg.py#L30-L160)
- [events.py:203-270](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/events.py#L203-L270)
- [rewards.py:255-334](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/rewards.py#L255-L334)

## Advanced Environment Configurations

### Gap Traversal Environment
The gap traversal environment is specifically designed for quadruped locomotion over gaps and obstacles:

- **Custom Terrain Generation**: Implements mesh-based gap terrains with configurable gap widths and landing platforms.
- **Specialized Reward Function**: Climbing progress reward optimized for gap traversal scenarios.
- **Enhanced Joint Scaling**: Increased scaling factors for hip and knee joints to enable leg lifting over gaps.
- **Modified Contact Sensors**: Reduced contact penalties to encourage controlled stepping behavior.
- **Height Scan Optimization**: Enhanced height scanning for terrain perception during gap traversal.

```mermaid
flowchart TD
GapStart["Gap Environment Init"] --> TerrainGen["Generate Gap Terrain"]
TerrainGen --> JointScale["Adjust Joint Position Scaling"]
JointScale --> RewardCfg["Configure Gap-Specific Rewards"]
RewardCfg --> ContactCfg["Modify Contact Sensor Settings"]
ContactCfg --> HeightScan["Optimize Height Scanning"]
HeightScan --> Ready["Ready for Training"]
```

**Diagram sources**
- [gap_env_cfg.py:27-104](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/gap_env_cfg.py#L27-L104)
- [gap_env_cfg.py:234-314](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/gap_env_cfg.py#L234-L314)

**Section sources**
- [gap_env_cfg.py:160-339](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/gap_env_cfg.py#L160-L339)

### Parkour Navigation Environment
The parkour environment provides advanced obstacle navigation capabilities:

- **Parkour Step Terrains**: Generates staircase-like terrains with rising and falling steps.
- **Dynamic Step Heights**: Configurable step heights ranging from 0.1m to 0.45m based on difficulty.
- **Specialized Reward System**: Climbing progress reward with forward and elevation weighting.
- **Enhanced Stability Controls**: Modified base height penalties and angular velocity constraints.
- **Advanced Gait Control**: Reduced feet contact rewards to encourage dynamic stepping.

**Updated** Enhanced parkour environment with terrain-level curriculum functionality.

The parkour environments now include terrain-level curriculum functionality that automatically adjusts difficulty based on robot performance, providing adaptive training progression.

```mermaid
flowchart TD
ParkourStart["Parkour Environment Init"] --> StepGen["Generate Parkour Steps"]
StepGen --> HeightRange["Configure Step Height Range"]
HeightRange --> RewardSetup["Setup Climbing Progress Rewards"]
RewardSetup --> StabilityCfg["Configure Stability Parameters"]
StabilityCfg --> GaitControl["Adjust Gait Rewards"]
GaitControl --> TerrainCurriculum["Enable Terrain-Level Curriculum"]
TerrainCurriculum --> Ready["Ready for Training"]
```

**Diagram sources**
- [parkour_env_cfg.py:27-117](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/parkour_env_cfg.py#L27-L117)
- [parkour_env_cfg.py:315-324](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/parkour_env_cfg.py#L315-L324)

**Section sources**
- [parkour_env_cfg.py:170-349](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/parkour_env_cfg.py#L170-L349)

### Stair Climbing Environment
The stair climbing environment focuses on vertical navigation capabilities:

- **Inverted Pyramid Stairs**: Advanced stair terrain generation with configurable step dimensions.
- **Target Height Configuration**: Specific base height targets for optimal stair climbing performance.
- **Enhanced Air Time Rewards**: Modified feet air time rewards to encourage controlled stair ascent.
- **Reduced Contact Penalties**: Lower undesired contact penalties to allow for dynamic stair navigation.
- **Specialized Joint Scaling**: Optimized joint position scaling for stair climbing mechanics.

**Section sources**
- [stair_env_cfg.py:56-235](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/stair_env_cfg.py#L56-L235)

## Dependency Analysis
The velocity task configuration composes multiple modules with enhanced support for specialized environments:
- Base environment configuration depends on MDP modules for commands, observations, rewards, curriculum, and events.
- Robot-specific configurations inherit from the base and override scales, joint names, and reward weights.
- Advanced environment configurations extend the base with specialized terrain generation and reward functions.
- Utilities support terrain-aware checks and environment assignments.

```mermaid
graph LR
Base["velocity_env_cfg.py"] --> Cmd["commands.py"]
Base --> Obs["observations.py"]
Base --> Rew["rewards.py"]
Base --> Cur["curriculums.py"]
Base --> Ev["events.py"]
Base --> Util["utils.py"]
Flat["flat_env_cfg.py"] --> Base
Rough["rough_env_cfg.py"] --> Base
Gap["gap_env_cfg.py"] --> Base
Parkour["parkour_env_cfg.py"] --> Base
Stair["stair_env_cfg.py"] --> Base
```

**Diagram sources**
- [velocity_env_cfg.py:12-29](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py#L12-L29)
- [flat_env_cfg.py:1-30](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_a1/flat_env_cfg.py#L1-L30)
- [rough_env_cfg.py:1-162](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_a1/rough_env_cfg.py#L1-L162)
- [gap_env_cfg.py:1-339](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/gap_env_cfg.py#L1-L339)
- [parkour_env_cfg.py:1-349](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/parkour_env_cfg.py#L1-L349)
- [stair_env_cfg.py:1-235](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/stair_env_cfg.py#L1-L235)
- [commands.py:1-185](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/commands.py#L1-L185)
- [observations.py:1-35](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/observations.py#L1-L35)
- [rewards.py:1-681](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/rewards.py#L1-L681)
- [curriculums.py:1-97](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/curriculums.py#L1-L97)
- [events.py:1-270](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/events.py#L1-L270)
- [utils.py:1-127](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/utils.py#L1-L127)

**Section sources**
- [velocity_env_cfg.py:12-29](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py#L12-L29)
- [flat_env_cfg.py:1-30](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_a1/flat_env_cfg.py#L1-L30)
- [rough_env_cfg.py:1-162](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_a1/rough_env_cfg.py#L1-L162)

## Performance Considerations
- Disable unused or zero-weighted rewards to reduce computational overhead.
- Tune observation scales to balance signal strength and numerical stability.
- Prefer generator-based terrains with appropriate GPU patch counts for large-scale training.
- Use curriculum updates at episode boundaries to avoid excessive resampling frequency.
- Optimize simulation timing: Configure decimation factor appropriately for target policy update frequency.
- Balance physics timestep (sim.dt) with computational budget for stable training performance.
- Leverage specialized reward functions for climbing scenarios to improve training efficiency.
- Use advanced terrain generation for complex locomotion scenarios to enhance generalization.
- **Systematic height_scan disabling**: Disable height_scan observations in flat environments to reduce computational overhead and improve training stability.
- **Observation processing optimization**: Use optimized observation groups with selective feature inclusion based on terrain complexity and computational requirements.
- **Terrain-level curriculum**: Enable automatic difficulty progression that adapts to robot performance for more efficient training.

**Updated** Added guidance on simulation timing optimization and decimation factor tuning, plus systematic height_scan disabling for computational efficiency.

[No sources needed since this section provides general guidance]

## Troubleshooting Guide
- Symmetry and data augmentation: Enable symmetry data augmentation for quadrupeds to improve generalization.
- Distillation: Train a teacher agent on flat terrain, then distill into a student agent for faster convergence.
- Multi-node distributed training: Use torch.distributed runner for multi-GPU and multi-node setups.
- Timing issues: Adjust decimation factor if experiencing slow/fast policy updates relative to physics simulation.
- Advanced terrain issues: Ensure proper mesh generation parameters for gap and parkour terrains.
- Reward balance: Monitor climbing progress rewards to ensure proper balance between forward progress and elevation gain.
- **Observation processing issues**: If experiencing high computational overhead, verify that height_scan observations are properly disabled in flat environments.
- **Curriculum adaptation**: If terrain difficulty isn't adjusting appropriately, check that terrain-level curriculum is enabled and the robot is making sufficient progress.

**Section sources**
- [README.md:291-312](file://README.md#L291-L312)

## Conclusion
The velocity-based locomotion tasks leverage a modular ManagerBasedRLEnv configuration with robust command generation, comprehensive reward shaping, and curriculum-driven difficulty progression. The framework now includes enhanced support for specialized locomotion scenarios through improved observation processing that systematically disables height_scan observations in flat environments to reduce computational overhead and improve training stability. **NEW** The framework includes sophisticated terrain-level curriculum functionality that automatically adjusts terrain difficulty based on robot performance, providing adaptive training progression that responds to actual learning rather than fixed schedules. These enhancements provide advanced terrain generation capabilities and specialized reward functions that improve training efficiency and generalization for complex locomotion tasks. The modular architecture supports diverse robot types (quadrupeds, wheeled, humanoids) and terrain regimes (flat/rough/advanced), with practical training optimizations and terrain-aware behaviors to improve stability and generalization.

[No sources needed since this section summarizes without analyzing specific files]

## Appendices

### Appendix A: Environment Registration and Launch
- Environments are registered with ManagerBasedRLEnv entry points and robot-specific configuration modules.
- Training and evaluation scripts are provided for RSL-RL and SKRL.
- Advanced environment configurations support specialized training scenarios.
- **Updated** Task naming conventions now use `RobotLab-Isaac-Velocity-<Robot>-<Terrain>-<Variant>-v0` format without `-Play` suffixes.

**Section sources**
- [README.md:193-332](file://README.md#L193-L332)
- [unitree_go2_parkour_init.py:19-162](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/__init__.py#L19-L162)
- [zsibot_zsl1_parkour_init.py:19-161](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1_parkour/__init__.py#L19-L161)

### Appendix B: Simulation Timing Configuration Reference

**Updated** Added detailed reference for simulation timing parameters.

The velocity-based locomotion tasks use a standardized simulation timing configuration:

- **Default Physics Timestep (sim.dt)**: 0.005 seconds
- **Default Decimation Factor**: 4
- **Default Policy Update Interval**: 0.02 seconds (4 × 0.005)
- **Default Render Interval**: 4 steps
- **Sensor Update Periods**:
  - Height scanners: decimation × sim.dt
  - Contact forces: sim.dt

**Section sources**
- [velocity_env_cfg.py:804-811](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py#L804-L811)
- [velocity_env_cfg.py:753-757](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py#L753-L757)

### Appendix C: Advanced Terrain Generation Reference

**Updated** Added reference for advanced terrain generation capabilities.

The velocity-based locomotion framework supports advanced terrain generation for specialized locomotion scenarios:

- **Gap Terrains**: Configurable gap widths with landing platforms and run-up sections.
- **Parkour Terrains**: Dynamic step heights with rising and falling staircases.
- **Stair Terrains**: Inverted pyramid designs with adjustable step dimensions.
- **Mesh Generation**: Custom terrain generation functions for complex geometries.
- **Difficulty Scaling**: Procedural terrain generation with difficulty-based parameter variation.
- **Terrain-Level Curriculum**: Automatic difficulty progression based on robot performance.

**Section sources**
- [gap_env_cfg.py:27-104](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/gap_env_cfg.py#L27-L104)
- [parkour_env_cfg.py:27-117](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/parkour_env_cfg.py#L27-L117)
- [stair_env_cfg.py:21-53](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/stair_env_cfg.py#L21-L53)

### Appendix D: Observation Processing Optimization Patterns

**Updated** Added comprehensive reference for observation processing optimization patterns.

The velocity-based locomotion framework implements systematic observation processing optimizations:

- **Flat Environment Pattern**: Height scan observations disabled in all flat environment configurations
- **Rough Terrain Pattern**: Height scan observations enabled for complex terrain perception
- **Computational Efficiency**: Reduced observation vector size in flat environments by ~15-20%
- **Training Stability**: Improved training stability through reduced computational overhead
- **Selective Feature Inclusion**: Observation groups optimized based on terrain complexity requirements

Common flat environment configurations that disable height_scan:
- Quadruped: Unitree A1, ZSIBOT ZSL1, Anymal D, MagicLab MagicDog
- Humanoid: Unitree G1, Unitree H1, FFTAI GR1T1, FFTAI GR1T2
- Wheeled: Deeprobotics M20, DDT Robot TITA, MagicLab MagicDogW

**Section sources**
- [flat_env_cfg.py:20-23](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_a1/flat_env_cfg.py#L20-L23)
- [opendoge_flat_env_cfg.py:20-23](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/opendoge_apx/flat_env_cfg.py#L20-L23)
- [fftai_flat_env_cfg.py:20-23](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/fftai_gr1t1/flat_env_cfg.py#L20-L23)
- [unitree_h1_flat_env_cfg.py:20-23](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/unitree_h1/flat_env_cfg.py#L20-L23)
- [deeprobotics_m20_flat_env_cfg.py:20-23](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/wheeled/deeprobotics_m20/flat_env_cfg.py#L20-L23)

### Appendix E: Terrain-Level Curriculum Functionality

**Updated** Added comprehensive documentation for terrain-level curriculum implementation.

The velocity-based locomotion framework includes sophisticated terrain-level curriculum functionality that automatically adjusts terrain difficulty based on robot performance:

- **terrain_levels_vel Function**: Core curriculum function that monitors robot progress and adjusts terrain difficulty
- **Performance-Based Difficulty**: Increases terrain difficulty when robots travel far enough and decreases it when they fall behind
- **Generator-Based Only**: Works exclusively with generator-type terrains, not with plane-based flat terrains
- **Automatic Enable/Disable**: Curriculum automatically enables/disables terrain generator curriculum based on configuration
- **Mean Terrain Level Output**: Returns average terrain level for monitoring and debugging

Implementation Details:
- Distance calculation uses robot's 2D position relative to environment origins
- Movement threshold: Robot must travel more than half the terrain size to advance difficulty
- Regression threshold: Robot must travel less than half of commanded velocity distance to decrease difficulty
- Terrain update occurs through `terrain.update_env_origins()` method

**Section sources**
- [curriculums.py:103-134](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/mdp/curriculums.py#L103-L134)
- [velocity_env_cfg.py:787-813](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py#L787-L813)
- [velocity_env_cfg.py:853-859](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py#L853-L859)
- [zsibot_zsl1_parkour_rough_env_cfg.py:512-518](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1_parkour/rough_env_cfg.py#L512-L518)
- [unitree_go2_parkour_rough_env_cfg.py:510-513](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/rough_env_cfg.py#L510-L513)