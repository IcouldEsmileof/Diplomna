from typing import Tuple
import time
from EVR.multi_sort.commons import _get_scenarios_and_executors, get_current_makespan, print_results, get_min_time_id
from common.common_classes import Scenario, EvrExecutor


class Runner:
    @staticmethod
    def min_time_and_executor_overall(scenario, executors) -> Tuple[Scenario, EvrExecutor, float]:
        min_time_executor = executors[0]
        min_time = min_time_executor.get_max_time_if_scenario_is_added(scenario) - min_time_executor.get_max_time()
        cur_makespan = get_current_makespan(executors)
        changed = False
        for executor in executors:
            cur_time = executor.get_max_time()
            time_after = executor.get_max_time_if_scenario_is_added(scenario)
            if time_after - cur_time < min_time and cur_makespan >= time_after:
                changed = True
                min_time = time_after - cur_time
                min_time_executor = executor
        if not changed:
            min_time_executor = executors[0]
            min_time = min_time_executor.get_max_time_if_scenario_is_added(scenario)
            for executor in executors:
                cur_time = executor.get_max_time_if_scenario_is_added(scenario)
                if cur_makespan == executor.get_max_time() and cur_time == cur_makespan:
                    min_time = EvrExecutor(executor).get_max_time_if_scenario_is_added(scenario)
                    min_time_executor = executor
                elif cur_time < min_time:
                    min_time = cur_time
                    min_time_executor = executor
        return scenario, min_time_executor, min_time

    @staticmethod
    def run(test_set=1, real=False):
        scenarios, executors = _get_scenarios_and_executors(test_set=test_set, real=real)
        start = time.time()
        groups = list(map(lambda scenario: Runner.min_time_and_executor_overall(scenario, executors), scenarios))
        best_fit = get_min_time_id(groups)
        while len(groups) != 0:
            groups[best_fit][1].add_scenario(groups[best_fit][0])

            if len(groups) == 1:
                break
            groups.pop(best_fit)

            groups = list(
                map(lambda group: Runner.min_time_and_executor_overall(group[0], executors), groups)
            )
            best_fit = get_min_time_id(groups)
            
        end = time.time()
        print_results(executors)
        print("Time = " + str(end - start))


if __name__ == '__main__':
    Runner.run(test_set=22, real=False)
    exit()
