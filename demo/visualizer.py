import copy
import tkinter as tk
import tkinter.messagebox

colors = {"1": "orange red", "2": "deep sky blue", "3": "light green", "4": "yellow", "5": "cyan3", "6": "violet"}


class ExecutorWindow(tk.Toplevel):
    def __init__(self, executor, **kw):
        def a(event):
            can.configure(scrollregion=can.bbox("all"), width=1500,
                          height=100 * executor.queue_count if executor.queue_count < 4 else 400)

        super().__init__(**kw)
        self.scenarios = copy.deepcopy(executor.scenario_list)
        self.lt = float(self.get_longest_task())
        self.title("Executor " + str(executor.id + 1))
        self.q = tk.Label(self, text="Опашка:")
        self.q.grid(row=0, column=0, padx=5, pady=10)
        self.qlframe = tk.Frame(self, bg="white", width=1200, height=40)
        self.qlframe.grid_propagate(0)
        self.qlframe.grid(row=0, column=1, columnspan=9, pady=10, padx=5)
        self.ltasks = []
        self.populate_tasks()
        asd = tk.Frame(self)
        asd.grid(row=1, column=0, columnspan=10, rowspan=8, padx=5, pady=10)
        can = tk.Canvas(asd)
        self.qcframe = tk.Frame(can)
        scr = tk.Scrollbar(asd, command=can.yview)
        can.configure(yscrollcommand=scr.set)
        scr.pack(side='right', fill='y')
        can.pack(side='left')
        can.create_window((0, 0), window=self.qcframe, anchor='nw')
        self.qcframe.bind("<Configure>", a)
        self.queues = self.create_queue_columns(executor.queue_count)
        self.bnx = tk.Button(self, command=self.next_task, text="Следваща стъпка", bg="light grey")
        self.bnx.grid(row=10, column=0, columnspan=10, pady=10, padx=5)

    def get_longest_task(self):
        max_t = 0
        for scenario in self.scenarios:
            for config in scenario.configurations:
                if config > max_t:
                    max_t = config
        return max_t

    def populate_tasks(self):
        for l in self.ltasks:
            l.destroy()
        self.ltasks.clear()
        i = 0
        for scenario in self.scenarios:
            for config in scenario.configurations:
                lbC = tk.Label(self.qlframe, text=str(config), bg=colors[scenario.name], width=3)
                lbC.grid(row=0, column=i, padx=5, pady=10, sticky=tk.W)
                self.ltasks.append(lbC)
                i += 1

    def create_queue_columns(self, count):
        qs = []
        for i in range(count):
            lbi = tk.Label(self.qcframe, text="Подизпълнител " + str(i + 1) + ": ")
            lbi.grid(row=i, column=0, padx=5, pady=10, sticky=tk.W)
            fri = tk.Frame(self.qcframe, bg="white", width=1000, height=40)
            fri.grid_propagate(0)
            fri.grid(row=i, column=1, padx=5, pady=10, sticky=tk.W)
            counter_lb = tk.Label(self.qcframe, text="0")
            counter_lb.grid(row=i, column=2, padx=5, pady=10, sticky=tk.E)
            qs.append([fri, None, counter_lb])
        return qs

    def next_task(self):
        min_q = self.queues[0]
        for queue in self.queues:
            if queue[1] is None:
                if len(self.scenarios) == 0:
                    continue
                curc = self.scenarios[0].configurations.pop(0)
                lb = tk.Label(queue[0], text=str(curc), bg=colors[self.scenarios[0].name],
                              width=int(100 * (curc / self.lt)))
                lb.grid(row=0, column=0, padx=5, pady=10, sticky=tk.W)
                queue[1] = lb
                if len(self.scenarios[0].configurations) == 0:
                    self.scenarios.pop(0)
                self.populate_tasks()
                return
            else:
                if min_q[1] is not None:
                    if int(str(min_q[1]['text'])) > int(str(queue[1]['text'])):
                        min_q = queue
                else:
                    min_q = queue
        if min_q[1] is None:
            return
        min_q_t = int(str(min_q[1]['text']))
        for queue in self.queues:
            if queue[1] is not None:
                cur_t = int(str((queue[1]['text'])))
                cur_bg = queue[1]['bg']
                queue[1].destroy()
                cur_t -= min_q_t
                if cur_t != 0:
                    new_lb = tk.Label(queue[0], text=str(cur_t), bg=cur_bg, width=int(100 * (cur_t / self.lt)))
                    new_lb.grid(row=0, column=0, padx=5, pady=10, sticky=tk.W)
                    queue[1] = new_lb
                else:
                    queue[1] = None
                queue[2]['text'] = str(int(str(queue[2]['text'])) + min_q_t)
        self.populate_tasks()


class AlgWindow(tk.Toplevel):
    def __init__(self, executors, scenarios, **kw):
        super(AlgWindow, self).__init__(**kw)
        self.title("Алгоритъм")
        self.executors = executors
        self.scenarios = copy.copy(scenarios)
        self.order = copy.copy(executors[0].order)
        self.lbs = []
        self.scen_lbs = []
        self.exec_frs = []
        lbSce = tk.Label(self, text="Сценарии: ")
        lbSce.grid(row=0, column=0, padx=5, pady=10, sticky=tk.W)
        self.lbs.append(lbSce)
        for i in range(1, len(self.executors) + 1):
            lbE = tk.Label(self, text="Изпълнител " + str(i) + ": ")
            lbE.grid(row=i, column=0, padx=5, pady=10, sticky=tk.W)
            frE = tk.Frame(self, bg="white", width=100, height=40)
            frE.grid(row=i, column=1, columnspan=6, padx=5, pady=10, sticky=tk.W)
            self.exec_frs.append((frE, 0))

        self.frScen = tk.Frame(self, bg="white", width=480, height=40)
        self.frScen.grid_propagate(0)
        self.frScen.grid(row=0, column=1, columnspan=6, padx=5, pady=10, sticky=tk.W)
        self.populate_scenario_list()

        self.btNext = tk.Button(self, text="Следваща стъпка", width=40, height=2, bg="light grey",
                                command=self.next_step)

        self.btNext.grid(row=len(self.executors) + 1, column=0, columnspan=3, pady=10, padx=5)

        self.btExe = tk.Button(self, text="Визуализирай на изпълнителите", width=40, height=2, bg="light grey",
                               command=self.show_executor_activity)
        self.btExe.grid(row=len(self.executors) + 1, column=3, columnspan=3, pady=10, padx=5)

    def populate_scenario_list(self):
        for l in self.scen_lbs:
            l.destroy()
        self.scen_lbs.clear()
        i = 0
        for scenario in self.scenarios:
            lbS = tk.Label(self.frScen, text="Сценарий " + scenario.name, bg=colors[scenario.name])
            lbS.grid(row=0, column=i, padx=5, pady=10, sticky=tk.W)
            self.scen_lbs.append(lbS)
            i += 1

    def next_step(self):
        if len(self.scenarios) == 0:
            return
        exec_id, scenario = self.order.pop(0)
        self.scenarios.remove(scenario)

        lbS = tk.Label(self.exec_frs[exec_id][0], text="Сценарий " + scenario.name, bg=colors[scenario.name])
        lbS.grid(row=0, column=self.exec_frs[exec_id][1], padx=5, pady=10, sticky=tk.W)
        self.exec_frs[exec_id] = (self.exec_frs[exec_id][0], self.exec_frs[exec_id][1] + 1)

        self.populate_scenario_list()

    def show_executor_activity(self):
        for executor in self.executors:
            ew = ExecutorWindow(executor)


def show_alg(executors, scenarios):
    if not executors or not isinstance(executors, (list, tuple)) or len(executors) == 0:
        tk.messagebox.showerror(title="Грешка", message="Не бяха намерени изпълнители")
        return
    ew = AlgWindow(executors, scenarios)
