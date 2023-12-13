from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from model.calories_module import CaloriesModule

class GetCalorieReportScreen(MDScreen):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.__report_label = MDLabel()
        self.__report_label.text = 'Данных нет'

        self.add_widget(MDBoxLayout(
            self.__report_label,
            orientation='vertical', padding=(dp(20), dp(80), dp(20), dp(20)), spacing=dp(20)
        ))

    def on_enter(self, *args):
        data_storage = MDApp.get_running_app().data_storage
        user_data = MDApp.get_running_app().user
        stress_module = CaloriesModule(user_data, data_storage)

        report = stress_module.create_daily_report()
        self.__report_label.text = report