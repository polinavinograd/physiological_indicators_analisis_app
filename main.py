from kivy.lang import Builder
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.selection import MDSelectionList
from kivymd.uix.scrollview import MDScrollView
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from model.user import User
from kivymd.uix.list import TwoLineAvatarListItem
from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from abc import ABC, abstractmethod
from kivy.clock import Clock

class IListItem(ABC):
    @property
    def id(self) -> int:
        return self._id
    
    @id.setter
    def id(self, id: int):
        self._id = id

    @abstractmethod
    def set_selected(self, is_selected: bool):
        pass

class SelectableListItem(OneLineAvatarIconListItem):
    checkbox = ObjectProperty(None)

    @property
    def item(self) -> IListItem:
        return self.__item
    
    @item.setter
    def item(self, item: IListItem):
        self.__item = item
        self.checkbox.item = item

class ListItemCheckbox(IRightBodyTouch, MDCheckbox):
    @property
    def item(self) -> IListItem:
        return self.__item
    
    @item.setter
    def item(self, item: IListItem):
        self.__item = item

    def on_active(self, something, is_selected: bool):
        self.item.set_selected(is_selected)

class SelectableList(MDScrollView):
    def add_item(self, text: str, item: IListItem):
        viewItem = SelectableListItem(text=text)
        viewItem.item = item

        self.ids.list_items.add_widget(viewItem)
        # self.root.ids.list_items.add_widget(SelectableListItem(item=item, text=text))
    


KV = '''
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

<SelectableListItem@OneLineAvatarIconListItem>:
    checkbox: checkbox

    ListItemCheckbox:
        id: checkbox
    
<SelectableList@MDScrollView>:
    
    MDList:
        id: list_items
        
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
                    
            MDScreen:
                name: "scr_stress_screen"

                MDLabel:
                    text: "Информация о стрессе"
                    halign: "center"
                    
            MDScreen:
                name: "scr_nutritions_screen"

                MDLabel:
                    text: "Информация о приеме пищи"
                    halign: "center"
                    
            MDScreen:
                name: "scr_fitness_screen"

                MDLabel:
                    text: "Информация о проведенной тренировке"
                    halign: "center"
                    
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
                    text: "Стресс"
                    on_press:
                        root.nav_drawer.set_state("close")
                        root.screen_manager.current = "scr_stress_screen"

                DrawerClickableItem:
                    icon: "alert-outline"
                    text: "Питание"
                    on_press:
                        root.nav_drawer.set_state("close")
                        root.screen_manager.current = "scr_nutritions_screen"

                DrawerClickableItem:
                    icon: "alert-outline"
                    text: "Тренировки"
                    on_press:
                        root.nav_drawer.set_state("close")
                        root.screen_manager.current = "scr_fitness_screen"

                DrawerClickableItem:
                    icon: "alert-outline"
                    text: "Месячный цикл"
                    on_press:
                        root.nav_drawer.set_state("close")
                        root.screen_manager.current = "scr_menstruation_screen"

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

<AddMenstruationInfoScreen>:
    selectable_list: selectable_list

    BoxLayoutBelowToolbar:

        MDStackLayout:            
            CheckBoxWithText:
                size_hint: 1, 0.2
                label_text: 'Есть ли месячные?'

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
                size_hint: 1, 0.63 

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

<MyItem>
    text: "Two-line item with avatar"
    secondary_text: "Secondary text here"
    _no_ripple_effect: True
'''

class MyItem(TwoLineAvatarListItem):
    pass

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
    
class AddMenstruationInfoScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_once(self.setup_widgets)

    def setup_widgets(self, dt):
        for i in range(30):
            self.ids.selectable_list.add_item(f"Item {i}", ListItem(id=i))

    def save_data(self):
        pass

class RadioButtonWithText(MDBoxLayout):
    label_text = StringProperty('')

class ListItem(IListItem):
    def __init__(self, id: int) -> None:
        self.id = id
        super().__init__()
    
    @property
    def id(self) -> int:
        return self._id
    
    @id.setter
    def id(self, id: int):
        self._id = id

    def set_selected(self, is_selected: bool):
        print(f"Item {self.id} selected!")
        
class CheckBoxWithText(MDBoxLayout):
    label_text = StringProperty('')

class Example(MDApp):
    def build(self):
        self.theme_cls.primary_palette = "Orange"
        self.theme_cls.theme_style = "Dark"
        return Builder.load_string(KV)


Example().run()