import copy
import random

from ML_EVR.common.envs.base_env import ClassificationEnv
from common.common_classes import Executor


class EvoClsEnv(ClassificationEnv):
    def __init__(self, scenarios, executors):
        super(EvoClsEnv, self).__init__(scenarios, executors)

    def _is_done(self):
        done = True if int(self._scheduled_scenarios) == self._scenarios_count else False
        if done and self._worst_case > self._get_current_makespan():
            self._worst_case = self._get_current_makespan()
        return done


class SortedScenariosClsEnvLPT(ClassificationEnv):
    def __init__(self, scenarios, executors):
        super(SortedScenariosClsEnvLPT, self).__init__(scenarios, executors)
        tmp = []
        for i in range(self._scenarios_count):
            tmp.append((self._scenarios_def[i], self._scenarios[i]))
        tmp.sort(reverse=True, key=lambda pair: pair[0])
        for i in range(self._scenarios_count):
            self._scenarios_def[i] = tmp[i][0]
            self._scenarios[i] = copy.deepcopy(tmp[i][1])

    def _special_action_on_reset(self):
        tmp = []
        for i in range(self._scenarios_count):
            tmp.append((self._scenarios_def[i], self._scenarios[i]))
        tmp.sort(reverse=True, key=lambda pair: pair[0])
        for i in range(self._scenarios_count):
            self._scenarios_def[i] = tmp[i][0]
            self._scenarios[i] = copy.deepcopy(tmp[i][1])


class SortedScenariosClsEnvSPT(ClassificationEnv):
    def __init__(self, scenarios, executors):
        super(SortedScenariosClsEnvSPT, self).__init__(scenarios, executors)
        tmp = []
        for i in range(self._scenarios_count):
            tmp.append((self._scenarios_def[i], self._scenarios[i]))
        tmp.sort(key=lambda pair: pair[0])
        for i in range(self._scenarios_count):
            self._scenarios_def[i] = tmp[i][0]
            self._scenarios[i] = copy.deepcopy(tmp[i][1])

    def _special_action_on_reset(self):
        tmp = []
        for i in range(self._scenarios_count):
            tmp.append((self._scenarios_def[i], self._scenarios[i]))
        tmp.sort(key=lambda pair: pair[0])
        for i in range(self._scenarios_count):
            self._scenarios_def[i] = tmp[i][0]
            self._scenarios[i] = copy.deepcopy(tmp[i][1])

