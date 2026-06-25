# Copyright (c) 2024-2026 Ziqi Fan
# SPDX-License-Identifier: Apache-2.0

import gymnasium as gym

from . import agents

##
# Register Gym environments.
##

gym.register(
    id="RobotLab-Isaac-Velocity-Flat-MirrorRobotics-BPX-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.flat_env_cfg:MirrormeroboticBPXFlatEnvCfg",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:MirrormeroboticBPXFlatPPORunnerCfg",
    },
)

gym.register(
    id="RobotLab-Isaac-Velocity-Rough-MirrorRobotics-BPX-v0",
    entry_point="isaaclab.envs:ManagerBasedRLEnv",
    disable_env_checker=True,
    kwargs={
        "env_cfg_entry_point": f"{__name__}.rough_env_cfg:MirrormeroboticBPXRoughEnvCfg",
        "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:MirrormeroboticBPXRoughPPORunnerCfg",
    },
)

# gym.register(
#     id="RobotLab-Isaac-Velocity-Stair-MirrorRobotics-BPX-v0",
#     entry_point="isaaclab.envs:ManagerBasedRLEnv",
#     disable_env_checker=True,
#     kwargs={
#         "env_cfg_entry_point": f"{__name__}.stair_env_cfg:ZsibotZSL1StairEnvCfg",
#         "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:ZsibotZSL1StairPPORunnerCfg",
#     },
# )

# gym.register(
#     id="RobotLab-Isaac-Velocity-Parkour-MirrorRobotics-BPX-v0",
#     entry_point="isaaclab.envs:ManagerBasedRLEnv",
#     disable_env_checker=True,
#     kwargs={
#         "env_cfg_entry_point": f"{__name__}.parkour_env_cfg:ZsibotZSL1ParkourEnvCfg",
#         "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:ZsibotZSL1ParkourPPORunnerCfg",
#     },
# )

# gym.register(
#     id="RobotLab-Isaac-Velocity-Gap-MirrorRobotics-BPX-v0",
#     entry_point="isaaclab.envs:ManagerBasedRLEnv",
#     disable_env_checker=True,
#     kwargs={
#         "env_cfg_entry_point": f"{__name__}.gap_env_cfg:ZsibotZSL1GapEnvCfg",
#         "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:ZsibotZSL1GapPPORunnerCfg",
#     },
# )

# gym.register(
#     id="RobotLab-Isaac-Velocity-Rough-Abl3_5-MirrorRobotics-BPX-v0",
#     entry_point="isaaclab.envs:ManagerBasedRLEnv",
#     disable_env_checker=True,
#     kwargs={
#         "env_cfg_entry_point": f"{__name__}.gap_env_cfg:ZsibotZSL1ParkourEnvCfg",
#         "rsl_rl_cfg_entry_point": f"{agents.__name__}.rsl_rl_ppo_cfg:ZsibotZSL1RoughAbl3_5PPORunnerCfg",
#     },
# )
