# Parkour Navigation System

<cite>
**Referenced Files in This Document**
- [rough_env_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/rough_env_cfg.py)
- [terrains_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/terrains_cfg.py)
- [mesh_terrains.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/mesh_terrains.py)
- [utils.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/utils.py)
- [observations.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/mdp/observations.py)
- [rewards.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/mdp/rewards.py)
- [rsl_rl_ppo_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/agents/rsl_rl_ppo_cfg.py)
- [actor_critic_scan.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/agents/actor_critic_scan.py)
- [unitree.py](file://source/robot_lab/robot_lab/assets/unitree.py)
- [rough_env_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1_parkour/rough_env_cfg.py)
- [rsl_rl_ppo_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1_parkour/agents/rsl_rl_ppo_cfg.py)
- [observations.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1_parkour/mdp/observations.py)
- [rewards.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1_parkour/mdp/rewards.py)
- [parkour_env_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/parkour_env_cfg.py)
- [README.md](file://README.md)
- [__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/__init__.py)
- [__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1_parkour/__init__.py)
- [__init__.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/__init__.py)
</cite>

## Update Summary
**Changes Made**
- Enhanced with standardized naming convention examples for Unitree Go2 and ZSIBOT ZSL1 parkour environments
- Updated environment registration to use RobotLab-Isaac-Velocity- prefixed environment names
- Added comprehensive environment listing with standardized naming patterns
- Integrated dual robot platform support with consistent naming conventions

## Table of Contents
1. [Introduction](#introduction)
2. [System Architecture](#system-architecture)
3. [Core Components](#core-components)
4. [Go2 Parkour Terrain Generation](#go2-parkour-terrain-generation)
5. [ZSL1 Parkour Implementation](#zsl1-parkour-implementation)
6. [Advanced Neural Network Architecture](#advanced-neural-network-architecture)
7. [Enhanced Reward System Design](#enhanced-reward-system-design)
8. [Robot Configuration](#robot-configuration)
9. [Training Configuration](#training-configuration)
10. [Environment Naming Convention](#environment-naming-convention)
11. [Environment Registration Examples](#environment-registration-examples)
12. [Performance Considerations](#performance-considerations)
13. [Troubleshooting Guide](#troubleshooting-guide)
14. [Conclusion](#conclusion)

## Introduction

The Parkour Navigation System has undergone a comprehensive enhancement to provide a dual-platform implementation supporting both Unitree Go2 and ZSIBOT ZSL1 quadruped robots. This advanced system represents a significant evolution from the previous ZSL1-focused approach, now offering sophisticated parkour capabilities for multiple robot platforms with custom neural networks, advanced terrain generation, and specialized reward systems.

The system leverages NVIDIA's Isaac Lab platform with a modular architecture that combines advanced terrain generation algorithms, custom neural network architectures, and reward shaping techniques. The new implementation focuses on parkour-style navigation capabilities including obstacle negotiation, step climbing, gap traversal, and complex terrain adaptation across both robot platforms.

**Updated** Enhanced with standardized naming convention examples for Unitree Go2 and ZSIBOT ZSL1 parkour environments. The system now uses consistent RobotLab-Isaac-Velocity- prefixed environment names for improved organization and discoverability.

## System Architecture

The dual-platform Parkour System follows a modernized modular architecture built around the Isaac Lab framework, providing comprehensive solutions for advanced quadruped parkour navigation across multiple robot platforms:

```mermaid
graph TB
subgraph "Dual Platform Architecture"
Go2Platform[Go2 Platform]
ZSL1Platform[ZSL1 Platform]
EndEffector[End Effector Control]
EndEffector --> Go2Platform
EndEffector --> ZSL1Platform
end
subgraph "User Interface Layer"
CLI[Command Line Interface]
GUI[Graphical Interface]
PlayMode[Play Mode Interface]
end
subgraph "Environment Layer"
EnvCfg[Environment Configuration]
TerrainGen[Advanced Terrain Generator]
Physics[Physics Engine]
MeshGen[Mesh Generation System]
end
subgraph "Robot Layer"
Go2Robot[Go2 Robot Configuration]
ZSL1Robot[ZSL1 Robot Configuration]
Sensors[Sensors & Actuators]
Control[Control System]
DR[Domain Randomization]
end
subgraph "ML Layer"
MDP[MDP Framework]
Rewards[Enhanced Reward System]
Policy[Custom Neural Network]
ScanEnc[Scan Encoder]
PrivEnc[Privileged Encoder]
end
subgraph "Training Layer"
Trainer[Training Engine]
Optimizer[Optimizer]
Logger[Logging System]
Ablation[Ablation Studies]
end
CLI --> EnvCfg
EnvCfg --> TerrainGen
EnvCfg --> Physics
EnvCfg --> MeshGen
Physics --> Go2Robot
Physics --> ZSL1Robot
Go2Robot --> Sensors
ZSL1Robot --> Sensors
Sensors --> MDP
MDP --> Rewards
MDP --> Policy
Policy --> ScanEnc
Policy --> PrivEnc
PrivEnc --> Trainer
ScanEnc --> Trainer
Trainer --> Optimizer
Optimizer --> Logger
Logger --> PlayMode
PlayMode --> Ablation
```

**Diagram sources**
- [rough_env_cfg.py:448-502](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/rough_env_cfg.py#L448-L502)
- [rsl_rl_ppo_cfg.py:128-193](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/agents/rsl_rl_ppo_cfg.py#L128-L193)

The architecture consists of several key layers with enhanced capabilities:

- **Dual Platform Support**: Advanced terrain generation with mesh-based algorithms and domain randomization for both Go2 and ZSL1 robots
- **Robot Layer**: Platform-specific configurations with enhanced sensor integration and actuator control
- **ML Layer**: Custom neural network architecture with separate encoders for different observation types
- **Training Layer**: Comprehensive training framework with ablation studies and performance monitoring

## Core Components

### Advanced Environment Configuration System

The system utilizes a sophisticated hierarchical configuration approach with enhanced modularity and dual-platform support:

```mermaid
classDiagram
class DualParkourEnvCfg {
+scene : DualParkourSceneCfg
+observations : DualParkourObservationsCfg
+actions : DualParkourActionsCfg
+commands : DualParkourCommandsCfg
+rewards : DualParkourRewardsCfg
+terminations : DualParkourTerminationsCfg
+events : DualParkourEventCfg
+curriculum : DualParkourCurriculumCfg
+__post_init__()
}
class DualParkourSceneCfg {
+terrain : TerrainImporterCfg
+go2_robot : ArticulationCfg
+zsibot_robot : ArticulationCfg
+height_scanner : RayCasterCfg
+contact_forces : ContactSensorCfg
+sky_light : AssetBaseCfg
}
class MeshParkourStepTerrainCfg {
+function : callable
+start_platform_length : float
+step_height_range : tuple[float, float]
+step_length_base_range : tuple[float, float]
+steps : int
}
class ActorCriticScan {
+num_actor_obs : int
+num_critic_obs : int
+scan_encoder : nn.Module
+priv_encoder : nn.Module
+actor : nn.Sequential
+critic : nn.Sequential
}
DualParkourEnvCfg --> DualParkourSceneCfg
DualParkourSceneCfg --> MeshParkourStepTerrainCfg
DualParkourEnvCfg --> ActorCriticScan
```

**Diagram sources**
- [rough_env_cfg.py:448-502](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/rough_env_cfg.py#L448-L502)
- [rsl_rl_ppo_cfg.py:30-120](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/agents/rsl_rl_ppo_cfg.py#L30-L120)

**Section sources**
- [rough_env_cfg.py:448-502](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/rough_env_cfg.py#L448-L502)
- [rsl_rl_ppo_cfg.py:30-120](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/agents/rsl_rl_ppo_cfg.py#L30-L120)

### Enhanced Observation and Action Spaces

The system defines sophisticated observation and action spaces with custom neural network integration for both platforms:

```mermaid
flowchart TD
Start([Environment Reset]) --> SensorReadings[Sensor Data Collection]
SensorReadings --> Proprioception[Proprioceptive Data]
SensorReadings --> HeightScan[Height Scan Data]
SensorReadings --> PrivilegedObs[Privileged Observations]
Proprioception --> ScanEncoder[Scan Encoder]
HeightScan --> ScanEncoder
PrivilegedObs --> PrivEncoder[Privileged Encoder]
ScanEncoder --> ActorInput[Actor Input]
PrivEncoder --> CriticInput[Critic Input]
ActorInput --> Policy[Custom Neural Network]
CriticInput --> ValueNetwork[Value Network]
Policy --> Action[Action Selection]
ValueNetwork --> ValueOutput[Value Output]
Action --> Environment[Environment Update]
ValueOutput --> NextStep[Next Simulation Step]
```

**Diagram sources**
- [rough_env_cfg.py:207-288](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/rough_env_cfg.py#L207-L288)
- [actor_critic_scan.py:20-146](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/agents/actor_critic_scan.py#L20-L146)

**Section sources**
- [rough_env_cfg.py:207-288](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/rough_env_cfg.py#L207-L288)
- [actor_critic_scan.py:20-146](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/agents/actor_critic_scan.py#L20-L146)

## Go2 Parkour Terrain Generation

The Go2 terrain generation system creates sophisticated and challenging environments for Go2 parkour training:

### Advanced Mesh-Based Terrain Generation

The system generates complex terrains using advanced mesh generation algorithms with customizable parameters:

```mermaid
flowchart TD
TerrainStart([Advanced Terrain Generation]) --> MeshConfig[Load Mesh Configuration]
MeshConfig --> GenerateType{Generate Terrain Type}
GenerateType --> |Parkour Step| ParkourGen[Parkour Step Generation]
GenerateType --> |Gap Strip| GapGen[Gap Strip Generation]
GenerateType --> |Hurdle Strip| HurdleGen[Hurdle Strip Generation]
GenerateType --> |Stairs Strip| StairsGen[Stairs Strip Generation]
GenerateType --> |Debris Field| DebrisGen[Debris Field Generation]
ParkourGen --> MeshProcessing[Mesh Processing]
GapGen --> MeshProcessing
HurdleGen --> MeshProcessing
StairsGen --> MeshProcessing
DebrisGen --> MeshProcessing
MeshProcessing --> CombineMesh[Combine Meshes]
CombineMesh --> FinalizeTerrain[Finalize Terrain]
FinalizeTerrain --> ReturnMesh[Return Mesh List]
```

**Diagram sources**
- [mesh_terrains.py:749-800](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/mesh_terrains.py#L749-L800)
- [terrains_cfg.py:194-208](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/terrains_cfg.py#L194-L208)

The terrain generation algorithm creates diverse parkour environments with configurable parameters:

- **Parkour Step Terrain**: Variable height and length ranges for realistic obstacle progression
- **Gap Strip Terrain**: Repeated gap-and-landing sequences for landing precision training
- **Hurdle Strip Terrain**: Series of hurdles with configurable heights and spacing
- **Stairs Strip Terrain**: Up/down stair segments with customizable patterns
- **Debris Field Terrain**: Mixed box and cylinder obstacles for complex navigation

**Section sources**
- [mesh_terrains.py:749-800](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/mesh_terrains.py#L749-L800)
- [terrains_cfg.py:194-208](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/terrains_cfg.py#L194-L208)

### Enhanced Terrain Configuration System

The system provides comprehensive terrain configuration with advanced customization options:

```mermaid
classDiagram
class MeshParkourStepTerrainCfg {
+function : mesh_terrains.parkour_step_terrain
+start_platform_length : float
+step_height_range : tuple[float, float]
+step_length_base_range : tuple[float, float]
+steps : int
}
class MeshGapStripTerrainCfg {
+function : mesh_terrains.gap_strip_terrain
+gap_width_range : tuple[float, float]
+landing_length : float
+start_platform_length : float
}
class MeshHurdleStripTerrainCfg {
+function : mesh_terrains.hurdle_strip_terrain
+hurdle_height_range : tuple[float, float]
+hurdle_thickness : float
+hurdle_gap_range : tuple[float, float]
+start_platform_length : float
}
class MeshStairsStripTerrainCfg {
+function : mesh_terrains.stairs_strip_terrain
+start_platform_length : float
+segment_length : float
+step_height_range : tuple[float, float]
+steps_per_segment : int
+pattern : tuple[str, ...]
}
class MeshDebrisTerrainCfg {
+function : mesh_terrains.debris_terrain
+num_debris_min : int
+num_debris_max : int
+ground_thickness : float
+box_length_range : tuple[float, float]
+box_width_range : tuple[float, float]
+box_thickness_range : tuple[float, float]
+cyl_radius_range : tuple[float, float]
+cyl_length_range : tuple[float, float]
}
MeshParkourStepTerrainCfg --> MeshParkourStepTerrainCfg
MeshGapStripTerrainCfg --> MeshGapStripTerrainCfg
MeshHurdleStripTerrainCfg --> MeshHurdleStripTerrainCfg
MeshStairsStripTerrainCfg --> MeshStairsStripTerrainCfg
MeshDebrisTerrainCfg --> MeshDebrisTerrainCfg
```

**Diagram sources**
- [terrains_cfg.py:194-315](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/terrains_cfg.py#L194-L315)

**Section sources**
- [terrains_cfg.py:194-315](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/terrains_cfg.py#L194-L315)

## ZSL1 Parkour Implementation

The ZSL1 implementation provides specialized parkour capabilities tailored for the ZSIBOT ZSL1 robot platform:

### Custom ZSL1 Terrain Generation

The ZSL1 system features unique terrain configurations optimized for the ZSL1 robot's capabilities:

```mermaid
flowchart TD
ZSL1Start([ZSL1 Terrain Generation]) --> ZSL1Config[Load ZSL1 Configuration]
ZSL1Config --> ZSL1GenerateType{Generate ZSL1 Terrain Type}
ZSL1GenerateType --> |Simple Parkour Step| SimpleParkourGen[Simple Parkour Step Generation]
ZSL1GenerateType --> |Custom Parkour Step| CustomParkourGen[Custom Parkour Step Generation]
SimpleParkourGen --> ZSL1MeshProcessing[Mesh Processing]
CustomParkourGen --> ZSL1MeshProcessing
ZSL1MeshProcessing --> ZSL1CombineMesh[Combine Meshes]
ZSL1CombineMesh --> ZSL1FinalizeTerrain[Finalize Terrain]
ZSL1FinalizeTerrain --> ZSL1ReturnMesh[Return Mesh List]
```

**Diagram sources**
- [parkour_env_cfg.py:26-208](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/parkour_env_cfg.py#L26-L208)

The ZSL1 terrain generation includes specialized configurations:

- **Simple Parkour Step**: Optimized for controlled stepping with reduced complexity
- **Custom Parkour Step**: Advanced configuration with enhanced step parameters
- **Parkour Terrains Configuration**: Custom terrain generator with specific proportions and parameters

**Section sources**
- [parkour_env_cfg.py:26-208](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/parkour_env_cfg.py#L26-L208)

### ZSL1-Specific Reward System

The ZSL1 reward system includes specialized functions optimized for ZSL1 parkour performance:

#### Climbing Progress Reward

The climbing progress reward encourages controlled ascent and descent movements:

```mermaid
flowchart TD
Start([Calculate Climbing Progress]) --> GetBasePos[Extract Base Position]
GetBasePos --> GetTargetPos[Extract Target Position]
GetTargetPos --> CalcDistance[Calculate Distance]
CalcDistance --> CalcProgress[Calculate Progress Ratio]
CalcProgress --> ApplyWeights[Apply Alignment and Forward Weights]
ApplyWeights --> End([Return Climbing Progress Reward])
```

**Diagram sources**
- [parkour_env_cfg.py:410-414](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/parkour_env_cfg.py#L410-L414)

#### Joint Mirror Reward

Advanced joint mirroring prevents asymmetrical movement patterns:

```mermaid
flowchart TD
Start([Check Joint Mirroring]) --> GetJointPos[Extract Joint Positions]
GetJointPos --> GetMirrorPairs[Identify Mirror Joint Pairs]
GetMirrorPairs --> CalcDiff[Calculate Position Differences]
CalcDiff --> CompareThreshold[Compare Against Threshold]
CompareThreshold --> |Within Threshold| NoPenalty[No Penalty]
CompareThreshold --> |Exceeds Threshold| ApplyPenalty[Apply Mirror Penalty]
NoPenalty --> End([Return Joint Mirror Reward])
ApplyPenalty --> End
```

**Diagram sources**
- [parkour_env_cfg.py:362-366](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/parkour_env_cfg.py#L362-L366)

**Section sources**
- [parkour_env_cfg.py:410-414](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/parkour_env_cfg.py#L410-L414)
- [parkour_env_cfg.py:362-366](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/parkour_env_cfg.py#L362-L366)

## Advanced Neural Network Architecture

The system implements custom neural network architectures specifically designed for both Go2 and ZSL1 parkour navigation:

### Actor-Critic with Scan and Privileged Encoders

```mermaid
classDiagram
class ActorCriticScan {
+num_actor_obs : int
+num_critic_obs : int
+actor_scan_encoder : nn.Module
+critic_scan_encoder : nn.Module
+priv_encoder : nn.Module
+actor : nn.Sequential
+critic : nn.Sequential
+noise_std_type : str
+std : nn.Parameter
+log_std : nn.Parameter
}
class ScanEncoder {
+input_dim : int
+hidden_dims : list[int]
+activation : nn.Module
+layers : nn.Sequential
}
class PrivEncoder {
+input_dim : int
+hidden_dims : list[int]
+activation : nn.Module
+layers : nn.Sequential
}
class ActorNetwork {
+input_dim : int
+hidden_dims : list[int]
+output_dim : int
+layers : nn.Sequential
}
class CriticNetwork {
+input_dim : int
+hidden_dims : list[int]
+output_dim : int
+layers : nn.Sequential
}
ActorCriticScan --> ScanEncoder
ActorCriticScan --> PrivEncoder
ActorCriticScan --> ActorNetwork
ActorCriticScan --> CriticNetwork
```

**Diagram sources**
- [actor_critic_scan.py:20-146](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/agents/actor_critic_scan.py#L20-L146)
- [rsl_rl_ppo_cfg.py:30-120](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/agents/rsl_rl_ppo_cfg.py#L30-L120)

The neural network architecture features:

- **Separate Encoders**: Dedicated encoders for scan observations and privileged observations
- **Flexible Architecture**: Configurable hidden dimensions and activation functions
- **Dual Policy**: Separate actor and critic networks with shared observation processing
- **Noise Parameterization**: Support for both scalar and log-standard deviation parameterization

**Section sources**
- [actor_critic_scan.py:20-146](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/agents/actor_critic_scan.py#L20-L146)
- [rsl_rl_ppo_cfg.py:30-120](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/agents/rsl_rl_ppo_cfg.py#L30-L120)

### Custom Observation Processing Pipeline

The system processes different observation types through specialized encoders:

```mermaid
sequenceDiagram
participant Obs as Raw Observations
participant PropEnc as Proprioceptive Encoder
participant ScanEnc as Scan Encoder
participant PrivEnc as Privileged Encoder
participant Actor as Actor Network
participant Critic as Critic Network
Obs->>PropEnc : Process proprioceptive data
Obs->>ScanEnc : Process scan data
Obs->>PrivEnc : Process privileged data
PropEnc-->>Actor : Encoded proprioceptive
ScanEnc-->>Actor : Encoded scan
PropEnc-->>Critic : Encoded proprioceptive
PrivEnc-->>Critic : Encoded privileged
Actor-->>Actor : Generate action distribution
Critic-->>Critic : Evaluate state value
```

**Diagram sources**
- [actor_critic_scan.py:178-231](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/agents/actor_critic_scan.py#L178-L231)

**Section sources**
- [actor_critic_scan.py:178-231](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/agents/actor_critic_scan.py#L178-L231)

## Enhanced Reward System Design

The reward system employs sophisticated shaping techniques with platform-specific parkour metrics:

### Advanced Reward Function Architecture

```mermaid
classDiagram
class DualParkourRewardsCfg {
+track_lin_vel_xy_exp : RewTerm
+track_ang_vel_z_exp : RewTerm
+lin_vel_z_l2 : RewTerm
+ang_vel_xy_l2 : RewTerm
+dof_torques_l2 : RewTerm
+dof_acc_l2 : RewTerm
+action_rate_l2 : RewTerm
+feet_air_time : RewTerm
+undesired_contacts : RewTerm
+flat_orientation_l2 : RewTerm
+base_height : RewTerm
+torque_sum : RewTerm
+stop_penalty_lin : RewTerm
+stop_penalty_ang : RewTerm
+hip_pos : RewTerm
+feet_stumble : RewTerm
+dof_close_to_default : RewTerm
+work : RewTerm
+climbing_progress : RewTerm
+feet_height_body : RewTerm
+feet_gait : RewTerm
+feet_slide : RewTerm
+feet_contact_without_cmd : RewTerm
+stand_still : RewTerm
+joint_pos_limits : RewTerm
+joint_power : RewTerm
+joint_mirror : RewTerm
}
class CustomParkourRewards {
+torque_sum : torque_sum
+stop_penalty_lin : stop_penalty_lin
+stop_penalty_ang : stop_penalty_ang
+hip_pos_l2 : hip_pos_l2
+feet_stumble : feet_stumble
+joint_deviation_l2 : joint_deviation_l2
+mechanical_work : mechanical_work
+climbing_progress : climbing_progress
+feet_height_body : feet_height_body
+feet_gait : feet_gait
+feet_slide : feet_slide
+feet_contact_without_cmd : feet_contact_without_cmd
+stand_still : stand_still
+joint_pos_limits : joint_pos_limits
+joint_power : joint_power
+joint_mirror : joint_mirror
}
DualParkourRewardsCfg --> CustomParkourRewards
```

**Diagram sources**
- [rough_env_cfg.py:367-423](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/rough_env_cfg.py#L367-L423)
- [rewards.py:24-32](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/mdp/rewards.py#L24-L32)

### Platform-Specific Reward Functions

The reward system includes specialized functions optimized for each platform's parkour performance:

#### Mechanical Work Reward

The mechanical work reward encourages efficient energy usage during parkour maneuvers:

```mermaid
flowchart TD
Start([Calculate Mechanical Work]) --> GetTorque[Extract Applied Torque]
GetTorque --> GetJointVel[Extract Joint Velocities]
GetJointVel --> CalcPower[Calculate Power = Torque * Joint Vel]
CalcPower --> ClampPower[Clamp to Non-Negative Values]
ClampPower --> ScalePower[Scale by Time Step]
ScalePower --> End([Return Work Reward])
```

**Diagram sources**
- [rewards.py:119-131](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/mdp/rewards.py#L119-L131)

#### ZSL1 Joint Mirror Reward

Advanced joint mirroring prevents asymmetrical movement patterns specific to ZSL1:

```mermaid
flowchart TD
Start([Check Joint Mirroring]) --> GetJointPos[Extract Joint Positions]
GetJointPos --> GetMirrorPairs[Identify Mirror Joint Pairs]
GetMirrorPairs --> CalcDiff[Calculate Position Differences]
CalcDiff --> CompareThreshold[Compare Against Threshold]
CompareThreshold --> |Within Threshold| NoPenalty[No Penalty]
CompareThreshold --> |Exceeds Threshold| ApplyPenalty[Apply Mirror Penalty]
NoPenalty --> End([Return Joint Mirror Reward])
ApplyPenalty --> End
```

**Diagram sources**
- [parkour_env_cfg.py:362-366](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/parkour_env_cfg.py#L362-L366)

**Section sources**
- [rewards.py:119-131](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/mdp/rewards.py#L119-L131)
- [parkour_env_cfg.py:362-366](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/parkour_env_cfg.py#L362-L366)

## Robot Configuration

The system provides dual-platform configuration optimized for parkour performance:

### Unitree Go2 Configuration

The Unitree Go2 robot configuration includes specialized parameters for advanced parkour capabilities:

```mermaid
classDiagram
class UNITREE_GO2_CFG {
+spawn : UrdfFileCfg
+init_state : InitialStateCfg
+soft_joint_pos_limit_factor : float
+actuators : dict
}
class DCMotorCfg {
+joint_names_expr : list[string]
+effort_limit : float
+saturation_effort : float
+velocity_limit : float
+stiffness : float
+damping : float
+friction : float
}
class InitialStateCfg {
+pos : tuple[float, float, float]
+joint_pos : dict
+joint_vel : dict
}
class ArticulationCfg {
+prim_path : string
+spawn : UrdfFileCfg
+init_state : InitialStateCfg
+soft_joint_pos_limit_factor : float
+actuators : dict
}
UNITREE_GO2_CFG --> ArticulationCfg
UNITREE_GO2_CFG --> DCMotorCfg
UNITREE_GO2_CFG --> InitialStateCfg
```

**Diagram sources**
- [unitree.py:71-117](file://source/robot_lab/robot_lab/assets/unitree.py#L71-L117)

### ZSIBOT ZSL1 Configuration

The ZSIBOT ZSL1 robot configuration includes specialized parameters optimized for controlled parkour:

```mermaid
classDiagram
class ZSIBOT_ZSL1_CFG {
+spawn : UrdfFileCfg
+init_state : InitialStateCfg
+soft_joint_pos_limit_factor : float
+actuators : dict
}
class ZSL1DCMotorCfg {
+joint_names_expr : list[string]
+effort_limit : float
+saturation_effort : float
+velocity_limit : float
+stiffness : float
+damping : float
+friction : float
}
class ZSL1InitialStateCfg {
+pos : tuple[float, float, float]
+joint_pos : dict
+joint_vel : dict
}
class ZSL1ArticulationCfg {
+prim_path : string
+spawn : UrdfFileCfg
+init_state : InitialStateCfg
+soft_joint_pos_limit_factor : float
+actuators : dict
}
ZSIBOT_ZSL1_CFG --> ZSL1ArticulationCfg
ZSIBOT_ZSL1_CFG --> ZSL1DCMotorCfg
ZSIBOT_ZSL1_CFG --> ZSL1InitialStateCfg
```

**Diagram sources**
- [parkour_env_cfg.py:14](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/parkour_env_cfg.py#L14)

Key configuration aspects include:

- **Enhanced Actuator Specifications**: Optimized for higher torque and faster response
- **Improved Joint Limits**: Configured for maximum range of motion required for parkour
- **Advanced Initial Pose**: Stable starting position with appropriate joint angles
- **Optimized Physical Properties**: Mass and damping characteristics for superior agility

**Section sources**
- [unitree.py:71-117](file://source/robot_lab/robot_lab/assets/unitree.py#L71-L117)
- [parkour_env_cfg.py:14](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/parkour_env_cfg.py#L14)

## Training Configuration

The training system provides comprehensive configuration options for both robot platforms:

### Environment Variants

The system registers multiple environment variants with specialized configurations for each platform:

| Environment Type | Configuration File | Key Features |
|------------------|-------------------|--------------|
| Flat Terrain | `Go2ParkourFlatEnvCfg` / `ZSL1ParkourFlatEnvCfg` | Baseline locomotion training without height scan |
| Rough Terrain | `Go2ParkourRoughEnvCfg` / `ZSL1ParkourRoughEnvCfg` | Complex terrain adaptation with full observation |
| Play Mode | `Go2ParkourRoughPlayEnvCfg` / `ZSL1ParkourRoughPlayEnvCfg` | Evaluation and visualization mode |
| Ablation Studies | Multiple variants | Systematic analysis of observation types |

### Advanced Training Parameters

The training configuration includes sophisticated parameter tuning for optimal performance:

- **Custom Neural Networks**: Actor-Critic with separate scan and privileged encoders
- **Adaptive Learning Rates**: Configurable learning rate schedules and KL divergence control
- **Empirical Normalization**: Automatic normalization of observations and rewards
- **Ablation Study Support**: Multiple variants for systematic analysis of components

**Section sources**
- [rsl_rl_ppo_cfg.py:128-237](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/agents/rsl_rl_ppo_cfg.py#L128-L237)

## Environment Naming Convention

**Updated** The system now uses a standardized naming convention for all parkour environments, ensuring consistency across platforms and easy identification of environment variants.

### Standardized Naming Pattern

All environment IDs follow the RobotLab-Isaac-Velocity- prefixed naming convention:

```
RobotLab-Isaac-Velocity-{Platform}-{Task}-{Variant}-v0
```

Where:
- `{Platform}` = Go2, ZSL1, or other supported robots
- `{Task}` = Parkour, Flat, Rough, Gap, Stair, or other locomotion tasks
- `{Variant}` = Base variant or specific ablation study
- `-v0` = Version suffix

### Go2 Environment Naming Examples

| Environment ID | Description |
|----------------|-------------|
| `RobotLab-Isaac-Velocity-Go2-Parkour-Flat-v0` | Flat terrain parkour training for Go2 |
| `RobotLab-Isaac-Velocity-Go2-Parkour-Rough-v0` | Rough terrain parkour training for Go2 |
| `RobotLab-Isaac-Velocity-Go2-Parkour-Rough-Abl1-v0` | Go2 parkour with ablation study 1 |
| `RobotLab-Isaac-Velocity-Go2-Parkour-Rough-Abl2_5-v0` | Go2 parkour with scan-first ordering |
| `RobotLab-Isaac-Velocity-Go2-Parkour-Rough-Abl3_5-v0` | Go2 parkour with explicit scan encoder |
| `RobotLab-Isaac-Velocity-Go2-Parkour-Rough-Abl4_0-v0` | Go2 parkour with critic-only scan |
| `RobotLab-Isaac-Velocity-Go2-Parkour-Rough-Abl7_0-v0` | Go2 parkour with reduced privileged encoder |

### ZSL1 Environment Naming Examples

| Environment ID | Description |
|----------------|-------------|
| `RobotLab-Isaac-Velocity-ZSL1-Parkour-Flat-v0` | Flat terrain parkour training for ZSL1 |
| `RobotLab-Isaac-Velocity-ZSL1-Parkour-Rough-v0` | Rough terrain parkour training for ZSL1 |
| `RobotLab-Isaac-Velocity-ZSL1-Parkour-Rough-Abl1-v0` | ZSL1 parkour with ablation study 1 |
| `RobotLab-Isaac-Velocity-ZSL1-Parkour-Rough-Abl2_5-v0` | ZSL1 parkour with scan-first ordering |
| `RobotLab-Isaac-Velocity-ZSL1-Parkour-Rough-Abl3_5-v0` | ZSL1 parkour with explicit scan encoder |
| `RobotLab-Isaac-Velocity-ZSL1-Parkour-Rough-Abl4_0-v0` | ZSL1 parkour with critic-only scan |
| `RobotLab-Isaac-Velocity-ZSL1-Parkour-Rough-Abl7_0-v0` | ZSL1 parkour with reduced privileged encoder |

### Additional ZSL1 Task Environments

| Environment ID | Description |
|----------------|-------------|
| `RobotLab-Isaac-Velocity-Flat-Zsibot-ZSL1-v0` | Basic flat terrain training |
| `RobotLab-Isaac-Velocity-Rough-Zsibot-ZSL1-v0` | Basic rough terrain training |
| `RobotLab-Isaac-Velocity-Stair-Zsibot-ZSL1-v0` | Stair climbing training |
| `RobotLab-Isaac-Velocity-Parkour-Zsibot-ZSL1-v0` | Parkour-specific training |
| `RobotLab-Isaac-Velocity-Gap-Zsibot-ZSL1-v0` | Gap crossing training |
| `RobotLab-Isaac-Velocity-Rough-Abl3_5-Zsibot-ZSL1-v0` | ZSL1 gap training with ablation |

**Section sources**
- [__init__.py:21-161](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/__init__.py#L21-L161)
- [__init__.py:21-160](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1_parkour/__init__.py#L21-L160)
- [__init__.py:12-70](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/__init__.py#L12-L70)

## Environment Registration Examples

**Updated** The environment registration system now uses the standardized naming convention consistently across all parkour environments.

### Go2 Parkour Environment Registration

The Go2 parkour environments are registered with comprehensive ablation study support:

```python
# Flat terrain variants
gym.register(
    id="RobotLab-Isaac-Velocity-Go2-Parkour-Flat-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.rough_env_cfg:Go2ParkourFlatEnvCfg",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:Go2ParkourFlatPPORunnerCfg",
    },
)

# Rough terrain variants
gym.register(
    id="RobotLab-Isaac-Velocity-Go2-Parkour-Rough-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.rough_env_cfg:Go2ParkourRoughEnvCfg",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:Go2ParkourRoughPPORunnerCfg",
    },
)

# Ablation study variants
gym.register(
    id="RobotLab-Isaac-Velocity-Go2-Parkour-Rough-Abl1-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.rough_env_cfg:Go2ParkourRoughAbl1EnvCfg",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:Go2ParkourRoughAbl1PPORunnerCfg",
    },
)
```

### ZSL1 Parkour Environment Registration

The ZSL1 parkour environments follow the same standardized pattern:

```python
# Flat terrain variants
gym.register(
    id="RobotLab-Isaac-Velocity-ZSL1-Parkour-Flat-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.rough_env_cfg:ZSL1ParkourFlatEnvCfg",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:ZSL1ParkourFlatPPORunnerCfg",
    },
)

# Rough terrain variants
gym.register(
    id="RobotLab-Isaac-Velocity-ZSL1-Parkour-Rough-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.rough_env_cfg:ZSL1ParkourRoughEnvCfg",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:ZSL1ParkourRoughPPORunnerCfg",
    },
)

# Ablation study variants
gym.register(
    id="RobotLab-Isaac-Velocity-ZSL1-Parkour-Rough-Abl3_5-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.rough_env_cfg:ZSL1ParkourRoughEnvCfg",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:ZSL1ParkourRoughAbl3_5PPORunnerCfg",
    },
)
```

### Additional ZSL1 Task Environments

```python
# Basic locomotion environments
gym.register(
    id="RobotLab-Isaac-Velocity-Flat-Zsibot-ZSL1-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.flat_env_cfg:ZsibotZSL1FlatEnvCfg",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:ZsibotZSL1FlatPPORunnerCfg",
    },
)

# Specialized task environments
gym.register(
    id="RobotLab-Isaac-Velocity-Parkour-Zsibot-ZSL1-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.parkour_env_cfg:ZsibotZSL1ParkourEnvCfg",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:ZsibotZSL1ParkourPPORunnerCfg",
    },
)
```

**Section sources**
- [__init__.py:19-161](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/__init__.py#L19-L161)
- [__init__.py:19-160](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1_parkour/__init__.py#L19-L160)
- [__init__.py:12-70](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/zsibot_zsl1/__init__.py#L12-L70)

## Performance Considerations

The system incorporates several optimization strategies for efficient parkour operation across both platforms:

### Computational Efficiency

- **GPU Acceleration**: Leverages GPU computing for parallel neural network inference
- **Memory Management**: Optimized memory allocation for large-scale terrain generation
- **Real-time Processing**: Efficient algorithms for real-time command generation and response
- **Custom Network Architecture**: Specialized neural network design for reduced computational overhead

### Stability Enhancements

- **Advanced Contact Force Monitoring**: Real-time contact force analysis for stability assessment
- **Enhanced Upright Orientation Control**: Maintains robot stability during aggressive maneuvers
- **Energy Efficiency Optimization**: Optimized joint power consumption for extended operation
- **Domain Randomization**: Systematic variation of physical properties for robust generalization

### Scalability Features

- **Modular Terrain Generation**: Configurable environment sizes and complexities
- **Distributed Training Support**: Multi-GPU and distributed training capabilities
- **Extensible Architecture**: Modular design for adding new terrain types and robot models
- **Ablation Study Framework**: Comprehensive analysis capabilities for system optimization

## Troubleshooting Guide

Common issues and their solutions for the dual-platform parkour system:

### Training Instability

**Symptoms**: Unstable training curves, frequent falls, poor convergence
**Solutions**:
- Adjust reward scaling factors for better balance
- Modify action clipping ranges for safer exploration
- Increase terrain difficulty gradually
- Verify sensor configuration accuracy
- Check neural network architecture compatibility

### Robot Behavior Issues

**Symptoms**: Inconsistent obstacle negotiation, poor foothold selection
**Solutions**:
- Calibrate sensor heights and field of view
- Adjust joint position scales for better reach
- Modify contact force thresholds
- Review terrain generation parameters
- Verify domain randomization settings

### Performance Problems

**Symptoms**: Slow simulation speeds, memory leaks, rendering issues
**Solutions**:
- Optimize environment complexity for available hardware
- Adjust physics simulation parameters
- Monitor GPU utilization and memory usage
- Clear temporary simulation caches regularly
- Check neural network memory usage

### Neural Network Issues

**Symptoms**: Poor policy performance, training divergence
**Solutions**:
- Verify observation dimension compatibility
- Check scan encoder configuration
- Adjust learning rate and KL divergence parameters
- Review privileged observation processing
- Validate custom reward function implementation

### Environment Registration Issues

**Symptoms**: Environment not found errors, incorrect naming
**Solutions**:
- Verify environment ID matches registration pattern
- Check module import paths in gym.register kwargs
- Ensure environment configuration files exist
- Validate version suffix (-v0) in environment IDs
- Confirm proper namespace usage in prim_path fields

## Conclusion

The enhanced Parkour Navigation System represents a comprehensive and sophisticated solution for advanced quadruped locomotion capabilities across multiple robot platforms. The transition from ZSL1-focused to dual-platform implementation provides significantly enhanced parkour navigation abilities through custom neural networks, advanced terrain generation, and specialized reward systems.

The system leverages NVIDIA's Isaac Lab platform with a modular architecture that combines advanced terrain generation algorithms, custom neural network architectures, and reward shaping techniques. The new implementation focuses on parkour-style navigation capabilities including obstacle negotiation, step climbing, gap traversal, and complex terrain adaptation across both robot platforms.

**Updated** The standardized naming convention ensures consistent environment identification and easy integration with the broader Isaac Lab ecosystem. The RobotLab-Isaac-Velocity- prefixed environment names provide clear categorization and improve discoverability across different robot platforms and task variants.

The modular architecture ensures extensibility for different robot platforms and application scenarios, while the comprehensive training framework supports rapid deployment and optimization. The system's focus on safety, stability, and performance makes it suitable for real-world applications in search and rescue, industrial inspection, and autonomous exploration missions.

The custom neural network architecture with separate scan and privileged encoders, combined with advanced terrain generation algorithms, provides unprecedented capabilities for complex parkour navigation. The systematic approach to ablation studies and performance analysis ensures continuous improvement and optimization of the system's capabilities across both Go2 and ZSL1 platforms.

Future enhancements could include expanded terrain types, multi-robot coordination capabilities, and integration with advanced perception systems for even more sophisticated navigation scenarios.