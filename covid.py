import argparse
import service
from typing import List

if __name__ == '__main__':
    us_service = service.USService()
    print('Today is {}'.format(us_service.us_dailies[0].date))

    print('\nCases info:')
    print('Total number of current us cases = {}'.format(us_service.get_current_total_positives()))
    print('New positive cases today = {}'.format(us_service.get_positives_change_since_yesterday()))
    print('last 14 days us cases = {}'.format(us_service.get_14_day_positives()))
    print('moving average of new us cases = {}'.format(us_service.get_moving_avg()))

    # Hospitalizations across the country
    print('\nHospitalization info:')
    print('Today\'s new hospitalizations = {}'.format(us_service.get_new_hosps()))
    last_two_weeks_hosps: List[int] = [us_service.get_new_hosps(day) for day in range(0, 14)]
    print('Last 14 days of new hospitalizations = {}'.format(last_two_weeks_hosps))
    print('14 day moving average of hospitalizations = {}'.format(us_service.get_14_day_moving_avg_hosps()))

    print('\nPositivity Info:')
    print('Today\'s positivity = {0:.1%}'.format(us_service.get_positivity()))
    positivity_14_day = us_service.get_recent_positivities(0, 14)
    print('last 14 days positivity = ', end='')
    for day in positivity_14_day:
        if day != positivity_14_day[-1]:
            print(' {0:.1%}'.format(day), end=',')
        else:
            print(' {0:.1%}'.format(day))

    print('positivity 14 day average = {0:.1%}'.format(us_service.get_average_positivities()))
    print('14 day moving average of positivities for the US:', end='')
    us_moving_avg_positivity = us_service.get_moving_average_positivities()
    count = 0
    for daily_positivity in us_moving_avg_positivity:
        count += 1
        if count != len(us_moving_avg_positivity):
            print(' {0:.1%}'.format(daily_positivity), end=',')
        else:
            print(' {0:.1%}'.format(daily_positivity))

    show_state_data = False
    if show_state_data:
        print('\n~~~~~~~~~~ States Info ~~~~~~~~~\n')
        state_service = service.StateService()

        for state in state_service.state_dailies_map.keys():
            daily = state_service.state_dailies_map.get(state)[0]
            print('{} has a daily increase on {} of {}'.format(daily.state, daily.date, daily.positives_increase))

            print('{} is trucking along with positivities of '.format(state), end='')
            historic_positivity = state_service.get_historic_positivity(state)
            count = 0
            for daily_positivity in historic_positivity:
                count += 1
                if count != len(historic_positivity):
                    print(' {0:.1%}'.format(daily_positivity), end=',')
                else:
                    print(' {0:.1%}'.format(daily_positivity))

            print('{} tracked new cases of the following: '.format(state), end='')
            historic_cases = state_service.get_historic_positive_cases(state)
            count = 0
            for day in historic_cases:
                count += 1
                if count != len(historic_cases):
                    print(' {}'.format(day), end=',')
                else:
                    print(' {}'.format(day))

            print('{} has the following hospitalization numbers: '.format(state), end='')
            hosps = state_service.get_historic_hospitalizations(state)
            count = 0
            for day in hosps:
                count += 1
                if count != len(hosps):
                    print(' {}'.format(day), end=',')
                else:
                    print(' {}'.format(day))

        todays_positives = state_service.get_positivities_today_over_threshold()
        for state in todays_positives:
            print('{0} has a positivity rate of {1:.1%}'.format(state, todays_positives[state]))

        danger_positivities = state_service.get_danger_states_avg_positivities()
        for state in danger_positivities:
            print('{0} has a 14 day positivity average of {1:.1%}'.format(state, danger_positivities[state]))
