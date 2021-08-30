import time

from common.common_classes import Executor, EvrExecutor
from ML_EVR.common.classification_runner import ClassificationRunner
from ML_EVR.common.envs.combination_envs import EvoSortClsEnvLPT
from ML_EVR.v1 import print_results


class Runner:
    @staticmethod
    def reorder(scenarios: list, executor: EvrExecutor) -> Executor:
        while len(scenarios) != 0:
            scenario_id = 0
            min_time = executor.get_max_time_if_scenario_is_added(scenarios[scenario_id])
            for i in range(1, len(scenarios)):
                cur_time = executor.get_max_time_if_scenario_is_added(scenarios[i])
                if min_time > cur_time:
                    scenario_id = i
                    min_time = cur_time
            executor.add_scenario(scenarios[scenario_id])
            scenarios.pop(scenario_id)
        return executor

    @staticmethod
    def run(test_case: int = 1, real: bool = True):
        r1 = ClassificationRunner(env_class=EvoSortClsEnvLPT, test_set=test_case, real=real)
        r1.run()
        r1.tester.env.reset()
        start = time.time()
        r1.tester.test()
        executors = []
        for executor in r1.tester.env.executors:
            new_executor = Runner.reorder(executor.scenario_list, EvrExecutor(executor))
            executors.append(new_executor)
        end = time.time()
        print_results(executors)
        print("Time = " + str(end - start))


if __name__ == '__main__':
    test_set = 24
    real = True
    Runner.run(test_set, real)
    exit()
