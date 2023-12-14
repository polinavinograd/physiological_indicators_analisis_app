from views.shared_components import InputTextField, SaveableInputInteger, DatePickerButton, TimePickerButton
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.screen import MDScreen
from kivymd.app import MDApp
from kivy.metrics import dp
from model.stress_module import StressModule

class StressEntryViewModel:
    '''
    Contains the stress data displayed and entered from screen.
    '''

    def __init__(self) -> None:
        self.__strees_level = SaveableInputInteger()

    @property
    def strees_level(self) -> SaveableInputInteger:
        return self.__strees_level
    
    @strees_level.setter
    def strees_level(self, strees_level: int) -> None:
        self.__strees_level.save_value(strees_level)

class AddStressScreen(MDScreen):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.__stress_entry = StressEntryViewModel()
        
        save_button = MDRaisedButton(text='Добавить', pos_hint={'center_x': 0.5, 'center_y': 0.5})
        save_button.bind(on_release=self.add_stress_entry)

        self.__date_picker = DatePickerButton(title='Выберите дату', pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.__time_picker = TimePickerButton(title='Выберите время', pos_hint={'center_x': 0.5, 'center_y': 0.5})
        
        self.add_widget(MDBoxLayout(
            InputTextField(self.__stress_entry.strees_level, title='Уровень стресса (число)', input_filter='int', pos_hint={'center_x': 0.5, 'center_y': 0.5}),
            self.__date_picker,
            self.__time_picker,
            save_button,
            orientation='vertical', padding=(dp(20), dp(0), dp(20), dp(20)), spacing=dp(20)
        ))

    def add_stress_entry(self, instance: MDRaisedButton):
        data_storage = MDApp.get_running_app().data_storage
        user_data = MDApp.get_running_app().user
        stress_module = StressModule(user_data, data_storage)

        stress_module.set_stress_level(
            self.__stress_entry.strees_level.get_value().__str__(),
            self.__date_picker.selected_date.__str__(),
            self.__time_picker.selected_time.__str__()
        )