from ML_EVR.common.envs.otp import *


class EvoSortClsEnvLPT(EvoClsEnv, SortedScenariosClsEnvLPT):
    def __init__(self, scenarios, executors):
        super(EvoSortClsEnvLPT, self).__init__(scenarios, executors)

    def _is_done(self):
        return EvoClsEnv._is_done(self)

    def _special_action_on_reset(self):
        return SortedScenariosClsEnvLPT._special_action_on_reset(self)


class EvoSortClsEnvSPT(EvoClsEnv, SortedScenariosClsEnvSPT):
    def __init__(self, scenarios, executors):
        super(EvoSortClsEnvSPT, self).__init__(scenarios, executors)

    def _is_done(self):
        return EvoClsEnv._is_done(self)

    def _special_action_on_reset(self):
        return SortedScenariosClsEnvSPT._special_action_on_reset(self)


