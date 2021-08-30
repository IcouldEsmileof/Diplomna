def get_current_makespan(executors):
    max_makespan = executors[0].get_max_time()
    for executor in executors[1:]:
        if max_makespan < executor.get_max_time():
            max_makespan = executor.get_max_time()
    return max_makespan


def print_results(executors):
    print("Makespan = " + str(get_current_makespan(executors)))
    for executor in executors:
        print(str(executor))
