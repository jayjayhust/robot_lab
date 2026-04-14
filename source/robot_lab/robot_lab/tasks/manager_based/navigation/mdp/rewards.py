# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

from __future__ import annotations

import torch
from typing import TYPE_CHECKING

from isaaclab.managers import SceneEntityCfg

if TYPE_CHECKING:
    from isaaclab.envs import ManagerBasedRLEnv


def position_command_error_tanh(env: ManagerBasedRLEnv, std: float, command_name: str) -> torch.Tensor:
    """Reward position tracking with tanh kernel."""
    command = env.command_manager.get_command(command_name)
    des_pos_b = command[:, :3]
    distance = torch.norm(des_pos_b, dim=1)
    return 1 - torch.tanh(distance / std)


def heading_command_error_abs(env: ManagerBasedRLEnv, command_name: str) -> torch.Tensor:
    """Penalize tracking orientation error."""
    command = env.command_manager.get_command(command_name)
    heading_b = command[:, 3]
    return heading_b.abs()


def standing_reward_near_target(
    env: ManagerBasedRLEnv,
    command_name: str,
    asset_cfg: "SceneEntityCfg" = None,
    near_target_threshold: float = 0.1,
) -> torch.Tensor:
    """Reward standing posture when near the target position.

    When the robot is within near_target_threshold distance of the pose command target,
    this reward penalizes leg joint deviation from default pose to encourage
    the robot to stand upright instead of crouching or stepping in place.
    """
    if asset_cfg is None:
        asset_cfg = SceneEntityCfg("robot")
    asset = env.scene[asset_cfg.name]

    # Calculate distance to target
    command = env.command_manager.get_command(command_name)
    des_pos_b = command[:, :3]
    distance = torch.norm(des_pos_b, dim=1)

    # Check if near target
    is_near = distance < near_target_threshold

    # Penalize leg joint deviation from default (encourage standing upright)
    # Use L1 norm of joint position error from default
    joint_pos = asset.data.joint_pos[:, asset_cfg.joint_ids]
    default_pos = asset.data.default_joint_pos[:, asset_cfg.joint_ids]
    joint_deviation = torch.sum(torch.abs(joint_pos - default_pos), dim=1)

    # Only apply reward when near target (negative = penalize deviation)
    reward = -joint_deviation * is_near.float()

    return reward
