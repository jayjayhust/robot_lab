# Copyright (c) 2024-2026 Ziqi Fan
# SPDX-License-Identifier: Apache-2.0

"""Manager-based BPX parkour environments registration.

Provides Flat, Rough, Play, and 5 ablation variants (+ their Play modes) = 14 task IDs.
"""

import gymnasium as gym

from . import agents

##
# Register Gym environments.
##

# -- Flat terrain --

gym.register(
    id="RobotLab-Isaac-Velocity-BPX-Parkour-Flat-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.rough_env_cfg:BPXParkourFlatEnvCfg",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:BPXParkourFlatPPORunnerCfg",
    },
)

# -- Rough terrain --

gym.register(
    id="RobotLab-Isaac-Velocity-BPX-Parkour-Rough-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.rough_env_cfg:BPXParkourRoughEnvCfg",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:BPXParkourRoughPPORunnerCfg",
    },
)

gym.register(
    id="RobotLab-Isaac-Velocity-BPX-Parkour-Rough-Play-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.rough_env_cfg:BPXParkourRoughPlayEnvCfg",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:BPXParkourRoughPPORunnerCfg",
    },
)

# -- Ablation 1: no scan in policy --

gym.register(
    id="RobotLab-Isaac-Velocity-BPX-Parkour-Rough-Abl1-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.rough_env_cfg:BPXParkourRoughAbl1EnvCfg",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:BPXParkourRoughAbl1PPORunnerCfg",
    },
)

gym.register(
    id="RobotLab-Isaac-Velocity-BPX-Parkour-Rough-Abl1-Play-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.rough_env_cfg:BPXParkourRoughAbl1PlayEnvCfg",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:BPXParkourRoughAbl1PPORunnerCfg",
    },
)

# -- Ablation 2.5: scan-first ordering --

gym.register(
    id="BPX-Parkour-Rough-Abl2_5-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.rough_env_cfg:BPXParkourRoughAbl2_5EnvCfg",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:BPXParkourRoughAbl2_5PPORunnerCfg",
    },
)

gym.register(
    id="RobotLab-Isaac-Velocity-BPX-Parkour-Rough-Abl2_5-Play-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.rough_env_cfg:BPXParkourRoughAbl2_5PlayEnvCfg",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:BPXParkourRoughAbl2_5PPORunnerCfg",
    },
)

# -- Ablation 3.5: explicit scan encoder (same env cfg as Rough) --
gym.register(
    id="RobotLab-Isaac-Velocity-BPX-Parkour-Rough-Abl3_5-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.rough_env_cfg:BPXParkourRoughEnvCfg",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:BPXParkourRoughAbl3_5PPORunnerCfg",
    },
)

gym.register(
    id="RobotLab-Isaac-Velocity-BPX-Parkour-Rough-Abl3_5-Play-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.rough_env_cfg:BPXParkourRoughPlayEnvCfg",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:BPXParkourRoughAbl3_5PPORunnerCfg",
    },
)

# -- Ablation 4.0: no scan encoding for critic (same env cfg as Rough) --

gym.register(
    id="RobotLab-Isaac-Velocity-BPX-Parkour-Rough-Abl4_0-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.rough_env_cfg:BPXParkourRoughEnvCfg",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:BPXParkourRoughAbl4_0PPORunnerCfg",
    },
)

gym.register(
    id="RobotLab-Isaac-Velocity-BPX-Parkour-Rough-Abl4_0-Play-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.rough_env_cfg:BPXParkourRoughPlayEnvCfg",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:BPXParkourRoughAbl4_0PPORunnerCfg",
    },
)

# -- Ablation 7.0: reduced privileged encoder (same env cfg as Rough) --

gym.register(
    id="RobotLab-Isaac-Velocity-BPX-Parkour-Rough-Abl7_0-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.rough_env_cfg:BPXParkourRoughEnvCfg",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:BPXParkourRoughAbl7_0PPORunnerCfg",
    },
)

gym.register(
    id="RobotLab-Isaac-Velocity-BPX-Parkour-Rough-Abl7_0-Play-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.rough_env_cfg:BPXParkourRoughPlayEnvCfg",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:BPXParkourRoughAbl7_0PPORunnerCfg",
    },
)
