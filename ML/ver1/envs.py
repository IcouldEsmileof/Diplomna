import numpy as np
from common.common_classes import EnvP
from gym.spaces import Discrete


class SimpleEnv(EnvP):
    version = 1

    def __init__(self, scenarios, executors):
        super(SimpleEnv, self).__init__(scenarios, executors)
        self._scheduled_scenarios = 0
        self._worst_case = self._calculate_worst_time(self._scenarios)
        self._action_spec = Discrete(len(self._executors) * len(self._scenarios))
        self._action_spec.shape = (self._action_spec.n,)
        self._observation_spec = np.zeros(self._get_state_parameters_count())
        self._available_actions = {i: True for i in range(self._action_spec.shape[0])}
        self._testing = False
        self._last_pair = None
        self._counter = 0

    def observation_spec(self):
        return self._observation_spec

    def action_spec(self):
        return self._action_spec

    @property
    def scenarios(self):
        return self._scenarios

    @property
    def executors(self):
        return self._executors

    @property
    def testing(self):
        return self._testing

    @testing.setter
    def testing(self, testing: bool):
        self._testing = testing

    def _get_state_parameters_count(self):
        count = 1  # scheduled scenarios
        count += 1  # scenarios count
        count += 1  # executors count
        for scenario in self._scenarios:  # scenarios' config times
            count += len(scenario.configurations)
        for executor in self._executors:  # executors' queues
            count += executor.queue_count
        count += self._action_spec.shape[0]
        return count

    def step(self, action: int):
        if not self._is_action_available(action):
            state = self._create_state()

            reward = -1000 * (self._counter + 1)

            done = False

            info = {}

            if self._testing:
                if self._last_pair and self._last_pair["action"] == action:
                    self._last_pair["count"] = self._last_pair["count"] + 1
                    if self._last_pair["count"] >= 100:
                        done = True
                        reward = -100000
                else:
                    self._last_pair = {"action": action, "count": 1}
            else:
                self._counter += 1
                if self._counter == 20:
                    done = True
                    reward = -100000
                    self._counter = 0

            return state, reward, done, info

        executor_index = int(action) % len(self._executors)
        scenario_index = int(action) // len(self._executors)

        self._executors[executor_index].add_scenario(self._scenarios[scenario_index])
        self._remove_actions_for_scenario(scenario_index)
        self._scheduled_scenarios += 1

        state = self._create_state()

        current_makespan = self._get_current_makespan()

        reward = (self._worst_case / current_makespan) * (self._scheduled_scenarios / len(self._executors))

        done = self._is_done()

        info = {}

        return state, reward, done, info

    def _create_state(self):
        state = [self._scheduled_scenarios, len(self._scenarios)]

        for scenario in self._scenarios:
            for config in scenario.configurations:
                state.append(config)

        state.append(len(self._executors))
        for executor in self._executors:
            for queue in executor.queues:
                state.append(queue)

        for action in self._available_actions.keys():
            if self._available_actions[action]:
                state.append(1.0)
            else:
                state.append(0.0)

        return state

    def _remove_actions_for_scenario(self, scenario_index):
        for action_number in self._available_actions.keys():
            if action_number // len(self._executors) == scenario_index:
                self._available_actions[action_number] = False

    def _get_current_makespan(self):
        current_makespan = 0.0
        for executor in self._executors:
            if executor.get_max_time() > current_makespan:
                current_makespan = executor.get_max_time()
        return current_makespan

    def _is_action_available(self, action):
        if action not in self._available_actions.keys():
            return False
        return self._available_actions[action]

    def _is_done(self):
        done = True if int(self._scheduled_scenarios) == len(self._scenarios) else False
        return done

    @staticmethod
    def _calculate_worst_time(scenarios: list) -> float:
        result = 0.0
        for scenario in scenarios:
            for config in scenario.configurations:
                result += config
        return result

    def reset(self):
        self._available_actions = {i: True for i in range(self._action_spec.shape[0])}

        for i in self._executors:
            i.clean()

        self._scheduled_scenarios = 0
        self._last_pair = None
        return self._create_state()

    def render(self, mode='human'):
        print(self._get_current_makespan())

        for executor in self._executors:
            print(executor)


class EvolvingEnv(SimpleEnv):
    def __init__(self, scenarios, executors):
        super(EvolvingEnv, self).__init__(scenarios=scenarios, executors=executors)

    def _is_done(self):
        done = super(EvolvingEnv, self)._is_done()
        if done and self._worst_case > self._get_current_makespan():
            self._worst_case = self._get_current_makespan()
        return done
