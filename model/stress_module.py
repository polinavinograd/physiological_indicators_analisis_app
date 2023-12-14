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

    def get_average_stress_by_period(self, start_date, end_date) -> float:
        stress_levels = []
        for date in date_range(start_date, end_date):
            stress_for_day = self.get_average_stress_by_day(date)
            if stress_for_day == None:
                continue

            stress_levels.append(stress_for_day)

        if stress_levels.__len__() == 0:
            return None

        return math.ceil(sum(stress_levels)/len(stress_levels))

    def get_average_stress_by_day(self, date) -> float:
        stress_levels = self.ds.get_stress_by_day(self.user.name, date)

        if stress_levels.__len__() == 0:
            return None

        return math.ceil(sum(stress_levels)/len(stress_levels))


ds = IndicatorsDataStorage()
u = User('vadim', 80, 190, 20, sex=True)
s = StressModule(u, ds)
s.set_stress_level(1, "2022-04-18", '14:00:00')
