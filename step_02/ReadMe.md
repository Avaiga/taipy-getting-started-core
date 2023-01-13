# Step 2: Basic functions

Let's discuss the basic functions that come along with Taipy.

- `<Data Node>.write(<new value>)`: this is how data can be changed through Taipy. _write_ will change the _last_edit_date_ of the data node, which will influence if a task can be skipped or not.

- `tp.get_scenarios()`: this function returns a list of all the scenarios

- `tp.get(<Taipy object ID>)`: this function returns an entity based on the id of the entity

- `tp.delete(<Taipy object ID>)`: this function deletes the entity and nested elements based on the id of the entity

## Utility of having scenarios

Taipy lets the user create multiple instances of the same configuration. Data can differ between instances and can be used to compare different scenarios.

Data can naturally differ depending on the input Data Nodes or the randomness of functions. Moreover, the user can change them with the _write_ function.

![](config_02.svg){ width=700 style="margin:auto;display:block;border: 4px solid rgb(210,210,210);border-radius:7px" }

```python
scenario = tp.create_scenario(scenario_cfg, name="Scenario")
tp.submit(scenario)
print("First submit", scenario.output.read())
```
Results:
```
    [2022-12-22 16:20:02,874][Taipy][INFO] job JOB_double_a5ecfa4d-1963-4776-8f68-0859d22970b9 is completed.
    First submit 42
```

## _write_ function

Data of a Data Node can be changed using _write_. The syntax is `<Scenario>.<Pipeline>.<Data Node>.write(value)`. If there is just one pipeline, we can just write `<Scenario>.<Data Node>.write(value)`.


```python
print("Before write", scenario.input.read())
scenario.input.write(54)
print("After write",scenario.input.read())
```

Results:
```
    Before write 21
    After write 54
```

The submission of the scenario will update the output values.


```python
tp.submit(scenario)
print("Second submit",scenario.output.read())
```
Results:
```
    [2022-12-22 16:20:03,011][Taipy][INFO] job JOB_double_7eee213f-062c-4d67-b0f8-4b54c04e45e7 is completed.
    Second submit 108
```
    
## Other useful functions

- How to access all the scenarios

```python
print([s.input.read() for s in tp.get_scenarios()])
```

Results:
```
    [21, 54]
```

- Get an entity from its id

```python
scenario = tp.get(scenario.id)
```

- Delete an entity though its id. Example: how to delete a scenario.

```python
tp.delete(scenario.id)
```

