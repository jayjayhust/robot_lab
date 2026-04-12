# Unitree Go2 Series

<cite>
**Referenced Files in This Document**
- [README.md](file://README.md)
- [unitree.py](file://source/robot_lab/robot_lab/assets/unitree.py)
- [go2_description.urdf](file://source/robot_lab/data/Robots/unitree/go2_description/urdf/go2_description.urdf)
- [go2w_description.urdf](file://source/robot_lab/data/Robots/unitree/go2w_description/urdf/go2w_description.urdf)
- [flat_env_cfg.py (Go2 Flat)](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2/flat_env_cfg.py)
- [rough_env_cfg.go2](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2/rough_env_cfg.py)
- [flat_env_cfg.py (Go2W Flat)](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/wheeled/unitree_go2w/flat_env_cfg.py)
- [rough_env_cfg.go2w](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/wheeled/unitree_go2w/rough_env_cfg.py)
- [actor_critic_scan.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/agents/actor_critic_scan.py)
- [rsl_rl_ppo_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/agents/rsl_rl_ppo_cfg.py)
- [observations.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/mdp/observations.py)
- [rewards.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/mdp/rewards.py)
- [terrains_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/terrains_cfg.py)
- [mesh_terrains.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/mesh_terrains.py)
- [utils.py](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/utils.py)
</cite>

## Update Summary
**Changes Made**
- Enhanced Go2 parkour configuration with new terrain-level curriculum support
- Improved observation system documentation with comprehensive comments explaining dimensional characteristics
- Added enhanced curriculum parameter specifications for terrain generation
- Documented new terrain types with curriculum-based difficulty progression
- Updated neural network architecture documentation with detailed observation dimension explanations

## Table of Contents
1. [Introduction](#introduction)
2. [Project Structure](#project-structure)
3. [Core Components](#core-components)
4. [Architecture Overview](#architecture-overview)
5. [Detailed Component Analysis](#detailed-component-analysis)
6. [Go2 Parkour Training System](#go2-parkour-training-system)
7. [Enhanced Terrain Curriculum System](#enhanced-terrain-curriculum-system)
8. [Improved Observation System](#improved-observation-system)
9. [Dependency Analysis](#dependency-analysis)
10. [Performance Considerations](#performance-considerations)
11. [Troubleshooting Guide](#troubleshooting-guide)
12. [Conclusion](#conclusion)
13. [Appendices](#appendices)

## Introduction
This document provides comprehensive technical documentation for the Unitree Go2 series, covering both the standard quadruped Go2 and the wheeled Go2W variants. It explains motor configurations, actuator distributions, joint setups, initial poses, simulation parameters, and environment configurations used in reinforcement learning tasks. The document now includes the newly enhanced Go2 parkour training system with advanced neural network architecture, terrain-level curriculum support, and improved observation system documentation with detailed dimensional characteristics explanations. It also compares the two variants and offers selection guidance based on terrain and mobility requirements.

## Project Structure
The repository integrates the Go2 and Go2W robots into the Isaac Lab ecosystem. The robot assets and URDF definitions are located under the data directory, while the robot configurations and environment setups are defined in the assets and task configuration modules. The enhanced Go2 parkour system is organized as a self-contained package with custom RL configuration, advanced neural network architecture, and comprehensive terrain generation capabilities with curriculum support.

```mermaid
graph TB
subgraph "Assets"
UCFG["unitree.py<br/>Robot configurations"]
end
subgraph "URDF Models"
GO2["go2_description.urdf"]
GO2W["go2w_description.urdf"]
end
subgraph "Environments"
QGO2["Quadruped Go2 Configs"]
WGO2W["Wheeled Go2W Configs"]
GOPARKOUR["Go2 Parkour System"]
end
subgraph "Enhanced Parkour Components"
ACTNET["ActorCriticScan<br/>Custom NN Architecture"]
TERRAINS["Enhanced Terrain<br/>Curriculum System"]
MDP["Improved MDP<br/>Observations & Rewards"]
CURRICULUM["Terrain-Level<br/>Curriculum Support"]
end
UCFG --> GO2
UCFG --> GO2W
GO2 --> QGO2
GO2W --> WGO2W
GOPARKOUR --> ACTNET
GOPARKOUR --> TERRAINS
GOPARKOUR --> MDP
GOPARKOUR --> CURRICULUM
```

**Diagram sources**
- [unitree.py:71-177](file://source/robot_lab/robot_lab/assets/unitree.py#L71-L177)
- [go2_description.urdf:1-761](file://source/robot_lab/data/Robots/unitree/go2_description/urdf/go2_description.urdf#L1-L761)
- [go2w_description.urdf:1-764](file://source/robot_lab/data/Robots/unitree/go2w_description/urdf/go2w_description.urdf#L1-L764)
- [actor_critic_scan.py:20-133](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/agents/actor_critic_scan.py#L20-L133)
- [terrains_cfg.py:22-384](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/terrains_cfg.py#L22-L384)

**Section sources**
- [README.md:18-31](file://README.md#L18-L31)
- [unitree.py:71-177](file://source/robot_lab/robot_lab/assets/unitree.py#L71-L177)

## Core Components
- Robot configurations:
  - Standard Go2: Uses DCMotorCfg for all leg joints.
  - Go2W: Uses ImplicitActuatorCfg for legs and ImplicitActuatorCfg for wheels.
- Simulation parameters:
  - Effort limits, velocity limits, stiffness, and damping are defined per actuator group.
  - Initial heights differ between variants (Go2: 0.38 m; Go2W: 0.45 m).
- Environment configurations:
  - Separate flat and rough environments for both variants.
  - Observation/action scaling and reward shaping tuned for locomotion tasks.
- **Enhanced**: Go2 Parkour System:
  - Custom ActorCriticScan neural network with scan and privileged observation encoders.
  - Advanced terrain generation with 15+ different terrain types and curriculum-based difficulty progression.
  - Specialized MDP observations and rewards for parkour training with detailed dimensional characteristics.
  - Enhanced curriculum parameter specifications for terrain generation.

**Section sources**
- [unitree.py:107-116](file://source/robot_lab/robot_lab/assets/unitree.py#L107-L116)
- [unitree.py:157-174](file://source/robot_lab/robot_lab/assets/unitree.py#L157-L174)
- [actor_critic_scan.py:20-133](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/agents/actor_critic_scan.py#L20-L133)
- [terrains_cfg.py:22-384](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/terrains_cfg.py#L22-L384)

## Architecture Overview
The system architecture connects environment configurations to robot assets and actuators. The environment defines observations, actions, rewards, and terminations, while the assets module provides robot-specific configurations and URDF definitions. The enhanced Go2 parkour system introduces a self-contained package with custom RL configuration, advanced neural network architecture, and comprehensive terrain generation capabilities with curriculum support.

```mermaid
graph TB
Env["Environment Configs<br/>Go2 Flat/Rough & Go2W Flat/Rough"]
Parkour["Enhanced Go2 Parkour System<br/>Custom RL Package"]
Assets["Robot Assets<br/>unitree.py"]
URDF["URDF Models<br/>go2/go2w"]
NN["ActorCriticScan<br/>Neural Network"]
Terrains["Enhanced Terrains<br/>15+ Types with Curriculum"]
MDP["Improved MDP<br/>Observations & Rewards"]
Curriculum["Terrain-Level<br/>Curriculum Support"]
Env --> Assets
Assets --> URDF
Parkour --> NN
Parkour --> Terrains
Parkour --> MDP
Parkour --> Curriculum
```

**Diagram sources**
- [rough_env_cfg.go2:34-35](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2/rough_env_cfg.py#L34-L35)
- [rough_env_cfg.go2w:76-77](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/wheeled/unitree_go2w/rough_env_cfg.py#L76-L77)
- [unitree.py:71-177](file://source/robot_lab/robot_lab/assets/unitree.py#L71-L177)
- [rsl_rl_ppo_cfg.py:128-193](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/agents/rsl_rl_ppo_cfg.py#L128-L193)

## Detailed Component Analysis

### DC Motor Configuration (Go2)
- Actuator type: DCMotorCfg applied to all leg joints.
- Limits:
  - Effort limit: 23.5 Nm
  - Velocity limit: 30.0 rad/s
  - Stiffness: 25.0 Nm/rad
  - Damping: 0.5 Nm/rad/s
- Initial pose:
  - Base position Z: 0.38 m
  - Joint positions: hip ~0, thigh ~0.8, calf ~-1.5

```mermaid
classDiagram
class DCMotorCfg {
+effort_limit : 23.5 Nm
+velocity_limit : 30.0 rad/s
+stiffness : 25.0 Nm/rad
+damping : 0.5 Nm/rad/s
}
class Go2Legs {
+joint_names_expr : ".*"
+initial_height : 0.38 m
}
Go2Legs --> DCMotorCfg : "uses"
```

**Diagram sources**
- [unitree.py:107-116](file://source/robot_lab/robot_lab/assets/unitree.py#L107-L116)

**Section sources**
- [unitree.py:107-116](file://source/robot_lab/robot_lab/assets/unitree.py#L107-L116)
- [go2_description.urdf:79-84](file://source/robot_lab/data/Robots/unitree/go2_description/urdf/go2_description.urdf#L79-L84)

### Wheeled Actuator Distribution (Go2W)
- Actuator groups:
  - Legs: ImplicitActuatorCfg with identical limits to Go2 motors.
  - Wheels: ImplicitActuatorCfg with zero stiffness and nonzero damping.
- Joint configuration:
  - Foot joints are continuous (rotational) and named *_foot_joint.
- Initial pose:
  - Base position Z: 0.45 m
  - Includes *_foot_joint in initial joint positions.

```mermaid
classDiagram
class ImplicitActuatorCfg {
+effort_limit_sim : 23.5 Nm
+velocity_limit_sim : 30.0 rad/s
+stiffness : 25.0 Nm/rad (legs)<br/>0.0 Nm/rad (wheels)
+damping : 0.5 Nm/rad/s
}
class Go2WLegs {
+joint_names_expr : ^(?!.*_foot_joint).*
+initial_height : 0.45 m
}
class Go2WWheels {
+joint_names_expr : .*_foot_joint
+initial_joint_pos : 0.0
}
Go2WLegs --> ImplicitActuatorCfg : "uses"
Go2WWheels --> ImplicitActuatorCfg : "uses"
```

**Diagram sources**
- [unitree.py:157-174](file://source/robot_lab/robot_lab/assets/unitree.py#L157-L174)

**Section sources**
- [unitree.py:157-174](file://source/robot_lab/robot_lab/assets/unitree.py#L157-L174)
- [go2w_description.urdf:222-229](file://source/robot_lab/data/Robots/unitree/go2w_description/urdf/go2w_description.urdf#L222-L229)
- [go2w_description.urdf:392-398](file://source/robot_lab/data/Robots/unitree/go2w_description/urdf/go2w_description.urdf#L392-L398)
- [go2w_description.urdf:562-568](file://source/robot_lab/data/Robots/unitree/go2w_description/urdf/go2w_description.urdf#L562-L568)
- [go2w_description.urdf:731-737](file://source/robot_lab/data/Robots/unitree/go2w_description/urdf/go2w_description.urdf#L731-L737)

### Joint Configurations and Initial Poses
- Joint naming:
  - Leg joints: FR/FL/RR/RL hip/thigh/calf.
  - Wheel joints: *_foot_joint.
- Initial pose:
  - Go2: Base Z = 0.38 m; leg joints initialized as described.
  - Go2W: Base Z = 0.45 m; includes *_foot_joint initialization.

```mermaid
flowchart TD
Start(["Initialize Robot"]) --> SetBase["Set Base Height<br/>Go2: 0.38 m<br/>Go2W: 0.45 m"]
SetBase --> InitLegs["Initialize Leg Joints<br/>Hip≈0, Thigh≈0.8, Calf≈-1.5"]
InitLegs --> InitWheels{"Is Go2W?"}
InitWheels --> |Yes| InitFootJoints["Initialize *_foot_joint = 0.0"]
InitWheels --> |No| End(["Ready"])
InitFootJoints --> End
```

**Diagram sources**
- [unitree.py:94-104](file://source/robot_lab/robot_lab/assets/unitree.py#L94-L104)
- [unitree.py:144-155](file://source/robot_lab/robot_lab/assets/unitree.py#L144-L155)

**Section sources**
- [unitree.py:94-104](file://source/robot_lab/robot_lab/assets/unitree.py#L94-L104)
- [unitree.py:144-155](file://source/robot_lab/robot_lab/assets/unitree.py#L144-L155)

### Simulation Parameters and Environment Setup
- Observation/action scaling and reward shaping are defined per environment.
- Go2:
  - Rewards emphasize velocity tracking and stability; base height target adjusted accordingly.
- Go2W:
  - Separate action channels for leg joint positions and wheel joint velocities.
  - Rewards tailored to minimize wheel torques and accelerations while maintaining locomotion performance.

```mermaid
sequenceDiagram
participant Env as "Environment"
participant Robot as "Robot Asset"
participant Act as "Actuators"
Env->>Robot : Load URDF and ArticulationCfg
Robot->>Act : Apply DCMotorCfg (Go2) or ImplicitActuatorCfg (Go2W)
Env->>Env : Configure observations/actions/rewards
Env-->>Robot : Step simulation with actions
```

**Diagram sources**
- [rough_env_cfg.go2:34-53](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2/rough_env_cfg.py#L34-L53)
- [rough_env_cfg.go2w:76-106](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/wheeled/unitree_go2w/rough_env_cfg.py#L76-L106)
- [unitree.py:71-177](file://source/robot_lab/robot_lab/assets/unitree.py#L71-L177)

**Section sources**
- [flat_env_cfg.go2:10-25](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2/flat_env_cfg.py#L10-L25)
- [rough_env_cfg.go2:30-80](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2/rough_env_cfg.py#L30-L80)
- [flat_env_cfg.go2w:9-25](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/wheeled/unitree_go2w/flat_env_cfg.py#L9-L25)
- [rough_env_cfg.go2w:72-133](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/wheeled/unitree_go2w/rough_env_cfg.py#L72-L133)

## Go2 Parkour Training System

### Enhanced Neural Network Architecture
The Go2 parkour system introduces a sophisticated custom neural network architecture called ActorCriticScan, designed specifically for complex parkour locomotion tasks with enhanced observation processing capabilities.

**Updated** Enhanced with improved observation dimension handling and curriculum-aware architecture

```mermaid
classDiagram
class ActorCriticScan {
+num_actor_obs : int
+num_critic_obs : int
+num_actions : int
+actor_hidden_dims : list[int]
+critic_hidden_dims : list[int]
+scan_encoder_dims : list[int]
+num_prop_obs : int
+num_scan_obs : int
+actor_scan_encoder : nn.Sequential
+critic_scan_encoder : nn.Sequential
+priv_encoder : nn.Sequential
+actor : nn.Sequential
+critic : nn.Sequential
+std : nn.Parameter
+noise_std_type : str
+obs_groups : dict
+num_actor_scan : int
+num_critic_scan : int
+num_priv : int
+update_distribution()
+act()
+evaluate()
}
```

**Diagram sources**
- [actor_critic_scan.py:20-280](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/agents/actor_critic_scan.py#L20-L280)

### Advanced Terrain Generation Capabilities
The system provides comprehensive terrain generation with 15+ different terrain types and enhanced curriculum support for progressive difficulty scaling.

**Updated** Enhanced with terrain-level curriculum support and improved parameter specifications

#### Available Terrain Types with Curriculum Support
- **Basic Terrains**: Plane, Pyramid Stairs, Inverted Pyramid Stairs
- **Grid Systems**: Random Grid, Repeated Objects (Cylinders, Boxes, Pyramids) with curriculum parameters
- **Obstacle Courses**: Rails, Pit, Box Terrain, Gap Terrain
- **Linear Obstacles**: Gap Strip, Hurdle Strip, Stairs Strip
- **Parkour-Specific**: Parkour Step, Floating Ring, Star Pattern, Debris Field

```mermaid
graph TB
Terrains["Enhanced Terrain System"]
Basic["Basic Terrains<br/>• Plane<br/>• Pyramid Stairs<br/>• Inverted Pyramid Stairs"]
Grid["Grid Systems<br/>• Random Grid<br/>• Repeated Objects<br/>• Debris Field"]
Obstacles["Obstacle Courses<br/>• Rails<br/>• Pit<br/>• Box Terrain<br/>• Gap Terrain"]
Linear["Linear Obstacles<br/>• Gap Strip<br/>• Hurdle Strip<br/>• Stairs Strip"]
Parkour["Parkour-Specific<br/>• Parkour Step<br/>• Floating Ring<br/>• Star Pattern"]
Terrains --> Basic
Terrains --> Grid
Terrains --> Obstacles
Terrains --> Linear
Terrains --> Parkour
```

**Diagram sources**
- [terrains_cfg.py:22-384](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/terrains_cfg.py#L22-L384)

### Enhanced Custom MDP Observations and Rewards
The parkour system includes specialized observations and rewards tailored for complex locomotion tasks with detailed dimensional characteristics.

**Updated** Improved documentation with comprehensive comments explaining sensor input dimensions

#### Enhanced Custom Observations with Dimensional Characteristics
- **Foot Contacts**: Binary contact flags from contact sensors, shape: (num_envs, num_feet)
- **Physical Properties**: Base mass, center of mass, friction coefficients
- **Control Parameters**: P-gain and D-gain scaling factors

#### Enhanced Custom Rewards with Dimensional Specifications
- **Mechanical Work**: Positive mechanical work with regeneration clamping, shape: (num_envs,)
- **Joint Deviations**: L2 penalty on joint positions from defaults
- **Stumble Detection**: Penalizes horizontal forces dominating vertical forces
- **Torque Sum**: Sum of applied joint torques, shape: (num_envs,)
- **Stop Penalties**: Exponential penalties for linear and angular velocity

```mermaid
sequenceDiagram
participant Env as "Enhanced Parkour Environment"
participant Sensor as "Contact Sensors"
participant Asset as "Robot Asset"
participant MDP as "Custom MDP"
Env->>Sensor : Collect Contact Data (Shape : (N, num_feet, 3))
Sensor->>MDP : Process Foot Contacts
Env->>Asset : Monitor Joint States
MDP->>MDP : Calculate Custom Rewards with Dimensions
MDP->>Env : Return Enhanced Observations with Shapes
```

**Diagram sources**
- [observations.py:33-111](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/mdp/observations.py#L33-L111)
- [rewards.py:35-131](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/mdp/rewards.py#L35-L131)

### Enhanced Ablation Study Configurations
The system supports comprehensive ablation studies with multiple runner configurations and enhanced curriculum parameter specifications:

- **Baseline**: Standard ActorCritic network
- **Scan Encoder Ablations**: Different scan encoder configurations
- **Privileged Observation Ablations**: Various privileged observation setups
- **Training Variants**: Flat vs Rough terrain training with curriculum support
- **Curriculum Parameter Ablations**: Enhanced difficulty progression controls

**Section sources**
- [actor_critic_scan.py:20-280](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/agents/actor_critic_scan.py#L20-L280)
- [rsl_rl_ppo_cfg.py:128-242](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/agents/rsl_rl_ppo_cfg.py#L128-L242)
- [terrains_cfg.py:22-384](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/terrains_cfg.py#L22-L384)
- [observations.py:33-111](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/mdp/observations.py#L33-L111)
- [rewards.py:35-131](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/mdp/rewards.py#L35-L131)

## Enhanced Terrain Curriculum System

### Terrain-Level Curriculum Support
The enhanced terrain system provides progressive difficulty scaling with comprehensive parameter specifications for each terrain type.

**Updated** Added terrain-level curriculum support with detailed parameter explanations

#### Curriculum Parameter Specifications
- **Difficulty Range**: 0.0 to 1.0 representing minimum to maximum difficulty
- **Parameter Interpolation**: Linear interpolation between start and end parameters based on difficulty
- **Terrain-Specific Parameters**: Each terrain type defines its own difficulty-dependent parameters

#### Enhanced Terrain Configuration Classes
- **MeshPyramidStairsTerrainCfg**: step_height_range, step_width, platform_width
- **MeshRandomGridTerrainCfg**: grid_width, grid_height_range, platform_width
- **MeshRepeatedObjectsTerrainCfg**: object_type, object_params_start/end, height noise parameters
- **MeshParkourStepTerrainCfg**: step_height_range, step_length_base_range, steps

```mermaid
graph LR
Difficulty["Difficulty Scale<br/>0.0 to 1.0"]
StartParams["Start Parameters<br/>At Difficulty=0"]
EndParams["End Parameters<br/>At Difficulty=1"]
Interpolated["Interpolated Parameters<br/>Linear Combination"]
Difficulty --> StartParams
Difficulty --> EndParams
StartParams --> Interpolated
EndParams --> Interpolated
```

**Diagram sources**
- [terrains_cfg.py:76-87](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/terrains_cfg.py#L76-L87)
- [terrains_cfg.py:264-277](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/terrains_cfg.py#L264-L277)

**Section sources**
- [terrains_cfg.py:22-384](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/terrains_cfg.py#L22-L384)
- [mesh_terrains.py:74-81](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/mesh_terrains.py#L74-L81)

## Improved Observation System

### Enhanced Observation Dimension Documentation
The observation system now includes comprehensive comments explaining the dimensional characteristics of sensor inputs and processing pipeline.

**Updated** Added detailed dimensional characteristics documentation for sensor inputs

#### Observation Pipeline with Dimensional Characteristics
- **Proprioceptive Observations**: Shape (num_envs, num_prop_obs)
- **Scan Observations**: Shape (num_envs, num_scan_obs) processed through scan encoders
- **Privileged Observations**: Shape (num_envs, num_priv_obs) processed through privileged encoders
- **Combined Observations**: Concatenated tensors with explicit dimension calculations

#### Enhanced Sensor Input Documentation
- **Contact Sensors**: Net forces with shape (num_envs, num_feet, 3)
- **Articulation Sensors**: Joint positions, velocities, torques with shape (num_envs, num_joints)
- **IMU Sensors**: Orientation, angular velocity, linear acceleration with shape (num_envs, 10)

```mermaid
graph TD
PropObs["Proprioceptive<br/>Shape: (N, 52)"]
ScanObs["Scan Observations<br/>Shape: (N, 187)"]
PrivObs["Privileged Observations<br/>Shape: (N, ?)"]
ContactSensors["Contact Sensors<br/>Shape: (N, num_feet, 3)"]
Articulation["Articulation Data<br/>Shape: (N, num_joints)"]
IMU["IMU Data<br/>Shape: (N, 10)"]
PropObs --> ActorInput["Actor Input<br/>Shape: (N, ?)"]
ScanObs --> ScanEncoder["Scan Encoder<br/>Shape: (N, latent_dim)"]
PrivObs --> CriticInput["Critic Input<br/>Shape: (N, ?)"]
ContactSensors --> PropObs
Articulation --> PropObs
IMU --> PropObs
ScanEncoder --> ActorInput
PrivObs --> CriticInput
```

**Diagram sources**
- [actor_critic_scan.py:62-71](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/agents/actor_critic_scan.py#L62-L71)
- [observations.py:33-47](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/mdp/observations.py#L33-L47)

**Section sources**
- [actor_critic_scan.py:54-71](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/agents/actor_critic_scan.py#L54-L71)
- [observations.py:33-111](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/mdp/observations.py#L33-L111)

## Dependency Analysis
- Environment configurations depend on robot assets for spawning and actuator definitions.
- Go2W introduces a dual-actuator strategy: implicit actuators for legs and wheels, altering dynamics compared to pure DC motors.
- **Enhanced Dependencies**: Go2 parkour system introduces dependencies on custom neural networks, terrain generation utilities, specialized MDP components, and curriculum parameter systems.

```mermaid
graph LR
QCfg["Quadruped Go2 Configs"] --> UAsset["unitree.py"]
WCfg["Wheeled Go2W Configs"] --> UAsset
UAsset --> URDFG["go2_description.urdf"]
UAsset --> URDFGW["go2w_description.urdf"]
GOParkour["Enhanced Go2 Parkour System"] --> ActorNet["ActorCriticScan"]
GOParkour --> TerrainGen["Enhanced Terrains"]
GOParkour --> CustomMDP["Improved MDP"]
GOParkour --> Curriculum["Terrain Curriculum"]
```

**Diagram sources**
- [rough_env_cfg.go2:34-35](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2/rough_env_cfg.py#L34-L35)
- [rough_env_cfg.go2w:76-77](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/wheeled/unitree_go2w/rough_env_cfg.py#L76-L77)
- [unitree.py:71-177](file://source/robot_lab/robot_lab/assets/unitree.py#L71-L177)
- [rsl_rl_ppo_cfg.py:21-22](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2_parkour/agents/rsl_rl_ppo_cfg.py#L21-L22)

**Section sources**
- [rough_env_cfg.go2:34-35](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2/rough_env_cfg.py#L34-L35)
- [rough_env_cfg.go2w:76-77](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/wheeled/unitree_go2w/rough_env_cfg.py#L76-L77)

## Performance Considerations
- Motor limits:
  - Both variants share identical effort/velocity/stiffness/damping limits for comparable torque and speed capabilities.
- Height differences:
  - Go2W's higher center of mass (0.45 m vs 0.38 m) affects stability and energy consumption; reward targets and penalties reflect this.
- Actuator modeling:
  - Go2W's wheels use implicit actuators with zero stiffness, emphasizing compliant rolling contact and reduced control complexity for wheel joints.
- **Enhanced Considerations**: Go2 parkour system requires additional computational resources for custom neural networks, terrain generation, and curriculum management, but enables more sophisticated training scenarios with progressive difficulty scaling.

## Troubleshooting Guide
- Validation of motor limits:
  - Confirm effort and velocity limits match expectations for both Go2 and Go2W actuators.
- Initial pose issues:
  - Ensure base height and joint positions align with configuration files for the chosen variant.
- Environment mismatch:
  - Verify the environment registration and configuration correspond to the intended variant (Go2 vs Go2W).
- **Enhanced Issues**: For Go2 parkour system:
  - Ensure custom neural network dependencies are properly installed.
  - Verify terrain generation parameters are within valid ranges and curriculum specifications are correct.
  - Check ablation study configurations for proper parameter combinations and observation dimension compatibility.
  - Validate observation dimension calculations and tensor shape compatibility in the neural network architecture.

**Section sources**
- [unitree.py:107-116](file://source/robot_lab/robot_lab/assets/unitree.py#L107-L116)
- [unitree.py:157-174](file://source/robot_lab/robot_lab/assets/unitree.py#L157-L174)
- [rough_env_cfg.go2:34-35](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/quadruped/unitree_go2/rough_env_cfg.py#L34-L35)
- [rough_env_cfg.go2w:76-77](file://source/robot_lab/robot_lab/tasks/manager_based/locomotion/velocity/config/wheeled/unitree_go2w/rough_env_cfg.py#L76-L77)

## Conclusion
The Unitree Go2 series integrates seamlessly with the Isaac Lab RL framework. Go2 relies on DC motors across all joints, while Go2W employs implicit actuators for legs and wheels, reflecting distinct locomotion strategies. The enhanced Go2 parkour training system provides a comprehensive self-contained package with custom RL configuration, advanced neural network architecture, enhanced terrain generation capabilities with curriculum support, and improved observation system documentation with detailed dimensional characteristics. The documented configurations, limits, and environment parameters enable reproducible simulations and informed selection between variants depending on terrain and mobility requirements.

## Appendices

### Selection Guidance: Go2 vs Go2W vs Enhanced Go2 Parkour
- Choose Go2 when:
  - Terrain requires robust foothold adaptability and dynamic balance.
  - Emphasis on bipedal-like legged locomotion with articulated feet.
- Choose Go2W when:
  - Smooth, efficient transport on relatively flat surfaces is prioritized.
  - Reduced actuator count for wheels lowers control complexity and power consumption.
- Choose Enhanced Go2 Parkour when:
  - Complex parkour and obstacle navigation training is required.
  - Advanced neural network architectures with curriculum support are beneficial.
  - Comprehensive ablation studies and enhanced observation system are needed.
  - Progressive difficulty scaling and terrain-level curriculum support are essential.
- **Enhanced Comparison Highlights**:
  - Effort/velocity/stiffness/damping limits are consistent between variants for fair comparisons.
  - Go2W's higher center of mass improves ground clearance but may increase overturning risk on uneven terrain.
  - Enhanced Go2 parkour system provides the most sophisticated training capabilities with curriculum support but requires additional computational resources.
  - Improved observation system documentation enables better debugging and parameter tuning.
  - Terrain-level curriculum support enables progressive skill development with systematic difficulty scaling.