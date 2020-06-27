import argparse
import service

if __name__ == '__main__':
    us_service = service.USService()
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
