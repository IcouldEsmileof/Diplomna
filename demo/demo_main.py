import tkinter as tk
import tkinter.messagebox

from common.common_classes import Executor, Scenario, EvrExecutor
import visualizer
from visualizer import colors


class MEvrExecutor(EvrExecutor):
    order = []

    def __init__(self, e: Executor):
        super().__init__(e)
        MEvrExecutor.order.clear()

    def add_scenario(self, scenario: Scenario) -> None:
        MEvrExecutor.order.append((self.id, scenario))
        super().add_scenario(scenario)


def get_scenarios_and_executors(*args, **kwargs):
    def check_input():
        if not str(enExecCount.get()).isnumeric() or not str(enSubCount.get()).isnumeric():
            raise ValueError
        if int(str(enExecCount.get())) > 6:
            raise ValueError
        for row in table:
            for cell in row:
                if not str(cell.get()).isnumeric() and str(cell.get()) != "":
                    raise ValueError

    scenarios = []
    executors = []
    try:
        check_input()
    except ValueError:
        tk.messagebox.showerror(title="Грешка", message="Невалидни входни данни")
        return scenarios, executors

    for id in range(int(str(enExecCount.get()))):
        executor = Executor(id, int(str(enSubCount.get())))
        executors.append(MEvrExecutor(executor))

    for tid in range(len(table)):
        config = []
        for task in table[tid]:
            l = str(task.get())
            if l.isnumeric():
                config.append(int(l))
        if len(config) != 0:
            scenario = Scenario(str(tid + 1), config)
            scenarios.append(scenario)
    global scenToShow
    scenToShow = scenarios
    return scenarios, executors


import EVR.multi_sort.commons


def print_results(executors):
    global execsToShow
    execsToShow = executors
    s = "Makespan = " + str(EVR.multi_sort.commons.get_current_makespan(executors)) + "\n"
    for executor in executors:
        s += str(executor) + "\n"
    outputText["state"] = tk.NORMAL
    outputText.delete(1.0, tk.END)
    outputText.insert(tk.END, s)
    outputText["state"] = tk.DISABLED
    visButton["state"] = tk.NORMAL


EVR.multi_sort.commons._get_scenarios_and_executors = get_scenarios_and_executors
EVR.multi_sort.commons.print_results = print_results
import EVR.single_sort.commons

EVR.single_sort.commons._get_scenarios_and_executors = get_scenarios_and_executors
EVR.single_sort.commons.print_results = print_results

test_configs = [
    {"execs": "1",
     "sub": "2",
     "table": [[2, 2, 3],
               [3, 3, 3],
               [1, 1, 2],
               [1, 2, 2],
               [1, 1, 1, 1, 1],
               [4]]},
    {"execs": "1",
     "sub": "2",
     "table": [[2, 2, 3],
               [3, 3, 3],
               [1, 1, 2],
               [1, 2, 2]]}
]


def set_table(id):
    enExecCount.insert(0, test_configs[id]["execs"])
    enSubCount.insert(0, test_configs[id]["sub"])

    t = test_configs[id]["table"]

    for i in range(len(t)):
        for j in range(len(t[i])):
            table[i][j].insert(0, str(t[i][j]))


def do_alg():
    s = var.get()
    s_id = algs_list.index(s)
    if s_id == 0:
        scenarios, executors = get_scenarios_and_executors()
        executor = executors[0]
        for scenario in scenarios:
            executor.add_scenario(scenario)
        print_results([executor])
        return
    if s_id == 1:
        from EVR.multi_sort.v2_LPT import Runner
    if s_id == 2:
        from EVR.multi_sort.v2_SPT import Runner
    Runner.run(0, True)
    return


def visualize_alg():
    visualizer.show_alg(execsToShow, scenToShow)


execsToShow = []
scenToShow = []

table = []

root = tk.Tk()
root.title("Демо")
lbExecCount = tk.Label(root, text="Брой изпълнители: ")
lbExecCount.grid(row=0, column=0, sticky=tk.W, pady=10, padx=5)
enExecCount = tk.Entry(root, width=10)
enExecCount.grid(row=0, column=1, pady=10, padx=5)
lbSubCount = tk.Label(root, text="Брой подизпълнители: ")
lbSubCount.grid(row=1, column=0, sticky=tk.W, pady=10, padx=5)
enSubCount = tk.Entry(root, width=10)
enSubCount.grid(row=1, column=1, pady=10, padx=5)

lbAlgList = tk.Label(root, text="Алгоритъм: ")
lbAlgList.grid(row=0, column=2, sticky=tk.W, pady=10, padx=5)
algs_list = ["По подразбиране",
             "Динамично избиране 2 - LPT",
             "Динамично избиране 2 - SPT"]

var = tk.StringVar(root)
var.set(algs_list[0])

lAlgs = tk.OptionMenu(root, var, *algs_list)
lAlgs.grid(row=0, column=3, columnspan=3, pady=10, padx=5, sticky=tk.W)

lbScens = tk.Label(root, text="Сценарии")
lbScens.grid(row=2, column=0, sticky=tk.W, pady=10, padx=5)
lbT1 = tk.Label(root, text="Задача 1")
lbT1.grid(row=2, column=1, sticky=tk.W, pady=10, padx=5)
lbT2 = tk.Label(root, text="Задача 2")
lbT2.grid(row=2, column=2, sticky=tk.W, pady=10, padx=5)
lbT3 = tk.Label(root, text="Задача 3")
lbT3.grid(row=2, column=3, sticky=tk.W, pady=10, padx=5)
lbT4 = tk.Label(root, text="Задача 4")
lbT4.grid(row=2, column=4, sticky=tk.W, pady=10, padx=5)
lbT5 = tk.Label(root, text="Задача 5")
lbT5.grid(row=2, column=5, sticky=tk.W, pady=10, padx=5)

lbSn1 = tk.Label(root, text="Сценарий 1:", bg=colors["1"])
lbSn1.grid(row=3, column=0, sticky=tk.W, pady=10, padx=5)
enS1T1 = tk.Entry(root, width=10)
enS1T1.grid(row=3, column=1, pady=10, padx=5)
enS1T2 = tk.Entry(root, width=10)
enS1T2.grid(row=3, column=2, pady=10, padx=5)
enS1T3 = tk.Entry(root, width=10)
enS1T3.grid(row=3, column=3, pady=10, padx=5)
enS1T4 = tk.Entry(root, width=10)
enS1T4.grid(row=3, column=4, pady=10, padx=5)
enS1T5 = tk.Entry(root, width=10)
enS1T5.grid(row=3, column=5, pady=10, padx=5)
table.append([enS1T1, enS1T2, enS1T3, enS1T4, enS1T5])

lbSn2 = tk.Label(root, text="Сценарий 2:", bg=colors["2"])
lbSn2.grid(row=4, column=0, sticky=tk.W, pady=10, padx=5)
enS2T1 = tk.Entry(root, width=10)
enS2T1.grid(row=4, column=1, pady=10, padx=5)
enS2T2 = tk.Entry(root, width=10)
enS2T2.grid(row=4, column=2, pady=10, padx=5)
enS2T3 = tk.Entry(root, width=10)
enS2T3.grid(row=4, column=3, pady=10, padx=5)
enS2T4 = tk.Entry(root, width=10)
enS2T4.grid(row=4, column=4, pady=10, padx=5)
enS2T5 = tk.Entry(root, width=10)
enS2T5.grid(row=4, column=5, pady=10, padx=5)
table.append([enS2T1, enS2T2, enS2T3, enS2T4, enS2T5])

lbSn3 = tk.Label(root, text="Сценарий 3:", bg=colors["3"])
lbSn3.grid(row=5, column=0, sticky=tk.W, pady=10, padx=5)
enS3T1 = tk.Entry(root, width=10)
enS3T1.grid(row=5, column=1, pady=10, padx=5)
enS3T2 = tk.Entry(root, width=10)
enS3T2.grid(row=5, column=2, pady=10, padx=5)
enS3T3 = tk.Entry(root, width=10)
enS3T3.grid(row=5, column=3, pady=10, padx=5)
enS3T4 = tk.Entry(root, width=10)
enS3T4.grid(row=5, column=4, pady=10, padx=5)
enS3T5 = tk.Entry(root, width=10)
enS3T5.grid(row=5, column=5, pady=10, padx=5)
table.append([enS3T1, enS3T2, enS3T3, enS3T4, enS3T5])

lbSn4 = tk.Label(root, text="Сценарий 4:", bg=colors["4"])
lbSn4.grid(row=6, column=0, sticky=tk.W, pady=10, padx=5)
enS4T1 = tk.Entry(root, width=10)
enS4T1.grid(row=6, column=1, pady=10, padx=5)
enS4T2 = tk.Entry(root, width=10)
enS4T2.grid(row=6, column=2, pady=10, padx=5)
enS4T3 = tk.Entry(root, width=10)
enS4T3.grid(row=6, column=3, pady=10, padx=5)
enS4T4 = tk.Entry(root, width=10)
enS4T4.grid(row=6, column=4, pady=10, padx=5)
enS4T5 = tk.Entry(root, width=10)
enS4T5.grid(row=6, column=5, pady=10, padx=5)
table.append([enS4T1, enS4T2, enS4T3, enS4T4, enS4T5])

lbSn5 = tk.Label(root, text="Сценарий 5:", bg=colors["5"])
lbSn5.grid(row=7, column=0, sticky=tk.W, pady=10, padx=5)
enS5T1 = tk.Entry(root, width=10)
enS5T1.grid(row=7, column=1, pady=10, padx=5)
enS5T2 = tk.Entry(root, width=10)
enS5T2.grid(row=7, column=2, pady=10, padx=5)
enS5T3 = tk.Entry(root, width=10)
enS5T3.grid(row=7, column=3, pady=10, padx=5)
enS5T4 = tk.Entry(root, width=10)
enS5T4.grid(row=7, column=4, pady=10, padx=5)
enS5T5 = tk.Entry(root, width=10)
enS5T5.grid(row=7, column=5, pady=10, padx=5)
table.append([enS5T1, enS5T2, enS5T3, enS5T4, enS5T5])

lbSn6 = tk.Label(root, text="Сценарий 6:", bg=colors["6"])
lbSn6.grid(row=8, column=0, sticky=tk.W, pady=10, padx=5)
enS6T1 = tk.Entry(root, width=10)
enS6T1.grid(row=8, column=1, pady=10, padx=5)
enS6T2 = tk.Entry(root, width=10)
enS6T2.grid(row=8, column=2, pady=10, padx=5)
enS6T3 = tk.Entry(root, width=10)
enS6T3.grid(row=8, column=3, pady=10, padx=5)
enS6T4 = tk.Entry(root, width=10)
enS6T4.grid(row=8, column=4, pady=10, padx=5)
enS6T5 = tk.Entry(root, width=10)
enS6T5.grid(row=8, column=5, pady=10, padx=5)
table.append([enS6T1, enS6T2, enS6T3, enS6T4, enS6T5])

set_table(0)

algButton = tk.Button(root, text="Старт", width=50, height=2, bg="light grey", command=do_alg)
algButton.grid(row=9, column=0, columnspan=6, pady=15, padx=5)

frame = tk.Frame(root)
frame.grid(row=0, column=6, rowspan=9, pady=10, padx=5)

outputText = tk.Text(frame, wrap=tk.WORD, state=tk.DISABLED)
outputText.grid(row=0, column=0)

yscroll = tk.Scrollbar(frame, command=outputText.yview)
yscroll.grid(row=0, column=1, sticky='nsew')

outputText['yscrollcommand'] = yscroll.set

visButton = tk.Button(root, text="Визуализация на действието на алгоритъма", width=50, height=2, bg="light grey",
                      command=visualize_alg, state=tk.DISABLED)
visButton.grid(row=9, column=6, columnspan=6, pady=15, padx=5)

if __name__ == '__main__':
    root.mainloop()
    exit()
