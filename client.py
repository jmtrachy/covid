import json
import model
import requests


def get_us_dailies():
    resp = requests.get('https://covidtracking.com/api/v1/us/daily.json')
    resp_json = json.loads(resp.content)

    dailies = []
    for daily in resp_json:
        dailies.append(model.USDaily(
            date=daily.get('date'),
            date_entered=daily.get('dateChecked'),
            total_deaths=daily.get('death'),
            hospitalized_currently=daily.get('hospitalizedCurrently'),
            in_icu_currently=daily.get('inIcuCurrently'),
            on_vent_currently=daily.get('onVentilatorCurrently'),
            total_negatives=daily.get('negative'),
            total_positives=daily.get('positive'),
            states_reporting=daily.get('states')
        ))

    return dailies


def get_us_states():
    resp = requests.get('https://covidtracking.com/api/v1/states/info.json')
    return json.loads(resp.content)


def get_state_dailies(state):
    resp = requests.get('https://covidtracking.com/api/v1/states/{}/daily.json'.format(state))
    resp_json = json.loads(resp.content)

    dailies = []
    for daily in resp_json:
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
        print('date = {}; deaths_increase = {}'.format(
            dailies[len(dailies) - 1].date,
            dailies[len(dailies) - 1].deaths_increase
        ))


if __name__ == '__main__':
    # us_dailies = get_us_dailies()
    get_state_dailies('mn')
