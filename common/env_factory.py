from common._fake_env_creators import fake_case, fake_executor_configs_len
from common._real_env_creators import real_case, real_executor_configs_len


def get_fake_set(env_class, test_case: int = 1):
    test_case -= 1
    executor_case = (test_case % fake_executor_configs_len)
    scenario_case = (test_case // fake_executor_configs_len)

    return fake_case(env_class=env_class, executor_case=executor_case, scenario_case=scenario_case)


def get_real_set(env_class, test_case: int = 1):
    test_case -= 1
    executor_case = (test_case % real_executor_configs_len)
    scenario_case = (test_case // real_executor_configs_len)

    return real_case(env_class=env_class, executor_case=executor_case, scenario_case=scenario_case)



