from common.env_factory import get_fake_set, get_real_set
from common.common_classes import EnvP, EvrExecutor


def _get_scenarios_and_executors(test_case: int = 1, real: bool = False) -> (list, list):
    if real:
        env, _, _ = get_real_set(env_class=EnvP, test_case=test_case)
    else:
        env, _, _ = get_fake_set(env_class=EnvP, test_case=test_case)
    return env.scenarios, list(map(lambda x: EvrExecutor(x), env.executors))


def get_current_makespan(executors):
    max_makespan = executors[0].get_max_time()
    for executor in executors[1:]:
        if max_makespan < executor.get_max_time():
            max_makespan = executor.get_max_time()
    return max_makespan


def print_results(executors):
    print("Makespan = " + str(get_current_makespan(executors)))
    for executor in executors:
        print(str(executor))
