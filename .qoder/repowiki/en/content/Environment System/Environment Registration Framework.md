# Environment Registration Framework

<cite>
**Referenced Files in This Document**
- [robot_lab/__init__.py](file://source/robot_lab/robot_lab/__init__.py)
- [beyondmimic_g1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/beyondmimic/config/g1/__init__.py)
- [booster_t1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/booster_t1/__init__.py)
- [fftai_gr1t1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/fftai_gr1t1/__init__.py)
- [unitree_g1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/unitree_g1/__init__.py)
- [unitree_h1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/unitree_h1/__init__.py)
- [magiclab_magicbot_gen1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/magiclab_magicbot_gen1/__init__.py)
- [openloong_loong/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/openloong_loong/__init__.py)
- [roboparty_atom01/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/roboparty_atom01/__init__.py)
- [robotera_xbot/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/robotera_xbot/__init__.py)
- [README.md](file://README.md)
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

## Introduction
This document explains the environment registration framework used by the Robot Lab project to integrate Gymnasium-compatible environments with the ManagerBasedRLEnv class. It focuses on the standardized naming convention for environments (for example, RobotLab-Isaac-Velocity-Flat-Unitree-A1-v0), the registration mechanism via gym.register(), and how environment names map to configuration classes and the underlying RL environment implementation. The guide also covers common registration issues, naming conflicts, and debugging techniques for environment setup.

## Project Structure
The environment registration system is organized around a set of modular configuration packages under the manager-based locomotion velocity task. Each robot family (for example, Unitree G1, Unitree H1, Booster T1, FFTAI GR1T1, Magiclab Magicbot Gen1, OpenLoong Loong, Roboparty Atom01, Robotera XBot) defines its own registration entry points and configuration classes. The top-level package initializer triggers task-level registrations.

```mermaid
graph TB
RL["Robot Lab Package<br/>source/robot_lab/robot_lab/__init__.py"]
Tasks["Tasks Module<br/>source/robot_lab/robot_lab/tasks"]
MB["Manager-Based Task<br/>source/robot_lab/robot_lab/tasks/manager_based"]
Vel["Velocity Task<br/>source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity"]
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
Vel --> Humanoid
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
- [robot_lab/__init__.py](file://source/robot_lab/robot_lab/__init__.py#L8-L12)
- [unitree_g1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/unitree_g1/__init__.py#L11-L23)
- [unitree_h1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/unitree_h1/__init__.py#L11-L22)
- [booster_t1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/booster_t1/__init__.py#L7-L18)
- [fftai_gr1t1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/fftai_gr1t1/__init__.py#L11-L22)
- [magiclab_magicbot_gen1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/magiclab_magicbot_gen1/__init__.py#L11-L23)
- [openloong_loong/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/openloong_loong/__init__.py#L11-L22)
- [roboparty_atom01/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/roboparty_atom01/__init__.py#L11-L23)
- [robotera_xbot/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/robotera_xbot/__init__.py#L7-L18)

**Section sources**
- [robot_lab/__init__.py](file://source/robot_lab/robot_lab/__init__.py#L8-L12)

## Core Components
- Environment Naming Convention: RobotLab-Isaac-{TaskType}-{Terrain}-{RobotCategory}-{Model}-{Version}
  - TaskType: Velocity
  - Terrain: Flat or Rough
  - RobotCategory: Unitree, FFTAI, Magiclab, OpenLoong, Roboparty, Robotera
  - Model: A1, G1, H1, GR1T1, GR1T2, Magicbot Gen1/Z1, Loong, Atom01, XBot
  - Version: v0
- Registration Mechanism: gym.register() with:
  - id: Standardized environment name
  - entry_point: "isaaclab.envs:ManagerBasedRLEnv"
  - disable_env_checker: True
  - kwargs:
    - env_cfg_entry_point: "{package}.flat_env_cfg:{ClassName}"
    - rsl_rl_cfg_entry_point: "{package}.agents.rsl_rl_ppo_cfg:{ClassName}"

Examples of registration patterns are visible in the humanoid configurations for Unitree G1, Unitree H1, Booster T1, FFTAI GR1T1, Magiclab Magicbot Gen1, OpenLoong Loong, Roboparty Atom01, and Robotera XBot.

**Section sources**
- [beyondmimic_g1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/beyondmimic/config/g1/__init__.py#L12-L19)
- [unitree_g1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/unitree_g1/__init__.py#L11-L23)
- [unitree_h1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/unitree_h1/__init__.py#L11-L22)
- [booster_t1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/booster_t1/__init__.py#L7-L18)
- [fftai_gr1t1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/fftai_gr1t1/__init__.py#L11-L22)
- [magiclab_magicbot_gen1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/magiclab_magicbot_gen1/__init__.py#L11-L23)
- [openloong_loong/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/openloong_loong/__init__.py#L11-L22)
- [roboparty_atom01/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/roboparty_atom01/__init__.py#L11-L23)
- [robotera_xbot/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/robotera_xbot/__init__.py#L7-L18)

## Architecture Overview
The environment registration architecture connects standardized environment names to configuration classes through ManagerBasedRLEnv. The flow below illustrates how a gym.register() call maps to the RL training configuration and environment configuration classes.

```mermaid
sequenceDiagram
participant Reg as "Registration Script<br/>(.../humanoid/*/__init__.py)"
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
- [beyondmimic_g1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/beyondmimic/config/g1/__init__.py#L12-L19)
- [unitree_g1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/unitree_g1/__init__.py#L11-L23)

## Detailed Component Analysis

### Environment Naming Scheme Breakdown
- RobotLab-Isaac: Project and ecosystem prefix
- Velocity: Task type indicating locomotion policy training
- Flat/Rough: Terrain type for the environment
- Unitree/A1: Robot category and model
- v0: Version identifier

This scheme ensures uniqueness and discoverability across robots and terrains while keeping names concise and readable.

**Section sources**
- [README.md](file://README.md#L404-L415)

### Registration Pattern in Manager-Based Environments
Each humanoid configuration package registers one or more environments using gym.register(). The pattern includes:
- id: Standardized environment name following the naming scheme
- entry_point: "isaaclab.envs:ManagerBasedRLEnv"
- disable_env_checker: True
- kwargs:
  - env_cfg_entry_point: "{package}.flat_env_cfg:{ClassName}"
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

These registrations demonstrate consistent mapping between environment names and configuration classes.

**Section sources**
- [unitree_g1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/unitree_g1/__init__.py#L11-L23)
- [unitree_h1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/unitree_h1/__init__.py#L11-L22)
- [booster_t1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/booster_t1/__init__.py#L7-L18)
- [fftai_gr1t1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/fftai_gr1t1/__init__.py#L11-L22)
- [magiclab_magicbot_gen1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/magiclab_magicbot_gen1/__init__.py#L11-L23)
- [openloong_loong/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/openloong_loong/__init__.py#L11-L22)
- [roboparty_atom01/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/roboparty_atom01/__init__.py#L11-L23)
- [robotera_xbot/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/robotera_xbot/__init__.py#L7-L18)

### Relationship Between Names, Configuration Classes, and ManagerBasedRLEnv
- Environment Name: Determines the registry id used by gym.make()
- Configuration Classes:
  - Environment Config: Loaded via env_cfg_entry_point pointing to a class in the package’s flat_env_cfg module
  - RL Runner Config: Loaded via rsl_rl_cfg_entry_point pointing to a class in the package’s agents.rsl_rl_ppo_cfg module
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
ManagerBasedRLEnv --> EnvConfigClass : "loads via env_cfg_entry_point"
ManagerBasedRLEnv --> RLRunnerConfigClass : "loads via rsl_rl_cfg_entry_point"
```

**Diagram sources**
- [beyondmimic_g1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/beyondmimic/config/g1/__init__.py#L12-L19)
- [unitree_g1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/unitree_g1/__init__.py#L11-L23)

## Dependency Analysis
The registration system depends on:
- Gymnasium for environment registration and creation
- ManagerBasedRLEnv as the entry_point class
- Package-specific configuration modules for environment and RL runner settings

```mermaid
graph TB
Gymnasium["Gymnasium Library"]
RegScripts["Registration Scripts<br/>.../humanoid/*/__init__.py"]
EnvClass["ManagerBasedRLEnv<br/>(entry_point)"]
EnvCfg["Environment Config Modules<br/>.../flat_env_cfg.py"]
RLCfg["RL Runner Config Modules<br/>.../agents/rsl_rl_ppo_cfg.py"]
Gymnasium --> RegScripts
RegScripts --> EnvClass
EnvClass --> EnvCfg
EnvClass --> RLCfg
```

**Diagram sources**
- [beyondmimic_g1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/beyondmimic/config/g1/__init__.py#L12-L19)
- [unitree_g1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/unitree_g1/__init__.py#L11-L23)

**Section sources**
- [beyondmimic_g1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/beyondmimic/config/g1/__init__.py#L12-L19)
- [unitree_g1/__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/humanoid/unitree_g1/__init__.py#L11-L23)

## Performance Considerations
- Keep registration scripts lightweight; avoid heavy imports during import time.
- Use disable_env_checker=True to reduce overhead during registration.
- Centralize configuration loading to minimize repeated disk reads.
- Ensure environment and runner configuration classes are efficient and avoid unnecessary computations at initialization.

## Troubleshooting Guide
Common issues and resolutions:
- Environment name not found
  - Verify the exact name matches the registered id and includes the correct task type, terrain, robot category, model, and version.
  - Confirm the registration script is imported by the package initializer.
- Entry point resolution errors
  - Ensure entry_point is exactly "isaaclab.envs:ManagerBasedRLEnv".
  - Verify that the environment and RL runner configuration entry points resolve to existing classes in their respective modules.
- Configuration class not found
  - Check that env_cfg_entry_point and rsl_rl_cfg_entry_point point to valid modules and class names.
  - Confirm the modules exist and export the expected classes.
- Naming conflicts
  - Ensure unique ids across robots and terrains to avoid collisions.
  - Use the standardized naming scheme consistently to prevent ambiguity.
- Debugging techniques
  - List registered environments using a helper script to confirm registration.
  - Temporarily print or log configuration class names during registration to validate imports.
  - Test gym.make() with verbose logging to capture instantiation errors.

## Conclusion
The Robot Lab environment registration framework leverages a standardized naming scheme and consistent registration patterns to integrate Gymnasium environments with ManagerBasedRLEnv. By organizing configurations per robot family and terrain, the system achieves clarity, maintainability, and scalability across diverse robotic platforms. Following the documented patterns and troubleshooting steps ensures reliable environment setup and training workflows.