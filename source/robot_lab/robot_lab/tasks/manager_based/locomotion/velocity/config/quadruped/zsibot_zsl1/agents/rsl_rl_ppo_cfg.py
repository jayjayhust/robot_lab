# Copyright (c) 2024-2026 Ziqi Fan
# SPDX-License-Identifier: Apache-2.0

from isaaclab.utils import configclass

from isaaclab_rl.rsl_rl import RslRlOnPolicyRunnerCfg, RslRlPpoActorCriticCfg, RslRlPpoAlgorithmCfg


@configclass
class ZsibotZSL1RoughPPORunnerCfg(RslRlOnPolicyRunnerCfg):
    num_steps_per_env = 24
    max_iterations = 50000
    save_interval = 100
    experiment_name = "zsibot_zsl1_rough"
    policy = RslRlPpoActorCriticCfg(
        init_noise_std=1.0,
        actor_obs_normalization=False,
        critic_obs_normalization=False,
        actor_hidden_dims=[512, 256, 128],
        critic_hidden_dims=[512, 256, 128],
        activation="elu",
    )
    algorithm = RslRlPpoAlgorithmCfg(
        value_loss_coef=1.0,
        use_clipped_value_loss=True,
        clip_param=0.2,
        entropy_coef=0.01,
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
class ZsibotZSL1FlatPPORunnerCfg(ZsibotZSL1RoughPPORunnerCfg):
    def __post_init__(self):
        super().__post_init__()

        self.max_iterations = 5000
        self.experiment_name = "zsibot_zsl1_flat"


@configclass
class ZsibotZSL1StairPPORunnerCfg(RslRlOnPolicyRunnerCfg):
    num_steps_per_env = 24
    max_iterations = 50000
    save_interval = 100
    experiment_name = "zsibot_zsl1_stair"
    policy = RslRlPpoActorCriticCfg(
        # The policy class name. Defaults to ActorCritic.
        # REF: https://github.com/isaac-sim/IsaacLab/blob/f4aa17f87e2e5db5484f0b5974918573e8918ce2/source/isaaclab_rl/isaaclab_rl/rsl_rl/rl_cfg.py#L356
        class_name="ActorCritic",
        init_noise_std=1.0,
        actor_obs_normalization=False,
        critic_obs_normalization=False,
        actor_hidden_dims=[512, 256, 128],
        critic_hidden_dims=[512, 256, 128],
        activation="elu",
    )
    algorithm = RslRlPpoAlgorithmCfg(
        value_loss_coef=1.0,
        use_clipped_value_loss=True,
        clip_param=0.2,
        entropy_coef=0.01,
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
class ZsibotZSL1ParkourPPORunnerCfg(RslRlOnPolicyRunnerCfg):
    num_steps_per_env = 24
    max_iterations = 50000
    save_interval = 100
    experiment_name = "zsibot_zsl1_parkour"
    policy = RslRlPpoActorCriticCfg(
        # The policy class name. Defaults to ActorCritic.
        # REF: https://github.com/isaac-sim/IsaacLab/blob/f4aa17f87e2e5db5484f0b5974918573e8918ce2/source/isaaclab_rl/isaaclab_rl/rsl_rl/rl_cfg.py#L356
        class_name="ActorCritic",
        init_noise_std=1.0,
        actor_obs_normalization=False,
        critic_obs_normalization=False,
        actor_hidden_dims=[512, 256, 128],
        critic_hidden_dims=[512, 256, 128],
        activation="elu",
    )
    algorithm = RslRlPpoAlgorithmCfg(
        value_loss_coef=1.0,
        use_clipped_value_loss=True,
        clip_param=0.2,
        entropy_coef=0.01,
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
class ZsibotZSL1GapPPORunnerCfg(RslRlOnPolicyRunnerCfg):
    num_steps_per_env = 24
    max_iterations = 50000
    save_interval = 100
    experiment_name = "zsibot_zsl1_gap"
    policy = RslRlPpoActorCriticCfg(
        init_noise_std=1.0,
        actor_obs_normalization=False,
        critic_obs_normalization=False,
        actor_hidden_dims=[512, 256, 128],
        critic_hidden_dims=[512, 256, 128],
        activation="elu",
    )
    algorithm = RslRlPpoAlgorithmCfg(
        value_loss_coef=1.0,
        use_clipped_value_loss=True,
        clip_param=0.2,
        entropy_coef=0.01,
        num_learning_epochs=5,
        num_mini_batches=4,
        learning_rate=1.0e-3,
        schedule="adaptive",
        gamma=0.99,
        lam=0.95,
        desired_kl=0.01,
        max_grad_norm=1.0,
    )

from scripts.reinforcement_learning.rsl_rl.rl_cfg import RslRlCustomPpoActorCriticCfg

def _make_zsl1_rough_policy_cfg(
    *,
    num_actor_scan_obs: int | None = None,
    num_critic_scan_obs: int | None = None,
    scan_encoder_dims: list[int] | None = None,
    actor_scan_encoder_dims: list[int] | None = None,
    critic_scan_encoder_dims: list[int] | None = None,
    encode_scan_for_critic: bool = True,
    priv_obs_encoder_dims: list[int] | None = None,
    priv_encoder_dims: list[int] | None = None,
) -> RslRlCustomPpoActorCriticCfg:
    if priv_encoder_dims is None:
        priv_encoder_dims = priv_obs_encoder_dims
    return RslRlCustomPpoActorCriticCfg(
        class_name="ActorCritic",
        init_noise_std=1.0,
        noise_std_type="log",
        actor_hidden_dims=[512, 256, 128],
        critic_hidden_dims=[512, 256, 128],
        activation="elu",
        num_prop_obs=52,  # 52D
        num_scan_obs=187,  # 187D(1.6mx1.0m, 0.1m resolution, so 17*11=187)
        num_actor_scan_obs=num_actor_scan_obs,
        num_critic_scan_obs=num_critic_scan_obs,
        scan_encoder_dims=scan_encoder_dims,
        actor_scan_encoder_dims=actor_scan_encoder_dims,
        critic_scan_encoder_dims=critic_scan_encoder_dims,
        encode_scan_for_critic=encode_scan_for_critic,
        priv_obs_encoder_dims=priv_obs_encoder_dims,
        priv_encoder_dims=priv_encoder_dims,
    )


@configclass
class ZsibotZSL1RoughScanPPORunnerCfg(RslRlOnPolicyRunnerCfg):
    num_steps_per_env = 24
    max_iterations = 20000 # 모든 Abl 다 20000 통일
    save_interval = 50
    experiment_name = "zsibot_zsl1_rough_scan"
    empirical_normalization = True # Default는 False였는데, 대걸님꺼에 맞춰봄

    # init_noise_std, noise_std_type은 Actor network가 출력한 mean에 더해주는 "std"를 학습할 때 사용하는 변수
    policy = RslRlCustomPpoActorCriticCfg(
        class_name="ActorCritic",
        init_noise_std=1.0,
        noise_std_type="log",
        actor_hidden_dims=[512, 256, 128],
        critic_hidden_dims=[512, 256, 128],
        activation="elu",
        num_prop_obs=52,  # 52D
        num_scan_obs=187,  # 187D
        scan_encoder_dims=[128, 64, 32],  # 187D->32D
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
class ZsibotZSL1RoughAbl3_5PPORunnerCfg(ZsibotZSL1RoughScanPPORunnerCfg):
    experiment_name = "zsl1_rough_scan_abl3_5"
    policy = _make_zsl1_rough_policy_cfg(scan_encoder_dims=[128, 64, 32])  # 187D->32D
