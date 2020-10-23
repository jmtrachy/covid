from client import CovidClient
from functools import reduce
from model import StateDaily
from operator import add
from typing import Dict, List, Optional


class USService:
    """
    Service designed for analyzing national level data. Upon instantiation it will acquire a collection
    of all the national level data available from the data feed
    """

    def __init__(self):
        client = CovidClient()
        self.us_dailies = client.get_us_dailies()

    ###########################################################
    # ---------------- Positive Cases methods --------------- #
    ###########################################################

    def get_current_total_positives(self) -> int:
        return self.us_dailies[0].total_positives

    def get_positives_change_since_for_day(self, offset: int = 0) -> int:
        return self.us_dailies[offset].total_positives - self.us_dailies[offset + 1].total_positives

    def get_14_day_avg_positives(self, offset: int = 0, num_days: int = 14) -> int:
        return int(sum([
            self.get_positives_change_since_for_day(day)
            for day in range(offset, offset + num_days)]
        ) / num_days)

    def get_moving_avg_cases(self, offset: int = 0, num_days: int = 14) -> List[int]:
        return [self.get_14_day_avg_positives(offset) for offset in range(offset, offset + num_days)]

    def get_14_day_positives(self) -> List[int]:
        return [self.get_positives_change_since_for_day(offset) for offset in range(0, 14)]

    ###########################################################
    # ---------------- Hospitalization methods -------------- #
    ###########################################################
    def get_new_hosps(self, offset: int = 0) -> int:
        today_hosps = self.us_dailies[offset].hospitalized_cumulatively
        yesterday_hosps = self.us_dailies[offset + 1].hospitalized_cumulatively

        return today_hosps - yesterday_hosps

    def get_avg_hosps(self, offset: int = 0, num_days: int = 14) -> int:
        selected_hosps = [self.get_new_hosps(day) for day in range(offset, offset + num_days)]
        return int(sum(selected_hosps) / num_days)

    def get_14_day_moving_avg_hosps(self, offset: int = 0, num_days: int = 14) -> List[int]:
        return [self.get_avg_hosps(offset=day) for day in range(offset, offset + num_days)]

    ###########################################################
    # ---------------- US Deaths methods -------------------- #
    ###########################################################

    def get_new_deaths(self, offset: int = 0) -> int:
        today_deaths = self.us_dailies[offset].total_deaths
        yesterday_deaths = self.us_dailies[offset + 1].total_deaths

        return today_deaths - yesterday_deaths

    def get_avg_deaths(self, offset: int = 0, num_days: int = 14) -> int:
        selected_deaths = [self.get_new_deaths(day) for day in range(offset, offset + num_days)]
        return int(sum(selected_deaths) / num_days)

    def get_moving_avg_deaths(self, offset: int = 0, num_days: int = 14) -> List[int]:
        return [self.get_avg_deaths(offset=day) for day in range(offset, offset + num_days)]

    ###########################################################
    # ---------------- Positivity methods ------------------- #
    ###########################################################

    def get_positivity(self, offset: int = 0) -> float:
        today = self.us_dailies[offset]
        yesterday = self.us_dailies[offset + 1]

        new_positives = today.total_positives - yesterday.total_positives
        new_negatives = today.total_negatives - yesterday.total_negatives

        return new_positives / (new_positives + new_negatives)

    def get_average_positivities(self, offset: int = 0, num_days: int = 14) -> float:
        return get_positivity_average([
            self.get_positivity(day) for day in range(offset, offset + num_days)
        ])

    def get_recent_positivities(self, offset: int = 0, num_days: int = 14) -> List[float]:
        return [self.get_positivity(day) for day in range(offset, num_days)]

    def get_moving_average_positivities(self, offset: int = 0, num_days: int = 14) -> List[float]:
        return [
            self.get_average_positivities(day, 14)
            for day in range(offset, offset + num_days)
        ]


class StateService:
    def __init__(self):
        client = CovidClient()
        self.states = client.get_us_states()
        self.state_meta = CovidClient.get_state_meta()
        self.state_abbvs: List[str] = [state.get('state') for state in self.states]
        self.state_dailies_map: Dict[str, List[StateDaily]] = {
            state.get('state'): client.get_state_dailies(state.get('state')) for state in self.states
        }

    ###########################################################
    # ---------------------- ICU methods -------------------- #
    ###########################################################
    def get_icu(self, state: str, offset: int = 0) -> int:
        return self.state_dailies_map.get(state)[offset].in_icu_currently

    def get_icus(self, state: str, offset: int = 0, num_days: int = 14) -> List[int]:
        state_dailies: List[StateDaily] = self.state_dailies_map.get(state)
        return [state_dailies[day].in_icu_currently for day in range(offset, num_days)]

    def get_change_in_icu(self, state: str, offset: int = 0, timespan: int = 7) -> float:
        todays_icus: int = self.get_icu(state, offset)
        older_icus: int = self.get_icu(state, timespan)

        if todays_icus is not None and older_icus is not None and older_icus != 0:
            return (older_icus - todays_icus) / older_icus
        else:
            return 0

    def get_current_total_positives(self, state: str, offset=0) -> int:
        return self.state_dailies_map.get(state)[offset].total_positives

    def get_current_positives_increase(self, state: str, offset=0) -> int:
        return self.state_dailies_map.get(state)[offset].positives_increase

    def get_historic_positive_cases(self, state: str, num_days: int = 14, offset: int = 0) -> List[int]:
        state_dailies: List[StateDaily] = self.state_dailies_map.get(state)
        return [state_dailies[day].positives_increase for day in range(offset, num_days)]

    def get_new_tests_for_day(self, state: str, offset: int = 0) -> int:
        return self.state_dailies_map.get(state)[offset].total_tests_increase

    def get_historic_new_tests(self, state: str, offset: int = 0, num_days: int = 14) -> List[int]:
        return [self.get_new_tests_for_day(state, day) for day in range(offset, offset + num_days)]

    def get_new_deaths_for_day(self, state: str, offset: int = 0) -> int:
        return self.state_dailies_map.get(state)[offset].deaths_increase

    def get_historic_new_deaths(self, state: str, offset: int = 0, num_days: int = 14) -> List[int]:
        return [self.get_new_deaths_for_day(state, day) for day in range(offset, offset + num_days)]

    def get_avg_new_deaths(self, state: str, offset: int = 0, num_days: int = 14) -> int:
        return int(sum(self.get_historic_new_deaths(state, offset, num_days)) / num_days)

    def get_moving_avg_new_deaths(self, state: str, offset: int = 0, num_days: int = 14, num_days_in_avg: int = 14) \
            -> List[int]:
        return [self.get_avg_new_deaths(state, day, num_days_in_avg) for day in range(offset, num_days + offset)]

    def get_historic_hospitalizations(self, state: str, num_days: int = 14, offset: int = 0) -> List[int]:
        state_dailies: List[StateDaily] = self.state_dailies_map.get(state)
        return [state_dailies[day].hospitalized_currently for day in range(offset, num_days)]

    def get_14_day_avg_cases(self, state: str, offset: int = 0) -> int:
        state_dailies = self.state_dailies_map.get(state)
        return int((state_dailies[offset].total_positives - state_dailies[offset + 13].total_positives) / 14)

    def get_average_positivities(self, state: str, offset: int = 0, num_days: int = 14) -> float:
        state_dailies = self.state_dailies_map.get(state)
        avg_positivity = get_positivity_average([
            self.get_positivity(state_dailies[day]) for day in range(offset, num_days + offset)
        ])
        if avg_positivity is None:
            avg_positivity = 0
        return avg_positivity

    def get_moving_average_positivities(self, state: str, offset: int = 0, num_days: int = 14) -> List[float]:
        return [
            self.get_average_positivities(state, day)
            for day in range(offset, num_days)
        ]

    @staticmethod
    def get_pro_rated_number(numerator: int, denominator: int) -> int:
        if denominator is not None and denominator > 0 and numerator is not None:
            return int(numerator / denominator)
        else:
            return 0

    def get_icus_pro_rated(self, threshold: int = 10) -> [(str, int)]:
        all_valid_pro_rated = [
            (state, pro_rated_result)
            for state in self.state_dailies_map.keys()
            if (pro_rated_result := self.get_pro_rated_number(
                self.state_dailies_map.get(state)[0].in_icu_currently,
                self.state_meta.get(state).get('electoral_votes'))) > threshold
        ]
        # Sort so it's by highest pro-rated value first
        return sorted(all_valid_pro_rated, key=lambda tup: tup[1], reverse=True)

    def get_danger_states_avg_positivities(
            self,
            offset: int = 0,
            num_days: int = 14,
            threshold: int = 10
    ) -> [(str, float)]:
        all_avg_positivities: [(str, float)] = [
            (state, avg_positivity)
            for state in self.state_dailies_map.keys()
            if (avg_positivity := self.get_average_positivities(state, offset, num_days)) is not None
            and avg_positivity > float(threshold / 100)
        ]
        return sorted(all_avg_positivities, key=lambda tup: tup[1], reverse=True)

    @staticmethod
    def get_positivity(daily: StateDaily) -> float:
        if daily.total_tests_increase > 0:
            return daily.positives_increase / daily.total_tests_increase
        else:
            return 0

    def get_historic_positivity(self, state: str, num_days: int = 14, offset: int = 0) -> List[float]:
        dailies = self.state_dailies_map.get(state)
        return [StateService.get_positivity(dailies[day]) for day in range(offset, offset + num_days)]

    def get_positivities_today_over_threshold(self, threshold: int = 10) -> [(str, float)]:
        positivities_over_threshold: List[(str, float)] = [
            (state_dailies[0].state, positivity)
            for state_dailies in self.state_dailies_map.values()
            if (positivity := StateService.get_positivity(state_dailies[0])) > (threshold / 100)
            and positivity < 1.0
        ]
        return sorted(positivities_over_threshold, key=lambda tup: tup[1], reverse=True)

    def get_top_death_states(self, threshold: int = 10) -> [(str, Optional[int])]:
        all_state_deaths: [(str, Optional[int])] = [
            (state, self.state_dailies_map.get(state)[0].deaths_increase)
            for state in self.state_dailies_map.keys()
        ]
        sorted_state_deaths = sorted(all_state_deaths, key=lambda tup: tup[1], reverse=True)
        return sorted_state_deaths[:threshold]


def is_valid_positivity(positivity: float) -> bool:
    return positivity is not None and positivity != 0.0 and positivity != 1.0


def get_positivity_average(positivities: List[float]) -> Optional[float]:
    p_filtered = [
        p
        for p in positivities
        if is_valid_positivity(p)
    ]

    if len(p_filtered) == 0:
        return None
    else:
        return reduce(add, p_filtered) / len(p_filtered)


if __name__ == '__main__':
    ss = StateService()
