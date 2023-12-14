from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from views.shared_components import DropDownList, DropDownListItem, InputTextField, ListItem, SaveableInputInteger, DatePickerButton, SelectableList, SaveableInputString
from kivymd.app import MDApp
from kivy.metrics import dp
from typing import List, Tuple
from model.calories_module import CaloriesModule

class NewTrainingRecord:
    def __init__(self) -> None:
        self.__training_name = SaveableInputString()
        self.__minutes = SaveableInputInteger()

    @property
    def training_name(self) -> SaveableInputString:
        return self.__training_name
    
    @training_name.setter
    def training_name(self, ingredient_name: str) -> None:
        self.__training_name.save_value(ingredient_name)
        
    @property
    def minutes(self) -> SaveableInputInteger:
        return self.__minutes
    
    @minutes.setter
    def minutes(self, minutes: int) -> None:
        self.__minutes.save_value(minutes)
        
class SelectedTrainingRecord:
    def __init__(self, exercise_name: str, calorie: int, minutes: int) -> None:
        self.__exercise_name = exercise_name
        self.__calorie = calorie
        self.__minutes = minutes

    @property
    def exercise_name(self) -> str:
        return self.__exercise_name
    
    @property
    def calorie(self) -> int:
        return self.__calorie
        
    @property
    def minutes(self) -> int:
        return self.__minutes

class AddTrainingBox(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.orientation = 'vertical'
        self.padding=(dp(20), dp(0), dp(20), dp(20))
        self.spacing=dp(20)

        data_storage = MDApp.get_running_app().data_storage
        available_exercises = data_storage.get_exercises_list()

        # Ключ - название, значение - калории
        items = self.__get_exercises_list(available_exercises)
        self.__available_exercises_drop_down_list = DropDownList(items, size_hint=(0.6, 1))

        self.__time_entered = SaveableInputInteger()
        self.__mass_input = InputTextField(
            self.__time_entered,
            title='Время (в минутах)',
            input_filter='int',
            size_hint=(0.8, 1))

        save_button = MDRaisedButton(
            text='Добавить',
            size_hint=(0.2, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5})
        save_button.bind(on_release=self.add_training)

        self.add_widget(MDBoxLayout(
            self.__available_exercises_drop_down_list,
            self.__mass_input,
            save_button,
            orientation='horizontal',
            size_hint=(1, 0.2)
        ))

        self.__selected_trainings = SelectableList(size_hint=(1, 1))
        self.add_widget(self.__selected_trainings)
        
    def __get_exercises_list(self, exercises: List[Tuple[str,int]]) -> List[DropDownListItem]:
        result = []
        for exercise in exercises:
            result.append(DropDownListItem(exercise[0], exercise[1]))

        return result
        
    def get_selected_exercises(self) -> List[SelectedTrainingRecord]:
        selected_items = self.__selected_trainings.get_selected_items()
        return list(map(lambda item: item.value, selected_items))

    def add_training(self, *args):
        time_entered = self.__time_entered.get_value()
        if time_entered <= 0:
            return
        
        # Ключ - название, значение - калории
        item_selected = self.__available_exercises_drop_down_list.selected_item

        list_item = ListItem(
            id=item_selected.title,
            value=SelectedTrainingRecord(
                exercise_name=item_selected.title,
                calorie=item_selected.value,
                minutes=time_entered),
            is_selected=True)

        self.__selected_trainings.add_item(
            text=list_item.id,
            item=list_item)

class AddTrainingScreen(MDScreen):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        save_button = MDRaisedButton(text='Сохранить', pos_hint={'center_x': 0.5, 'center_y': 0.5})
        save_button.bind(on_release=self.add_training_entry)

        self.__date_picker = DatePickerButton(title='Выберите дату', pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.__trainings_box = AddTrainingBox()

        self.add_widget(MDBoxLayout(
            self.__date_picker,
            self.__trainings_box,
            save_button,
            orientation='vertical', padding=(dp(20), dp(80), dp(20), dp(20)), spacing=dp(20)
            ))

    def add_training_entry(self, *args):
        added_exercises = self.__trainings_box.get_selected_exercises()
        if added_exercises.__len__() == 0:
            return
        
        data_storage = MDApp.get_running_app().data_storage
        user_data = MDApp.get_running_app().user
        calories_module = CaloriesModule(user_data, data_storage)
        
        selected_date = self.__date_picker.selected_date

        exercises_and_minutes = { record.exercise_name: record.minutes for record in added_exercises }
        calories_module.set_calories_outcome(selected_date.__str__(), exercises_and_minutes)