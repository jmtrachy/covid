class USDaily:
    def __init__(self,
                 date,  # Date for which the daily totals were collected
                 date_entered,  # DateTime this data was entered into our database
                 total_deaths,  # Total number of people who have died as a result of COVID-19 so far
                 hospitalized_currently,  # Number of people in hospital for COVID-19 on this day
                 hospitalized_cumulatively, # Total number of people ever in the hospital for COVID-19
                 in_icu_currently,  # Total number of people in the ICU for COVID-19 on this day
                 on_vent_currently,  # Number of people using a ventilator for COVID-19 on this day
                 total_negatives,  # Total number of people who have tested negative for COVID-19 so far
                 total_positives,  # Total number of people who have tested positive for COVID-19 so far
                 states_reporting  # Number of states included in the data for this day
                 ):
        self.date = date
        self.date_entered = date_entered
        self.total_deaths = total_deaths
        self.hospitalized_currently = hospitalized_currently
        self.hospitalized_cumulatively = hospitalized_cumulatively
        self.in_icu_currently = in_icu_currently
        self.on_vent_currently = on_vent_currently
        self.total_negatives = total_negatives
        self.total_positives = total_positives
        self.states_reporting = states_reporting


class StateDaily:
    def __init__(self,
                 state,  # Two letter code for the state
                 date,  # Date for which the daily totals were collected
                 total_deaths,  # Total number of people who have died as a result of COVID-19 so far
                 deaths_increase,  # Daily difference in death
                 hospitalized_currently,  # Number of people in hospital for COVID-19 on this day
                 hospitalized_cumulative,  # Total number of people who have gone to the hospital for COVID-19 so far,
                 # including those who have since recovered or died
                 hospitalized_increase,  # Daily difference in hospitalized
                 in_icu_currently,  # Total number of people in the ICU for COVID-19 on this day
                 in_icu_cumulative,  # Total number of people who have gone to the ICU for COVID-19 so far,
                 # including those who have since recovered or died
                 total_negatives,  # Total number of people who have tested negative for COVID-19 so far
                 on_vent_currently,  # Number of people using a ventilator for COVID-19 on this day
                 on_vent_cumulative,  # Total number of people who have used a ventilator for COVID-19 so far,
                 # including those who have since recovered or died
                 total_positives,  # Total number of people who have tested positive for COVID-19 so far
                 positives_increase,  # Daily Difference in positive
                 total_tests,  # Total Test Results Provided by the State
                 total_tests_increase  # Daily Difference in totalTestResults
                ):
        self.state = state
        self.date = date
        self.total_deaths = total_deaths
        self.deaths_increase = deaths_increase
        self.hospitalized_currently = hospitalized_currently
        self.hospitalized_cumulative = hospitalized_cumulative
        self.hospitalized_increase = hospitalized_increase
        self.in_icu_currently = in_icu_currently
        self.in_icu_cumulative = in_icu_cumulative
        self.total_negatives = total_negatives
        self.on_vent_currently = on_vent_currently
        self.on_vent_cumulative = on_vent_cumulative
        self.total_positives = total_positives
        self.positives_increase = positives_increase
        self.total_tests = total_tests
        self.total_tests_increase = total_tests_increase

