# Copyright (c) 2024-2026 Ziqi Fan
# SPDX-License-Identifier: Apache-2.0

import math
import robot_lab.tasks.manager_based.locomotion.velocity.mdp as mdp
from robot_lab.tasks.manager_based.locomotion.velocity.velocity_env_cfg import LocomotionVelocityStairEnvCfg

from isaaclab.utils import configclass
from isaaclab.managers import SceneEntityCfg

##
# Pre-defined configs
##
from robot_lab.assets.zsibot import ZSIBOT_ZSL1_CFG  # isort: skip

# https://github.com/isaac-sim/IsaacLab/blob/main/source/isaaclab/isaaclab/terrains/config/rough.py
"""Configuration for custom terrains."""
import isaaclab.terrains as terrain_gen
from isaaclab.terrains.terrain_generator_cfg import TerrainGeneratorCfg

STAIR_TERRAINS_CFG = TerrainGeneratorCfg(
    size=(8.0, 8.0),  # The width (along x) and length (along y) of each sub-terrain (in m)
    border_width=10.0,  # The width of the border around the terrain (in m)
    num_rows=10,  # Number of rows of sub-terrains to generate
    num_cols=10,  # Number of columns of sub-terrains to generate
    horizontal_scale=0.1,  # Horizontal scale of the terrain (in m)
    vertical_scale=0.005,  # Vertical scale of the terrain (in m)
    slope_threshold=0.75,  # The slope threshold above which surfaces are made vertical (in rad)
    use_cache=False,
    # https://github.com/isaac-sim/IsaacLab/blob/main/source/isaaclab/isaaclab/terrains/sub_terrain_cfg.py
    sub_terrains={
        # "pyramid_stairs": terrain_gen.MeshPyramidStairsTerrainCfg(
        #     proportion=0.2,
        #     step_height_range=(0.05, 0.23),
        #     step_width=0.3,
        #     platform_width=3.0,
        #     border_width=1.0,
        #     holes=False,
        # ),
        "pyramid_stairs_inv": terrain_gen.MeshInvertedPyramidStairsTerrainCfg(
            proportion=0.2,  # Proportion of the terrain to generate
            # step_height_range=(0.05, 0.23),  # 每节阶梯的高度范围
            # step_height_range=(0.05, 0.10),  # 每节阶梯的高度范围
            step_height_range=(0.05, 0.15),  # 每节阶梯的高度范围
            step_width=0.3,  # 每节阶梯的宽度
            platform_width=3.0,  # 平台宽度
            border_width=1.0,  # 边缘宽度
            holes=False,
        )
    },
)
"""Stair terrains configuration."""

@configclass
class ZsibotZSL1StairEnvCfg(LocomotionVelocityStairEnvCfg):
    base_link_name = "BASE_LINK"
    foot_link_name = ".*_FOOT_LINK"
    # fmt: off
    joint_names = [
        "FAR_ABAD_JOINT", "FAR_HIP_JOINT", "FAR_KNEE_JOINT",
        "FBL_ABAD_JOINT", "FBL_HIP_JOINT", "FBL_KNEE_JOINT",
        "RAR_ABAD_JOINT", "RAR_HIP_JOINT", "RAR_KNEE_JOINT",
        "RBL_ABAD_JOINT", "RBL_HIP_JOINT", "RBL_KNEE_JOINT",
    ]
    # fmt: on

    def __post_init__(self):
        # post init of parent
        super().__post_init__()

        self.scene.robot = ZSIBOT_ZSL1_CFG.replace(prim_path="{ENV_REGEX_NS}/Robot")
        self.scene.height_scanner.prim_path = "{ENV_REGEX_NS}/Robot/" + self.base_link_name
        self.scene.height_scanner_base.prim_path = "{ENV_REGEX_NS}/Robot/" + self.base_link_name

        # change terrain to flat
        self.scene.terrain.terrain_type = "generator"  # “plane”, “usd”, and “generator”
        self.scene.terrain.terrain_generator = STAIR_TERRAINS_CFG

        # ------------------------------Observations------------------------------
        self.observations.policy.base_lin_vel.scale = 2.0
        self.observations.policy.base_ang_vel.scale = 0.25
        self.observations.policy.joint_pos.scale = 1.0
        self.observations.policy.joint_vel.scale = 0.05
        self.observations.policy.base_lin_vel = None
        # Height scan enabled for terrain perception (stair climbing)
        # self.observations.policy.height_scan = None
        self.observations.policy.joint_pos.params["asset_cfg"].joint_names = self.joint_names
        self.observations.policy.joint_vel.params["asset_cfg"].joint_names = self.joint_names

        # ------------------------------Actions------------------------------
        # Action scale for stair climbing - larger scale for HIP/KNEE to enable leg lifting
        self.actions.joint_pos.scale = {
            ".*_ABAD_JOINT": 0.15,   # Abduction: moderate (sideways movement)
            ".*_HIP_JOINT": 0.4,     # Hip: larger for leg swing/lifting
            ".*_KNEE_JOINT": 0.4,    # Knee: larger for leg extension
        }
        self.actions.joint_pos.clip = {".*": (-100.0, 100.0)}
        self.actions.joint_pos.joint_names = self.joint_names

        # ------------------------------Events------------------------------
        self.events.randomize_reset_base.params = {
            "pose_range": {
                "x": (-0.5, 0.5),
                "y": (-0.5, 0.5),
                "z": (0.0, 0.2),
                "roll": (-3.14, 3.14),
                "pitch": (-3.14, 3.14),
                "yaw": (-3.14, 3.14),
            },
            "velocity_range": {
                "x": (-0.5, 0.5),
                "y": (-0.5, 0.5),
                "z": (-0.5, 0.5),
                "roll": (-0.5, 0.5),
                "pitch": (-0.5, 0.5),
                "yaw": (-0.5, 0.5),
            },
        }
        self.events.randomize_rigid_body_mass_base.params["asset_cfg"].body_names = [self.base_link_name]
        self.events.randomize_rigid_body_mass_others.params["asset_cfg"].body_names = [
            f"^(?!.*{self.base_link_name}).*"
        ]
        self.events.randomize_com_positions.params["asset_cfg"].body_names = [self.base_link_name]
        self.events.randomize_apply_external_force_torque.params["asset_cfg"].body_names = [self.base_link_name]

        # ------------------------------Rewards------------------------------
        # General
        self.rewards.is_terminated.weight = 0

        # Root penalties
        self.rewards.lin_vel_z_l2.weight = -2.0  # Vertical velocity penalty
        self.rewards.ang_vel_xy_l2.weight = -0.05  # Angular velocity penalty
        self.rewards.flat_orientation_l2.weight = 0  # Flat orientation penalty
        self.rewards.base_height_l2.weight = 0  # Base height penalty
        self.rewards.base_height_l2.params["target_height"] = 0.32
        self.rewards.base_height_l2.params["asset_cfg"].body_names = [self.base_link_name]
        self.rewards.body_lin_acc_l2.weight = 0  # Body linear acceleration penalty
        self.rewards.body_lin_acc_l2.params["asset_cfg"].body_names = [self.base_link_name]

        # Joint penalties
        self.rewards.joint_torques_l2.weight = -2.5e-5
        self.rewards.joint_vel_l2.weight = 0
        self.rewards.joint_acc_l2.weight = -2.5e-7
        # self.rewards.create_joint_deviation_l1_rewterm("joint_deviation_hip_l1", -0.2, [".*_hip_joint"])
        self.rewards.joint_pos_limits.weight = -5.0
        self.rewards.joint_vel_limits.weight = 0
        self.rewards.joint_power.weight = -2e-5
        self.rewards.stand_still.weight = -2.0
        self.rewards.joint_pos_penalty.weight = -0.3  # Reduced to allow climbing poses
        self.rewards.joint_mirror.weight = -0.05
        self.rewards.joint_mirror.params["mirror_joints"] = [
            ["FAR_(ABAD|HIP|KNEE).*", "RBL_(ABAD|HIP|KNEE).*"],
            ["FBL_(ABAD|HIP|KNEE).*", "RAR_(ABAD|HIP|KNEE).*"],
        ]

        # Action penalties
        self.rewards.action_rate_l2.weight = -0.01

        # Contact sensor
        self.rewards.undesired_contacts.weight = -1.0
        self.rewards.undesired_contacts.params["sensor_cfg"].body_names = [f"^(?!.*{self.foot_link_name}).*"]
        self.rewards.contact_forces.weight = -1.5e-4
        self.rewards.contact_forces.params["sensor_cfg"].body_names = [self.foot_link_name]

        # Velocity-tracking rewards
        self.rewards.track_lin_vel_xy_exp.weight = 3.0
        self.rewards.track_ang_vel_z_exp.weight = 1.5

        # Others
        self.rewards.feet_air_time.weight = 0.5  # Increased to encourage leg lifting
        self.rewards.feet_air_time.params["threshold"] = 0.4
        self.rewards.feet_air_time.params["sensor_cfg"].body_names = [self.foot_link_name]
        self.rewards.feet_air_time_variance.weight = -1.0
        self.rewards.feet_air_time_variance.params["sensor_cfg"].body_names = [self.foot_link_name]
        self.rewards.feet_contact.weight = 0
        self.rewards.feet_contact.params["sensor_cfg"].body_names = [self.foot_link_name]
        self.rewards.feet_contact_without_cmd.weight = 0.1
        self.rewards.feet_contact_without_cmd.params["sensor_cfg"].body_names = [self.foot_link_name]
        self.rewards.feet_stumble.weight = 0
        self.rewards.feet_stumble.params["sensor_cfg"].body_names = [self.foot_link_name]
        self.rewards.feet_slide.weight = -0.1
        self.rewards.feet_slide.params["sensor_cfg"].body_names = [self.foot_link_name]
        self.rewards.feet_slide.params["asset_cfg"].body_names = [self.foot_link_name]
        self.rewards.feet_height.weight = 0
        self.rewards.feet_height.params["target_height"] = 0.05
        self.rewards.feet_height.params["asset_cfg"].body_names = [self.foot_link_name]
        self.rewards.feet_height_body.weight = -2.0  # Reduced to allow higher foot lifts
        self.rewards.feet_height_body.params["target_height"] = -0.35  # Allow feet to lift higher for climbing
        self.rewards.feet_height_body.params["asset_cfg"].body_names = [self.foot_link_name]
        self.rewards.feet_gait.weight = 0.2  # Reduced to allow more flexible gait during climbing
        self.rewards.feet_gait.params["synced_feet_pair_names"] = (
            ("FL_FOOT_LINK", "RR_FOOT_LINK"),
            ("FR_FOOT_LINK", "RL_FOOT_LINK"),
        )
        self.rewards.upward.weight = 0.6  # Reduced - too easy to achieve by standing

        # Climbing rewards - phased approach
        # Phase 1: Align robot heading with commanded velocity direction
        self.rewards.heading_alignment.weight = 2.0
        self.rewards.heading_alignment.params["std"] = 0.5
        # Phase 2: Reward forward progress + elevation gain (only when aligned)
        self.rewards.climbing_progress.weight = 1.5
        self.rewards.climbing_progress.params["alignment_threshold"] = 0.1  # 0.7=>45°/0.3=>30°/0.1=>10° tolerance
        self.rewards.climbing_progress.params["forward_weight"] = 1.0
        self.rewards.climbing_progress.params["elevation_weight"] = 2.0

        # If the weight of rewards is 0, set rewards to None
        if self.__class__.__name__ == "ZsibotZSL1StairEnvCfg":
            self.disable_zero_weight_rewards()

        # ------------------------------Terminations------------------------------
        # self.terminations.illegal_contact.params["sensor_cfg"].body_names = [self.base_link_name, ".*_hip"]
        self.terminations.illegal_contact = None

        # ------------------------------Curriculums------------------------------
        # self.curriculum.command_levels_lin_vel.params["range_multiplier"] = (0.2, 1.0)
        # self.curriculum.command_levels_ang_vel.params["range_multiplier"] = (0.2, 1.0)
        self.curriculum.command_levels_lin_vel = None
        self.curriculum.command_levels_ang_vel = None

        # ------------------------------Commands------------------------------
        # self.commands.base_velocity.ranges.lin_vel_x = (-1.0, 1.0)
        self.commands.base_velocity.ranges.lin_vel_x = (0.0, 1.0)  # Forward movement only, no backward movement
        # self.commands.base_velocity.ranges.lin_vel_y = (-0.5, 0.5)
        self.commands.base_velocity.ranges.lin_vel_y = (-0.0, 0.0)  # No lateral movement
        self.commands.base_velocity.ranges.ang_vel_z = (-1.0, 1.0)
        # self.commands.base_velocity.ranges.ang_vel_z = (-0.0, 0.0)
        self.commands.base_velocity.ranges.heading = (-math.pi, math.pi)
