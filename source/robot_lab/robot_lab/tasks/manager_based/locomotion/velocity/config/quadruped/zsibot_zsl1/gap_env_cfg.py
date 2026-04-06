# Copyright (c) 2024-2026 Ziqi Fan
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations
import math
import robot_lab.tasks.manager_based.locomotion.velocity.mdp as mdp
from robot_lab.tasks.manager_based.locomotion.velocity.velocity_env_cfg import LocomotionVelocityGapEnvCfg

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

##########################################################
# https://github.com/jayjayhust/extreme-quadruped-parkour/blob/self-dev/source/isaaclab/isaaclab/terrains/trimesh/mesh_terrains.py#L600
# import isaaclab.terrains.trimesh.mesh_terrains_cfg as mesh_terrains_cfg
import trimesh
import numpy as np
def gap_terrain(
    difficulty: float, cfg: MeshGapTerrainCfg
) -> tuple[list[trimesh.Trimesh], np.ndarray]:
    """Generate a terrain with a gap around the platform.

    The terrain has a ground with a platform in the middle. The platform is surrounded by a gap
    of width :obj:`gap_width` on all sides.

    .. image:: ../../_static/terrains/trimesh/gap_terrain.jpg
       :width: 40%
       :align: center

    Args:
        difficulty: The difficulty of the terrain. This is a value between 0 and 1.
        cfg: The configuration for the terrain.

    Returns:
        A tuple containing the tri-mesh of the terrain and the origin of the terrain (in m).
    """
    # resolve the terrain configuration
    gap_width = cfg.gap_width_range[0] + difficulty * (cfg.gap_width_range[1] - cfg.gap_width_range[0])

    # initialize list of meshes
    meshes_list = list()
    # constants for terrain generation
    terrain_height = 1.0
    terrain_center = (0.5 * cfg.size[0], 0.5 * cfg.size[1], -terrain_height / 2)

    # Generate the outer ring
    inner_size = (cfg.platform_width + 2 * gap_width, cfg.platform_width + 2 * gap_width)
    meshes_list += make_border(cfg.size, inner_size, terrain_height, terrain_center)
    # Generate the inner box
    box_dim = (cfg.platform_width, cfg.platform_width, terrain_height)
    box = trimesh.creation.box(box_dim, trimesh.transformations.translation_matrix(terrain_center))
    meshes_list.append(box)

    # specify the origin of the terrain
    origin = np.array([terrain_center[0], terrain_center[1], 0.0])

    return meshes_list, origin

def gap_strip_terrain(
    difficulty: float, cfg: MeshGapStripTerrainCfg
) -> tuple[list[trimesh.Trimesh], np.ndarray]:
    """Generate a repeated gap + landing strip along +X with a run-up platform."""
    gap_width = cfg.gap_width_range[0] + difficulty * (cfg.gap_width_range[1] - cfg.gap_width_range[0])
    landing_len = cfg.landing_length
    start_len = cfg.start_platform_length

    meshes_list: list[trimesh.Trimesh] = []
    terrain_height = 1.0
    z_center = -terrain_height / 2
    y_center = 0.5 * cfg.size[1]

    # start platform / x_ptr를 runup끝으로 이동
    x_ptr = 0.0
    start_dim = (start_len, cfg.size[1], terrain_height)
    start_center = (x_ptr + 0.5 * start_len, y_center, z_center)
    meshes_list.append(trimesh.creation.box(start_dim, trimesh.transformations.translation_matrix(start_center)))
    x_ptr += start_len

    # repeat [gap + landing] until size.x is filled
    while x_ptr + gap_width + landing_len <= cfg.size[0]:
        x_ptr += gap_width  # skip gap region (air)
        land_center = (x_ptr + 0.5 * landing_len, y_center, z_center)
        land_dim = (landing_len, cfg.size[1], terrain_height)
        meshes_list.append(trimesh.creation.box(land_dim, trimesh.transformations.translation_matrix(land_center)))
        x_ptr += landing_len

    # fill any remaining tail with flat ground to avoid an extra-long final gap
    if x_ptr < cfg.size[0]:
        tail_len = cfg.size[0] - x_ptr
        tail_center = (x_ptr + 0.5 * tail_len, y_center, z_center)
        tail_dim = (tail_len, cfg.size[1], terrain_height)
        meshes_list.append(trimesh.creation.box(tail_dim, trimesh.transformations.translation_matrix(tail_center)))

    origin = np.array([start_len * 0.5, y_center, 0.0])
    return meshes_list, origin

# https://github.com/jayjayhust/extreme-quadruped-parkour/blob/self-dev/source/isaaclab/isaaclab/terrains/trimesh/mesh_terrains_cfg.py#L194
from isaaclab.terrains.sub_terrain_cfg import SubTerrainBaseCfg
from dataclasses import MISSING
@configclass
class MeshGapTerrainCfg(SubTerrainBaseCfg):
    """Configuration for a terrain with a gap around the platform."""

    function = gap_terrain

    gap_width_range: tuple[float, float] = MISSING
    """The minimum and maximum width of the gap (in m)."""
    platform_width: float = 1.0
    """The width of the square platform at the center of the terrain. Defaults to 1.0."""

@configclass
class MeshGapStripTerrainCfg(SubTerrainBaseCfg):
    """Configuration for a repeated gap-and-landing strip along +X."""

    function = gap_strip_terrain

    gap_width_range: tuple[float, float] = MISSING
    """The minimum and maximum width of the gaps (in m)."""
    landing_length: float = 0.5
    """Length of each landing platform between gaps (in m)."""
    start_platform_length: float = 3.0
    """Length of the initial run-up platform (in m)."""
    platform_width: float = 3.0
    """Alias for the run-up platform length for spawn clamping."""
##########################################################

GAP_TERRAINS_CFG = TerrainGeneratorCfg(
    size=(23.0, 6.0),  # Terrain Size 23m X 6m
    # border_width=10.0,  # The width of the border around the terrain (in m)
    num_rows=10,  # Number of rows of sub-terrains to generate
    num_cols=10,  # Number of columns of sub-terrains to generate. gap occupy 10 columns
    # horizontal_scale=0.1,  # Horizontal scale of the terrain (in m)
    # vertical_scale=0.005,  # Vertical scale of the terrain (in m)
    # slope_threshold=0.75,  # The slope threshold above which surfaces are made vertical (in rad)
    # use_cache=False,
    # REF1: https://github.com/isaac-sim/IsaacLab/blob/main/source/isaaclab/isaaclab/terrains/sub_terrain_cfg.py
    # REF2: https://github.com/jayjayhust/extreme-quadruped-parkour/blob/self-dev/source/isaaclab_tasks/isaaclab_tasks/direct/go2/go2_env_cfg.py
    sub_terrains={
        "gap_bar": MeshGapStripTerrainCfg(
            proportion=(3 / 18),
            size=(23.0, 23.0),
            gap_width_range=(0.1, 0.8),
            landing_length=0.45,
            start_platform_length=8.0,  # longer run-up for the gap strip
        ),
    },
)
"""Gap terrains configuration."""

@configclass
class ZsibotZSL1GapEnvCfg(LocomotionVelocityGapEnvCfg):
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
        self.scene.terrain.terrain_generator = GAP_TERRAINS_CFG

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
        # Increased for 0.23m max step height (was 0.4 for 0.15m steps)
        self.actions.joint_pos.scale = {
            ".*_ABAD_JOINT": 0.2,    # Abduction: moderate (sideways movement)
            ".*_HIP_JOINT": 0.6,     # Hip: larger for leg swing/lifting (0.23m steps need more)
            ".*_KNEE_JOINT": 0.6,    # Knee: larger for leg extension (0.23m steps need more)
        }
        self.actions.joint_pos.clip = {".*": (-100.0, 100.0)}
        self.actions.joint_pos.joint_names = self.joint_names

        # ------------------------------Events------------------------------
        self.events.randomize_reset_base.params = {
            "pose_range": {
                "x": (-0.5, 0.5),
                "y": (-0.5, 0.5),
                "z": (0.0, 0.2),
                # "roll": (-3.14, 3.14),
                # "pitch": (-3.14, 3.14),
                "roll": (-0.5, 0.5),  # Limited roll range for stability
                "pitch": (-0.5, 0.5),  # Limited pitch range for stability
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
        self.rewards.lin_vel_z_l2.weight = -1.0  # Moderate penalty to discourage jumping while allowing climbing
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
        self.rewards.joint_acc_l2.weight = -5.0e-7
        # self.rewards.create_joint_deviation_l1_rewterm("joint_deviation_hip_l1", -0.2, [".*_hip_joint"])
        self.rewards.joint_pos_limits.weight = -5.0
        self.rewards.joint_vel_limits.weight = 0
        self.rewards.joint_power.weight = -1e-5  # -2e-5(strong penalty)/-1e-5(weak penalty)
        self.rewards.stand_still.weight = -2.0
        self.rewards.joint_pos_penalty.weight = -0.1  # Further reduced to allow extreme joint positions for 0.23m steps
        self.rewards.joint_mirror.weight = -0.05
        self.rewards.joint_mirror.params["mirror_joints"] = [
            ["FAR_(ABAD|HIP|KNEE).*", "RBL_(ABAD|HIP|KNEE).*"],
            ["FBL_(ABAD|HIP|KNEE).*", "RAR_(ABAD|HIP|KNEE).*"],
        ]

        # Action penalties
        self.rewards.action_rate_l2.weight = -0.02  # Increased to smooth out jumping motions

        # Contact sensor
        self.rewards.undesired_contacts.weight = -1.0
        self.rewards.undesired_contacts.params["sensor_cfg"].body_names = [f"^(?!.*{self.foot_link_name}).*"]
        self.rewards.contact_forces.weight = -1.5e-4
        self.rewards.contact_forces.params["sensor_cfg"].body_names = [self.foot_link_name]

        # Velocity-tracking rewards - reduced to prioritize climbing
        self.rewards.track_lin_vel_xy_exp.weight = 1.5
        self.rewards.track_ang_vel_z_exp.weight = 0.5

        # Others
        self.rewards.feet_air_time.weight = 0.8  # Reduced to discourage jumping
        self.rewards.feet_air_time.params["threshold"] = 0.35  # Lower threshold for controlled stepping
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
        self.rewards.feet_height_body.weight = -0.5  # Further reduced to allow higher foot lifts for 0.23m steps
        self.rewards.feet_height_body.params["target_height"] = -0.15  # Allow feet to lift higher (0.23m step clearance)
        self.rewards.feet_height_body.params["asset_cfg"].body_names = [self.foot_link_name]
        self.rewards.feet_gait.weight = 0.15  # Reduced to allow more flexible gait during climbing
        self.rewards.feet_gait.params["synced_feet_pair_names"] = (
            ("FL_FOOT_LINK", "RR_FOOT_LINK"),
            ("FR_FOOT_LINK", "RL_FOOT_LINK"),
        )
        self.rewards.upward.weight = 0.15  # Slightly increased to maintain some horizontal posture

        # Climbing rewards - balanced for controlled stepping
        self.rewards.heading_alignment.weight = 0  # Removed heading alignment requirement
        self.rewards.climbing_progress.weight = 2.5  # Balanced to encourage climbing without jumping
        self.rewards.climbing_progress.params["alignment_threshold"] = 0.0  # No alignment requirement
        self.rewards.climbing_progress.params["forward_weight"] = 4.0  # Add forward progress to encourage walking up
        self.rewards.climbing_progress.params["elevation_weight"] = 5.0  # Moderate elevation reward

        # If the weight of rewards is 0, set rewards to None
        if self.__class__.__name__ == "ZsibotZSL1GapEnvCfg":
            self.disable_zero_weight_rewards()

        # ------------------------------Terminations------------------------------
        # self.terminations.illegal_contact.params["sensor_cfg"].body_names = [self.base_link_name, ".*_ABAD"]
        self.terminations.illegal_contact = None

        # ------------------------------Curriculums------------------------------
        # self.curriculum.command_levels_lin_vel.params["range_multiplier"] = (0.2, 1.0)
        # self.curriculum.command_levels_ang_vel.params["range_multiplier"] = (0.2, 1.0)
        self.curriculum.command_levels_lin_vel = None
        self.curriculum.command_levels_ang_vel = None
        self.curriculum.terrain_levels = None  # No terrain levels

        # ------------------------------Commands------------------------------
        self.commands.base_velocity.resampling_time_range = (10.0, 10.0)  # Resample command every 10.0 to 10.0 seconds
        self.commands.base_velocity.rel_standing_envs = 0.02  # 2% of environments are standing environments
        self.commands.base_velocity.rel_heading_envs = 1.0  # 100% of environments are heading environments
        self.commands.base_velocity.heading_command = False  # Disable heading command, let robot rotate freely
        # self.commands.base_velocity.ranges.lin_vel_x = (-1.0, 1.0)  # X-axis
        self.commands.base_velocity.ranges.lin_vel_x = (0.0, 0.5)  # X-axis: Forward movement only, no backward movement
        # self.commands.base_velocity.ranges.lin_vel_y = (-0.5, 0.5)  # Y-axis
        self.commands.base_velocity.ranges.lin_vel_y = (-0.0, 0.0)  # Y-axis: No lateral movement
        self.commands.base_velocity.ranges.ang_vel_z = (-1.0, 1.0)  # Z-axis
        # self.commands.base_velocity.ranges.ang_vel_z = (-0.0, 0.0)  # Z-axis
        self.commands.base_velocity.ranges.heading = (-math.pi, math.pi)
