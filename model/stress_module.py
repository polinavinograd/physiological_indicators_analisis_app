import math

from data_storage.data_store import IndicatorsDataStorage
from model.user import User
from utils import date_range


class StressModule:
    def __init__(self, user: User, ds: IndicatorsDataStorage):
        self.user = user
        self.ds = ds
        print("\033[91mStressModule created! \033[0m")

    def set_stress_level(self, stress, date, time):
        data = {'user_id': self.user.name,
                'stress_level': stress,
                'date': date,
                'time': time}
        self.ds.insert_stress_data(data)

    def get_average_stress_by_period(self, start_date, end_date):
        stress_levels = []
        for date in date_range(start_date, end_date):
            stress_levels.append(self.get_average_stress_by_day(date))
        return math.ceil(sum(stress_levels)/len(stress_levels))

    def get_average_stress_by_day(self, date) -> float:
        stress_levels = self.ds.get_stress_by_day(self.user.name, date)
        return math.ceil(sum(stress_levels)/len(stress_levels))
