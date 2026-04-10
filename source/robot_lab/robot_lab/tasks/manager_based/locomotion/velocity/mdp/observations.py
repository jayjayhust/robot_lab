# Copyright (c) 2024-2026 Ziqi Fan
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

from typing import TYPE_CHECKING

import torch

from isaaclab.assets import Articulation
from isaaclab.managers import SceneEntityCfg

if TYPE_CHECKING:
    from isaaclab.envs import ManagerBasedEnv, ManagerBasedRLEnv


def joint_pos_rel_without_wheel(
    env: ManagerBasedEnv,
    asset_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
    wheel_asset_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
) -> torch.Tensor:
    """The joint positions of the asset w.r.t. the default joint positions.(Without the wheel joints)"""
    # extract the used quantities (to enable type-hinting)
    asset: Articulation = env.scene[asset_cfg.name]
    joint_pos_rel = asset.data.joint_pos[:, asset_cfg.joint_ids] - asset.data.default_joint_pos[:, asset_cfg.joint_ids]
    joint_pos_rel[:, wheel_asset_cfg.joint_ids] = 0
    return joint_pos_rel


def phase(env: ManagerBasedRLEnv, cycle_time: float) -> torch.Tensor:
    if not hasattr(env, "episode_length_buf") or env.episode_length_buf is None:
        env.episode_length_buf = torch.zeros(env.num_envs, device=env.device, dtype=torch.long)
    phase = env.episode_length_buf[:, None] * env.step_dt / cycle_time
    phase_tensor = torch.cat([torch.sin(2 * torch.pi * phase), torch.cos(2 * torch.pi * phase)], dim=-1)
    return phase_tensor


def feet_height_in_body_frame(
    env: ManagerBasedEnv,
    asset_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
) -> torch.Tensor:
    """The feet height relative to body frame.

    This observation is useful for complex terrain (e.g., stairs) where the critic needs to
    understand the relative height of feet to the body for better value estimation.

    Args:
        env: The environment.
        asset_cfg: The SceneEntity associated with the robot. Defaults to SceneEntityCfg("robot").
            body_names should specify the foot links.

    Returns:
        The feet height in body frame, shape is [num_envs, num_feet].
    """
    asset: Articulation = env.scene[asset_cfg.name]
    # Get foot positions in world frame
    foot_pos_w = asset.data.body_pos_w[:, asset_cfg.body_ids, 2]  # [num_envs, num_feet]
    # Get root position in world frame
    root_pos_w = asset.data.root_pos_w[:, 2]  # [num_envs]
    # Compute height relative to body
    feet_height = foot_pos_w - root_pos_w.unsqueeze(1)
    return feet_height

# REF1： https://isaac-sim.github.io/IsaacLab/main/source/api/lab/isaaclab.sensors.html#isaaclab.sensors.ContactSensorData.net_forces_w_history
def foot_contact_states(
    env: ManagerBasedEnv,
    sensor_cfg: SceneEntityCfg = SceneEntityCfg("contact_forces"),
    asset_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
    force_threshold: float = 1.0,
) -> torch.Tensor:
    """Binary foot contact states based on contact force threshold.

    This observation provides binary flags indicating whether each foot is in contact with the ground.
    A foot is considered in contact when the norm of the contact force exceeds the threshold.

    Args:
        env: The environment.
        sensor_cfg: The SceneEntityCfg for the contact sensor. Defaults to SceneEntityCfg("contact_forces").
            body_names should specify the foot links.
        asset_cfg: The SceneEntityCfg for the robot asset. Defaults to SceneEntityCfg("robot").
        force_threshold: The force threshold to determine contact. Defaults to 1.0.

    Returns:
        Binary contact flags for each foot, shape is [num_envs, num_feet].
        1.0 indicates contact, 0.0 indicates no contact.
    """
    from isaaclab.sensors import ContactSensor

    contact_sensor: ContactSensor = env.scene.sensors[sensor_cfg.name]
    # Get the latest contact forces from history: [num_envs, history_len, num_bodies, 3]
    net_contact_forces = contact_sensor.data.net_forces_w_history
    # Use the most recent frame and compute force norm for specified bodies
    foot_force_norm = torch.norm(net_contact_forces[:, -1, sensor_cfg.body_ids], dim=-1)
    # Binary contact flags: 1.0 when contact force exceeds threshold
    foot_contacts = (foot_force_norm > force_threshold).float()
    return foot_contacts

def height_scan_encoded(
    env: ManagerBasedEnv,
    sensor_cfg: SceneEntityCfg = SceneEntityCfg("height_scanner"),
    in_dim: int = 187,
    encoder_dims: list[int] | tuple[int, ...] = (128, 64, 32),
    activation: str = "elu",
) -> torch.Tensor:
    """Height scan observation encoded through a neural network.

    This function processes raw height scan observations (e.g., 187D from a grid ray-caster)
    through a learned encoder to produce a compact latent representation (e.g., 32D).
    The encoder is lazily created and cached on the env object on first call.

    Architecture: Linear(in_dim, dims[0]) -> activation -> ... -> Linear(dims[-2], dims[-1]) -> Tanh

    Args:
        env: The environment.
        sensor_cfg: The SceneEntityCfg for the height scanner sensor.
        in_dim: Input dimension of the height scan (e.g., 187 for 17x11 grid at 0.1m resolution).
        encoder_dims: Hidden layer dimensions. The last element determines the output latent dimension.
        activation: Activation function name ('relu', 'elu', etc.). Defaults to 'elu'.

    Returns:
        Encoded height scan tensor of shape [num_envs, latent_dim].
    """
    import torch.nn as nn
    from isaaclab.sensors import RayCaster

    # Lazily create and cache the encoder on the env object
    if not hasattr(env, "_height_scan_encoder"):
        # Resolve activation function
        act_map = {
            "relu": nn.ReLU,
            "elu": nn.ELU,
            "tanh": nn.Tanh,
            "selu": nn.SELU,
            "leaky_relu": nn.LeakyReLU,
        }
        act_cls = act_map.get(activation.lower(), nn.ELU)

        layers = []
        _in_dim = in_dim
        for i, out_dim in enumerate(encoder_dims):
            layers.append(nn.Linear(_in_dim, out_dim))
            if i == len(encoder_dims) - 1:
                layers.append(nn.Tanh())
            else:
                layers.append(act_cls())
            _in_dim = out_dim
        env._height_scan_encoder = nn.Sequential(*layers)

    encoder = env._height_scan_encoder

    # Get raw height scan data
    scanner: RayCaster = env.scene.sensors[sensor_cfg.name]
    height_scan = scanner.data.ray_hits_w[..., 2] - env.scene["robot"].data.root_pos_w[:, 2:3]

    # Move encoder to same device and dtype as the data
    if encoder[0].weight.device != height_scan.device:
        env._height_scan_encoder = encoder.to(device=height_scan.device, dtype=height_scan.dtype)
        encoder = env._height_scan_encoder

    # Encode: [num_envs, in_dim] -> [num_envs, out_dim]
    z_scan = encoder(height_scan)
    return z_scan


# ---- Domain randomization(dr) privileged observations ----
# These capture the actual DR values from PhysX after startup events.
# Values are lazily captured on first call and cached on the env object.


def base_mass(
    env: ManagerBasedEnv,
    asset_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
) -> torch.Tensor:
    """Base body mass after domain randomization (1D).

    Captures the actual mass of the base body from PhysX after startup domain randomization.
    The value is lazily captured on first call and cached.

    Args:
        env: The environment.
        asset_cfg: SceneEntityCfg for the robot. body_names should specify the base link.

    Returns:
        Base mass tensor of shape [num_envs, 1].
    """
    if not hasattr(env, "_dr_base_mass"):
        asset: Articulation = env.scene[asset_cfg.name]
        try:
            masses = asset.root_physx_view.get_masses().to(env.device)
            base_mass = masses[:, asset_cfg.body_ids[0]]
            if base_mass.dim() > 2:
                base_mass = base_mass.squeeze(1)
            env._dr_base_mass = base_mass.view(-1, 1)
        except Exception:
            if getattr(asset.data, "default_mass", None) is not None:
                env._dr_base_mass = asset.data.default_mass[:, asset_cfg.body_ids[0]].view(-1, 1)
            else:
                env._dr_base_mass = torch.ones(env.num_envs, 1, device=env.device)
    return env._dr_base_mass


def base_com(
    env: ManagerBasedEnv,
    asset_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
) -> torch.Tensor:
    """Base body center of mass after domain randomization (3D).

    Captures the actual COM of the base body from PhysX after startup domain randomization.
    The value is lazily captured on first call and cached.

    Args:
        env: The environment.
        asset_cfg: SceneEntityCfg for the robot. body_names should specify the base link.

    Returns:
        Base COM tensor of shape [num_envs, 3].
    """
    if not hasattr(env, "_dr_base_com"):
        asset: Articulation = env.scene[asset_cfg.name]
        try:
            coms = asset.root_physx_view.get_coms().to(env.device)
            base_com = coms[:, asset_cfg.body_ids[0], :3]
            if base_com.dim() > 3:
                base_com = base_com.squeeze(1)
            env._dr_base_com = base_com.view(-1, 3)
        except Exception:
            if getattr(asset.data, "body_com_pos_b", None) is not None:
                env._dr_base_com = asset.data.body_com_pos_b[:, asset_cfg.body_ids[0], :].view(-1, 3)
            else:
                env._dr_base_com = torch.zeros(env.num_envs, 3, device=env.device)
    return env._dr_base_com


def friction_coeff(
    env: ManagerBasedEnv,
) -> torch.Tensor:
    """Terrain static friction coefficient from physics material (1D).

    The value is lazily captured on first call and cached.

    Args:
        env: The environment.

    Returns:
        Static friction coefficient tensor of shape [num_envs, 1].
    """
    if not hasattr(env, "_dr_friction"):
        try:
            terrain_cfg = env.cfg.scene.terrain
            if hasattr(terrain_cfg, "physics_material") and terrain_cfg.physics_material is not None:
                pm = terrain_cfg.physics_material
                friction = torch.tensor(
                    [float(pm.static_friction)],
                    device=env.device,
                    dtype=torch.float32,
                )
                env._dr_friction = friction.unsqueeze(0).expand(env.num_envs, -1).clone()
            else:
                env._dr_friction = torch.ones(env.num_envs, 1, device=env.device)
        except Exception:
            env._dr_friction = torch.ones(env.num_envs, 1, device=env.device)
    return env._dr_friction


def p_gain_scale(
    env: ManagerBasedEnv,
    asset_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
) -> torch.Tensor:
    """Joint stiffness (P gain) scale relative to defaults after domain randomization.

    Computes the ratio of current actuator stiffness to default stiffness for each joint.
    A value of 1.0 means no change from default. Lazily captured and cached.

    Args:
        env: The environment.
        asset_cfg: SceneEntityCfg for the robot. joint_names should specify the joints.

    Returns:
        P gain scale tensor of shape [num_envs, num_selected_joints].
    """
    if not hasattr(env, "_dr_p_gain_scale"):
        asset: Articulation = env.scene[asset_cfg.name]
        joint_ids = asset_cfg.joint_ids

        # Build current stiffness from all actuators
        cur_stiffness = torch.zeros(env.num_envs, asset.num_joints, device=env.device)
        for actuator in asset.actuators.values():
            cur_stiffness[:, actuator.joint_indices] = actuator.stiffness

        # Compute scale for specified joints
        default_stiffness = asset.data.default_joint_stiffness[:, joint_ids]
        sel_current = cur_stiffness[:, joint_ids]
        scale = torch.ones_like(sel_current)
        nonzero = torch.abs(default_stiffness) > 1e-6
        scale[nonzero] = sel_current[nonzero] / default_stiffness[nonzero]
        env._dr_p_gain_scale = scale
    return env._dr_p_gain_scale


def d_gain_scale(
    env: ManagerBasedEnv,
    asset_cfg: SceneEntityCfg = SceneEntityCfg("robot"),
) -> torch.Tensor:
    """Joint damping (D gain) scale relative to defaults after domain randomization.

    Computes the ratio of current actuator damping to default damping for each joint.
    A value of 1.0 means no change from default. Lazily captured and cached.

    Args:
        env: The environment.
        asset_cfg: SceneEntityCfg for the robot. joint_names should specify the joints.

    Returns:
        D gain scale tensor of shape [num_envs, num_selected_joints].
    """
    if not hasattr(env, "_dr_d_gain_scale"):
        asset: Articulation = env.scene[asset_cfg.name]
        joint_ids = asset_cfg.joint_ids

        # Build current damping from all actuators
        cur_damping = torch.zeros(env.num_envs, asset.num_joints, device=env.device)
        for actuator in asset.actuators.values():
            cur_damping[:, actuator.joint_indices] = actuator.damping

        # Compute scale for specified joints
        default_damping = asset.data.default_joint_damping[:, joint_ids]
        sel_current = cur_damping[:, joint_ids]
        scale = torch.ones_like(sel_current)
        nonzero = torch.abs(default_damping) > 1e-6
        scale[nonzero] = sel_current[nonzero] / default_damping[nonzero]
        env._dr_d_gain_scale = scale
    return env._dr_d_gain_scale

