from ax.service.ax_client import AxClient, ObjectiveProperties
from ax.utils.measurement.synthetic_functions import hartmann6
from ax.utils.notebook.plotting import init_notebook_plotting, render

import numpy as np

from flask import Flask, request
from flask.json import jsonify
from flask_caching import Cache

config = {
    "DEBUG":True,
    "CACHE_TYPE":"SimpleCache",
}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)


@app.route('/new_experiment', methods = ['POST'])
def new_experiment():
    ax_client = AxClient()

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
        outcome_constraints=["l2norm <= 1.25"],  # Optional.
    )

    cache.set('ax_client', ax_client)

    return('Initialized new experiment')


@app.route('/complete_trial')
def complete_trial():
    ax_client = cache.get('ax_client')
    data = request.json
    # add a bunch of json validation stuff here for real version

    trial_index = data['trial_index']
    results = data['results']
    results_cleaned = {}
    results_cleaned['hartmann6'] = tuple(results['hartmann6'])
    results_cleaned['l2norm'] = tuple(results['l2norm'])
    ax_client.complete_trial(trial_index, raw_data = results_cleaned)
    cache.set('ax_client', ax_client)
    return(f'Updated experiment for trial {trial_index}')


@app.route('/get_next_trial')
def get_next_trial():

    ax_client = cache.get('ax_client')
    parameterization, trial_index = ax_client.get_next_trial()
    cache.set('ax_client', ax_client)

    data = {'trial_index':trial_index, "parameterization":parameterization}
    return jsonify(data)