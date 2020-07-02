import argparse
import service

if __name__ == '__main__':
    us_service = service.USService()
    state_service = service.StateService()
    print('Today is {}'.format(us_service.us_dailies[0].date))
    print('Total number of current us cases = {}'.format(us_service.get_current_total_positives()))
    print('New positive cases today = {}'.format(us_service.get_positives_change_since_yesterday()))
    print('14 day average of new cases = {}'.format(us_service.get_14_day_avg()))
    print('last 14 days us cases = {}'.format(us_service.get_14_day_positives()))
    print('moving average of new us cases = {}'.format(us_service.get_moving_avg()))
    print('today\'s positivity = {0:.1%}'.format(us_service.get_positivity()))

    positivity_14_day = us_service.get_14_day_positivity()
    print('last 14 days positivity = ', end='')
    for day in positivity_14_day:
        if day != positivity_14_day[-1]:
            print(' {0:.1%}'.format(day), end=',')
        else:
            print(' {0:.1%}'.format(day))

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

    todays_positives = state_service.get_positivities_today()
    for state in todays_positives:
        print('{0} has a positivity rate of {1:.1%}'.format(state, todays_positives[state]))
