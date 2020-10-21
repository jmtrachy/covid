import argparse
import service
from typing import List, Optional

if __name__ == '__main__':
    us_service = service.USService()
    print('Today is {}'.format(us_service.us_dailies[0].date))

    print('\nCases info:')
    print('Total number of current us cases = {}'.format(us_service.get_current_total_positives()))
    print('New positive cases today = {}'.format(us_service.get_positives_change_since_for_day()))
    print('last 14 days us cases = {}'.format(us_service.get_14_day_positives()))
    print('moving average of new us cases = {}'.format(us_service.get_moving_avg_cases(num_days=30)))

    # Hospitalizations across the country
    print('\nHospitalization info:')
    print('Today\'s new hospitalizations = {}'.format(us_service.get_new_hosps()))
    print('Today\'s total hospitalizations = {}'.format(us_service.us_dailies[0].hospitalized_currently))
    last_two_weeks_hosps: List[int] = [us_service.get_new_hosps(day) for day in range(0, 14)]
    print('Last 14 days of new hospitalizations = {}'.format(last_two_weeks_hosps))
    print('Moving average of hospitalizations = {}'.format(us_service.get_14_day_moving_avg_hosps(num_days=30)))

    # Deaths across the country
    print('\nDeath info:')
    print('Today\'s new deaths = {}'.format(us_service.get_new_deaths()))
    print('Today\'s total deaths = {}'.format(us_service.us_dailies[0].total_deaths))
    last_two_weeks_deaths: List[int] = [us_service.get_new_deaths(day) for day in range(0, 14)]
    print('Last 14 days of new deaths = {}'.format(last_two_weeks_deaths))
    print('Moving average of deaths = {}'.format(us_service.get_moving_avg_deaths(num_days=30)))

    print('\nPositivity Info:')
    print('Today\'s positivity = {0:.1%}'.format(us_service.get_positivity()))
    positivity_14_day = us_service.get_recent_positivities(0, 14)
    print('last 14 days positivity = ', end='')
    for day in positivity_14_day:
        if day != positivity_14_day[-1]:
            print(' {0:.1%}'.format(day), end=',')
        else:
            print(' {0:.1%}'.format(day))

    print('moving average of positivities for the US:', end='')
    us_moving_avg_positivity = us_service.get_moving_average_positivities()
    count = 0
    for daily_positivity in us_moving_avg_positivity:
        count += 1
        if count != len(us_moving_avg_positivity):
            print(' {0:.1%}'.format(daily_positivity), end=',')
        else:
            print(' {0:.1%}'.format(daily_positivity))

    show_state_data = True
    if show_state_data:
        print('\n~~~~~~~~~~ States Info ~~~~~~~~~')
        state_service = service.StateService()

        for state in state_service.state_dailies_map.keys():
            daily = state_service.state_dailies_map.get(state)[0]
            electoral_votes = state_service.state_meta.get(state).get('electoral_votes')
            print('\n~~~~ {} for {} with pop = {} ~~~~'.format(state, daily.date, electoral_votes))

            print('New Cases Trend:', end='')
            historic_cases = state_service.get_historic_positive_cases(state)
            count = 0
            for day in historic_cases:
                count += 1
                if count != len(historic_cases):
                    print(' {}'.format(day), end=',')
                else:
                    print(' {}'.format(day))

            print('Daily Tests Trend:', end='')
            historic_tests = state_service.get_historic_new_tests(state)
            count = 0
            for day in historic_tests:
                count += 1
                if count != len(historic_tests):
                    print(' {}'.format(day), end=',')
                else:
                    print(' {}'.format(day))

            print('Positivities =', end='')
            historic_positivity = state_service.get_historic_positivity(state)
            count = 0
            for daily_positivity in historic_positivity:
                count += 1
                if count != len(historic_positivity):
                    print(' {0:.1%}'.format(daily_positivity), end=',')
                else:
                    print(' {0:.1%}'.format(daily_positivity))

            # Positivity trend
            seven_day_state_avg = state_service.get_average_positivities(state, offset=0, num_days=7)
            last_week_state_avg = state_service.get_average_positivities(state, offset=7, num_days=7)
            two_weeks_ago_state_avg = state_service.get_average_positivities(state, offset=14, num_days=7)
            three_weeks_ago_state_avg = state_service.get_average_positivities(state, offset=21, num_days=7)
            four_weeks_ago_state_avg = state_service.get_average_positivities(state, offset=28, num_days=7)
            five_weeks_ago_state_avg = state_service.get_average_positivities(state, offset=35, num_days=7)
            print('Positivity Trend - today, 7 days ago, 14, etc... = '
                  '{0:.1%}, {1:.1%}, {2:.1%}, {3:.1%}, {4:.1%}, {5:.1%}'.format(
                seven_day_state_avg,
                last_week_state_avg,
                two_weeks_ago_state_avg,
                three_weeks_ago_state_avg,
                four_weeks_ago_state_avg,
                five_weeks_ago_state_avg
            ))

            two_week_positivity = state_service.get_average_positivities(state)
            if two_week_positivity is not None:
                two_week_positivity_str = '{0:.1%}'.format(two_week_positivity)
            else:
                two_week_positivity_str = 'unreported'
            print('14 day Positivity = {}'.format(two_week_positivity_str))

            print('Hospitalizations =', end='')
            hosps = state_service.get_historic_hospitalizations(state)
            count = 0
            for day in hosps:
                count += 1
                if count != len(hosps):
                    print(' {}'.format(day), end=',')
                else:
                    print(' {}'.format(day))

            print('ICUs =', end='')
            icus = state_service.get_icus(state)
            count = 0
            for day in icus:
                count += 1
                if count != len(icus):
                    print(' {}'.format(day), end=',')
                else:
                    print(' {}'.format(day))
            if electoral_votes > 0 and icus[0] is not None:
                print('ICU per electoral vote: {}'.format(int(icus[0] / electoral_votes)))

            print('Total Deaths = {}'.format(state_service.state_dailies_map.get(state)[0].total_deaths))
            print('Deaths =', end='')
            deaths = state_service.get_historic_new_deaths(state)
            count = 0
            for day in deaths:
                count += 1
                if count != len(deaths):
                    print(' {}'.format(day), end=',')
                else:
                    print(' {}'.format(day))

        print('\n~~~~~~~~ Highway to the Danger Zone ~~~~~~~\n')

        print('Positivities over 8% today')
        todays_positives: [(str, float)] = state_service.get_positivities_today_over_threshold(threshold=8)
        for (state, positivity) in todays_positives:
            print('{0} = {1:.1%} - previous 4 days: '.format(state, positivity), end='')
            previous_days = state_service.get_historic_positivity(state, offset=1, num_days=4)
            count = 0
            for day in previous_days:
                count += 1
                if count != len(previous_days):
                    print(' {0:.1%}'.format(day), end=',')
                else:
                    print(' {0:.1%}'.format(day))

        print('\nPositivity numbers where 14 day is over 10%')
        danger_positivities: [(str, float)] = state_service.get_danger_states_avg_positivities()
        for (state, avg_positivity) in danger_positivities:
            seven_day_avg = state_service.get_average_positivities(state, offset=0, num_days=7)
            seven_day_two_weeks_ago = state_service.get_average_positivities(state, offset=14, num_days=7)
            print('{0}: 14-day = {1:.1%};    7-day = {2:.1%};     diff from 2 weeks ago: {3:.1%}'.format(
                state,
                avg_positivity,
                seven_day_avg,
                seven_day_avg - seven_day_two_weeks_ago
            ))

        print('\nTop 20 state deaths reported')
        top_death_states: [(str, Optional[int])] = state_service.get_top_death_states(threshold=20)
        for (state, deaths) in top_death_states:
            seven_day_avg = state_service.get_avg_new_deaths(state, offset=0, num_days=7)
            moving_seven_day = state_service.get_moving_avg_new_deaths(state, offset=1, num_days=7)
            print('{}: today = {};     7-day avg = {};   moving-7-day: {}'.format(
                state,
                deaths,
                seven_day_avg,
                moving_seven_day
            ))

        print('\nTop state ICU')
        pro_rated_icus: [(str, int)] = state_service.get_icus_pro_rated(threshold=0)
        for (state, pro_rated_icu) in pro_rated_icus:
            print('{} pro rated at {}'.format(state, pro_rated_icu))

