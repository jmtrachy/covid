import client
from model import StateDaily
from typing import Dict, List


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
        self.states = client.get_us_states()
        self.state_abbvs: List[str] = [state.get('state') for state in self.states]
        self.state_dailies_map: Dict[str, List[StateDaily]] = {
            state.get('state'): client.get_state_dailies(state.get('state')) for state in self.states
        }

    def get_current_total_positives(self, state, offset=0):
        return self.state_dailies_map.get(state)[offset].total_positives

    def get_current_positives_increase(self, state, offset=0):
        return self.state_dailies_map.get(state)[offset].positives_increase

    def get_historic_positive_cases(self, state: str, num_days: int = 14, offset: int = 0):
        state_dailies: List[StateDaily] = self.state_dailies_map.get(state)
        return [state_dailies[day].positives_increase for day in range(offset, num_days)]

    def get_historic_hospitalizations(self, state: str, num_days: int = 14, offset: int = 0):
        state_dailies: List[StateDaily] = self.state_dailies_map.get(state)
        return [state_dailies[day].hospitalized_currently for day in range(offset, num_days)]

    def get_14_day_avg_cases(self, state: str, offset: int =0):
        state_dailies = self.state_dailies_map.get(state)
        return int((state_dailies[offset].total_positives - state_dailies[offset + 13].total_positives) / 14)

    def define_dangerous_case_increases(self, state: str):
        print('hi')

    def get_dangerous_positive_increases(self):
        dangerous_increases: Dict[str, float] = {
            state: self.get_historic_positive_cases(state) for state in self.state_abbvs
        }

    @staticmethod
    def get_positivity(daily):
        if daily.total_tests_increase > 0:
            return daily.positives_increase / daily.total_tests_increase
        else:
            return 0

    def get_historic_positivity(self, state, num_days=14, offset=0):
        dailies = self.state_dailies_map.get(state)
        return [StateService.get_positivity(dailies[day]) for day in range(offset, num_days)]

    def get_positivities_today(self, threshold: int = 10):
        return {
            state_dailies[0].state: positivity
            for state_dailies in self.state_dailies_map.values()
            if (positivity := StateService.get_positivity(state_dailies[0])) > (threshold / 100)
        }


if __name__ == '__main__':
    ss = StateService()

