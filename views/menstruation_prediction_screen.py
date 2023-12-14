from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.app import MDApp
from model.menstruation_delay_module import MenstruationDelayModule
from model.stress_module import StressModule
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.metrics import dp

class MenstruationPredictionScreen(MDScreen):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.__next_sycle_label = MDLabel(text='Данных нет. Ожидайте', size_hint_y=None)
        self.__next_sycle_label.font_size = "24sp"

        self.add_widget(MDBoxLayout(
            MDScrollView(
            self.__next_sycle_label),
            orientation='vertical', padding=(dp(20), dp(60), dp(20), dp(20)), size_hint=(1, 0.9)))

    def on_enter(self, *args):
        data_storage = MDApp.get_running_app().data_storage
        user_data = MDApp.get_running_app().user
        stress_module = StressModule(user_data, data_storage)
        menstruation_module = MenstruationDelayModule(user_data, stress_module, data_storage)

        report = menstruation_module.generate_report()
        self.__next_sycle_label.text = report