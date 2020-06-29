import client


class USService:
    def __init__(self):
        self.us_dailies = client.get_us_dailies()

    def get_current_total_positives(self):
        return self.us_dailies[0].total_positives

    def get_positives_change_since_yesterday(self, offset=0):
        return self.us_dailies[offset].total_positives - self.us_dailies[offset + 1].total_positives

    def get_14_day_avg(self, offset=0):
        return int((self.us_dailies[offset].total_positives - self.us_dailies[offset + 13].total_positives) / 14)

    def get_positivity(self, offset=0):
        today = self.us_dailies[offset]
        yesterday = self.us_dailies[offset + 1]

        new_positives = today.total_positives - yesterday.total_positives
        new_negatives = today.total_negatives - yesterday.total_negatives

        return new_positives / (new_positives + new_negatives)

    def get_moving_avg(self):
        return [self.get_14_day_avg(offset) for offset in range(0, 30)]

    def get_14_day_positives(self):
        return [self.get_positives_change_since_yesterday(offset) for offset in range(0, 14)]

    def get_14_day_positivity(self):
        return [self.get_positivity(offset) for offset in range(0, 14)]


class StateService:
    def __init__(self):
        states = client.get_us_states()
        self.state_dailies_map = {}
        for s in states:
            state = s.get('state')
            self.state_dailies_map[state] = client.get_state_dailies(state)

    def get_current_total_positives(self, state, offset=0):
        return self.state_dailies_map.get(state)[offset].total_positives

    def get_current_positives_increase(self, state, offset=0):
        return self.state_dailies_map.get(state)[offset].positives_increase

    @staticmethod
    def get_positivity(daily):
        if daily.total_tests_increase > 0:
            return daily.positives_increase / daily.total_tests_increase
        else:
            return 0

    def get_historic_positivity(self, state, num_days=14, offset=0):
        dailies = self.state_dailies_map.get(state)
        return [StateService.get_positivity(dailies[day]) for day in range(offset, num_days)]

    def get_positivities_today(self, threshold=10):
        return [(state_dailies[0].state, StateService.get_positivity(state_dailies[0]))
                for state_dailies in self.state_dailies_map.values()
                if 1 > StateService.get_positivity(state_dailies[0]) > (threshold / 100)]



