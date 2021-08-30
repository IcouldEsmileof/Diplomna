import copy
from gym import Env
import numpy as np


class Scenario(object):
    def __init__(self, name: str, configuration_times: list or np.ndarray):
        self._name = name
        self._configurations = configuration_times

    @property
    def name(self) -> str:
        return self._name

    @property
    def configurations(self) -> list:
        return self._configurations

    def __eq__(self, other) -> bool:
        if isinstance(other, Scenario):
            return self._name == other._name
        else:
            return False

    def __len__(self) -> int:
        return len(self._configurations)

    def __str__(self) -> str:
        string = "Scenario: " + self._name + "\n"
        string += "Configurations:\n"
        for i in range(len(self._configurations)):
            string += "\t" + str(i) + " : " + str(self._configurations[i]) + "\n"
        return string


class Executor(object):
    def __init__(self, executor_id: int, parallel_queues_count: int):
        self.queue_count = parallel_queues_count
        self.queues = np.zeros(self.queue_count, dtype=float)
        self._max_time = 0.0
        self.id = executor_id
        self.scenario_list = []

    def __eq__(self, other) -> bool:
        if not isinstance(other, Executor):
            return False
        return self.scenario_list.__eq__(other.scenario_list)

    def __str__(self) -> str:
        result = f"Executor {self.id}:\n"
        for i in range(self.queue_count):
            result += f"\tQueue {i}: {self.queues[i]}\n"
        result += "\tScenarios:"
        for scenario in self.scenario_list:
            result += f"{scenario.name}, "
        return result

    def add_scenario(self, scenario: Scenario) -> None:
        for config in scenario.configurations:
            min_time_queue = self.get_min_index(self.queues)
            self.queues[min_time_queue] += config
            if self.queues[min_time_queue] > self._max_time:
                self._max_time = self.queues[min_time_queue]
        self.scenario_list.append(scenario)


    @staticmethod
    def get_min_index(queues: list or np.ndarray) -> int:
        mid = 0
        for i in range(queues.size):
            if queues[i] < queues[mid]:
                mid = i
        return mid

    def get_max_time(self) -> float:
        return self._max_time

    def clean(self) -> None:
        self.queues = np.zeros(self.queue_count, dtype=float)
        self.scenario_list = []
        self._max_time = 0.0


class EvrExecutor(Executor):
    def __init__(self, e: Executor):
        super(EvrExecutor, self).__init__(e.id, e.queue_count)

    def min_max_diff(self) -> float:
        return self._max_time - self.queues[self.get_min_index(self.queues)]

    def get_max_time_if_scenario_is_added(self, scenario: Scenario) -> float:
        queues = copy.deepcopy(self.queues)
        max_time = copy.copy(self._max_time)
        for config in scenario.configurations:
            min_time_queue = self.get_min_index(queues)
            queues[min_time_queue] += config
            if queues[min_time_queue] > max_time:
                max_time = queues[min_time_queue]
        return max_time


class EnvP(object):
    def __init__(self, scenarios, executors):
        self._scenarios = scenarios
        self._executors = executors

    @property
    def scenarios(self):
        return self._scenarios

    @property
    def executors(self):
        return self._executors



