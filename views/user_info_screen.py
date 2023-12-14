from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from model.user import User
from enum import Enum
from views.shared_components import InputTextField, SaveableInputString, SaveableInputInteger, DropDownList, DropDownListItem
from kivymd.uix.button import MDRaisedButton
from kivymd.app import MDApp
from kivy.metrics import dp

class Gender(Enum):
    Undefined = None
    Female = False
    Male = True

class UserViewModel:
    '''
    Contains the user data displayed on screen.
    '''

    def __init__(self) -> None:
        self.__user_name = SaveableInputString()
        self.__weight = SaveableInputInteger()
        self.__height = SaveableInputInteger()
        self.__age = SaveableInputInteger()
        self.__sex = None
        self.__brm = None

    @property
    def user_name(self) -> SaveableInputString:
        return self.__user_name
    
    @user_name.setter
    def user_name(self, user_name: str) -> None:
        self.__user_name.save_value(user_name)
        
    @property
    def weight(self) -> SaveableInputInteger:
        return self.__weight
    
    @weight.setter
    def weight(self, weight: int) -> None:
        self.__weight.save_value(weight)

    @property
    def height(self) -> SaveableInputInteger:
        return self.__height
    
    @height.setter
    def height(self, height: int) -> None:
        self.__height.save_value(height)
        
    @property
    def age(self) -> SaveableInputInteger:
        return self.__age
    
    @age.setter
    def age(self, age: int) -> None:
        self.__age.save_value(age)
        
    @property
    def brm(self) -> float:
        return self.__brm
    
    @brm.setter
    def brm(self, brm: float) -> None:
        self.__brm = brm

class UserInfoScreen(MDScreen):
    '''
    Экран управления данными пользователя.
    '''

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        user_data = MDApp.get_running_app().user
        self.__set_user_view(user_data)

        saveButton = MDRaisedButton(text='Обновить')
        saveButton.bind(on_release=self.save_user_data)

        self.add_widget(MDBoxLayout(
            InputTextField(self.__user_view_model.user_name, title='Ваш никнейм'),
            InputTextField(self.__user_view_model.weight, title='Вес (в кг)', input_filter='int'),
            InputTextField(self.__user_view_model.height, title='Рост (в см)', input_filter='int'),
            InputTextField(self.__user_view_model.age, title='Возраст', input_filter='int'),
            self.__gender_list,
            saveButton,
            orientation='vertical', padding=(dp(20), dp(0), dp(20), dp(20)), spacing=dp(20)
        ))
    
    def save_user_data(self, instance: MDRaisedButton):
        user_data = User(
            self.__user_view_model.user_name.get_value(),
            self.__user_view_model.weight.get_value(),
            self.__user_view_model.height.get_value(),
            self.__user_view_model.age.get_value(),
            self.__gender_list.selected_item.value.value,
            self.__user_view_model.brm)
        
        data_storage = MDApp.get_running_app().data_storage

        user_data_dict = {"user_id": user_data.name,
                     "weight": user_data.weight,
                     "height": user_data.height,
                     "age": user_data.age,
                     "brm": user_data.brm}

        data_storage.try_insert_user(user_data_dict)
        MDApp.get_running_app().user = user_data

    def __set_user_view(self, user_data: User) -> None:
        self.__user_view_model = UserViewModel()
        self.__user_view_model.user_name.save_value(user_data.name)
        self.__user_view_model.weight.save_value(user_data.weight)
        self.__user_view_model.height.save_value(user_data.height)
        self.__user_view_model.age.save_value(user_data.age)
        self.__user_view_model.brm = user_data.brm
        
        index_to_display = 2 # Индекс опции 'Не указан'
        if user_data.sex == Gender.Female.value:
            index_to_display = 0
        elif user_data.sex == Gender.Male.value:
            index_to_display = 1
        
        self.__gender_list = DropDownList([
                DropDownListItem('Женский', Gender.Female),
                DropDownListItem('Мужской', Gender.Male),
                DropDownListItem('Не указан', Gender.Undefined)],
                index_to_display=index_to_display)