# Environment Registration Framework

<cite>
**Referenced Files in This Document**
- [robot_lab/__init__.py](file://source/robot_lab/robot_lab/__init__.py)
- [beyondmimic_g1/__init__.py](file://source/robot_lab/robot_lab/tasks/direct/g1_amp/__init__.py)
- [booster_t1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/booster_t1/__init__.py)
- [fftai_gr1t1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/fftai_gr1t1/__init__.py)
- [unitree_g1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/unitree_g1/__init__.py)
- [unitree_h1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/unitree_h1/__init__.py)
- [magiclab_magicbot_gen1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/magiclab_magicbot_gen1/__init__.py)
- [openloong_loong/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/openloong_loong/__init__.py)
- [roboparty_atom01/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/roboparty_atom01/__init__.py)
- [robotera_xbot/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/robotera_xbot/__init__.py)
- [unitree_a1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_a1/__init__.py)
- [zsibot_zsl1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/__init__.py)
- [stair_env_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/stair_env_cfg.py)
- [gap_env_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/gap_env_cfg.py)
- [parkour_env_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/parkour_env_cfg.py)
- [flat_env_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/flat_env_cfg.py)
- [velocity_env_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/velocity_env_cfg.py)
- [README.md](file://README.md)
</cite>

## Update Summary
**Changes Made**
- Added documentation for new gap and parkour environment registration system
- Updated environment naming scheme to include Gap and Parkour terrain types
- Added Zsibot ZSL1 gap and parkour environment configuration details
- Enhanced examples with gap traversal and parkour-style stepping environment registration patterns
- Updated README.md references to reflect new gap and parkour capabilities
- Added specialized terrain generation and reward systems for gap and parkour environments

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

## Introduction
This document explains the environment registration framework used by the Robot Lab project to integrate Gymnasium-compatible environments with the ManagerBasedRLEnv class. It focuses on the standardized naming convention for environments (for example, RobotLab-Isaac-Velocity-Flat-Unitree-A1-v0), the registration mechanism via gym.register(), and how environment names map to configuration classes and the underlying RL environment implementation. The guide also covers common registration issues, naming conflicts, and debugging techniques for environment setup.

**Updated** Added support for gap traversal and parkour-style stepping environments with specialized terrain generation and reward systems for Zsibot ZSL1.

## Project Structure
The environment registration system is organized around a set of modular configuration packages under the manager-based locomotion velocity task. Each robot family (for example, Unitree G1, Unitree H1, Booster T1, FFTAI GR1T1, Magiclab Magicbot Gen1, OpenLoong Loong, Roboparty Atom01, Robotera XBot, Zsibot ZSL1) defines its own registration entry points and configuration classes. The top-level package initializer triggers task-level registrations.

```mermaid
graph TB
RL["Robot Lab Package<br/>source/robot_lab/robot_lab/__init__.py"]
Tasks["Tasks Module<br/>source/robot_lab/robot_lab/tasks"]
MB["Manager-Based Task<br/>source/robot_lab/robot_lab/tasks/manager_based"]
Vel["Velocity Task<br/>source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity"]
Quad["Quadruped Configurations<br/>.../quadruped/*"]
ZSL1["Zsibot ZSL1 Config<br/>.../quadruped/zsibot_zsl1"]
A1["Unitree A1 Config<br/>.../quadruped/unitree_a1"]
Humanoid["Humanoid Configurations<br/>.../humanoid/*"]
G1["Unitree G1 Config<br/>.../humanoid/unitree_g1"]
H1["Unitree H1 Config<br/>.../humanoid/unitree_h1"]
BT1["Booster T1 Config<br/>.../humanoid/booster_t1"]
FGR1T1["FFTAI GR1T1 Config<br/>.../humanoid/fftai_gr1t1"]
MMG1["Magiclab Magicbot Gen1 Config<br/>.../humanoid/magiclab_magicbot_gen1"]
OLG["OpenLoong Loong Config<br/>.../humanoid/openloong_loong"]
RPA["Roboparty Atom01 Config<br/>.../humanoid/roboparty_atom01"]
REX["Robotera XBot Config<br/>.../humanoid/robotera_xbot"]
RL --> Tasks
Tasks --> MB
MB --> Vel
Vel --> Quad
Vel --> Humanoid
Quad --> ZSL1
Quad --> A1
Humanoid --> G1
Humanoid --> H1
Humanoid --> BT1
Humanoid --> FGR1T1
Humanoid --> MMG1
Humanoid --> OLG
Humanoid --> RPA
Humanoid --> REX
```

**Diagram sources**
- [robot_lab/__init__.py:8-12](file://source/robot_lab/robot_lab/__init__.py#L8-L12)
- [unitree_g1/__init__.py:11-23](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/unitree_g1/__init__.py#L11-L23)
- [unitree_h1/__init__.py:11-22](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/unitree_h1/__init__.py#L11-L22)
- [booster_t1/__init__.py:7-18](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/booster_t1/__init__.py#L7-L18)
- [fftai_gr1t1/__init__.py:11-22](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/fftai_gr1t1/__init__.py#L11-L22)
- [magiclab_magicbot_gen1/__init__.py:11-23](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/magiclab_magicbot_gen1/__init__.py#L11-L23)
- [openloong_loong/__init__.py:11-22](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/openloong_loong/__init__.py#L11-L22)
- [roboparty_atom01/__init__.py:11-23](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/roboparty_atom01/__init__.py#L11-L23)
- [robotera_xbot/__init__.py:7-18](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/robotera_xbot/__init__.py#L7-L18)
- [unitree_a1/__init__.py:12-32](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_a1/__init__.py#L12-L32)
- [zsibot_zsl1/__init__.py:12-60](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/__init__.py#L12-L60)

**Section sources**
- [robot_lab/__init__.py:8-12](file://source/robot_lab/robot_lab/__init__.py#L8-L12)

## Core Components
- Environment Naming Convention: RobotLab-Isaac-{TaskType}-{Terrain}-{RobotCategory}-{Model}-{Version}
  - TaskType: Velocity
  - Terrain: Flat, Rough, Stair, Gap (newly added), Parkour (newly added)
  - RobotCategory: Unitree, FFTAI, Magiclab, OpenLoong, Roboparty, Robotera, Zsibot
  - Model: A1, G1, H1, GR1T1, GR1T2, Magicbot Gen1/Z1, Loong, Atom01, XBot, ZSL1
  - Version: v0
- Registration Mechanism: gym.register() with:
  - id: Standardized environment name
  - entry_point: "isaaclab.envs:ManagerBasedRLEnv"
  - disable_env_checker: True
  - kwargs:
    - env_cfg_entry_point: "{package}.flat_env_cfg:{ClassName}" or "{package}.{terrain}_env_cfg:{ClassName}"
    - rsl_rl_cfg_entry_point: "{package}.agents.rsl_rl_ppo_cfg:{ClassName}"

Examples of registration patterns are visible in the humanoid configurations for Unitree G1, Unitree H1, Booster T1, FFTAI GR1T1, Magiclab Magicbot Gen1, OpenLoong Loong, Roboparty Atom01, and Robotera XBot, as well as the quadruped configurations for Unitree A1 and Zsibot ZSL1.

**Updated** Added gap and parkour environment registration patterns for Zsibot ZSL1 with specialized terrain generation and reward systems.

**Section sources**
- [beyondmimic_g1/__init__.py:21-29](file://source/robot_lab/robot_lab/tasks/direct/g1_amp/__init__.py#L21-L29)
- [unitree_g1/__init__.py:11-23](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/unitree_g1/__init__.py#L11-L23)
- [unitree_h1/__init__.py:11-22](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/unitree_h1/__init__.py#L11-L22)
- [booster_t1/__init__.py:7-18](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/booster_t1/__init__.py#L7-L18)
- [fftai_gr1t1/__init__.py:11-22](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/fftai_gr1t1/__init__.py#L11-L22)
- [magiclab_magicbot_gen1/__init__.py:11-23](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/magiclab_magicbot_gen1/__init__.py#L11-L23)
- [openloong_loong/__init__.py:11-22](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/openloong_loong/__init__.py#L11-L22)
- [roboparty_atom01/__init__.py:11-23](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/roboparty_atom01/__init__.py#L11-L23)
- [robotera_xbot/__init__.py:7-18](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/robotera_xbot/__init__.py#L7-L18)
- [unitree_a1/__init__.py:12-32](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_a1/__init__.py#L12-L32)
- [zsibot_zsl1/__init__.py:12-60](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/__init__.py#L12-L60)

## Architecture Overview
The environment registration architecture connects standardized environment names to configuration classes through ManagerBasedRLEnv. The flow below illustrates how a gym.register() call maps to the RL training configuration and environment configuration classes.

```mermaid
sequenceDiagram
participant Reg as "Registration Script<br/>(.../humanoid/*/__init__.py or .../quadruped/*/gap_env_cfg.py or .../quadruped/*/parkour_env_cfg.py)"
participant Gym as "Gymnasium Registry"
participant Env as "ManagerBasedRLEnv<br/>(entry_point)"
participant Cfg as "Environment Config Class<br/>(env_cfg_entry_point)"
participant RL as "RL Runner Config Class<br/>(rsl_rl_cfg_entry_point)"
Reg->>Gym : "gym.register(id, entry_point, kwargs)"
Gym-->>Reg : "Registration OK"
Note over Gym,Env : "Later, when env is created via gym.make(name)"
Gym->>Env : "Instantiate with env_cfg_entry_point and rsl_rl_cfg_entry_point"
Env->>Cfg : "Load environment configuration"
Env->>RL : "Load RL runner configuration"
Env-->>Gym : "Return configured environment instance"
```

**Diagram sources**
- [beyondmimic_g1/__init__.py:21-29](file://source/robot_lab/robot_lab/tasks/direct/g1_amp/__init__.py#L21-L29)
- [unitree_g1/__init__.py:11-23](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/unitree_g1/__init__.py#L11-L23)
- [stair_env_cfg.py:50-219](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/stair_env_cfg.py#L50-L219)
- [gap_env_cfg.py:159-339](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/gap_env_cfg.py#L159-L339)
- [parkour_env_cfg.py:169-349](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/parkour_env_cfg.py#L169-L349)

## Detailed Component Analysis

### Environment Naming Scheme Breakdown
- RobotLab-Isaac: Project and ecosystem prefix
- Velocity: Task type indicating locomotion policy training
- Flat/Rough/Stair/Gap/Parkour: Terrain type for the environment (Gap and Parkour are newly added)
- Unitree/A1: Robot category and model
- v0: Version identifier

This scheme ensures uniqueness and discoverability across robots and terrains while keeping names concise and readable.

**Updated** Added Gap and Parkour terrain types to support specialized traversal and stepping environments.

**Section sources**
- [README.md:17-41](file://README.md#L17-L41)
- [stair_env_cfg.py:20-47](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/stair_env_cfg.py#L20-L47)
- [gap_env_cfg.py:159-160](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/gap_env_cfg.py#L159-L160)
- [parkour_env_cfg.py:169-170](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/parkour_env_cfg.py#L169-L170)

### Registration Pattern in Manager-Based Environments
Each humanoid configuration package registers one or more environments using gym.register(). The pattern includes:
- id: Standardized environment name following the naming scheme
- entry_point: "isaaclab.envs:ManagerBasedRLEnv"
- disable_env_checker: True
- kwargs:
  - env_cfg_entry_point: "{package}.flat_env_cfg:{ClassName}" or "{package}.{terrain}_env_cfg:{ClassName}"
  - rsl_rl_cfg_entry_point: "{package}.agents.rsl_rl_ppo_cfg:{ClassName}"

Concrete examples:
- Unitree G1 Flat: RobotLab-Isaac-Velocity-Flat-Unitree-G1-v0
- Unitree G1 Rough: RobotLab-Isaac-Velocity-Rough-Unitree-G1-v0
- Unitree H1 Flat: RobotLab-Isaac-Velocity-Flat-Unitree-H1-v0
- Booster T1 Flat: RobotLab-Isaac-Velocity-Flat-Booster-T1-v0
- FFTAI GR1T1 Flat: RobotLab-Isaac-Velocity-Flat-FFTAI-GR1T1-v0
- Magiclab Magicbot Gen1 Flat: RobotLab-Isaac-Velocity-Flat-Magiclab-Magicbot-Gen1-v0
- OpenLoong Loong Flat: RobotLab-Isaac-Velocity-Flat-OpenLoong-Loong-v0
- Roboparty Atom01 Flat: RobotLab-Isaac-Velocity-Flat-Roboparty-Atom01-v0
- Robotera XBot Flat: RobotLab-Isaac-Velocity-Flat-Robotera-XBot-v0
- Unitree A1 Flat: RobotLab-Isaac-Velocity-Flat-Unitree-A1-v0
- Unitree A1 Rough: RobotLab-Isaac-Velocity-Rough-Unitree-A1-v0
- Zsibot ZSL1 Flat: RobotLab-Isaac-Velocity-Flat-Zsibot-ZSL1-v0
- Zsibot ZSL1 Rough: RobotLab-Isaac-Velocity-Rough-Zsibot-ZSL1-v0
- Zsibot ZSL1 Stair: RobotLab-Isaac-Velocity-Stair-Zsibot-ZSL1-v0
- **Zsibot ZSL1 Gap: RobotLab-Isaac-Velocity-Gap-Zsibot-ZSL1-v0 (NEW)**
- **Zsibot ZSL1 Parkour: RobotLab-Isaac-Velocity-Parkour-Zsibot-ZSL1-v0 (NEW)**

**Updated** Added Zsibot ZSL1 gap and parkour environment registration patterns with specialized terrain generation.

These registrations demonstrate consistent mapping between environment names and configuration classes.

**Section sources**
- [unitree_g1/__init__.py:11-23](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/unitree_g1/__init__.py#L11-L23)
- [unitree_h1/__init__.py:11-22](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/unitree_h1/__init__.py#L11-L22)
- [booster_t1/__init__.py:7-18](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/booster_t1/__init__.py#L7-L18)
- [fftai_gr1t1/__init__.py:11-22](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/fftai_gr1t1/__init__.py#L11-L22)
- [magiclab_magicbot_gen1/__init__.py:11-23](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/magiclab_magicbot_gen1/__init__.py#L11-L23)
- [openloong_loong/__init__.py:11-22](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/openloong_loong/__init__.py#L11-L22)
- [roboparty_atom01/__init__.py:11-23](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/roboparty_atom01/__init__.py#L11-L23)
- [robotera_xbot/__init__.py:7-18](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/robotera_xbot/__init__.py#L7-L18)
- [unitree_a1/__init__.py:12-32](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_a1/__init__.py#L12-L32)
- [zsibot_zsl1/__init__.py:12-60](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/__init__.py#L12-L60)

### Specialized Gap Environment Configuration
The Zsibot ZSL1 gap environment introduces specialized configuration for gap traversal scenarios:

- **Custom Gap Terrain Generation**: Uses MeshGapTerrainCfg and MeshGapStripTerrainCfg with configurable gap widths (0.1m to 0.8m) and landing platforms
- **Enhanced Reward System**: 
  - Specialized gap traversal rewards encouraging successful crossing
  - Reduced jumping tendencies while maintaining stability
  - Customized action scaling for precise gap navigation
- **Run-up Platform**: Extended start platform (8.0m) for approach running
- **Landing Strips**: Repeated gap-landing combinations for continuous traversal training

**New** Specialized gap environment configuration with custom terrain generation and reward systems for gap traversal.

**Section sources**
- [gap_env_cfg.py:27-157](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/gap_env_cfg.py#L27-L157)
- [gap_env_cfg.py:159-339](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/gap_env_cfg.py#L159-L339)

### Specialized Parkour Environment Configuration
The Zsibot ZSL1 parkour environment introduces specialized configuration for parkour-style stepping scenarios:

- **Custom Parkour Terrain Generation**: Uses MeshParkourStepTerrainCfg with configurable step heights (0.1m to 0.45m) and varying step lengths
- **Dynamic Step Patterns**: Alternating ascending and descending steps creating complex terrain challenges
- **Enhanced Reward System**: 
  - Specialized climbing rewards for step progression
  - Customized action scaling for dynamic stepping motions
  - Reduced jumping tendencies while encouraging controlled climbing
- **Side Walls**: Thin side walls added for safety and realism
- **Complex Terrain Curricula**: Multiple step configurations for progressive difficulty

**New** Specialized parkour environment configuration with custom terrain generation and reward systems for complex stepping challenges.

**Section sources**
- [parkour_env_cfg.py:27-167](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/parkour_env_cfg.py#L27-L167)
- [parkour_env_cfg.py:169-349](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/parkour_env_cfg.py#L169-L349)

### Relationship Between Names, Configuration Classes, and ManagerBasedRLEnv
- Environment Name: Determines the registry id used by gym.make()
- Configuration Classes:
  - Environment Config: Loaded via env_cfg_entry_point pointing to a class in the package's flat_env_cfg, gap_env_cfg, or parkour_env_cfg module
  - RL Runner Config: Loaded via rsl_rl_cfg_entry_point pointing to a class in the package's agents.rsl_rl_ppo_cfg module
- ManagerBasedRLEnv: The entry_point class that consumes the configuration classes to construct the environment and training runner

```mermaid
classDiagram
class ManagerBasedRLEnv {
+env_cfg_entry_point
+rsl_rl_cfg_entry_point
+create_environment()
+configure_training_runner()
}
class EnvConfigClass {
+training_steps
+episode_length_s
+terrain_type
+robot_model
}
class RLRunnerConfigClass {
+num_epochs
+num_steps_per_env
+policy_arch
+value_arch
}
class GapEnvConfigClass {
+gap_terrain_cfg
+custom_action_scaling
+gap_traversal_rewards
}
class ParkourEnvConfigClass {
+parkour_step_terrain_cfg
+dynamic_step_patterns
+climbing_rewards
}
class StairEnvConfigClass {
+stair_terrain_cfg
+aggressive_action_scaling
+enhanced_reward_system
}
ManagerBasedRLEnv --> EnvConfigClass : "loads via env_cfg_entry_point"
ManagerBasedRLEnv --> RLRunnerConfigClass : "loads via rsl_rl_cfg_entry_point"
GapEnvConfigClass --|> EnvConfigClass : "extends"
ParkourEnvConfigClass --|> EnvConfigClass : "extends"
StairEnvConfigClass --|> EnvConfigClass : "extends"
```

**Diagram sources**
- [beyondmimic_g1/__init__.py:21-29](file://source/robot_lab/robot_lab/tasks/direct/g1_amp/__init__.py#L21-L29)
- [unitree_g1/__init__.py:11-23](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/unitree_g1/__init__.py#L11-L23)
- [stair_env_cfg.py:50-219](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/stair_env_cfg.py#L50-L219)
- [gap_env_cfg.py:159-339](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/gap_env_cfg.py#L159-L339)
- [parkour_env_cfg.py:169-349](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/parkour_env_cfg.py#L169-L349)

## Dependency Analysis
The registration system depends on:
- Gymnasium for environment registration and creation
- ManagerBasedRLEnv as the entry_point class
- Package-specific configuration modules for environment and RL runner settings
- **Specialized terrain generation utilities** for gap and parkour environments
- **Custom terrain generator configurations** for gap traversal and parkour-style stepping

```mermaid
graph TB
Gymnasium["Gymnasium Library"]
RegScripts["Registration Scripts<br/>.../humanoid/*/__init__.py<br/>.../quadruped/*/gap_env_cfg.py<br/>.../quadruped/*/parkour_env_cfg.py"]
EnvClass["ManagerBasedRLEnv<br/>(entry_point)"]
EnvCfg["Environment Config Modules<br/>.../flat_env_cfg.py<br/>.../gap_env_cfg.py<br/>.../parkour_env_cfg.py<br/>.../stair_env_cfg.py"]
RLCfg["RL Runner Config Modules<br/>.../agents/rsl_rl_ppo_cfg.py"]
GapTerrains["Gap Terrain Generation<br/>MeshGapTerrainCfg/MeshGapStripTerrainCfg"]
ParkourTerrains["Parkour Terrain Generation<br/>MeshParkourStepTerrainCfg"]
StairTerrains["Stair Terrain Generation<br/>MeshInvertedPyramidStairsTerrainCfg"]
Gymnasium --> RegScripts
RegScripts --> EnvClass
EnvClass --> EnvCfg
EnvClass --> RLCfg
EnvCfg --> GapTerrains
EnvCfg --> ParkourTerrains
EnvCfg --> StairTerrains
```

**Diagram sources**
- [beyondmimic_g1/__init__.py:21-29](file://source/robot_lab/robot_lab/tasks/direct/g1_amp/__init__.py#L21-L29)
- [unitree_g1/__init__.py:11-23](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/unitree_g1/__init__.py#L11-L23)
- [stair_env_cfg.py:17-47](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/stair_env_cfg.py#L17-L47)
- [gap_env_cfg.py:27-157](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/gap_env_cfg.py#L27-L157)
- [parkour_env_cfg.py:27-167](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/parkour_env_cfg.py#L27-L167)

**Section sources**
- [beyondmimic_g1/__init__.py:21-29](file://source/robot_lab/robot_lab/tasks/direct/g1_amp/__init__.py#L21-L29)
- [unitree_g1/__init__.py:11-23](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/unitree_g1/__init__.py#L11-L23)
- [stair_env_cfg.py:17-47](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/stair_env_cfg.py#L17-L47)
- [gap_env_cfg.py:27-157](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/gap_env_cfg.py#L27-L157)
- [parkour_env_cfg.py:27-167](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/parkour_env_cfg.py#L27-L167)

## Performance Considerations
- Keep registration scripts lightweight; avoid heavy imports during import time.
- Use disable_env_checker=True to reduce overhead during registration.
- Centralize configuration loading to minimize repeated disk reads.
- Ensure environment and runner configuration classes are efficient and avoid unnecessary computations at initialization.
- **Gap and parkour environments require specialized terrain generation** which may increase initial setup time but provides more realistic traversal scenarios.
- **Custom terrain generation functions** may require additional computational resources for procedural terrain creation.

## Troubleshooting Guide
Common issues and resolutions:
- Environment name not found
  - Verify the exact name matches the registered id and includes the correct task type, terrain, robot category, model, and version.
  - Confirm the registration script is imported by the package initializer.
  - **For gap and parkour environments, ensure the gap_env_cfg.py and parkour_env_cfg.py modules exist and are properly imported.**
- Entry point resolution errors
  - Ensure entry_point is exactly "isaaclab.envs:ManagerBasedRLEnv".
  - Verify that the environment and RL runner configuration entry points resolve to existing classes in their respective modules.
- Configuration class not found
  - Check that env_cfg_entry_point and rsl_rl_cfg_entry_point point to valid modules and class names.
  - Confirm the modules exist and export the expected classes.
  - **For gap and parkour environments, verify that gap_env_cfg.py and parkour_env_cfg.py contain the ZsibotZSL1GapEnvCfg and ZsibotZSL1ParkourEnvCfg classes respectively.**
- Naming conflicts
  - Ensure unique ids across robots and terrains to avoid collisions.
  - Use the standardized naming scheme consistently to prevent ambiguity.
  - **Include the Gap and Parkour terrain types in the naming convention for specialized environments.**
- Debugging techniques
  - List registered environments using a helper script to confirm registration.
  - Temporarily print or log configuration class names during registration to validate imports.
  - Test gym.make() with verbose logging to capture instantiation errors.
  - **For gap and parkour environments, verify terrain generation configuration and reward system setup.**
  - **Check custom terrain generation functions for proper parameter validation and error handling.**

## Conclusion
The Robot Lab environment registration framework leverages a standardized naming scheme and consistent registration patterns to integrate Gymnasium environments with ManagerBasedRLEnv. By organizing configurations per robot family and terrain, the system achieves clarity, maintainability, and scalability across diverse robotic platforms. The addition of gap traversal and parkour-style stepping environments demonstrates the framework's extensibility for specialized locomotion tasks with custom terrain generation and reward systems. Following the documented patterns and troubleshooting steps ensures reliable environment setup and training workflows.

**Updated** Enhanced with gap and parkour environment registration capabilities and specialized terrain generation systems for Zsibot ZSL1, expanding the framework's support for diverse terrain types and locomotion challenges including gap traversal and complex stepping scenarios.