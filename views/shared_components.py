from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.pickers import MDDatePicker, MDTimePicker
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import MDList
from datetime import date, time, datetime
from typing import Any, List
from abc import ABC, abstractmethod


from kivymd.uix.list import OneLineIconListItem
from kivy.properties import StringProperty

class ListItem:
    '''
    The data of the SelectableList item.
    '''
        
    def __init__(self, id: Any, value: Any, is_selected: bool = False) -> None:
        super().__init__()
        self.__id = id
        self.__value = value
        self.__is_selected = is_selected

    @property
    def id(self) -> Any:
        return self.__id
    
    @property
    def value(self) -> Any:
        return self.__value
    
    @property
    def is_selected(self) -> bool:
        return self.__is_selected
    
    @is_selected.setter
    def is_selected(self, is_selected: bool) -> None:
        self.__is_selected = is_selected

class ListItemCheckbox(IRightBodyTouch, MDCheckbox):
    '''
    The checkbox of the SelectableList item.
    '''

    def __init__(self, item: ListItem, **kwargs) -> None:
        self.active = item.is_selected
        self.__item = item
        super().__init__(**kwargs)

    @property
    def item(self) -> ListItem:
        return self.__item
    
    @item.setter
    def item(self, item: ListItem):
        self.__item = item

    def on_active(self, object, is_selected: bool):
        self.__item.is_selected = is_selected

class SelectableListItem(OneLineAvatarIconListItem):
    '''
    An item of the SelectableList.
    '''

    def __init__(self, item: ListItem, **kwargs) -> None:
        super().__init__(**kwargs)
        self.__item = item
        self.checkbox = ListItemCheckbox(self.__item)
        self.add_widget(self.checkbox)

    @property
    def item(self) -> ListItem:
        return self.__item
    
    @item.setter
    def item(self, item: ListItem):
        self.__item = item
        self.checkbox.item = item

class SelectableList(MDScrollView):
    '''
    A list containing selectable items.
    '''

    __items_data : List[ListItem]

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.list_items = MDList()
        self.__items_data = []
        self.add_widget(self.list_items)

    def add_item(self, text: str, item: ListItem):
        # TODO: Проверять Item'ы по id

        viewItem = SelectableListItem(item, text=text)
        viewItem.item = item

        self.list_items.add_widget(viewItem)
        self.__items_data.append(item)

    def get_selected_items(self) -> List[ListItem]:
        return list(filter(lambda item: item.is_selected, self.__items_data))
    
class ISaveableInputValue(ABC):
    '''
    Defines the contract to save the input values.
    '''

    @abstractmethod
    def save_value(self, value: str) -> None:
        pass
    
    @abstractmethod
    def get_value(self):
        pass
    
class SaveableInputString(ISaveableInputValue):
    __value: str
    
    def __init__(self) -> None:
        self.__value = ''

    def save_value(self, value: str) -> None:
        self.__value = value
    
    def get_value(self) -> str:
        return self.__value
    
class SaveableInputInteger(ISaveableInputValue):
    __value: int
    
    def __init__(self) -> None:
        self.__value = 0

    def save_value(self, value: str) -> None:
        if value is not '':
            self.__value = int(value)
    
    def get_value(self) -> int:
        return self.__value
    
class InputTextField(MDTextField):
    def __init__(self, value: ISaveableInputValue, title: str, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.value = value
        self.hint_text= title
        self.text = self.value.get_value().__str__()

    def on_focus(self, instance_text_field: MDTextField, focus: bool) -> None:
        if focus is False: # If user leaves the field
            self.value.save_value(instance_text_field.text)

class DropDownListItem:
    def __init__(self, title: str, value: Any) -> None:
        self.__title = title
        self.__value = value

    @property
    def title(self) -> str:
        return self.__title
    
    @property
    def value(self) -> Any:
        return self.__value

class IconListItem(OneLineIconListItem):
    icon = StringProperty()

class DropDownList(MDDropDownItem):
    __selected_item: DropDownListItem

    def __init__(self, items: List[DropDownListItem], index_to_display: int = 0, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if items.__len__() == 0:
            raise ValueError('DropDownList must have at least one value.')

        self.__set_selected_item(items[index_to_display])

        menu_items = [
            {
                "viewclass": "IconListItem",
                "text": item.title,
                "on_release": lambda selected_item = item: self.on_item_set(selected_item)
            } for item in items
        ]

        self.__menu = MDDropdownMenu(
            caller=self,
            items=menu_items,
            position="center",
            width_mult=4,
        )

    @property
    def selected_item(self) -> DropDownListItem:
        return self.__selected_item

    def on_release(self) -> None:
        self.__menu.open()

    def on_item_set(self, selected_item: DropDownListItem) -> None:
        self.__set_selected_item(selected_item)
        self.__menu.dismiss()
    
    def __set_selected_item(self, item: DropDownListItem) -> None:
        self.__selected_item = item
        self.text = item.title

class DatePickerButton(MDRaisedButton):
    def __init__(self, title: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = title
        self.__selected_date = date.today()

    @property
    def selected_date(self) -> date:
        return self.__selected_date

    def on_release(self) -> None:
        self.__open_date_picker()

    def __open_date_picker(self) -> None:
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.save_selected_date)
        date_dialog.open()

    def save_selected_date(self, instance: MDDatePicker, selected_date: date, date_range):
        self.__selected_date = selected_date
        
class TimePickerButton(MDRaisedButton):
    def __init__(self, title: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text = title
        self.__selected_time = datetime.now().time()

    @property
    def selected_time(self) -> time:
        return self.__selected_time

    def on_release(self) -> None:
        self.__open_time_picker()

    def __open_time_picker(self) -> None:
        date_dialog = MDTimePicker()
        date_dialog.bind(on_save=self.save_selected_time)
        date_dialog.open()

    def save_selected_time(self, instance: MDDatePicker, selected_time: time):
        self.__selected_time = selected_time