import pandas as pd

from data_storage.data_store import ds
from model.user import User
from utils import date_range


class StressModule:
    def __init__(self, user: User):
        self.user = user

    def set_stress_level(self, stress, date, time):
        data = {'user_id': [self.user.name],
                'stress_level': [stress],
                'date': [date],
                'time': [time]}
        df = pd.DataFrame(data)
        ds.insert_data(df, 'UserStress')

    def get_average_stress_by_period(self, start_date, end_date):
        stress_levels = []
        for date in date_range(start_date, end_date):
            stress_levels.append(self.get_average_stress_by_day(date))
        return sum(stress_levels)/len(stress_levels)

    def get_average_stress_by_day(self, date) -> float:
        stress_levels = ds.get_stress_by_day(self.user.name, date)
        return sum(stress_levels)/len(stress_levels)


