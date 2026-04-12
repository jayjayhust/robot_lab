# In-Hand Manipulation

<cite>
**Referenced Files in This Document**
- [README.md](file://README.md)
- [inhand_env_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/inhand_env_cfg.py)
- [allegro_env_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/config/allegro_hand/allegro_env_cfg.py)
- [commands_cfg.py](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/commands/commands_cfg.py)
- [orientation_command.py](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/commands/orientation_command.py)
- [observations.py](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/observations.py)
- [rewards.py](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/rewards.py)
- [events.py](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/events.py)
- [terminations.py](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/terminations.py)
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
This document describes the in-hand manipulation capabilities implemented in the robot lab project. The focus is on enabling a robotic hand to reorient a small object (such as a cube) held within its grasp using reinforcement learning. The environment supports both full-kinematic observations (including velocities) and reduced-kinematic observations (without velocities), and it integrates with advanced robotic assets such as the Allegro hand. The system leverages the Manager-Based Reinforcement Learning framework provided by Isaac Lab to configure scenes, actions, observations, rewards, events, and terminations.

## Project Structure
The in-hand manipulation implementation is organized around a modular configuration and MDP (Markov Decision Process) structure:
- Environment configuration defines the scene, simulation parameters, and task-specific MDP components.
- Robot and object assets are configured via asset definitions and spawn parameters.
- MDP modules encapsulate command generation, observations, rewards, events, and termination conditions.
- Agent configurations for training and evaluation are provided under dedicated agent directories.

```mermaid
graph TB
subgraph "Environment Configuration"
ENV["InHandObjectEnvCfg<br/>Defines scene, actions, observations,<br/>rewards, events, terminations"]
SCENE["InHandObjectSceneCfg<br/>Robot + Object + Lighting"]
CMD["CommandsCfg<br/>InHandReOrientationCommand"]
OBS["ObservationsCfg<br/>KinematicObsGroup + NoVelocity variants"]
ACT["ActionsCfg<br/>EMAJointPositionToLimitsAction"]
EVT["EventCfg<br/>Randomization & Reset"]
RWD["RewardsCfg<br/>Orientation tracking + penalties"]
DONE["TerminationsCfg<br/>Timeouts + Success thresholds"]
end
subgraph "MDP Modules"
ORI_CMD["orientation_command.py<br/>InHandReOrientationCommand"]
OBS_FN["observations.py<br/>goal_quat_diff"]
RWD_FN["rewards.py<br/>success_bonus, track_orientation_inv_l2"]
EVT_FN["events.py<br/>reset_joints_within_limits_range"]
TERM_FN["terminations.py<br/>max_consecutive_success,<br/>object_away_from_robot"]
end
subgraph "Robot Assets"
ALLEGRO["ALLEGRO_HAND_CFG<br/>Asset definition"]
DEXCUBE["DexCube USD<br/>Object asset"]
end
ENV --> SCENE
ENV --> CMD
ENV --> OBS
ENV --> ACT
ENV --> EVT
ENV --> RWD
ENV --> DONE
CMD --> ORI_CMD
OBS --> OBS_FN
RWD --> RWD_FN
EVT --> EVT_FN
DONE --> TERM_FN
SCENE --> ALLEGRO
SCENE --> DEXCUBE
```

**Diagram sources**
- [inhand_env_cfg.py:33-347](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/inhand_env_cfg.py#L33-L347)
- [orientation_command.py:25-145](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/commands/orientation_command.py#L25-L145)
- [observations.py:20-39](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/observations.py#L20-L39)
- [rewards.py:20-97](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/rewards.py#L20-L97)
- [events.py:22-185](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/events.py#L22-L185)
- [terminations.py:18-84](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/terminations.py#L18-L84)

**Section sources**
- [README.md:11-531](file://README.md#L11-L531)
- [inhand_env_cfg.py:33-347](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/inhand_env_cfg.py#L33-L347)

## Core Components
- Environment configuration: Defines the scene with a robotic hand and a deformable or rigid object, sets simulation parameters, and aggregates MDP components.
- Command generator: Produces orientation goals for the object and updates goals upon successful completion.
- Observations: Provides kinematic state observations (with or without velocities) and derived quantities such as goal orientation differences.
- Rewards: Encourages orientation tracking and success, with penalties for excessive joint velocities and action rates.
- Events: Randomizes physical properties and resets robot/object states at episode start/reset.
- Termination conditions: Ends episodes based on timeouts, success streaks, or object drift from goal or robot.

Key implementation references:
- Environment configuration and MDP components: [inhand_env_cfg.py:33-347](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/inhand_env_cfg.py#L33-L347)
- Command configuration and generator: [commands_cfg.py:17-68](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/commands/commands_cfg.py#L17-L68), [orientation_command.py:25-145](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/commands/orientation_command.py#L25-L145)
- Observations: [observations.py:20-39](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/observations.py#L20-L39)
- Rewards: [rewards.py:20-97](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/rewards.py#L20-L97)
- Events: [events.py:22-185](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/events.py#L22-L185)
- Termination conditions: [terminations.py:18-84](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/terminations.py#L18-L84)

**Section sources**
- [inhand_env_cfg.py:33-347](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/inhand_env_cfg.py#L33-L347)
- [commands_cfg.py:17-68](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/commands/commands_cfg.py#L17-L68)
- [orientation_command.py:25-145](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/commands/orientation_command.py#L25-L145)
- [observations.py:20-39](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/observations.py#L20-L39)
- [rewards.py:20-97](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/rewards.py#L20-L97)
- [events.py:22-185](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/events.py#L22-L185)
- [terminations.py:18-84](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/terminations.py#L18-L84)

## Architecture Overview
The in-hand manipulation system is structured around a Manager-Based RL environment. The configuration composes:
- Scene: robot asset (e.g., Allegro hand) and object asset (e.g., DexCube).
- Actions: joint position commands constrained to actuator limits.
- Observations: robot joint positions/velocities and object root pose/velocity, plus derived command-related signals.
- Rewards: orientation tracking reward, success bonus, and penalty terms.
- Events: randomized material and mass properties, and joint/state resets.
- Termination: timeout, success streak, and object drift checks.

```mermaid
graph TB
A["ManagerBasedRLEnv"] --> B["Scene: InHandObjectSceneCfg"]
A --> C["Actions: EMATargetJointPositionAction"]
A --> D["Observations: KinematicObsGroup"]
A --> E["Commands: InHandReOrientationCommand"]
A --> F["Rewards: track_orientation_inv_l2, success_bonus"]
A --> G["Events: randomize_rigid_body_material, reset_*"]
A --> H["Terminations: time_out, max_consecutive_success,<br/>object_away_from_robot"]
B --> B1["Robot: ALLEGRO_HAND_CFG"]
B --> B2["Object: DexCube USD"]
B --> B3["Lights: Distant + Dome"]
```

**Diagram sources**
- [inhand_env_cfg.py:33-347](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/inhand_env_cfg.py#L33-L347)
- [allegro_env_cfg.py:16-67](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/config/allegro_hand/allegro_env_cfg.py#L16-L67)

**Section sources**
- [inhand_env_cfg.py:33-347](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/inhand_env_cfg.py#L33-L347)
- [allegro_env_cfg.py:16-67](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/config/allegro_hand/allegro_env_cfg.py#L16-L67)

## Detailed Component Analysis

### Environment Configuration
The environment configuration defines:
- Scene: number of environments, spacing, robot asset, object asset with physics properties, and lighting.
- Simulation: physics material and PhysX settings.
- MDP components: commands, actions, observations, rewards, events, and terminations.
- Episode timing: decimation, episode length, and simulation timestep.

```mermaid
classDiagram
class InHandObjectSceneCfg {
+ArticulationCfg robot
+RigidObjectCfg object
+AssetBaseCfg light
+AssetBaseCfg dome_light
}
class CommandsCfg {
+InHandReOrientationCommandCfg object_pose
}
class ActionsCfg {
+EMAJointPositionToLimitsActionCfg joint_pos
}
class ObservationsCfg {
+KinematicObsGroupCfg policy
+NoVelocityKinematicObsGroupCfg NoVelocity variant
}
class RewardsCfg {
+track_orientation_inv_l2
+success_bonus
+penalties : joint_vel_l2, action_l2, action_rate_l2
}
class EventCfg {
+robot_physics_material
+robot_scale_mass
+robot_joint_stiffness_and_damping
+object_physics_material
+object_scale_mass
+reset_object
+reset_robot_joints
}
class TerminationsCfg {
+time_out
+max_consecutive_success
+object_out_of_reach
}
class InHandObjectEnvCfg {
+scene : InHandObjectSceneCfg
+sim : SimulationCfg
+observations : ObservationsCfg
+actions : ActionsCfg
+commands : CommandsCfg
+rewards : RewardsCfg
+events : EventCfg
+terminations : TerminationsCfg
+episode_length_s
+decimation
+viewer.eye
}
InHandObjectEnvCfg --> InHandObjectSceneCfg
InHandObjectEnvCfg --> CommandsCfg
InHandObjectEnvCfg --> ActionsCfg
InHandObjectEnvCfg --> ObservationsCfg
InHandObjectEnvCfg --> RewardsCfg
InHandObjectEnvCfg --> EventCfg
InHandObjectEnvCfg --> TerminationsCfg
```

**Diagram sources**
- [inhand_env_cfg.py:33-347](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/inhand_env_cfg.py#L33-L347)

**Section sources**
- [inhand_env_cfg.py:33-347](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/inhand_env_cfg.py#L33-L347)

### Command Generation: In-Hand Re-Orientation
The command generator produces orientation goals for the object and updates them upon success. It maintains per-environment metrics for orientation and position errors and tracks consecutive successes.

```mermaid
sequenceDiagram
participant Env as "ManagerBasedRLEnv"
participant Cmd as "InHandReOrientationCommand"
participant Obj as "RigidObject"
Env->>Cmd : Initialize with cfg and env
Cmd->>Obj : Read default_root_state for initial position
loop Every step
Env->>Cmd : _update_command()
Cmd->>Obj : Read current root_quat_w/root_pos_w
Cmd->>Cmd : Compute orientation_error and position_error
Cmd->>Cmd : Update metrics["consecutive_success"]
alt Goal reached
Cmd->>Cmd : _resample_command(env_ids)
Cmd->>Obj : Sample new random orientation target
end
Cmd-->>Env : command = [pos_command_e, quat_command_w]
end
```

**Diagram sources**
- [orientation_command.py:25-145](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/commands/orientation_command.py#L25-L145)

**Section sources**
- [commands_cfg.py:17-68](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/commands/commands_cfg.py#L17-L68)
- [orientation_command.py:25-145](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/commands/orientation_command.py#L25-L145)

### Observations: Goal Orientation Difference
The observation module computes the quaternion difference between the object's current orientation and the goal orientation, ensuring a unique quaternion representation.

```mermaid
flowchart TD
Start(["Function Entry"]) --> Extract["Extract asset and command term"]
Extract --> GetOri["Get goal_quat_w and asset_quat_w"]
GetOri --> Diff["quat = quat_mul(asset_quat_w, quat_conjugate(goal_quat_w))"]
Diff --> Unique{"make_quat_unique?"}
Unique --> |Yes| MakeUnique["quat_unique(quat)"]
Unique --> |No| KeepQuat["quat"]
MakeUnique --> Return["Return quaternion"]
KeepQuat --> Return
```

**Diagram sources**
- [observations.py:20-39](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/observations.py#L20-L39)

**Section sources**
- [observations.py:20-39](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/observations.py#L20-L39)

### Rewards: Orientation Tracking and Success Bonus
Reward computation includes:
- Orientation tracking reward using inverse of orientation error magnitude.
- Success bonus when the orientation error is below a threshold.
- Penalty terms for joint velocities, action magnitudes, and action rate.

```mermaid
flowchart TD
Start(["Function Entry"]) --> Extract["Extract asset and command term"]
Extract --> Goal["Get goal_quat_w"]
Goal --> Error["Compute dtheta = quat_error_magnitude(asset_quat_w, goal_quat_w)"]
Error --> Success{"dtheta <= threshold?"}
Success --> |Yes| Bonus["Return 1.0"]
Success --> |No| Track["Return 1.0 / (dtheta + rot_eps)"]
```

**Diagram sources**
- [rewards.py:20-97](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/rewards.py#L20-L97)

**Section sources**
- [rewards.py:20-97](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/rewards.py#L20-L97)

### Events: Randomization and Reset
Randomization and reset functions:
- Randomize rigid body materials and masses for robot and object.
- Reset robot joints within specified ranges and velocities.
- Reset object root state near its default position.

```mermaid
flowchart TD
Start(["Event Trigger"]) --> Parse["Parse params: position_range, velocity_range, asset_cfg, operation"]
Parse --> SamplePos["Sample joint positions within parsed ranges"]
SamplePos --> ClampPos["Clamp to soft joint position limits"]
Parse --> SampleVel["Sample joint velocities within parsed ranges"]
SampleVel --> ClampVel["Clamp to soft joint velocity limits"]
ClampPos --> Write["Write states to simulation"]
ClampVel --> Write
```

**Diagram sources**
- [events.py:22-185](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/events.py#L22-L185)

**Section sources**
- [events.py:22-185](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/events.py#L22-L185)

### Termination Conditions
Termination logic:
- Episode timeout after a fixed duration.
- Early termination if the object drifts too far from the goal or from the robot.
- Early termination if a success streak threshold is met.

```mermaid
flowchart TD
Start(["Step"]) --> Timeout["Check time_out"]
Timeout --> |True| End(["Terminate"])
Timeout --> |False| SuccessStreak["Check max_consecutive_success"]
SuccessStreak --> |True| End
SuccessStreak --> |False| DriftGoal["Check object_away_from_goal"]
DriftGoal --> |True| End
DriftGoal --> |False| DriftRobot["Check object_away_from_robot"]
DriftRobot --> |True| End
DriftRobot --> |False| Continue(["Continue"])
```

**Diagram sources**
- [terminations.py:18-84](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/terminations.py#L18-L84)

**Section sources**
- [terminations.py:18-84](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/terminations.py#L18-L84)

## Dependency Analysis
The in-hand manipulation system exhibits clear separation of concerns:
- Environment configuration depends on MDP modules for commands, observations, rewards, events, and terminations.
- Command generator depends on the object asset and visualization markers for debugging.
- Observations and rewards depend on math utilities and asset state access.
- Events and terminations depend on environment managers and scene entities.

```mermaid
graph LR
ENV["InHandObjectEnvCfg"] --> CMD["InHandReOrientationCommand"]
ENV --> OBS["Observations (goal_quat_diff)"]
ENV --> RWD["Rewards (success_bonus, track_orientation_inv_l2)"]
ENV --> EVT["Events (reset_joints_within_limits_range)"]
ENV --> DONE["Terminations (max_consecutive_success, object_away_from_robot)"]
CMD --> ORI["orientation_command.py"]
OBS --> OBS_M["observations.py"]
RWD --> RWD_M["rewards.py"]
EVT --> EVT_M["events.py"]
DONE --> TERM_M["terminations.py"]
```

**Diagram sources**
- [inhand_env_cfg.py:33-347](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/inhand_env_cfg.py#L33-L347)
- [orientation_command.py:25-145](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/commands/orientation_command.py#L25-L145)
- [observations.py:20-39](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/observations.py#L20-L39)
- [rewards.py:20-97](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/rewards.py#L20-L97)
- [events.py:22-185](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/events.py#L22-L185)
- [terminations.py:18-84](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/terminations.py#L18-L84)

**Section sources**
- [inhand_env_cfg.py:33-347](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/inhand_env_cfg.py#L33-L347)
- [orientation_command.py:25-145](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/commands/orientation_command.py#L25-L145)
- [observations.py:20-39](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/observations.py#L20-L39)
- [rewards.py:20-97](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/rewards.py#L20-L97)
- [events.py:22-185](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/events.py#L22-L185)
- [terminations.py:18-84](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/terminations.py#L18-L84)

## Performance Considerations
- Observation bandwidth: Full-kinematic observations include velocities, which can increase communication overhead. The no-velocity variant reduces this load when velocity information is unnecessary.
- Action smoothing: Penalties on action and action rate help stabilize training and reduce jitter.
- Physics tuning: Simulation parameters (e.g., solver iterations, contact patch counts) impact stability and speed; adjust based on hardware and task requirements.
- Environment scaling: The default environment count is large to support efficient RL training; reduce for interactive play or debugging.

## Troubleshooting Guide
- Goals not updating: Verify that the command generator is configured to update goals on success and that the success threshold is appropriate.
- Object falling off: Increase the success threshold or adjust the constant position command offset to keep the object above the palm.
- Instability during training: Reduce action penalties or adjust simulation dt and render interval; ensure proper asset mass and friction settings.
- Visualization issues: Confirm debug visualization markers are enabled and properly positioned relative to the object.

**Section sources**
- [orientation_command.py:94-125](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/mdp/commands/orientation_command.py#L94-L125)
- [inhand_env_cfg.py:258-299](file://source/robot_lab/robot_lab/tasks/manager_based/manipulation/inhand/inhand_env_cfg.py#L258-L299)

## Conclusion
The in-hand manipulation system provides a robust, configurable framework for teaching robotic hands to reorient objects within a grasp. By combining precise command generation, tailored observations, and carefully designed rewards and termination conditions, the environment supports efficient reinforcement learning. The modular MDP structure enables easy adaptation to different robotic hands and objects, while agent configurations support scalable training and evaluation.