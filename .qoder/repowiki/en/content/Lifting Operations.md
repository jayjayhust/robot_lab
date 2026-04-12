# Lifting Operations

<cite>
**Referenced Files in This Document**
- [lift_env_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/lift_env_cfg.py)
- [rewards.py](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/mdp/rewards.py)
- [observations.py](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/mdp/observations.py)
- [terminations.py](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/mdp/terminations.py)
- [joint_pos_env_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/config/franka/joint_pos_env_cfg.py)
- [ik_abs_env_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/config/franka/ik_abs_env_cfg.py)
- [ik_rel_env_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/config/franka/ik_rel_env_cfg.py)
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
This document describes the lifting operations implementation within the robot lab's manipulation task framework. It focuses on the lift task for fixed-arm robots, specifically configured for the Franka Panda manipulator. The lift task enables training and evaluation of robotic manipulation policies that:
- Reach toward a target object
- Grasp and lift the object above a minimum height
- Track a desired goal pose for the object in the world frame
- Terminate successfully when the object reaches the goal within a threshold

The lift task integrates with the Manager-Based Reinforcement Learning (RL) environment pattern, leveraging modular MDP components for observations, rewards, terminations, and events.

## Project Structure
The lifting operations are organized under the manipulation tasks module with a dedicated lift subpackage. The structure separates environment configurations (scene, actions, commands, rewards, terminations) from MDP-specific functions.

```mermaid
graph TB
subgraph "Lift Task"
A["lift_env_cfg.py<br/>Environment configuration"]
B["config/franka/<br/>Robot-specific configs"]
C["mdp/<br/>Observations, Rewards, Terminations"]
end
subgraph "Franka Configurations"
B1["joint_pos_env_cfg.py<br/>Joint position control"]
B2["ik_abs_env_cfg.py<br/>Absolute IK control"]
B3["ik_rel_env_cfg.py<br/>Relative IK control"]
end
subgraph "MDP Functions"
C1["observations.py<br/>Object position in robot root frame"]
C2["rewards.py<br/>Lift, reach, goal tracking"]
C3["terminations.py<br/>Goal reached detection"]
end
A --> B
A --> C
B --> B1
B --> B2
B --> B3
A --> C1
A --> C2
A --> C3
```

**Diagram sources**
- [lift_env_cfg.py:193-223](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/lift_env_cfg.py#L193-L223)
- [joint_pos_env_cfg.py:24-94](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/config/franka/joint_pos_env_cfg.py#L24-L94)
- [ik_abs_env_cfg.py:30-111](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/config/franka/ik_abs_env_cfg.py#L30-L111)
- [ik_rel_env_cfg.py:18-49](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/config/franka/ik_rel_env_cfg.py#L18-L49)
- [observations.py:19-30](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/mdp/observations.py#L19-L30)
- [rewards.py:20-68](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/mdp/rewards.py#L20-L68)
- [terminations.py:25-54](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/mdp/terminations.py#L25-L54)

**Section sources**
- [lift_env_cfg.py:193-223](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/lift_env_cfg.py#L193-L223)
- [joint_pos_env_cfg.py:24-94](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/config/franka/joint_pos_env_cfg.py#L24-L94)
- [ik_abs_env_cfg.py:30-111](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/config/franka/ik_abs_env_cfg.py#L30-L111)
- [ik_rel_env_cfg.py:18-49](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/config/franka/ik_rel_env_cfg.py#L18-L49)
- [observations.py:19-30](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/mdp/observations.py#L19-L30)
- [rewards.py:20-68](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/mdp/rewards.py#L20-L68)
- [terminations.py:25-54](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/mdp/terminations.py#L25-L54)

## Core Components
The lift task is composed of:
- Environment configuration defining scene, actions, commands, observations, rewards, terminations, and curriculum
- Robot-specific configurations for joint position control and differential inverse kinematics (absolute and relative modes)
- MDP functions for observations, rewards, and termination conditions

Key responsibilities:
- Scene: Defines robot, object, table, ground plane, lighting, and end-effector frame transformer
- Actions: Joint position control or differential inverse kinematics with optional gripper control
- Commands: Uniform pose command specifying target object pose in robot root frame
- Observations: Relative joint states, object position in robot root frame, target pose, last action
- Rewards: Reaching object (distance-based), lifting object (height-based), goal tracking (distance-based), action rate, joint velocity penalties
- Termination: Episode timeout and object dropping below minimum height
- Curriculum: Gradually increase weights of action rate and joint velocity penalties

**Section sources**
- [lift_env_cfg.py:31-223](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/lift_env_cfg.py#L31-L223)
- [joint_pos_env_cfg.py:24-94](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/config/franka/joint_pos_env_cfg.py#L24-L94)
- [ik_abs_env_cfg.py:30-111](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/config/franka/ik_abs_env_cfg.py#L30-L111)
- [ik_rel_env_cfg.py:18-49](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/config/franka/ik_rel_env_cfg.py#L18-L49)
- [rewards.py:20-68](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/mdp/rewards.py#L20-L68)
- [observations.py:19-30](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/mdp/observations.py#L19-L30)
- [terminations.py:25-54](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/mdp/terminations.py#L25-L54)

## Architecture Overview
The lift task architecture follows a modular design:
- Environment configuration aggregates MDP components
- Robot-specific configurations specialize actions and gripper behavior
- MDP functions encapsulate computation for observations, rewards, and terminations
- End-effector frame transformer provides target frame for IK actions

```mermaid
graph TB
Env["LiftEnvCfg<br/>Scene, Actions, Commands, Observations, Rewards, Terminations, Curriculum"]
Robot["FrankaCubeLiftEnvCfg<br/>Joint Position Control"]
IK_Abs["FrankaCubeLiftEnvCfg<br/>Differential IK Absolute"]
IK_Rel["FrankaCubeLiftEnvCfg<br/>Differential IK Relative"]
EE["End-Effector Frame Transformer<br/>Target: panda_hand"]
Obs["Observations<br/>object_position_in_robot_root_frame"]
Rew["Rewards<br/>object_is_lifted, object_ee_distance, object_goal_distance"]
Done["Terminations<br/>object_reached_goal"]
Env --> Robot
Env --> IK_Abs
Env --> IK_Rel
Env --> Obs
Env --> Rew
Env --> Done
Robot --> EE
IK_Abs --> EE
IK_Rel --> EE
```

**Diagram sources**
- [lift_env_cfg.py:193-223](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/lift_env_cfg.py#L193-L223)
- [joint_pos_env_cfg.py:24-94](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/config/franka/joint_pos_env_cfg.py#L24-L94)
- [ik_abs_env_cfg.py:30-111](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/config/franka/ik_abs_env_cfg.py#L30-L111)
- [ik_rel_env_cfg.py:18-49](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/config/franka/ik_rel_env_cfg.py#L18-L49)
- [observations.py:19-30](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/mdp/observations.py#L19-L30)
- [rewards.py:20-68](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/mdp/rewards.py#L20-L68)
- [terminations.py:25-54](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/mdp/terminations.py#L25-L54)

## Detailed Component Analysis

### Environment Configuration
The environment configuration defines the base lift environment with:
- Scene: Robot, object, table, ground plane, lighting, and end-effector frame transformer
- Commands: Uniform pose command for object target pose
- Actions: Arm action (joint position or differential IK) and gripper action
- Observations: Concatenated policy observations including joint positions/velocities, object position in robot root frame, target object position, and last action
- Rewards: Reaching object, lifting object, goal tracking, action rate, and joint velocity penalties
- Termination: Episode timeout and object dropping below minimum height
- Curriculum: Increasing weights for action rate and joint velocity penalties over time

```mermaid
classDiagram
class LiftEnvCfg {
+scene : ObjectTableSceneCfg
+actions : ActionsCfg
+commands : CommandsCfg
+observations : ObservationsCfg
+rewards : RewardsCfg
+terminations : TerminationsCfg
+events : EventCfg
+curriculum : CurriculumCfg
+__post_init__()
}
class ObjectTableSceneCfg {
+robot : ArticulationCfg
+ee_frame : FrameTransformerCfg
+object : RigidObjectCfg|DeformableObjectCfg
+table
+plane
+light
}
class ActionsCfg {
+arm_action
+gripper_action
}
class CommandsCfg {
+object_pose
}
class ObservationsCfg {
+policy : PolicyCfg
}
class RewardsCfg {
+reaching_object
+lifting_object
+object_goal_tracking
+object_goal_tracking_fine_grained
+action_rate
+joint_vel
}
class TerminationsCfg {
+time_out
+object_dropping
}
class EventCfg {
+reset_all
+reset_object_position
}
class CurriculumCfg {
+action_rate
+joint_vel
}
LiftEnvCfg --> ObjectTableSceneCfg : "contains"
LiftEnvCfg --> ActionsCfg : "contains"
LiftEnvCfg --> CommandsCfg : "contains"
LiftEnvCfg --> ObservationsCfg : "contains"
LiftEnvCfg --> RewardsCfg : "contains"
LiftEnvCfg --> TerminationsCfg : "contains"
LiftEnvCfg --> EventCfg : "contains"
LiftEnvCfg --> CurriculumCfg : "contains"
```

**Diagram sources**
- [lift_env_cfg.py:31-223](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/lift_env_cfg.py#L31-L223)

**Section sources**
- [lift_env_cfg.py:31-223](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/lift_env_cfg.py#L31-L223)

### Robot-Specific Configurations
Robot-specific configurations specialize the lift environment for the Franka Panda:
- Joint position control: Defines joint position action for arm and binary gripper action for fingers
- Differential IK absolute control: Uses absolute pose commands with a DLS IK solver and optional body offset
- Differential IK relative control: Uses relative pose commands with a DLS IK solver and scaling factor
- Teddy bear variant: Demonstrates deformable object handling with adjusted actuator limits and disabled physics replication

```mermaid
classDiagram
class FrankaCubeLiftEnvCfg_JointPos {
+scene.robot
+actions.arm_action
+actions.gripper_action
+commands.object_pose.body_name
+scene.object
+scene.ee_frame
}
class FrankaCubeLiftEnvCfg_IK_Abs {
+scene.robot
+actions.arm_action
}
class FrankaCubeLiftEnvCfg_IK_Rel {
+scene.robot
+actions.arm_action
}
class FrankaTeddyBearLiftEnvCfg {
+scene.object
+scene.robot.actuators
+scene.replicate_physics
+events.reset_object_position
+rewards.*
+observations.policy.object_position
}
FrankaCubeLiftEnvCfg_JointPos <|-- FrankaCubeLiftEnvCfg_IK_Abs : "extends"
FrankaCubeLiftEnvCfg_JointPos <|-- FrankaCubeLiftEnvCfg_IK_Rel : "extends"
FrankaCubeLiftEnvCfg_IK_Abs <|-- FrankaTeddyBearLiftEnvCfg : "extends"
```

**Diagram sources**
- [joint_pos_env_cfg.py:24-94](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/config/franka/joint_pos_env_cfg.py#L24-L94)
- [ik_abs_env_cfg.py:30-111](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/config/franka/ik_abs_env_cfg.py#L30-L111)
- [ik_rel_env_cfg.py:18-49](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/config/franka/ik_rel_env_cfg.py#L18-L49)

**Section sources**
- [joint_pos_env_cfg.py:24-94](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/config/franka/joint_pos_env_cfg.py#L24-L94)
- [ik_abs_env_cfg.py:30-111](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/config/franka/ik_abs_env_cfg.py#L30-L111)
- [ik_rel_env_cfg.py:18-49](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/config/franka/ik_rel_env_cfg.py#L18-L49)

### MDP Functions

#### Observations
- Object position in robot root frame: Transforms object world position into the robot's root frame for policy observation

**Section sources**
- [observations.py:19-30](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/mdp/observations.py#L19-L30)

#### Rewards
- Object lifted: Binary reward when object height exceeds minimal height
- Object-to-end-effector distance: Distance-based reward using a tanh kernel for reaching
- Object goal distance: Goal-tracking reward combining distance and height thresholds

```mermaid
flowchart TD
Start(["Reward Function Entry"]) --> CheckHeight["Check if object height > minimal_height"]
CheckHeight --> HeightOK{"Height threshold met?"}
HeightOK --> |Yes| ComputeDist["Compute distance between desired pose and object pose"]
HeightOK --> |No| ComputeDist
ComputeDist --> TanhKernel["Apply tanh kernel with std parameter"]
TanhKernel --> ScaleReward["Scale reward by weight"]
ScaleReward --> End(["Return reward"])
```

**Diagram sources**
- [rewards.py:20-68](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/mdp/rewards.py#L20-L68)

**Section sources**
- [rewards.py:20-68](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/mdp/rewards.py#L20-L68)

#### Termination
- Object reached goal: Episode terminates when object reaches desired pose within a threshold

```mermaid
flowchart TD
Start(["Termination Function Entry"]) --> GetCommand["Get desired pose from command manager"]
GetCommand --> Transform["Transform desired pose to world frame using robot root pose/quat"]
Transform --> ComputeDist["Compute Euclidean distance between desired and object pose"]
ComputeDist --> Compare["Compare distance with threshold"]
Compare --> |Distance < threshold| GoalReached["Return True (episode ends)"]
Compare --> |Distance >= threshold| NotReached["Return False (continue episode)"]
```

**Diagram sources**
- [terminations.py:25-54](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/mdp/terminations.py#L25-L54)

**Section sources**
- [terminations.py:25-54](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/mdp/terminations.py#L25-L54)

## Dependency Analysis
The lift task exhibits clear separation of concerns:
- Environment configuration depends on MDP modules for observations, rewards, and terminations
- Robot-specific configurations inherit from the base environment and override actions and gripper behavior
- MDP functions depend on environment scene assets and command manager for pose computations

```mermaid
graph TB
EnvCfg["lift_env_cfg.py"]
Obs["observations.py"]
Rew["rewards.py"]
Done["terminations.py"]
JP["joint_pos_env_cfg.py"]
IKAbs["ik_abs_env_cfg.py"]
IKRel["ik_rel_env_cfg.py"]
EnvCfg --> Obs
EnvCfg --> Rew
EnvCfg --> Done
JP --> EnvCfg
IKAbs --> EnvCfg
IKRel --> EnvCfg
```

**Diagram sources**
- [lift_env_cfg.py:31-223](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/lift_env_cfg.py#L31-L223)
- [observations.py:19-30](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/mdp/observations.py#L19-L30)
- [rewards.py:20-68](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/mdp/rewards.py#L20-L68)
- [terminations.py:25-54](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/mdp/terminations.py#L25-L54)
- [joint_pos_env_cfg.py:24-94](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/config/franka/joint_pos_env_cfg.py#L24-L94)
- [ik_abs_env_cfg.py:30-111](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/config/franka/ik_abs_env_cfg.py#L30-L111)
- [ik_rel_env_cfg.py:18-49](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/config/franka/ik_rel_env_cfg.py#L18-L49)

**Section sources**
- [lift_env_cfg.py:31-223](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/lift_env_cfg.py#L31-L223)
- [joint_pos_env_cfg.py:24-94](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/config/franka/joint_pos_env_cfg.py#L24-L94)
- [ik_abs_env_cfg.py:30-111](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/config/franka/ik_abs_env_cfg.py#L30-L111)
- [ik_rel_env_cfg.py:18-49](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/config/franka/ik_rel_env_cfg.py#L18-L49)
- [observations.py:19-30](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/mdp/observations.py#L19-L30)
- [rewards.py:20-68](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/mdp/rewards.py#L20-L68)
- [terminations.py:25-54](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/mdp/terminations.py#L25-L54)

## Performance Considerations
- Simulation settings: The environment uses a 100 Hz simulation step with PhysX tuned parameters for bounce threshold velocity and friction correlation distance
- Action decimation: Episode length and render interval are configured to balance training speed and fidelity
- IK solver: Differential IK uses a Damped Least Squares (DLS) method for robust pose tracking; absolute vs relative modes affect convergence behavior
- Curriculum: Gradual increase in action rate and joint velocity penalties encourages stable policy learning

[No sources needed since this section provides general guidance]

## Troubleshooting Guide
Common issues and resolutions:
- IK tracking instability: Switch to absolute IK mode or adjust solver damping and gains
- Gripper control mismatch: Verify joint names and open/close command expressions match the robot model
- Object dropping: Increase minimal height threshold or adjust termination conditions
- Deformable object handling: Adjust actuator effort limits and disable physics replication as demonstrated in the Teddy Bear variant

**Section sources**
- [ik_abs_env_cfg.py:30-111](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/config/franka/ik_abs_env_cfg.py#L30-L111)
- [joint_pos_env_cfg.py:24-94](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/config/franka/joint_pos_env_cfg.py#L24-L94)
- [terminations.py:25-54](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/lift/mdp/terminations.py#L25-L54)

## Conclusion
The lifting operations implementation provides a flexible and modular framework for training robotic manipulation policies. By separating environment configuration from robot-specific controls and MDP functions, the system supports rapid experimentation with different control modalities (joint position vs differential IK) and robot models. The use of standardized MDP components ensures consistent reward shaping and termination logic across tasks, while curriculum mechanisms support stable policy learning.