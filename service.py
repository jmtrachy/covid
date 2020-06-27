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
        state_dailies = {}
        for s in states:
            state = s.get('state')
            state_dailies[state] = client.get_state_dailies(state)
