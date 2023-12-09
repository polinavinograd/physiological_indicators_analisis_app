import math
from datetime import date, timedelta

from utils import date_range
from data_storage.data_store import ds
from model.calorie_report import CalorieReport
from model.user import User


class CaloriesModule:
    def __init__(self, user: User):
        self.user = user

    def __add_consumed_calories(self, calories: int, current_date: date):
        data = {'user_id': self.user.name,
                'calories_consumed': calories,
                'date': current_date}
        calories_old = ds.get_food_intake_by_day(self.user.name, current_date)
        if calories_old != 0:
            data['calories'] += calories_old
        ds.try_insert_calories(data, 'UserFoodIntake')

    def __add_burned_calories(self, calories: int, current_date: date):
        data = {'user_id': self.user.name,
                'calories': calories,
                'date': current_date}
        calories_old = ds.get_calories_burned_by_day(self.user.name, current_date)
        if calories_old != 0:
            data['calories_burned'] += calories_old
        ds.try_insert_calories(data, 'UserTraining')

    def __count_calories_intake_by_ingredients(self, ingredients: dict[str, int]):
        calories = 0
        for ingredient in ingredients:
            ingredient_calories_per_100g = ds.get_calories_by_ingredient(ingredient)
            calories += ingredient_calories_per_100g / 100 * ingredients[ingredient]
        return math.ceil(calories)

    # exercises - словарь всех упражений за день
    def __count_calories_outcome_by_exercises(self, exercises: dict[str, int]):
        calories = 0
        for exercise in exercises:
            exercise_calories_per_10min = ds.get_calories_by_exercise(exercise)
            calories += exercise_calories_per_10min / 10 * exercises[exercise]
        return math.ceil(calories) + 1500

    # MAIN вставка данных потребленные калории( + расчёт)
    def set_calories_intake(self, current_date: date, ingredients: dict[str, int]):
        calories = self.__count_calories_intake_by_ingredients(ingredients)
        self.__add_consumed_calories(calories, current_date)

    # MAIN вставка данных потраченных за день калории ( + расчет)
    def set_calories_outcome(self, current_date: date, exercises: dict[str, int]):
        calories = self.__count_calories_outcome_by_exercises(exercises)
        self.__add_burned_calories(calories, current_date)

    def __determine_activity_level(self):
        current_date = date.today()
        week_start_date = current_date - timedelta(days=6)
        calories = []
        for day in date_range(week_start_date, current_date):
            calories.append(ds.get_calories_burned_by_day(self.user.name, day))
        active_days_count = sum(1 for value in calories if value > 1800)
        if active_days_count == 0:
            return 1.2
        elif active_days_count < 3:
            return 1.375
        elif active_days_count < 5:
            return 1.55
        elif active_days_count < 7:
            return 1.725
        else:
            return 1.9

    def __count_daily_calories_norm(self):
        amr = self.__determine_activity_level()
        return math.ceil(amr * self.user.brm)

    # MAIN генерация отчета
    def create_daily_report(self):
        current_date = date.today()
        daily_norm = self.__count_daily_calories_norm()
        calories_consumed = ds.get_food_intake_by_day(self.user.name, current_date)
        calories_burned = ds.get_calories_burned_by_day(self.user.name, current_date)
        report = CalorieReport(self.user, current_date, calories_consumed, calories_burned, daily_norm).report
        return report


if __name__ == "__main__":
    user = User("polina.vngrd", 56, 169, 20, False)
    module = CaloriesModule(user)
    res = module.create_daily_report()
    print(res)

