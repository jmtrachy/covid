import json
import jsonpickle
import model
import os.path
import requests
import time


def generate_file_name(identifier):
    return './data/{}.json'.format(identifier)


def use_cache(state):
    # Get the generated file name - standardized to be in one place
    file_name = generate_file_name(state)

    # Check to see if the file exists.
    if os.path.isfile(file_name):
        # Get the current time in seconds
        now = time.time()

        # If the file was last modified more than an hour ago then it's not considered valid
        valid_file = (now - os.path.getmtime(file_name)) < 3600
    else:
        valid_file = False

    return valid_file


def get_us_dailies():
    us = 'US'

    if use_cache(us):

        # If the file is properly cached then just use it
        with open(generate_file_name(us), 'r') as f:
            dailies_json = json.load(f)

    else:
        # If the file has not been properly cached then retrieve
        resp = requests.get('https://covidtracking.com/api/v1/us/daily.json')
        dailies_json = json.loads(resp.content)

        # Now cache the file for next time through
        with open(generate_file_name(us), 'w') as f:
            f.write(jsonpickle.encode(dailies_json, unpicklable=False, indent=2))

    # Convert the raw json into our python objects
    dailies = []
    for daily in dailies_json:
        dailies.append(model.USDaily(
            date=daily.get('date'),
            date_entered=daily.get('dateChecked'),
            total_deaths=daily.get('death'),
            hospitalized_currently=daily.get('hospitalizedCurrently'),
            hospitalized_cumulatively=daily.get('hospitalizedCumulative'),
            in_icu_currently=daily.get('inIcuCurrently'),
            on_vent_currently=daily.get('onVentilatorCurrently'),
            total_negatives=daily.get('negative'),
            total_positives=daily.get('positive'),
            states_reporting=daily.get('states')
        ))

    return dailies


def get_us_states():
    if use_cache('states_list'):
        with open(generate_file_name('states_list'), 'r') as f:
            states_list_json = json.load(f)
    else:
        states_list_content: bytes = requests.get('https://covidtracking.com/api/v1/states/info.json').content
        states_list_json = json.loads(states_list_content)

        with open(generate_file_name('states_list'), 'w') as f:
            f.write(states_list_content.decode('utf-8'))

    return states_list_json


def get_state_dailies(state):

    if use_cache(state):
        with open(generate_file_name(state), 'r') as f:
            dailies_json = json.load(f)

    else:

        resp = requests.get('https://covidtracking.com/api/v1/states/{}/daily.json'.format(state.lower()))
        dailies_json = json.loads(resp.content)

        with open(generate_file_name(state), 'w') as f:
            f.write(jsonpickle.encode(dailies_json, unpicklable=False, indent=2))

    dailies = []
    for daily in dailies_json:
        dailies.append(model.StateDaily(
            state=daily.get('state'),
            date=daily.get('date'),
            total_deaths=daily.get('death'),
            deaths_increase=daily.get('deathIncrease'),
            hospitalized_currently=daily.get('hospitalizedCurrently'),
            hospitalized_cumulative=daily.get('hospitalizedCurrently'),
            hospitalized_increase=daily.get('hospitalizedIncrease'),
            in_icu_currently=daily.get('inIcuCurrently'),
            in_icu_cumulative=daily.get('inIcuCumulative'),
            total_negatives=daily.get('negative'),
            on_vent_currently=daily.get('onVentilatorCurrently'),
            on_vent_cumulative=daily.get('onVentilatorCumulative'),
            total_positives=daily.get('positive'),
            positives_increase=daily.get('positiveIncrease'),
            total_tests=daily.get('totalTestResults'),
            total_tests_increase=daily.get('totalTestResultsIncrease')
        ))

    return dailies


if __name__ == '__main__':
    # us_dailies = get_us_dailies()
    get_state_dailies('mn')
    print('hi')
