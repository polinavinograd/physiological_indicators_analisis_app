from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.stacklayout import MDStackLayout
from kivymd.uix.label import MDLabel
# from views.shared_components import InputTextField, ListItem, SaveableInputInteger, DatePickerButton, SelectableList, SaveableInputString
from kivymd.app import MDApp
from kivy.metrics import dp
from typing import List, Tuple
from model.calories_module import CaloriesModule
from kivy.properties import StringProperty
from kivy.clock import Clock
from model.menstruation_delay_module import MenstruationDelayModule
from model.stress_module import StressModule
from views.shared_components import *

'''
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
'''

class RadioButtonWithText(MDBoxLayout):
    label_text = StringProperty('')
        
class CheckBoxWithText(MDBoxLayout):
    def __init__(self, text: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.orientation = 'horizontal'

        self.checkbox = MDCheckbox(size_hint=(0.1, 1))
        self.label = MDLabel(size_hint=(0.9, 1), halign='left', valign='middle', text=text)

        self.add_widget(self.checkbox)
        self.add_widget(self.label)

    def has_menstruation(self) -> bool:
        return self.checkbox.active
    
    
class AddSymptomsBox(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.orientation = 'vertical'
        # self.padding=(dp(20), dp(0), dp(20), dp(20))
        # self.spacing=dp(20)
        
        items = [
            DropDownListItem(title='боль в животе', value='abdominal_pain'),
            DropDownListItem(title='расстройство пищеварения', value='digestive_disorders'),
            DropDownListItem(title='боль в груди', value='breast_pain'),
            DropDownListItem(title='кожные воспаления', value='skin_rash')
        ]

        self.__available_symptoms_drop_down_list = DropDownList(items, size_hint=(0.6, 1))
        save_button = MDRaisedButton(
            text='Добавить',
            size_hint=(0.2, 1),
            pos_hint={'center_x': 0.5, 'center_y': 0.5})
        save_button.bind(on_release=self.add_symptom)

        self.add_widget(MDBoxLayout(
            self.__available_symptoms_drop_down_list,
            save_button,
            orientation='horizontal',
            size_hint=(1, 0.2)
        ))

        self.__selected_symptoms = SelectableList(size_hint=(1, 1))
        self.add_widget(self.__selected_symptoms)
        
    def add_symptom(self, *args):
        item_selected = self.__available_symptoms_drop_down_list.selected_item
        
        list_item = ListItem(
            id=item_selected.title,
            value=item_selected.value,
            is_selected=True)
        
        self.__selected_symptoms.add_item(
            text=list_item.id,
            item=list_item)
        
    def get_symptoms(self) -> List[Tuple[str, bool]]:
        return [
            ('abdominal_pain', self.__contains_item('abdominal_pain')),
            ('digestive_disorders', self.__contains_item('digestive_disorders')),
            ('breast_pain', self.__contains_item('breast_pain')),
            ('skin_rash', self.__contains_item('skin_rash'))
            ]
    
    def __contains_item(self, id: str) -> bool:
        selected_items = list(map(lambda i: i.value, self.__selected_symptoms.get_selected_items()))
        return id in selected_items 
        
class SelectMoodBox(MDBoxLayout):
    def __init__(self, *args, **kwargs):
        self.orientation = 'vertical'

        items = [
            DropDownListItem(title='Грустное', value=0),
            DropDownListItem(title='Спокойное', value=1),
            DropDownListItem(title='Веселое', value=2)
        ]
        
        self.__available_mood_drop_down_list = DropDownList(items, size_hint=(1, 1))
        self.add_widget(self.__available_mood_drop_down_list)

class AddMenstruationInfoScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.__data_picker = DatePickerButton('Дата')
        self.__has_menstruation_box = CheckBoxWithText(text='Есть ли месячные?', size_hint=(0.4, 1))
        self.__symptoms_box = AddSymptomsBox(size_hint=(1, 0.6))
        # self.__mood_box = SelectMoodBox()

        moods = [
            DropDownListItem(title='Грустное', value=0),
            DropDownListItem(title='Спокойное', value=1),
            DropDownListItem(title='Веселое', value=2)
        ]

        self.__available_mood_drop_down_list = DropDownList(moods, size_hint=(1, 0.2))
        save_button = MDRaisedButton(text='Сохранить', pos_hint={'center_x': 0.5, 'center_y': 0.5}, size_hint=(1, 0.1))
        save_button.bind(on_release=self.add_symptoms_entry)

        self.add_widget(MDBoxLayout(
            MDStackLayout(
                MDBoxLayout(
                    self.__has_menstruation_box,
                    self.__data_picker,
                    orientation='horizontal', size_hint=(1, 0.1)
                ),
                self.__symptoms_box,
                self.__available_mood_drop_down_list,
                save_button
            ),
            orientation='vertical', padding=(dp(20), dp(60), dp(20), dp(20)), size_hint=(1, 0.9))
        )
        
    def add_symptoms_entry(self, *args):
        data_storage = MDApp.get_running_app().data_storage
        user_data = MDApp.get_running_app().user
        stress_module = StressModule(user_data, data_storage)
        menstruation_module = MenstruationDelayModule(user_data, stress_module, data_storage)

        selected_date = self.__data_picker.selected_date.__str__()

        selected_symptoms = self.__symptoms_box.get_symptoms()
        selected_mood = self.__available_mood_drop_down_list.selected_item.value
        
        menstruation_data_dict = {
            "user_id": user_data.name,
            "date": selected_date,
            selected_symptoms[0][0]: selected_symptoms[0][1],
            selected_symptoms[1][0]: selected_symptoms[1][1],
            selected_symptoms[2][0]: selected_symptoms[2][1],
            selected_symptoms[3][0]: selected_symptoms[3][1],
            'mood': selected_mood,
            'menstruation_status': self.__has_menstruation_box.has_menstruation()
            }

        menstruation_module.set_menstruation_data(menstruation_data_dict)

        # Clock.schedule_once(self.setup_widgets)

    # def setup_widgets(self, dt):
    #     for i in range(30):
    #         self.ids.selectable_list.add_item(f"Item {i}", ListItem(id=i, value=i))

    # def save_data(self):
    #     items = self.ids.selectable_list
    #     print(f'Selected Items:')
    #     for item in items.get_selected_items():
    #         print(f'Selected \'{item.id}\'.')