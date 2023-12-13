from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from views.shared_components import InputTextField, ListItem, SaveableInputInteger, DatePickerButton, SelectableList, SaveableInputString
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.metrics import dp
from typing import List
from model.calories_module import CaloriesModule
from model.stress_module import StressModule
from datetime import date, time, datetime

class CheckStressScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__period_start_picker = DatePickerButton(title='Выберите начало периода')
        self.__period_end_picker = DatePickerButton(title='Выберите конец периода')

        self.__average_stress_lable = MDLabel()
        calculate_button = MDRaisedButton(text='Сохранить', pos_hint={'center_x': 0.5, 'center_y': 0.5})
        calculate_button.bind(on_release=self.calculate_average_stress)

        self.add_widget(MDBoxLayout(
            MDBoxLayout(
                self.__period_start_picker,
                self.__period_end_picker,
                orientation='horizontal'
            ),
            self.__average_stress_lable,
            calculate_button,
            orientation='vertical', padding=(dp(20), dp(80), dp(20), dp(20)), spacing=dp(20)
        ))

    def calculate_average_stress(self, *args):
        period_start = self.__period_start_picker.selected_date
        period_end = self.__period_end_picker.selected_date

        data_storage = MDApp.get_running_app().data_storage
        user_data = MDApp.get_running_app().user
        stress_module = StressModule(user_data, data_storage)

        # Костыль, ибо дефолтное значение == date.today()
        if period_start == period_end and period_end == date.today():
            average_stress = stress_module.get_average_stress_by_day(period_start)
        else:
            average_stress = stress_module.get_average_stress_by_period(period_start, period_end)

        if average_stress == None:
            self.__average_stress_lable.text = 'Нет записей' 
            return

        self.__average_stress_lable.text = average_stress.__str__()