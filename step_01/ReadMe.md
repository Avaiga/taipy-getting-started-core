> You can download the code of this step [here](../src/step_01.py) or all the steps [here](https://github.com/Avaiga/taipy-getting-started-core/tree/develop/src).

# Configuration and execution

Before looking at some code examples, let’s define some basic terms Taipy Core uses. Taipy Core revolves around four major concepts.

## Four fundamental concepts in Taipy Core:
- [**Data Nodes**](https://docs.taipy.io/en/latest/manuals/core/concepts/data-node/): are the translation of _variables_ in Taipy. Data Nodes know how to retrieve any type of data. They can refer to: any Python object (string, int, list, dict, model, data frame, etc.), a Pickle file, a CSV file, a SQL database, etc.

- [**Tasks**](https://docs.taipy.io/en/latest/manuals/core/concepts/task/): are the expression of _functions_ in Taipy.

- [**Scenarios**](https://docs.taipy.io/en/latest/manuals/core/concepts/scenario/): are an instance of your pipelines. End-Users often require modifying various parameters to reflect different business situations. Taipy Scenarios provide the framework to "run"/"execute" pipelines under different conditions/variations (i.e., data/parameters modified by the end-user)


## What is a configuration?

A [**configuration**](https://docs.taipy.io/en/latest/manuals/core/config/) is a structure to define scenarios. It represents our Direct Acyclic Graph(s); it models the data sources, parameters, and tasks. Once defined, a configuration acts like a superclass; it is used to generate different instances of scenarios.


Let's create our first configuration. For this, we have two alternatives:

- Using Taipy Studio

- Or directly coding in Python.

Let’s consider the simplest possible pipeline: a single function taking an input as a CSV dataset and generating a cleaned dataset. See below:


```python
from taipy import Config
import taipy as tp

# Normal function used by Taipy
def clean(data):
    return data.drop_duplicates()
```

![](config_01.svg){ width=700 style="margin:auto;display:block;border: 4px solid rgb(210,210,210);border-radius:7px" }

- Two Data Nodes are being configured ('input' and 'output'). The 'input' Data Node has a _default_data_ set at 21. They will be stored as Pickle files (default storage format) and unique to each scenario entity/instance (this is the concept of scope which is covered later’). To clarify, the names given to the Data Nodes are arbitrary. The task links the two Data Nodes through the Python function double.

- The pipeline contains this task, and the scenario includes this single pipeline.

<video controls width="250">
    <source src="/step_01/config_01.mp4" type="video/mp4">
</video>


!!! example "Configuration"

    === "Taipy Studio"

        **Alternative 1:** Configuration using Taipy Studio

        By watching the animation below, you can feel how this configuration gets created using Taipy Studio. Once created, the configuration can be saved as a TOML file (see below)

        ![](config_01.gif){ width=700 style="margin:auto;display:block;border: 4px solid rgb(210,210,210);border-radius:7px" }

        To use this configuration in our code (`main.py` for example), we must load it and retrieve the `scenario_cfg`. This `scenario_cfg` is the basis to instantiate our scenarios.

        ```python
        Config.load('config_01.toml')

        # my_scenario is the id of the scenario configured
        scenario_cfg = Config.scenarios['my_scenario']
        ```

    === "Python configuration"

        **Alternative 2:** Configuration using Python Code

        Here is the code to configure a simple scenario.

        ```python
        # Configuration of Data Nodes
        input_data_node_cfg = Config.configure_data_node("input", default_data=21)
        output_data_node_cfg = Config.configure_data_node("output")

        # Configuration of tasks
        task_cfg = Config.configure_task("clean",
                                         clean,
                                         input_data_node_cfg,
                                         output_data_node_cfg)

        # Configuration of the pipeline and scenario
        scenario_cfg = Config.configure_scenario_from_tasks("my_scenario", [task_cfg])
        ```

Now that we have configured Taipy Core, you can create scenarios and submit them.

Before creating your entities, Taipy Core (the job scheduler) has to be launched (`tp.Core().run()`).

Then, you can play with Taipy: creating scenarios, submitting them, reading your data nodes. Creating a scenario (`tp.create_scenario(<Scenario Config>)`) creates all its related entities (_tasks_, _Data Nodes_, etc). These entities are being created thanks to the previous configuration. Still, no scenario has been run yet. `tp.submit(<Scenario>)` is the line of code that runs all the scenario-related pipelines and tasks.

```python
# Run of the Core
tp.Core().run()

# Creation of the scenario and execution
scenario = tp.create_scenario(scenario_cfg)
tp.submit(scenario)

print("Value at the end of task", scenario.output.read())
```

Results:

```
[2022-12-22 16:20:02,740][Taipy][INFO] job JOB_double_699613f8-7ff4-471b-b36c-d59fb6688905 is completed.
Value at the end of task 42
```    

## Ways of executing the code: Versioning

Taipy Core provides a [versioning system](https://docs.taipy.io/en/latest/manuals/core/versioning/) to keep track of the changes that a configuration will experience over time: new data sources, new parameters, new versions of your Machine Learning engine, etc. `python main.py -h` opens a helper to understand the versioning options at your disposal.
