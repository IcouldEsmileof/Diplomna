import time

from EVR.single_sort.commons import _get_scenarios_and_executors, print_results


class Runner:
    @staticmethod
    def run(test_set: int = 1, real: bool = False):
        scenarios, executors = _get_scenarios_and_executors(test_case=test_set, real=real)
        start = time.time()
        scenarios.sort(key=lambda x: executors[0].get_max_time_if_scenario_is_added(x))
        for scenario in scenarios:
            min_time_executor = executors[0]
            for executor in executors[1:]:
                if executor.get_max_time() < min_time_executor.get_max_time() \
                        or (executor.get_max_time() == min_time_executor.get_max_time()
                            and executor.min_max_diff() > min_time_executor.min_max_diff()):
                    min_time_executor = executor
            min_time_executor.add_scenario(scenario)
        end = time.time()
        print_results(executors)
        print("Time = " + str(end - start))


if __name__ == '__main__':
    Runner.run(test_set=23, real=True)
    exit()
