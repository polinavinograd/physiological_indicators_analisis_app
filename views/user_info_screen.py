from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from model.user import User
from enum import Enum
from views.shared_components import InputTextField, SaveableInputString, SaveableInputInteger
from kivymd.uix.button import MDRaisedButton
from kivy.metrics import dp

class Gender(Enum):
    Undefined = None
    Female = True
    Male = False

class UserViewModel:
    '''
    Contains the user data displayed on screen.
    '''

    def __init__(self) -> None:
        self.__user_name = SaveableInputString()
        self.__weight = SaveableInputInteger()
        self.__height = SaveableInputInteger()
        self.__age = SaveableInputString()
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
    def age(self) -> SaveableInputString:
        return self.__age
    
    @age.setter
    def age(self, age: int) -> None:
        self.__age.save_value(age)
        
    @property
    def sex(self) -> Gender:
        return self.__sex
    
    @sex.setter
    def sex(self, sex: Gender) -> None:
        self.__sex = sex
        
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
        self.user = UserViewModel()

        saveButton = MDRaisedButton(text='Обновить')
        saveButton.bind(on_release=self.save_user_data)

        self.add_widget(MDBoxLayout(
            InputTextField(self.user.user_name, hint_text='Ваш никнейм'),
            InputTextField(self.user.weight, input_filter='int', hint_text='Вес (в кг)'),
            InputTextField(self.user.height, input_filter='int', hint_text='Рост (в см)'),
            InputTextField(self.user.age, input_filter='int', hint_text='Возраст'),
            saveButton,
            orientation='vertical', padding=(dp(20), dp(0), dp(20), dp(20)), spacing=dp(20)
        ))
    
    def save_user_data(self, instance: MDRaisedButton):
        userData = User(
            self.user.user_name.get_value(),
            self.user.weight.get_value(),
            self.user.height.get_value(),
            self.user.age.get_value(),
            self.user.sex,
            self.user.brm) # TODO: Нужно ли отображать brm?
        
        # TODO: Обновить данные пользователя