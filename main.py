from kivy.lang import Builder

from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.menu import MDDropdownMenu

from model.user import User

KV = '''
MDScreen:
    screen_manager: screen_manager
    nav_drawer: nav_drawer

    # Объявлен вне навигации, чтобы присутствовал на каждом экране
    MDTopAppBar:
        pos_hint: {"top": 1}
        elevation: 4
        title: "Мое приложение"
        left_action_items: [["menu", lambda x: nav_drawer.set_state("open")]]

    MDNavigationLayout:

        MDScreenManager:
            id: screen_manager

            MDScreen:
                name: "scr_main_screen"

                MDLabel:
                    text: "Добро пожаловать!"
                    halign: "center"

            UserInfoScreen:
                name: "src_user_info"

                MDLabel:
                    text: "User info"
                    halign: "center"

        MDNavigationDrawer:
            id: nav_drawer
            radius: (0, 16, 16, 0)
            close_on_click: "false"
            
            MDNavigationDrawerMenu:
                screen_manager: screen_manager
                nav_drawer: nav_drawer

                MDNavigationDrawerItem:
                    icon: "account-box-outline"
                    text: "Мои данные"
                    on_press:
                        root.nav_drawer.set_state("close")
                        root.screen_manager.current = "src_user_info"

<UserInfoScreen>:
    MDBoxLayout:
        orientation: 'vertical'
        padding: dp(20), dp(60), dp(20), dp(20)  # Left, Top, Right, Bottom
        spacing: dp(10)

        # MDTextField:
        #     id: user_id_field
        #     hint_text: 'User ID'
        #     helper_text: 'Enter your user ID'
        #     helper_text_mode: 'on_focus'

        MDTextField:
            id: weight_field
            hint_text: 'Вес (в кг)'
            helper_text: 'Enter your weight in kg'
            helper_text_mode: 'on_focus'
            input_filter: 'float'
            text: root.user.weight.__str__()

        MDTextField:
            id: height_field
            hint_text: 'Рост (в см)'
            helper_text: 'Enter your height in cm'
            helper_text_mode: 'on_focus'
            input_filter: 'float',
            text: root.user.height.__str__()

        MDTextField:
            id: age_field
            hint_text: 'Возраст'
            helper_text: 'Enter your age'
            helper_text_mode: 'on_focus'
            input_filter: 'int'
            text: root.user.age.__str__()

        MDBoxLayout:
            orientation: 'horizontal'
            MDLabel:
                text: 'Пол: '
                size_hint_x: None
                width: dp(48)

            MDDropDownItem:
                id: sex_select
                text: 'Gender'
                on_release: root.genders.open()

            MDSwitch:
                id: sex_switch
                # 'active' will be True if the switch is on (male) and False if it's off (female)

        MDRaisedButton:
            text: 'Обновить'
            on_release: root.save_user_data()


'''

class UserInfoScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = User("V", 12, 12, 12, True, 12)
        self.gendersDict = {
            "Male": True,
            "Female": False
        }
    
    def save_user_data(self):
        pass

class Example(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)


Example().run()