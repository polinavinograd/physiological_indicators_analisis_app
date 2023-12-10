from model.user import User
from model.stress_module import StressModule
from model.menstruation_delay_module import MenstruationDelayModule
from model.calories_module import CaloriesModule
from data_storage.data_store import IndicatorsDataStorage


class MyApp:
    def __init__(self):
        self.data_storage = IndicatorsDataStorage()
        self.user = User("polina.vngrd", 56, 169, 20, False)
        user_data = {"user_id": self.user.name,
                     "weight": self.user.weight,
                     "height": self.user.height,
                     "age": self.user.age,
                     "brm": self.user.brm}
        self.data_storage.try_insert_user(user_data)
        self.stress_module = StressModule(self.user, self.data_storage)
        self.calories_module = CaloriesModule(self.user, self.data_storage)
        self.menstruation_module = MenstruationDelayModule(self.user, self.stress_module, self.data_storage)
        res = self.menstruation_module.predict_menstruation()
        print(res)


if __name__ == "__main__":
    app = MyApp()
