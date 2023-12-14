from kivy.lang import Builder
from kivymd.app import MDApp
from model.user import User
from views.shared_components import *
from views.user_info_screen import *
from views.add_stress_screen import *
from views.add_nutritions_screen import *
from views.add_training_screen import *
from views.check_stress_screen import *
from views.add_menstruation_info_screen import *
from views.get_calorie_report_screen import *
from views.menstruation_prediction_screen import *
from data_storage.data_store import IndicatorsDataStorage

KV = '''

# <MDBoxLayout>:
#     canvas.before:
#         Color:
#             rgba: 243, 156, 18, 1
#         Line:
#             width:
#             rectangle: self.x, self.y, self.width, self.height
        
<RadioButtonWithText@MDBoxLayout>:
    MDCheckbox:
        id: checkbox
        group: 'group'
        size_hint: 0.2, 1
        pos_hint: {'center_x': .5, 'center_y': .5}

    MDLabel:
        text: root.label_text
        size_hint: 0.8, 1
        halign: 'left'
        valign: 'middle'

<DrawerClickableItem@MDNavigationDrawerItem>:
    text_color: 1, 1, 1, 1
    # focus_color: "#e7e4c0"
    # ripple_color: "#c5bdd2"

MDScreen:
    screen_manager: screen_manager
    nav_drawer: nav_drawer

    # Объявлен вне навигации, чтобы присутствовал на каждом экране
    MDTopAppBar:
        id: top_bar
        pos_hint: {"top": 1}
        size_hint: 1, 0.1 
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
                    
            AddStressScreen:
                name: "scr_stress_screen"
                    
            AddNutritionsScreen:
                name: "scr_nutritions_screen"
                    
            AddTrainingScreen:
                name: "scr_fitness_screen"
                    
            AddMenstruationInfoScreen:
                name: "scr_menstruation_screen"

            CheckStressScreen:
                name: "scr_check_stress_screen"

            GetCalorieReportScreen:
                name: "scr_get_calorie_report_screen"

            MenstruationPredictionScreen:
                name: "scr_menstruation_prediction_screen"

        MDNavigationDrawer:
            id: nav_drawer
            radius: (0, 16, 16, 0)
            close_on_click: "false"
            
            MDNavigationDrawerMenu:
                screen_manager: screen_manager
                nav_drawer: nav_drawer

                DrawerClickableItem:
                    icon: "account-box-outline"
                    text: "Мои данные"
                    on_press:
                        root.nav_drawer.set_state("close")
                        root.screen_manager.current = "src_user_info"

                DrawerClickableItem:
                    icon: "alert-outline"
                    text: "Добавить стресс"
                    on_press:
                        root.nav_drawer.set_state("close")
                        root.screen_manager.current = "scr_stress_screen"

                DrawerClickableItem:
                    icon: "food-apple"
                    text: "Добавить питание"
                    on_press:
                        root.nav_drawer.set_state("close")
                        root.screen_manager.current = "scr_nutritions_screen"

                DrawerClickableItem:
                    icon: "dumbbell"
                    text: "Добавить тренировку"
                    on_press:
                        root.nav_drawer.set_state("close")
                        root.screen_manager.current = "scr_fitness_screen"

                DrawerClickableItem:
                    icon: "water"
                    text: "Добавить месячный цикл"
                    on_press:
                        root.nav_drawer.set_state("close")
                        root.screen_manager.current = "scr_menstruation_screen"
                        
                DrawerClickableItem:
                    icon: "alert-outline"
                    text: "Стресс за период"
                    on_press:
                        root.nav_drawer.set_state("close")
                        root.screen_manager.current = "scr_check_stress_screen"
                        
                DrawerClickableItem:
                    icon: "file-document-check-outline"
                    text: "Отчет по калориям"
                    on_press:
                        root.nav_drawer.set_state("close")
                        root.screen_manager.current = "scr_get_calorie_report_screen"
                        
                DrawerClickableItem:
                    icon: "calendar-alert"
                    text: "Прогноз"
                    on_press:
                        root.nav_drawer.set_state("close")
                        root.screen_manager.current = "scr_menstruation_prediction_screen"
'''


class Application(MDApp):
    def build(self):
        self.data_storage = IndicatorsDataStorage()
        self.user = self.data_storage.get_user('polina.vngrd')

        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)


Application().run()