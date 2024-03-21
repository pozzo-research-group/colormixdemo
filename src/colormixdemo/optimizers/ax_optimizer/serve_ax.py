from ax.service.ax_client import AxClient, ObjectiveProperties
from ax.utils.measurement.synthetic_functions import hartmann6
from ax.utils.notebook.plotting import init_notebook_plotting, render

import numpy as np

from flask import Flask, request
from flask.json import jsonify
from flask_caching import Cache

import ax_setup

config = {
    "DEBUG":True,
    "CACHE_TYPE":"SimpleCache",
}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)


@app.route('/new_experiment', methods = ['POST'])
def new_experiment():
    ax_client = ax_setup.initialize_ax_experiment()
    cache.set('ax_client', ax_client)
    return('Initialized new experiment')

@app.route('/append_data', methods = ['POST'])
def append_data():
    data = request.json
    cleaned_data = []

    # get our result values back to tuples 
    for entry in data:
        cleaned_result = ax_setup.clean_results_json(entry['results'])
        entry['results'] = cleaned_result
        cleaned_data.append(entry)

    ax_client = cache.get('ax_client')
    ax_setup.append_existing_data(ax_client, cleaned_data)
    cache.set('ax_client', ax_client)
    return('Updated experiment data')

@app.route('/check_trials')
def check_trials():
    ax_client = cache.get('ax_client')
    trials = ax_client.get_trials_data_frame()['trial_index'].to_list()
    return(f'Current trials are {trials}')


@app.route('/complete_trial')
def complete_trial():
    ax_client = cache.get('ax_client')
    data = request.json
    # add a bunch of json validation stuff here for real version
    # validate that data has trial index and results with correct values
    # 1. check that trial index is in RUNNING status
    # 2. Check that results keys match results expected by ax_client
    # 3. 

    trial_index = data['trial_index']
    results = data['results']
    ax_client.complete_trial(trial_index, raw_data = ax_setup.clean_results_json(results))
    cache.set('ax_client', ax_client)
    return(f'Updated experiment for trial {trial_index}')


@app.route('/get_next_trial')
def get_next_trial():

    # since this is time intensive, should consider how to handle that
    # option 1: Spawn a background thread, user checks back later to get result 

    ax_client = cache.get('ax_client')
    parameterization, trial_index = ax_client.get_next_trial()
    cache.set('ax_client', ax_client)

    data = {'trial_index':trial_index, "parameterization":parameterization}
    return jsonify(data)