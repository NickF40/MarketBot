# -*- coding: utf-8 -*-

import config


class Basket:
    sum_price = None
    items_num = None
    items = []

    def set_items(self, *args):         # на вход подается список готовых собранных объектов типа Item
        for item in range(args):        # input = list of Items objects
            self.items.append(item)     # no output
            self.items_num += 1
            self.sum_price += Item.get_price()

    def set_data_items(self, *args):     # на вход подается список , состоящий из структур данных типа Item.data_types
        for data in range(args):        # из каждой Item.data_types структуры собирается объект Item
            temp = Item()               # и переходит в основной список Basket.items[]
            temp.set_data(data)
            self.items.append(temp)
            temp.delete()

    def delete_item(self, arg):         # удаляет объект из Basket.items[]
        if isinstance(arg,Item):
            try:
                self.items.remove(arg)
                self.items.sort()
            except ValueError as e:
                config.log(Error=e, Text="CANT_DELETE_ITEM\nITEM_NOT_EXIST")
        if isinstance(arg,int):
            try:
                self.items.remove(self.items[arg])
                self.items.sort()
            except IndexError:
                config.log(Error=e, Text="CANT_DELETE_ITEM\nITEM_WITH_SUCH_INDEX_NOT_EXIST")

    def get_items(self):
        args = []
        for item in range(self.items):
            args.append((item.get_data()))
        return args

    def delete(self):
        self.sum_price = None
        self.items_num = None
        self.items = None
