from kivymd.uix.list import IRightBodyTouch, OneLineAvatarIconListItem
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList
from typing import List

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