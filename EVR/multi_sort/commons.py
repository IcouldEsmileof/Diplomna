from common.env_factory import get_fake_set, get_real_set
from common.common_classes import EnvP, EvrExecutor, Executor


def _get_scenarios_and_executors(test_set: int = 1, real: bool = False) -> (list, list):
    if real:
        env, _, _ = get_real_set(env_class=EnvP, test_case=test_set)
    else:
        env, _, _ = get_fake_set(env_class=EnvP, test_case=test_set)
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


def get_max_time_id(groups):
    max_id = 0
    max_time = groups[0][2]
    for i in range(1, len(groups)):
        if groups[i][2] > max_time:
            max_id = i
            max_time = groups[i][2]
    return max_id


def get_min_time_id(groups):
    min_id = 0
    min_time = groups[0][2]
    for i in range(1, len(groups)):
        if groups[i][2] < min_time:
            min_id = i
            min_time = groups[i][2]
    return min_id
