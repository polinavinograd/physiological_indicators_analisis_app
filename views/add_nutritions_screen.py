from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from views.shared_components import InputTextField, ListItem, SaveableInputInteger, DatePickerButton, SelectableList, SaveableInputString
from kivymd.app import MDApp
from kivy.metrics import dp
from typing import List
from model.calories_module import CaloriesModule

class NewIngredientRecord:
    def __init__(self) -> None:
        self.__ingredient_name = SaveableInputString()
        self.__mass = SaveableInputInteger()

    @property
    def ingredient_name(self) -> SaveableInputString:
        return self.__ingredient_name
    
    @ingredient_name.setter
    def ingredient_name(self, ingredient_name: str) -> None:
        self.__ingredient_name.save_value(ingredient_name)
        
    @property
    def mass(self) -> SaveableInputInteger:
        return self.__mass
    
    @mass.setter
    def mass(self, mass: int) -> None:
        self.__mass.save_value(mass)

class AddIngredientsBox(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.orientation = 'vertical'
        self.padding=(dp(20), dp(0), dp(20), dp(20))
        self.spacing=dp(20)

        self.__new_ingredient_record = NewIngredientRecord()

        self.__ingredient_input = InputTextField(self.__new_ingredient_record.ingredient_name, title='Введите ингредиент')
        self.__mass_input = InputTextField(
            self.__new_ingredient_record.mass,
            title='Масса (в г)',
            input_filter='int',
            size_hint=(0.8, 1))

        save_button = MDRaisedButton(
            text='Добавить',
            size_hint=(0.2, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5})
        save_button.bind(on_release=self.add_inredient)

        self.__ingredients = SelectableList(size_hint=(0.6, 1))

        self.add_widget(MDBoxLayout(
            self.__ingredient_input,
            self.__mass_input,
            save_button,
            orientation='horizontal',
            size_hint=(1, 0.2)
        ))

        self.add_widget(self.__ingredients)
        
    def get_selected_ingredients(self) -> List[NewIngredientRecord]:
        selected_items = self.__ingredients.get_selected_items()
        return list(map(lambda item: item.value, selected_items))

    def add_inredient(self, *args):
        if self.__new_ingredient_record.ingredient_name.get_value() == '':
            return
        
        list_item = ListItem(
            id=self.__new_ingredient_record.ingredient_name.get_value(),
            value=self.__new_ingredient_record,
            is_selected=True
        )

        self.__ingredients.add_item(
            text=self.__new_ingredient_record.ingredient_name.get_value(),
            item=list_item)

class AddNutritionsScreen(MDScreen):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        save_button = MDRaisedButton(text='Сохранить', pos_hint={'center_x': 0.5, 'center_y': 0.5})
        save_button.bind(on_release=self.add_nutritions_entry)

        self.__date_picker = DatePickerButton(title='Выберите дату', pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.__ingredients_box = AddIngredientsBox()

        self.add_widget(MDBoxLayout(
            self.__date_picker,
            self.__ingredients_box,
            save_button,
            orientation='vertical', padding=(dp(20), dp(80), dp(20), dp(20)), spacing=dp(20)
            ))

    def add_nutritions_entry(self, *args):
        added_ingredients = self.__ingredients_box.get_selected_ingredients()
        if added_ingredients.__len__() == 0:
            return

        data_storage = MDApp.get_running_app().data_storage
        user_data = MDApp.get_running_app().user
        calories_module = CaloriesModule(user_data, data_storage)

        selected_date = self.__date_picker.selected_date

        ingredients_and_mass = { record.ingredient_name.get_value(): record.mass.get_value() for record in added_ingredients }
        calories_module.set_calories_intake(selected_date.__str__(), ingredients_and_mass)