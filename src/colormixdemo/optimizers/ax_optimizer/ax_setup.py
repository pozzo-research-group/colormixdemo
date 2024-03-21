# set up an ax experiment to laod
from ax.service.ax_client import AxClient, ObjectiveProperties
from ax.utils.measurement.synthetic_functions import hartmann6
from ax.utils.notebook.plotting import init_notebook_plotting, render
from ax.modelbridge.generation_strategy import GenerationStep, GenerationStrategy
from ax.modelbridge.registry import Models

import numpy as np


def initialize_ax_experiment():
    """
    Helper function to set up an ax experiment and return the ax_client
    object. Modify this function to change how things are set up. Hacky yes. 
    """
    # 1. Define generation strategy.
    gs = GenerationStrategy(
        steps = [
            GenerationStep(
                model = Models.GPEI,
                num_trials = -1,
                max_parallelism = 1,
            )
        ]
    )

    ax_client = AxClient(generation_strategy=gs)

    ax_client.create_experiment(
        name="hartmann_test_experiment",
        parameters=[
            {
                "name": "x1",
                "type": "range",
                "bounds": [0.0, 1.0],
                "value_type": "float",  # Optional, defaults to inference from type of "bounds".
                "log_scale": False,  # Optional, defaults to False.
            },
            {
                "name": "x2",
                "type": "range",
                "bounds": [0.0, 1.0],
            },
            {
                "name": "x3",
                "type": "range",
                "bounds": [0.0, 1.0],
            },
            {
                "name": "x4",
                "type": "range",
                "bounds": [0.0, 1.0],
            },
            {
                "name": "x5",
                "type": "range",
                "bounds": [0.0, 1.0],
            },
            {
                "name": "x6",
                "type": "range",
                "bounds": [0.0, 1.0],
            },
        ],
        objectives={"hartmann6": ObjectiveProperties(minimize=True)},
        parameter_constraints=["x1 + x2 <= 2.0"],  # Optional.
        #outcome_constraints=["l2norm <= 1.25"],  # Optional.
    )

    return ax_client

def append_existing_data(ax_client, existing_data):
    """
    Append pre-existing data to an ax_client experiment. 
    
    :param ax_client: Ax client object to append data to.
    :type ax_client: ax.service.ax_client.AxClient
    :param existing_data: dictionary of new data parameterization and results
    :type existing_data: list of dicts 
    """
    # check that parameterization is correct 
    true_keys = ax_client.experiment.search_space.parameters.keys()
    true_metrics = ax_client.experiment.metrics.keys()
    for trial in existing_data:
        #print(trial)
        new_keys = trial['parameterization'].keys()
        new_metrics = trial['results'].keys()
        assert set(new_keys) == set(true_keys)
        assert set(new_metrics) == set(true_metrics)
    
    for trial in existing_data:
        params, trial_id = ax_client.attach_trial(trial['parameterization'])
        ax_client.complete_trial(trial_id, trial['results'])


def clean_results_json(results_json):
    """"
    Clean results json since tuples are lost
    """
    cleaned_json = {}
    #print(results_json)
    for key, value in results_json.items():
        if isinstance(value, list):
            if len(value) == 2:
                cleaned_json[key] = tuple(value)
        else:
            cleaned_json[key] = value

    return cleaned_json






