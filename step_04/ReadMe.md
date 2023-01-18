
# Step 4: Cycles :

So far, we have talked about how having different scenarios helps us to oversee our assumptions about the future. For example, in business, it is critical to weigh different options to come up with an optimal solution. However, this decision-making process isn’t just a one-time task but rather a recurrent operation that happens over a time period. This is why we want to introduce Cycles.

A cycle can be thought of as a place to store different and recurrent scenarios within a time frame. In Taipy Core, each Cycle will have a unique primary scenario representing the reference scenario for a time period.


In the step's example, scenarios are attached to a MONTHLY cycle. Using Cycles is useful because some specific Taipy's functions exist to navigate through these Cycles. Taipy can get all the scenarios created in a month by providing the Cycle. You can also get every primary scenario ever made to see their progress over time quickly.

We change the function to filter in order to have the month as argument.
```python
def filter_by_month(df, month):
    df['Date'] = pd.to_datetime(df['Date']) 
    df = df[df['Date'].dt.month == month]
    return df
```

![](config_04.svg){ width=700 style="margin:auto;display:block;border: 4px solid rgb(210,210,210);border-radius:7px" }


=== "Taipy Studio/TOML configuration"

        - Recreate the config of the previous step
        - Add the frequency property for the scenario and put "WEEKLY:FREQUENCY" (DAYLY, WEEKLY, MONTHLY, YEARLY)

    ```python
    Config.load('config_04.toml')

    # my_scenario is the id of the scenario configured
    scenario_cfg = Config.scenarios['my_scenario']
    ```




=== "Python configuration"
    
    The configuration is the same as the last step except for the configuration of the scenario. A new parameter is added for the frequency.
    
    ```python
    scenario_cfg = Config.configure_scenario(id="my_scenario",
                                             pipeline_configs=[pipeline_cfg],
                                             frequency=Frequency.MONTHLY)


    #scenario_cfg = Config.configure_scenario_from_tasks(id="my_scenario",
    #                                                    task_configs=[task_filter_by_month_cfg,
    #                                                                  task_count_values_cfg])
    ```



As you can see, a Cycle can be made very easily once you have the desired frequency. In this snippet of code, since we have specified `frequency=Frequency.MONTHLY`, the corresponding scenario will be automatically attached to the correct period (month) once it is created.



```python
tp.Core().run()

scenario_1 = tp.create_scenario(scenario_cfg,
                                creation_date=dt.datetime(2022,10,7),
                                name="Scenario 2022/10/7")
scenario_2 = tp.create_scenario(scenario_cfg,
                                creation_date=dt.datetime(2022,10,5),
                                name="Scenario 2022/10/5")
```

Scenario 1 and 2 belongs to the same cycle but they don't share the same data node. Each one have a Data Node by itself.


```python
scenario_1.month.write(10)
scenario_2.month.write(10)


print("Month Data Node of Scenario 1", scenario_1.month.read())
print("Month Data Node of Scenario 2", scenario_2.month.read())

scenario_1.submit()
scenario_2.submit()
```


Results:
```
    Month Data Node of Scenario 1 10
    Month Data Node of Scenario 2 10
    [2022-12-22 16:20:04,746][Taipy][INFO] job JOB_filter_by_month_a4d3c4a7-5ec9-4cca-8a1b-578c910e255a is completed.
    [2022-12-22 16:20:04,833][Taipy][INFO] job JOB_count_values_a81b2f60-e9f9-4848-aa58-272810a0b755 is completed.
    [2022-12-22 16:20:05,026][Taipy][INFO] job JOB_filter_by_month_22a3298b-ac8d-4b55-b51f-5fab0971cc9e is completed.
    [2022-12-22 16:20:05,084][Taipy][INFO] job JOB_count_values_a52b910a-4024-443e-8ea2-f3cdda6c1c9d is completed.
    [2022-12-22 16:20:05,317][Taipy][INFO] job JOB_filter_by_month_8643e5cf-e863-434f-a1ba-18222d6faab8 is completed.
    [2022-12-22 16:20:05,376][Taipy][INFO] job JOB_count_values_72ab71be-f923-4898-a8a8-95ec351c24d9 is completed.
```

## Primary scenarios

In each cycle, there is a primary scenario. Having a primary scenario is interesting because it will be the important one of the cycle, the one that is the reference. By default, the first scenario created for a cycle will be primary. `tp.set_primary()` allows to change which scenario is the primary scenario in a cycle. `<Scenario>.is_primary` will return a boolean whether the scenario is primary or not.

```python
print("Scenario 1 before", scenario_1.is_primary)
print("Scenario 2 before", scenario_2.is_primary)

tp.set_primary(scenario_2)

print("Scenario 1 after", scenario_1.is_primary)
print("Scenario 2 after", scenario_2.is_primary)
```
Results:

```
    Scenario 1 before True
    Scenario 2 before False
    Scenario 1 after False
    Scenario 2 after True
```

Scenario 3 will be alone in another Cycle due to its creation date and will be the default primary scenario.

```python
scenario_3 = tp.create_scenario(scenario_cfg,
                                creation_date=dt.datetime(2021,9,1),
                                name="Scenario 2022/9/1")
scenario_3.month.write(9)
scenario_3.submit()

print("Is scenario 3 primary?", scenario_3.is_primary)
```

Results:

```
    [2022-12-22 16:20:05,317][Taipy][INFO] job JOB_filter_by_month_8643e5cf-e863-434f-a1ba-18222d6faab8 is completed.
    [2022-12-22 16:20:05,376][Taipy][INFO] job JOB_count_values_72ab71be-f923-4898-a8a8-95ec351c24d9 is completed.

    Is scenario 3 primary? True
```

Also, as you can see every scenario has been submitted and executed entirely. However, the result for these tasks are all the same. Caching will help to skip certain redundant task.

## Useful functions concerning cycles

- `tp.get_primary_scenarios()`: returns a list of all primary scenarios

- `tp.get_scenarios(cycle=<Cycle>)`: returns all the scenarios in the Cycle

- `tp.get_cycles()`: returns the list of Cycles

- `tp.get_primary(<Cycle>)`: returns the primary scenario of the Cycle
