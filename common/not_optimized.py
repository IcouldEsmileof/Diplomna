from common._fake_env_creators import fake_executor_configs_len, _fake_scenario_configs, _fake_executor_configs
from common._real_env_creators import real_executor_configs_len, _real_scenario_configs, _real_executor_configs
from common.common_classes import Executor, Scenario


def calculate_default_time_executor(test_case: int = 1, real: bool = False) -> Executor:
    test_case -= 1
    scenario_configs = _fake_scenario_configs[test_case // fake_executor_configs_len]
    executor_data = _fake_executor_configs[test_case % fake_executor_configs_len][0]
    if real:
        scenario_configs = _real_scenario_configs[test_case // real_executor_configs_len]
        executor_data = _real_executor_configs[test_case % real_executor_configs_len][0]

    scenarios = []
    for scenario_config in scenario_configs:
        scenarios.append(
            Scenario(name=scenario_config["name"], configuration_times=scenario_config["configuration_times"]))
    executor = Executor(executor_data["executor_id"], executor_data["parallel_queues_count"])
    for scenario in scenarios:
        executor.add_scenario(scenario)
    return executor


if __name__ == '__main__':
    test_case = 1
    real = False
    e = calculate_default_time_executor(test_case, real)
    print(e.get_max_time())
    print(e)
    exit()
