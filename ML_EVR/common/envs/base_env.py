import copy

import numpy as np

from gym.spaces import Discrete
from common.common_classes import EnvP


class ClassificationEnv(EnvP):
    version = 2

    def __init__(self, scenarios, executors):
        super(ClassificationEnv, self).__init__(scenarios, executors)
        self._scheduled_scenarios = 0
        self._scenarios_count = len(scenarios)
        self._executors_count = len(executors)
        self._scenarios_def = list(map(lambda scenario: self._calculate_config_sum(scenario), scenarios))
        self._executors_def = list(map(lambda executor: sum(executor.queues), executors))
        self._executors_tmp = copy.copy(self._executors_def)
        self._worst_case = self._calculate_worst_time(scenarios, self._executors_count)
        self._action_spec = Discrete(self._executors_count)
        self._action_spec.shape = (self._action_spec.n,)
        self._observation_spec = np.zeros(self._get_state_parameters_count())


    def observation_spec(self):
        return self._observation_spec

    def action_spec(self):
        return self._action_spec


    @property
    def scenarios(self):
        return self._scenarios

    @scenarios.setter
    def scenarios(self, new_scenarios: list):
        if new_scenarios is not None and len(new_scenarios) == self._scenarios_count:
            self._scenarios = new_scenarios
            self._scenarios_def = list(map(lambda scenario: self._calculate_config_sum(scenario), new_scenarios))
            self.reset()
            self._worst_case = self._calculate_worst_time(self._scenarios_def, self._executors_count)

    @property
    def executors(self):
        return self._executors

    @executors.setter
    def executors(self, new_executors: list):
        if new_executors is not None and len(new_executors) == self._executors_count:
            self._executors = new_executors
            self._executors_def = list(map(lambda executor: sum(executor.queues), self._executors))
            self._executors_tmp = copy.copy(self._executors_def)
            self.reset()

    def _get_state_parameters_count(self):
        count = 1  # scheduled scenarios
        count += 1  # current scenario len
        count += self._executors_count
        count += self._scenarios_count
        return count

    def step(self, action):

        self._executors_def[action] += self._scenarios_def[self._scheduled_scenarios]
        self._executors[action].add_scenario(self._scenarios[self._scheduled_scenarios])
        self._scheduled_scenarios += 1

        state = self._create_state()

        current_makespan = self._get_current_makespan()
        if current_makespan > self._worst_case:
            reward = self._worst_case - current_makespan
        else:
            reward = (self._worst_case / current_makespan) * (self._scheduled_scenarios / self._executors_count)

        done = self._is_done()

        info = {}

        return state, reward, done, info

    def _create_state(self):
        state = [self._scheduled_scenarios, 0 if self._is_done() else self._scenarios_def[self._scheduled_scenarios]]

        for executor in self._executors_def:
            state.append(executor)

        for scenario in self._scenarios_def:
            state.append(scenario)

        return state

    def _get_current_makespan(self):
        current_makespan = 0.0
        for executor in self._executors_def:
            if executor > current_makespan:
                current_makespan = executor
        return current_makespan

    def _is_done(self):
        return True if int(self._scheduled_scenarios) == self._scenarios_count else False

    @staticmethod
    def _calculate_config_sum(scenario):
        if isinstance(scenario, int):
            return scenario
        result = 0
        for config in scenario.configurations:
            result += config
        return result

    @staticmethod
    def _calculate_worst_time(scenarios: list, executors_count: int) -> float:
        scenarios = list(map(lambda scenario: ClassificationEnv._calculate_config_sum(scenario), scenarios))
        scenarios.sort(reverse=True)

        max_sum = sum(scenarios)

        if len(scenarios) >= 2:
            return max(scenarios[0] + scenarios[1], max_sum // executors_count)
        else:
            return max_sum

    def reset(self):
        self._executors_def = copy.copy(self._executors_tmp)
        self._scheduled_scenarios = 0
        for executor in self._executors:
            executor.clean()
        self._special_action_on_reset()

        return self._create_state()

    def _special_action_on_reset(self):
        pass

    def render(self, mode='human'):
        print("Makespan = " + str(self._get_current_makespan()))

        for i in range(self._executors_count):
            print("Executor " + str(i) + " = " + str(self._executors_def[i]))
            print("Scenarios: " + str(self._executors[i]))
