from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.properties import StringProperty
from model.user import User
from kivy.clock import Clock
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from views.shared_components import *
from views.user_info_screen import *


KV = '''

<IconListItem>

    IconLeftWidget:
        icon: root.icon

<BoxLayoutBelowToolbar@MDBoxLayout>:
    orientation: 'vertical'
    pos_hint: {'top': 0.9}
    size_hint: 1, 0.9

<CheckBoxWithText@MDBoxLayout>:
    orientation: 'horizontal'
    canvas.before:
        Color:
            rgba: 255, 0, 0, 1
        Line:
            width:
            rectangle: self.x, self.y, self.width, self.height

    MDCheckbox:
        id: checkbox
        size_hint: 0.1, 1

    MDLabel:
        text: root.label_text
        size_hint: 0.9, 1
        halign: 'left'
        valign: 'middle'
        
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

<UserInfoScreen>:

    # MDDropDownItem:
    #     id: drop_item
    #     pos_hint: {'center_x': .5, 'center_y': .5}
    #     text: 'Item 0'
    #     on_release: app.menu.open()
        # MDBoxLayout:
        #     orientation: 'horizontal'
        #     MDLabel:
        #         text: 'Пол: '
        #         size_hint_x: None
        #         width: dp(48)

        #     MDDropDownItem:
        #         id: sex_select
        #         text: 'Gender'
        #         on_release: root.genders.open()

        #     MDSwitch:
        #         id: sex_switch
        #         # 'active' will be True if the switch is on (male) and False if it's off (female)

<AddMenstruationInfoScreen>:
    selectable_list: selectable_list

    BoxLayoutBelowToolbar:

        MDStackLayout:
            MDBoxLayout:
                orientation: 'horizontal'
                size_hint: 1, 0.1

                CheckBoxWithText:
                    size_hint: 0.4, 1
                    label_text: 'Есть ли месячные?'

                MDRaisedButton:
                    text: 'Дата'
                # MDDatePicker:
                #     size_hint: 0.6, 1

            MDBoxLayout:
                size_hint: 1, 0.07   

                MDLabel:    
                    size_hint: 0.6, 1            
                    halign: 'left'
                    valign: 'middle'
                    text: 'Симптомы'
                    padding: dp(30)
                    canvas.before:
                        Color:
                            rgba: 255, 0, 0, 1
                        Line:
                            width:
                            rectangle: self.x, self.y, self.width, self.height
                            
                MDLabel:
                    size_hint: 0.4, 1               
                    padding: dp(20)
                    halign: 'left'
                    valign: 'middle'
                    text: 'Настроение'
                    canvas.before:
                        Color:
                            rgba: 255, 0, 0, 1
                        Line:
                            width:
                            rectangle: self.x, self.y, self.width, self.height

            MDBoxLayout:
                orientation: 'horizontal'
                size_hint: 1, 0.73 

                SelectableList:
                    id: selectable_list
                    size_hint: 0.6, 1 
                    canvas.before:
                        Color:
                            rgba: 255, 0, 0, 1
                        Line:
                            width:
                            rectangle: self.x, self.y, self.width, self.height
                
                MDBoxLayout:
                    size_hint: 0.4, 1 
                    orientation: 'vertical'

                    RadioButtonWithText:
                        label_text: 'Веселое'
                        active: True
                        group: 'group'
                    
                    RadioButtonWithText:
                        label_text: 'Спокойное'
                        active: True
                        group: 'group'
                    
                    RadioButtonWithText:
                        label_text: 'Грустное'
                        active: True
                        group: 'group'

            MDBoxLayout:
                size_hint: 1, 0.1
                padding: 10

                MDRaisedButton:
                    text: "Сохранить"
                    on_press: root.save_data()

<AddStressScreen>:
    MDTextField:
        id: stress_level
        hint_text: "Уровень стресса (число)"
        pos_hint: {'center_x': 0.5, 'center_y': 0.7}
        input_filter: 'int'
        size_hint_x: None
        width: 300

    MDFlatButton:
        text: "Выбрать дату"
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        on_release: root.open_date_picker()

    MDFlatButton:
        text: "Добавить запись"
        pos_hint: {'center_x': 0.5, 'center_y': 0.4}
        on_release: root.add_stress_entry()

<AddNutritionsScreen>:
    MDFlatButton:
        text: "Выбрать дату"
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        on_release: root.open_date_picker()

    # SelectableList:
    #     id: selectable_list
    #     size_hint: 0.6, 1 
    #     canvas.before:
    #         Color:
    #             rgba: 255, 0, 0, 1
    #         Line:
    #             width:
    #             rectangle: self.x, self.y, self.width, self.height

    MDTextField:
        id: stress_level
        hint_text: "Масса (в граммах)"
        pos_hint: {'center_x': 0.5, 'center_y': 0.7}
        input_filter: 'float'
        size_hint_x: None
        width: 300
        
    MDFlatButton:
        text: "Добавить запись"
        pos_hint: {'center_x': 0.5, 'center_y': 0.4}
        on_release: root.add_nutritions_entry()

<AddTrainingScreen>:
    MDFlatButton:
        text: "Выбрать дату"
        pos_hint: {'center_x': 0.5, 'center_y': 0.6}
        on_release: root.open_date_picker()

    # SelectableList:
    #     id: selectable_list
    #     size_hint: 0.6, 1 
    #     canvas.before:
    #         Color:
    #             rgba: 255, 0, 0, 1
    #         Line:
    #             width:
    #             rectangle: self.x, self.y, self.width, self.height

    MDTextField:
        id: stress_level
        hint_text: "Время (в минутах)"
        pos_hint: {'center_x': 0.5, 'center_y': 0.7}
        input_filter: 'int'
        size_hint_x: None
        width: 300
        
    MDFlatButton:
        text: "Добавить запись"
        pos_hint: {'center_x': 0.5, 'center_y': 0.4}
        on_release: root.add_nutritions_entry()
'''
    
class AddMenstruationInfoScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_once(self.setup_widgets)

    def setup_widgets(self, dt):
        for i in range(30):
            self.ids.selectable_list.add_item(f"Item {i}", ListItem(id=i))

    def save_data(self):
        items = self.ids.selectable_list
        print(f'Selected Items:')
        for item in items.get_selected_items():
            print(f'Selected \'{item.id}\'.')

class AddStressScreen(MDScreen):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def open_date_picker(self):
        date_dialog = MDDatePicker()
        date_dialog.bind (on_save=self.get_date_of_picker)
        date_dialog.open()

    def get_date_of_picker(self, instance, value, date_range):
        # Обработка выбранной даты
        print("Выбранная дата:", value)

    def add_stress_entry(self):
        pass
        # stress_level = self.sm.get_screen('stress_entry').ids.stress_level.text
        # Добавление записи о стрессе
        # print("Уровень стресса:", stress_level)

class AddNutritionsScreen(MDScreen):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def open_date_picker(self) -> None:
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.get_date_of_picker)
        date_dialog.open()

    def get_date_of_picker(self, instance, value, date_range):
        # Обработка выбранной даты
        print("Выбранная дата:", value)

    def add_nutritions_entry(self):
        pass

class AddTrainingScreen(MDScreen):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

    def open_date_picker(self) -> None:
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.get_date_of_picker)
        date_dialog.open()
        
    def get_date_of_picker(self, instance, value, date_range):
        # Обработка выбранной даты
        print("Выбранная дата:", value)

    def add_training_entry(self):
        pass

class RadioButtonWithText(MDBoxLayout):
    label_text = StringProperty('')
        
class CheckBoxWithText(MDBoxLayout):
    label_text = StringProperty('')

class Example(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)


Example().run()