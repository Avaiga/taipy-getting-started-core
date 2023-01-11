#  Taipy Core Data nodes - CSV, pickle
from taipy.core.config import Config, Frequency
import taipy as tp
import datetime as dt
import time


Config.configure_job_executions(mode="standalone", max_nb_of_workers=2)

# Normal function used by Taipy
def double(nb):
    return nb * 2

def add(nb):
    print("Wait 10 seconds in add function")
    time.sleep(10)
    return nb + 10

Config.configure_job_executions(mode="standalone", max_nb_of_workers=2)

# Configuration of Data Nodes
input_data_node_cfg = Config.configure_data_node("input", default_data=21)
intermediate_data_node_cfg = Config.configure_data_node("intermediate")
output_data_node_cfg = Config.configure_data_node("output")

# Configuration of tasks
first_task_cfg = Config.configure_task("double",
                                    double,
                                    input_data_node_cfg,
                                    intermediate_data_node_cfg)

second_task_cfg = Config.configure_task("add",
                                    add,
                                    intermediate_data_node_cfg,
                                    output_data_node_cfg)

# Configuration of the pipeline and scenario
pipeline_cfg = Config.configure_pipeline("my_pipeline", [first_task_cfg, second_task_cfg])


def compare_function(*data_node_results):
    compare_result= {}
    current_res_i = 0
    for current_res in data_node_results:
        compare_result[current_res_i]={}
        next_res_i = 0
        for next_res in data_node_results:
            print(f"comparing result {current_res_i} with result {next_res_i}")
            compare_result[current_res_i][next_res_i] = next_res - current_res
            next_res_i += 1
        current_res_i += 1
    return compare_result


scenario_cfg = Config.configure_scenario("my_scenario",
                                         [pipeline_cfg],
                                         comparators={intermediate_data_node_cfg.id: compare_function})

#scenario_cfg = Config.configure_scenario_from_tasks(id="my_scenario",
#                                                    task_configs=[task_filter_by_month_cfg,
#                                                                  task_count_values_cfg])

Config.export("src/config_08.toml")

if __name__=="__main__":
    tp.Core().run()

    scenario_1 = tp.create_scenario(scenario_cfg)
    scenario_2 = tp.create_scenario(scenario_cfg)

    scenario_1.input.write(10)
    scenario_2.input.write(8)

    scenario_1.submit()
    scenario_2.submit()
    
    print(tp.compare_scenarios(scenario_1, scenario_2))

    tp.Rest().run()
