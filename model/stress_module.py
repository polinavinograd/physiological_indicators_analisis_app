from data_storage.data_store import IndicatorsDataStorage
from utils import date_range

ds = IndicatorsDataStorage()


class StressModule:
    def __init__(self, user_id: str):
        self.user = user_id

    def set_stress_level(self, stress):
        pass

    def get_average_stress_by_period(self, start_date, end_date):
        stress_levels = []
        for date in date_range(start_date, end_date):
            stress_levels.append(self.get_average_stress_by_day(date))
        return sum(stress_levels)/len(stress_levels)

    def get_average_stress_by_day(self, date) -> float:
        stress_levels = ds.get_stress_by_day(self.user, date)
        return sum(stress_levels)/len(stress_levels)
