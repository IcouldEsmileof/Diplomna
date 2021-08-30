from common.common_classes import Scenario, Executor
import numpy as np

#################################
#                             1x2   2x2   3x2   3x3   5x4  5xRand
# Scenario\Executor configs |  0  |  1  |  2  |  3  |  4  |  5  |
#          04           0   | 001 | 002 | 003 | 004 | 005 | 006 |
#          06           1   | 007 | 008 | 009 | 010 | 011 | 012 |
#          06           2   | 013 | 014 | 015 | 016 | 017 | 018 |
#          06           3   | 019 | 020 | 021 | 022 | 023 | 024 |
#          10           4   | 025 | 026 | 027 | 028 | 029 | 030 |
#          20           5   | 031 | 032 | 033 | 034 | 035 | 036 |
#
###########################


_fake_executor_configs = {0: [{"executor_id": 1, "parallel_queues_count": 2}],
                          1: [{"executor_id": 1, "parallel_queues_count": 2},
                              {"executor_id": 2, "parallel_queues_count": 2}],
                          2: [{"executor_id": 1, "parallel_queues_count": 2},
                              {"executor_id": 2, "parallel_queues_count": 2},
                              {"executor_id": 3, "parallel_queues_count": 2}],
                          3: [{"executor_id": 1, "parallel_queues_count": 3},
                              {"executor_id": 2, "parallel_queues_count": 3},
                              {"executor_id": 3, "parallel_queues_count": 3}],
                          4: [{"executor_id": 1, "parallel_queues_count": 4},
                              {"executor_id": 2, "parallel_queues_count": 4},
                              {"executor_id": 3, "parallel_queues_count": 4},
                              {"executor_id": 4, "parallel_queues_count": 4},
                              {"executor_id": 5, "parallel_queues_count": 4}],
                          5: [{"executor_id": 1, "parallel_queues_count": np.random.randint(4, high=20)},
                              {"executor_id": 2, "parallel_queues_count": np.random.randint(4, high=20)},
                              {"executor_id": 3, "parallel_queues_count": np.random.randint(4, high=20)},
                              {"executor_id": 4, "parallel_queues_count": np.random.randint(4, high=20)},
                              {"executor_id": 5, "parallel_queues_count": np.random.randint(4, high=20)}]
                          }
_fake_scenario_configs = {0: [{"name": "1", "configuration_times": [2, 2, 3]},
                              {"name": "2", "configuration_times": [3, 3, 3]},
                              {"name": "3", "configuration_times": [1, 1, 2]},
                              {"name": "4", "configuration_times": [1, 2, 2]}],
                          1: [{"name": "1", "configuration_times": [2, 2, 3]},
                              {"name": "2", "configuration_times": [3, 3, 3]},
                              {"name": "3", "configuration_times": [1, 1, 2]},
                              {"name": "4", "configuration_times": [1, 2, 2]},
                              {"name": "5", "configuration_times": [1, 1, 1]},
                              {"name": "6", "configuration_times": [1, 1, 1]}],
                          2: [{"name": "1", "configuration_times": [2, 2, 3]},
                              {"name": "2", "configuration_times": [3, 3, 3]},
                              {"name": "3", "configuration_times": [1, 1, 2]},
                              {"name": "4", "configuration_times": [1, 2, 2]},
                              {"name": "5", "configuration_times": [10]},
                              {"name": "6", "configuration_times": [1, 1, 1]}],
                          3: [{"name": "1", "configuration_times": [2, 2, 3]},
                              {"name": "2", "configuration_times": [3, 3, 3]},
                              {"name": "3", "configuration_times": [1, 1, 2]},
                              {"name": "4", "configuration_times": [1, 2, 2]},
                              {"name": "5", "configuration_times": [1, 2, 3, 4]},
                              {"name": "6", "configuration_times": [1, 1, 1]}],
                          4: [{"name": "1", "configuration_times": np.random.randint(1, high=20, size=[
                              np.random.randint(2, high=4)])},
                              {"name": "2", "configuration_times": np.random.randint(1, high=20, size=[
                                  np.random.randint(2, high=4)])},
                              {"name": "3", "configuration_times": np.random.randint(1, high=20, size=[
                                  np.random.randint(2, high=4)])},
                              {"name": "4", "configuration_times": np.random.randint(1, high=20, size=[
                                  np.random.randint(2, high=4)])},
                              {"name": "5", "configuration_times": np.random.randint(1, high=20, size=[
                                  np.random.randint(2, high=4)])},
                              {"name": "6", "configuration_times": np.random.randint(1, high=20, size=[
                                  np.random.randint(2, high=4)])},
                              {"name": "7", "configuration_times": np.random.randint(1, high=20, size=[
                                  np.random.randint(2, high=4)])},
                              {"name": "8", "configuration_times": np.random.randint(1, high=20, size=[
                                  np.random.randint(2, high=4)])},
                              {"name": "9", "configuration_times": np.random.randint(1, high=20, size=[
                                  np.random.randint(2, high=4)])},
                              {"name": "10", "configuration_times": np.random.randint(1, high=20, size=[
                                  np.random.randint(2, high=4)])}],
                          5: [{"name": "1", "configuration_times": np.random.randint(1, high=20, size=[
                              np.random.randint(2, high=4)])},
                              {"name": "2", "configuration_times": np.random.randint(1, high=20, size=[
                                  np.random.randint(2, high=4)])},
                              {"name": "3", "configuration_times": np.random.randint(1, high=20, size=[
                                  np.random.randint(2, high=4)])},
                              {"name": "4", "configuration_times": np.random.randint(1, high=20, size=[
                                  np.random.randint(2, high=4)])},
                              {"name": "5", "configuration_times": np.random.randint(1, high=20, size=[
                                  np.random.randint(2, high=4)])},
                              {"name": "6", "configuration_times": np.random.randint(1, high=20, size=[
                                  np.random.randint(2, high=4)])},
                              {"name": "7", "configuration_times": np.random.randint(1, high=20, size=[
                                  np.random.randint(2, high=4)])},
                              {"name": "8", "configuration_times": np.random.randint(1, high=20, size=[
                                  np.random.randint(2, high=4)])},
                              {"name": "9", "configuration_times": np.random.randint(1, high=20, size=[
                                  np.random.randint(2, high=4)])},
                              {"name": "10", "configuration_times": np.random.randint(1, high=20, size=[
                                  np.random.randint(2, high=4)])},
                              {"name": "11", "configuration_times": np.random.randint(1, high=20, size=[
                                  np.random.randint(2, high=4)])},
                              {"name": "12", "configuration_times": np.random.randint(1, high=20, size=[
                                  np.random.randint(2, high=4)])},
                              {"name": "13", "configuration_times": np.random.randint(1, high=20, size=[
                                  np.random.randint(2, high=4)])},
                              {"name": "14", "configuration_times": np.random.randint(1, high=20, size=[
                                  np.random.randint(2, high=4)])},
                              {"name": "15", "configuration_times": np.random.randint(1, high=20, size=[
                                  np.random.randint(2, high=4)])},
                              {"name": "16", "configuration_times": np.random.randint(1, high=20, size=[
                                  np.random.randint(2, high=4)])},
                              {"name": "17", "configuration_times": np.random.randint(1, high=20, size=[
                                  np.random.randint(2, high=4)])},
                              {"name": "18", "configuration_times": np.random.randint(1, high=20, size=[
                                  np.random.randint(2, high=4)])},
                              {"name": "19", "configuration_times": np.random.randint(1, high=20, size=[
                                  np.random.randint(2, high=4)])},
                              {"name": "20", "configuration_times": np.random.randint(1, high=20, size=[
                                  np.random.randint(2, high=4)])}
                              ]
                          }

fake_executor_configs_len = len(_fake_executor_configs)
fake_scenario_configs_len = len(_fake_scenario_configs)


def fake_case(env_class, executor_case=1, scenario_case=1):
    if not (executor_case in _fake_executor_configs.keys() and scenario_case in _fake_scenario_configs.keys()):
        raise ValueError("executor_case or scenario_case is not supported")
    executors = []
    scenarios = []

    for executor_config in _fake_executor_configs[executor_case]:
        executors.append(Executor(executor_id=executor_config["executor_id"],
                                  parallel_queues_count=executor_config["parallel_queues_count"]))

    for scenario_config in _fake_scenario_configs[scenario_case]:
        scenarios.append(
            Scenario(name=scenario_config["name"], configuration_times=scenario_config["configuration_times"]))

    env = env_class(scenarios=scenarios, executors=executors)
    if hasattr(env, 'observation_spec') and hasattr(env, 'action_spec'):
        if len(env.observation_spec().shape) == 0:
            observations = 1
        else:
            observations = env.observation_spec().shape[0]
        if len(env.action_spec().shape) == 0:
            actions = 1
        else:
            actions = env.action_spec().shape[0]
    else:
        observations = None
        actions = None

    return env, observations, actions
