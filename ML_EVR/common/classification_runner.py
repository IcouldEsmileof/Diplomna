import copy
import sys
import tkinter as tk
from tkinter import filedialog

from ML_EVR.common.agents import SimpleAgent
from ML_EVR.common.envs.combination_envs import *
from ML_EVR.common.models import SimpleModel
from ML_EVR.common.classification_tester import Tester


class ClassificationRunner:
    def __init__(self, env_class=ClassificationEnv, model_class=SimpleModel.build_model, agent_class=SimpleAgent,
                 test_set: int = 1, real: bool = False):
        self._test_set = test_set

        self._tester = Tester(env_class=env_class, model_class=model_class, agent_class=agent_class,
                              test_set=self._test_set, real=real)

        self._root = tk.Tk()
        self._root.withdraw()

    @property
    def tester(self):
        return self._tester

    def __del__(self):
        self._root.quit()

    def run(self):
        lamp = True
        while lamp:
            sys.stdout.writelines(
                ["Choose:\n",
                 "\t0) Exit\n",
                 "\t1) Save\n",
                 "\t2) Load\n",
                 "\t3) Fit for 1000 steps\n",
                 "\t4) Fit for 10000 steps\n",
                 "\t5) Fit for 100000 steps\n",
                 "\t6) Fit for custom steps\n",
                 "\t7) Test\n",
                 "\t8) Test shuffled scenario values\n",
                 "\t9) Test with different scenario values\n"
                 "\t10) Test with different executor values\n"
                 ])
            s = input()
            if not s.isdigit():
                continue
            a = int(s)
            if a == 0:
                lamp = False
            elif a == 1:
                self._root.deiconify()
                file_path = filedialog.asksaveasfilename()
                self._root.withdraw()
                self._tester.save(file_path)
            elif a == 2:
                self._root.deiconify()
                file_path = filedialog.askopenfilename()
                self._root.withdraw()
                self._tester.load(file_path)
            elif a == 3:
                self._tester.run(steps=1000)
            elif a == 4:
                self._tester.run(steps=10000)
            elif a == 5:
                self._tester.run(steps=100000)
            elif a == 6:
                s = input()
                steps = 1 if not s.isdigit() else int(s)
                self._tester.run(steps=steps)
            elif a == 7:
                test_env = copy.deepcopy(self._tester.env)
                self._tester.test(env=test_env)
            elif a == 8:
                test_env = copy.deepcopy(self._tester.env)
                scenarios = test_env.scenarios
                random.shuffle(scenarios)
                test_env.scenarios = scenarios
                self._tester.test(env=test_env)
            elif a == 9:
                test_env = copy.deepcopy(self._tester.env)
                test_env.scenarios = list(map(lambda x: x * x + 1, test_env.scenarios))
                self._tester.test(env=test_env)
            elif a == 10:
                test_env = copy.deepcopy(self._tester.env)
                test_env.reset()
                executors = test_env.executors
                executors[-1] = sum(test_env.scenarios) * len(test_env.scenarios)
                test_env.executors = executors
                self._tester.test(env=test_env)
