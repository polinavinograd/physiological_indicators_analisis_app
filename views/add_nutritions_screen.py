from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from views.shared_components import DropDownList, DropDownListItem, InputTextField, ListItem, DatePickerButton, SaveableInputInteger, SaveableInputString, SelectableList
from kivymd.app import MDApp
from kivy.metrics import dp
from typing import List, Tuple
from model.calories_module import CaloriesModule

class IngredientRecord:
    def __init__(self) -> None:
        self.__ingredient_name = SaveableInputString()
        self.__calorie = SaveableInputInteger()

    @property
    def ingredient_name(self) -> SaveableInputString:
        return self.__ingredient_name
    
    @ingredient_name.setter
    def ingredient_name(self, ingredient_name: str) -> None:
        self.__ingredient_name.save_value(ingredient_name)
        
    @property
    def calorie(self) -> SaveableInputInteger:
        return self.__calorie
    
    @calorie.setter
    def calorie(self, calorie: int) -> None:
        self.__calorie.save_value(calorie)
        
class SelectedIngredientRecord:
    def __init__(self, ingredient_name: str, calorie: int, mass: int) -> None:
        self.__ingredient_name = ingredient_name
        self.__calorie = calorie
        self.__mass = mass

    @property
    def ingredient_name(self) -> str:
        return self.__ingredient_name
    
    @property
    def calorie(self) -> int:
        return self.__calorie
        
    @property
    def mass(self) -> int:
        return self.__mass

class AddIngredientsBox(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.orientation = 'vertical'
        self.padding=(dp(20), dp(0), dp(20), dp(20))
        self.spacing=dp(20)

        data_storage = MDApp.get_running_app().data_storage
        available_ingredients = data_storage.get_ingredients_list()
        
        # Ключ - название, значение - калории
        items = self.__get_ingredients_list(available_ingredients)
        self.__available_ingredients_drop_down_list = DropDownList(items, size_hint=(0.6, 1))

        self.__mass_entered = SaveableInputInteger()
        self.__mass_input = InputTextField(
            self.__mass_entered,
            title='Масса (в г)',
            input_filter='int',
            size_hint=(0.8, 1))

        save_button = MDRaisedButton(
            text='Добавить',
            size_hint=(0.2, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5})
        save_button.bind(on_release=self.add_inredient)

        self.add_widget(MDBoxLayout(
            self.__available_ingredients_drop_down_list,
            self.__mass_input,
            save_button,
            orientation='horizontal',
            size_hint=(1, 0.2)
        ))

        self.__selected_ingredients = SelectableList(size_hint=(1, 1))
        self.add_widget(self.__selected_ingredients)

    def __get_ingredients_list(self, ingredients: List[Tuple[str,int]]) -> List[DropDownListItem]:
        result = []
        for ingredient in ingredients:
            result.append(DropDownListItem(ingredient[0], ingredient[1]))

        return result
        
    def get_selected_ingredients(self) -> List[SelectedIngredientRecord]:
        selected_items = self.__selected_ingredients.get_selected_items()
        return list(map(lambda item: item.value, selected_items))

    def add_inredient(self, *args):
        mass_entered = self.__mass_entered.get_value()
        if mass_entered <= 0:
            return

        # Ключ - название, значение - калории
        item_selected = self.__available_ingredients_drop_down_list.selected_item
        
        list_item = ListItem(
            id=item_selected.title,
            value=SelectedIngredientRecord(
                ingredient_name=item_selected.title,
                calorie=item_selected.value,
                mass=mass_entered),
            is_selected=True)

        self.__selected_ingredients.add_item(
            text=list_item.id,
            item=list_item)

class AddNutritionsScreen(MDScreen):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        save_button = MDRaisedButton(text='Сохранить', pos_hint={'center_x': 0.5, 'center_y': 0.5})
        save_button.bind(on_release=self.add_nutritions_entry)

        self.__date_picker = DatePickerButton(title='Выберите дату', pos_hint={'center_x': 0.5, 'center_y': 0.5})
        self.__ingredients_box = AddIngredientsBox(pos_hint={'center_y': 0.5})

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

        ingredients_and_mass = { record.ingredient_name: record.mass for record in added_ingredients }
        calories_module.set_calories_intake(selected_date.__str__(), ingredients_and_mass)