from __future__ import annotations

from dataclasses import MISSING
from typing import Literal

from isaaclab.utils import configclass

# parkour项目里是直接包含了isaaclab_rl的源码，直接进行了修改RslRlPpoActorCriticCfg
# robot_lab是新的项目架构，不包含isaaclab_rl的源码，所以需要自定义新的RslRlCustomPpoActorCriticCfg
# https://github.com/jayjayhust/extreme-quadruped-parkour/blob/self-dev/source/isaaclab_rl/isaaclab_rl/rsl_rl/rl_cfg.py
@configclass
class RslRlCustomPpoActorCriticCfg:
    """Configuration for the PPO actor-critic networks."""

    class_name: str = "ActorCritic"
    """The policy class name. Default is ActorCritic."""

    init_noise_std: float = MISSING
    """The initial noise standard deviation for the policy."""

    noise_std_type: Literal["scalar", "log"] = "scalar"
    """The type of noise standard deviation for the policy. Default is scalar."""

    actor_hidden_dims: list[int] = MISSING
    """The hidden dimensions of the actor network."""

    critic_hidden_dims: list[int] = MISSING
    """The hidden dimensions of the critic network."""

    activation: str = MISSING
    """The activation function for the actor and critic networks."""

    # optional custom encoders
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