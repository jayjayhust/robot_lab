# Copyright (c) 2024-2025 jayjayhust
# SPDX-License-Identifier: Apache-2.0

import isaaclab.sim as sim_utils
from isaaclab.actuators import DCMotorCfg, ImplicitActuatorCfg
from isaaclab.assets.articulation import ArticulationCfg

from robot_lab.assets import ISAACLAB_ASSETS_DATA_DIR

##
# Configuration
##

OPENDOGE_APX_CFG = ArticulationCfg(
    spawn=sim_utils.UrdfFileCfg(
        fix_base=False,
        merge_fixed_joints=True,
        replace_cylinders_with_capsules=False,
        asset_path=f"{ISAACLAB_ASSETS_DATA_DIR}/Robots/opendoge/apx_description/urdf/apx_description.urdf",
        activate_contact_sensors=True,
        rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=False,
            retain_accelerations=False,
            linear_damping=0.0,
            angular_damping=0.0,
            max_linear_velocity=1000.0,
            max_angular_velocity=1000.0,
            max_depenetration_velocity=1.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            enabled_self_collisions=False, solver_position_iteration_count=4, solver_velocity_iteration_count=0
        ),
        joint_drive=sim_utils.UrdfConverterCfg.JointDriveCfg(
            gains=sim_utils.UrdfConverterCfg.JointDriveCfg.PDGainsCfg(stiffness=0, damping=0)
        ),
    ),
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 0.4),
        joint_pos={
            ".*_hip_joint": 0.0,
            ".*_thigh_joint": 0.43,
            ".*_calf_joint": -1.04,  # -0.86,
        },
        joint_vel={".*": 0.0},
    ),
    soft_joint_pos_limit_factor=0.9,
    actuators={
        # "base_legs": DCMotorCfg(
        #     joint_names_expr=[".*_hip_joint", ".*_thigh_joint", ".*_calf_joint"],
        #     # effort_limit=28,
        #     # saturation_effort=28,
        #     # velocity_limit=28,
        #     effort_limit=1.8,  # 降低力矩限制(robstride eduLite05 spec: 额定负载1.8N.m)
        #     saturation_effort=1.8,  # 电机峰值力矩（峰值负载: 6N.m)
        #     velocity_limit=5,  # 降低速度限制(robstride eduLite05 spec)
        #     stiffness=20.0,  # stiffness gains (also known as p-gain) of the joints in the group.
        #     damping=0.7,  # damping gains (also known as d-gain) of the joints in the group.
        #     friction=0.0
        # ),
        # hips 和 thighs 组的配置
        "base_legs_hip_thigh": DCMotorCfg(
            joint_names_expr=[".*_hip_joint", ".*_thigh_joint"],
            effort_limit=6,  # 额定负载
            saturation_effort=6,  # 峰值力矩
            velocity_limit=5,  # 速度限制
            stiffness=20.0,
            damping=0.7,
            friction=0.0,
        ),
        # calf_joint 的配置：基于 thigh_joint 的 1.5 倍扭矩
        "base_legs_calf": DCMotorCfg(
            joint_names_expr=[".*_calf_joint"],
            # effort_limit=4 * 1.5,  # thigh_joint 力矩的 1.5 倍
            effort_limit=6 * 1.0,  # thigh_joint 力矩的 1.0 倍
            # saturation_effort=4 * 1.5,  # 峰值力矩
            saturation_effort=6 * 1.0,  # 峰值力矩
            velocity_limit=5,  # 保持速度限制为 thigh_joint 一致，若模型有需求可调整
            stiffness=20.0,  # stiffness 与 thigh_joint 保持一致
            damping=0.7,  # damping 与 thigh_joint 保持一致
            friction=0.0,
        ),
    },
)

"""Configuration of opendoge quadruped."""
