# Copyright (c) 2022-2025, The Isaac Lab Project Developers (https://github.com/isaac-sim/IsaacLab/blob/main/CONTRIBUTORS.md).
# All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause

"""RSL-RL PPO runner configs for Go2 parkour manager-based environments.

Self-contained: ActorCriticScan network and its config dataclass are defined
locally so this package does not depend on the direct/ workflow.
"""

from __future__ import annotations

from dataclasses import MISSING
from typing import Literal

from isaaclab.utils import configclass

from isaaclab_rl.rsl_rl import RslRlOnPolicyRunnerCfg, RslRlPpoAlgorithmCfg

# Local copy — no cross-dependency on direct/zsl1
from .actor_critic_scan import ActorCriticScan  # noqa: F401  (must be importable at runtime)

# Register custom class into rsl_rl runner's namespace so eval("ActorCriticScan") works
import rsl_rl.runners.on_policy_runner as _runner_mod

_runner_mod.ActorCriticScan = ActorCriticScan


# ---------------------------------------------------------------------------
# Policy config (replaces RslRlPpoActorCriticCfg for this package)
# ---------------------------------------------------------------------------


@configclass
class ActorCriticScanCfg:
    """Configuration for ActorCriticScan / ActorCritic networks."""

    class_name: str = "ActorCriticScan"
    """The policy class name. Default is ActorCriticScan."""

    init_noise_std: float = MISSING
    """The initial noise standard deviation for the policy."""

    noise_std_type: Literal["scalar", "log"] = "scalar"
    """The type of noise standard deviation. Default is scalar."""

    actor_hidden_dims: list[int] = MISSING
    """The hidden dimensions of the actor network."""

    critic_hidden_dims: list[int] = MISSING
    """The hidden dimensions of the critic network."""

    activation: str = MISSING
    """The activation function for the actor and critic networks."""

    # -- scan / privileged encoder knobs --

    num_prop_obs: int | None = None
    """Number of proprioceptive observations (for custom splits)."""

    num_scan_obs: int | None = None
    """Number of scan observations (for custom splits)."""

    num_actor_scan_obs: int | None = None
    """Number of scan observations for the actor (optional override)."""

    num_critic_scan_obs: int | None = None
    """Number of scan observations for the critic (optional override)."""

    scan_encoder_dims: list[int] | None = None
    """Hidden dims for scan encoder (if used)."""

    actor_scan_encoder_dims: list[int] | None = None
    """Hidden dims for actor scan encoder (optional override)."""

    critic_scan_encoder_dims: list[int] | None = None
    """Hidden dims for critic scan encoder (optional override)."""

    encode_scan_for_critic: bool = True
    """Whether to encode scan observations for critic inputs."""

    priv_obs_encoder_dims: list[int] | None = None
    """Hidden dims for critic priv_obs encoder (if used)."""

    priv_encoder_dims: list[int] | None = None
    """Legacy alias for priv_obs_encoder_dims (used by older checkpoints)."""


# ---------------------------------------------------------------------------
# Helper
# ---------------------------------------------------------------------------


def _make_zsl1_parkour_rough_policy_cfg(
    *,
    num_actor_scan_obs: int | None = None,
    num_critic_scan_obs: int | None = None,
    scan_encoder_dims: list[int] | None = None,
    actor_scan_encoder_dims: list[int] | None = None,
    critic_scan_encoder_dims: list[int] | None = None,
    encode_scan_for_critic: bool = True,
    priv_obs_encoder_dims: list[int] | None = None,
    priv_encoder_dims: list[int] | None = None,
) -> ActorCriticScanCfg:
    if priv_encoder_dims is None:
        priv_encoder_dims = priv_obs_encoder_dims
    return ActorCriticScanCfg(
        class_name="ActorCriticScan",
        init_noise_std=1.0,
        noise_std_type="log",
        actor_hidden_dims=[512, 256, 128],
        critic_hidden_dims=[512, 256, 128],
        activation="elu",
        num_prop_obs=52,
        num_scan_obs=187,
        num_actor_scan_obs=num_actor_scan_obs,
        num_critic_scan_obs=num_critic_scan_obs,
        scan_encoder_dims=scan_encoder_dims,
        actor_scan_encoder_dims=actor_scan_encoder_dims,
        critic_scan_encoder_dims=critic_scan_encoder_dims,
        encode_scan_for_critic=encode_scan_for_critic,
        priv_obs_encoder_dims=priv_obs_encoder_dims,
        priv_encoder_dims=priv_encoder_dims,
    )


# ---------------------------------------------------------------------------
# Runner configs
# ---------------------------------------------------------------------------


@configclass
class ZSL1ParkourFlatPPORunnerCfg(RslRlOnPolicyRunnerCfg):
    num_steps_per_env = 24
    max_iterations = 5000
    save_interval = 50
    experiment_name = "zsl1_parkour_flat"
    empirical_normalization = True
    policy = ActorCriticScanCfg(
        class_name="ActorCriticScan",
        init_noise_std=0.5,
        actor_hidden_dims=[512, 256, 128],
        critic_hidden_dims=[512, 256, 128],
        activation="elu",
        noise_std_type="log",
        num_prop_obs=52,
        num_scan_obs=0,
        scan_encoder_dims=[128, 64, 32],
    )
    algorithm = RslRlPpoAlgorithmCfg(
        value_loss_coef=1.0,
        use_clipped_value_loss=True,
        clip_param=0.2,
        entropy_coef=0.01,
        num_learning_epochs=5,
        num_mini_batches=4,
        learning_rate=1.0e-4,
        schedule="adaptive",
        gamma=0.99,
        lam=0.95,
        desired_kl=0.01,
        max_grad_norm=1.0,
    )


@configclass
class ZSL1ParkourRoughPPORunnerCfg(RslRlOnPolicyRunnerCfg):
    num_steps_per_env = 24
    max_iterations = 20000
    save_interval = 50
    experiment_name = "zsl1_parkour_rough"
    empirical_normalization = True
    policy = ActorCriticScanCfg(
        class_name="ActorCriticScan",
        init_noise_std=1.0,
        noise_std_type="log",
        actor_hidden_dims=[512, 256, 128],
        critic_hidden_dims=[512, 256, 128],
        activation="elu",
        num_prop_obs=52,
        num_scan_obs=187,
        scan_encoder_dims=[128, 64, 32],
    )
    algorithm = RslRlPpoAlgorithmCfg(
        value_loss_coef=1.0,
        use_clipped_value_loss=True,
        clip_param=0.2,
        entropy_coef=0.005,
        num_learning_epochs=5,
        num_mini_batches=4,
        learning_rate=1.0e-3,
        schedule="adaptive",
        gamma=0.99,
        lam=0.95,
        desired_kl=0.01,
        max_grad_norm=1.0,
    )


@configclass
class ZSL1ParkourRoughAbl1PPORunnerCfg(ZSL1ParkourRoughPPORunnerCfg):
    experiment_name = "zsl1_parkour_rough_abl1"
    policy = _make_zsl1_parkour_rough_policy_cfg(num_actor_scan_obs=0)


@configclass
class ZSL1ParkourRoughAbl2_5PPORunnerCfg(ZSL1ParkourRoughPPORunnerCfg):
    experiment_name = "zsl1_parkour_rough_abl2_5"
    policy = ActorCriticScanCfg(
        class_name="ActorCritic",
        init_noise_std=1.0,
        noise_std_type="log",
        actor_hidden_dims=[512, 256, 128],
        critic_hidden_dims=[512, 256, 128],
        activation="elu",
    )


@configclass
class ZSL1ParkourRoughAbl3_5PPORunnerCfg(ZSL1ParkourRoughPPORunnerCfg):
    experiment_name = "zsl1_parkour_rough_abl3_5"
    policy = _make_zsl1_parkour_rough_policy_cfg(scan_encoder_dims=[128, 64, 32])


@configclass
class ZSL1ParkourRoughAbl4_0PPORunnerCfg(ZSL1ParkourRoughPPORunnerCfg):
    experiment_name = "zsl1_parkour_rough_abl4_0"
    policy = _make_zsl1_parkour_rough_policy_cfg(
        scan_encoder_dims=[128, 64, 32],
        encode_scan_for_critic=False,
    )


@configclass
class ZSL1ParkourRoughAbl7_0PPORunnerCfg(ZSL1ParkourRoughPPORunnerCfg):
    experiment_name = "zsl1_parkour_rough_abl7_0"
    policy = _make_zsl1_parkour_rough_policy_cfg(
        scan_encoder_dims=[128, 64, 32],
        priv_encoder_dims=[64, 20],
    )
