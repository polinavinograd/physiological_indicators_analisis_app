﻿from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.dropdownitem import MDDropDownItem
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.textfield import MDTextField
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import MDList
from typing import List
from abc import ABC, abstractmethod

class ListItem:
    '''
    The data of the SelectableList item.
    '''
        
    def __init__(self, id: int) -> None:
        super().__init__()
        self.__id = id
        self.__is_selected = False

    @property
    def id(self) -> int:
        return self.__id
    
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

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.__item = None

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

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)
        self.checkbox = ListItemCheckbox()
        self.add_widget(self.checkbox)
        self.__item = None

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
        viewItem = SelectableListItem(text=text)
        viewItem.item = item

        self.list_items.add_widget(viewItem)
        self.__items_data.append(item)

    def get_selected_items(self) -> List[ListItem]:
        return filter(lambda item: item.is_selected, self.__items_data)
    
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
    def __init__(self, value: ISaveableInputValue, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.value = value
        self.text = self.value.get_value().__str__()

    def on_focus(self, instance_text_field: MDTextField, focus: bool) -> None:
        if focus is False: # If user leaves the field
            self.value.save_value(instance_text_field.text)

class DropDownListItem:
    def __init__(self, title: str) -> None:
        self.__title = title

    @property
    def title(self) -> str:
        return self.__title

class DropDownList(MDDropDownItem):
    def __init__(self, items: List[DropDownListItem], *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        if items.__len__() == 0:
            raise ValueError('DropDownList must have at least one value.')

        self.text = items[0].title

        menu_items = [
            {
                "text": item.title,
                "on_release": self.on_item_set,
            } for item in items
        ]

        self.__menu = MDDropdownMenu(
            caller=self,
            items=menu_items,
            position="center",
        )

        self.__menu.bind()

    def on_release(self):
        self.__menu.open()

    def set_item(self, text_item):
        pass
        # self.screen.ids.drop_item.set_item(text_item)
        # self.menu.dismiss()

    def on_item_set(self, *args):
        self.set_item('aaa')
        self.__menu.dismiss()