from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.boxlayout import MDBoxLayout
from views.shared_components import InputTextField, ListItem, SaveableInputInteger, DatePickerButton, SelectableList, SaveableInputString
from kivymd.app import MDApp
from kivy.metrics import dp
from typing import List
from model.calories_module import CaloriesModule
from kivy.clock import Clock

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

class AddMenstruationInfoScreen(MDScreen):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        Clock.schedule_once(self.setup_widgets)

    def setup_widgets(self, dt):
        for i in range(30):
            self.ids.selectable_list.add_item(f"Item {i}", ListItem(id=i, value=i))

    def save_data(self):
        items = self.ids.selectable_list
        print(f'Selected Items:')
        for item in items.get_selected_items():
            print(f'Selected \'{item.id}\'.')