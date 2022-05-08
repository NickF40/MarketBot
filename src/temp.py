import sqlite3 as sqlite
import config, const
import telebot


def type_finder(item_type):
    type = const.item_types[item_type]
    db = sqlite.connect("clientbase.db")
    cur = db.cursor()
    cur.execute("SELECT id FROM items WHERE type = ?", (str(type)))
    temp_items = cur.fetchall()
    items = []
    for item in temp_items:
        items.append(item_finder(item[0]))
    return items


def item_finder(item_id):
    db = sqlite.connect("clientbase.db")
    cur = db.cursor()
    cur.execute("SELECT * FROM items WHERE id = ?", (str(item_id)))
    item = Item()
    item.set_full_data(*cur.fetchone())
    print(item.get_data())
    return item


def isSeller(user_id):
    db = sqlite.connect("clientbase.db")
    cur = db.cursor()
    cur.execute('SELECT user_id FROM clients WHERE user_id = (?)', (str(user_id),))
    if cur.fetchone():
        return True
    else:
        return False


def add_user(message):
    db = sqlite.connect("clientbase.db")
    cur = db.cursor()
    try:
        cur.execute("SELECT * FROM users WHERE user_id = (?)", (message.from_user.id,))
    except Exception as e:
        config.log(Error=e, Text="DBTESTING ERROR")
    if not cur.fetchone():
        try:
            cur.execute("INSERT INTO users (user_id, first_name, last_name, username) VALUES (?,?,?,?)", (
                message.from_user.id,
                message.from_user.first_name,
                message.from_user.last_name,
                message.from_user.username))
            config.log(Text="User successfully added",
                       user=str(message.from_user.first_name + " " + message.from_user.last_name))
        except Exception as e:
            config.log(Error=e, Text="USER_ADDING_ERROR")
        db.commit()
    else:
        config.log(Error="IN_THE_BASE_YET",
                   id=message.from_user.id,
                   info=str(message.from_user.last_name) + " " + str(message.from_user.first_name),
                   username=message.from_user.username)


def add_client(message):
    db = sqlite.connect("clientbase.db")
    cur = db.cursor()
    login = message.text[1:]
    try:
        cur.execute("SELECT * FROM clients WHERE user_id = (?)", (message.from_user.id,))
    except Exception as e:
        config.log(Error=e, Text="DBTESTING ERROR")
    if not cur.fetchone():
        try:
            cur.execute("INSERT INTO clients (user_id) VALUES (?)", (message.from_user.id,))
            config.log(Text="Client successfully added",
                       user=str(message.from_user.first_name + " " + message.from_user.last_name))
        except Exception as e:
            config.log(Error=e, Text="CLIENT_ADDING_ERROR")
        db.commit()
    else:
        config.log(Error="IN_THE_BASE_YET",
                   id=message.from_user.id,
                   info=str(message.from_user.last_name) + " " + str(message.from_user.first_name),
                   username=message.from_user.username)


class Item:
    id = None
    type = None
    description = None
    seller = None
    data_types = ['id', 'type', 'description']

    def get_data(self):  # возвращает список , состо€щий из структуры данных типа Item.data_types
        args = (self.description,)
        return args

    def set_data(self, *args):
        try:
            self.description = args[3]
        except Exception as e:
            config.log(Error=e, text="SET_DATA_ERROR_OCCURED")

    def set_full_data(self, *args):
        try:
            self.id = args[0]
            self.type = args[1]
            self.description = args[5]
            self.seller = args[8]
            print('seller is ' + str(self.seller))
        except Exception as e:
            config.log(Error=e, text="SET_DATA_ERROR_OCCURED")

    def get_desc2(self):
        data = self.get_data()
        markup = telebot.types.InlineKeyboardMarkup()
        btn_buy = telebot.types.InlineKeyboardButton(text="Ваша цена", callback_data='p'+ str(self.id))
        markup.row(btn_buy)
        return markup

    def swap_desc(self):
        markup = telebot.types.InlineKeyboardMarkup()
        btn_buy = telebot.types.InlineKeyboardButton(text='Ваша цена', callback_data='p'+ str(self.id))
        markup.row(btn_buy)
        return markup

    def delete(self):
        self.id = None
        self.type = None
        self.id = None
        self.description = None
        self.seller = None


def add_item(item, user_id):
    db = sqlite.connect("clientbase.db")
    cur = db.cursor()
    cur.execute("SELECT * FROM items WHERE (name) = (?)", (item.get_name(),))
    print(cur.fetchone())
    if not cur.fetchone():
        try:
            cur.execute("INSERT INTO items "
                        "(type, description, hash, seller_name) "
                        "VALUES (?,?,?,?)",
                        (item.type, item.description, user_id,
                         item.seller))
            db.commit()
        except Exception as e:
            config.log(Error=e, Text='ADDING_NEW_ITEM_ERROR')


# типа хэш но нифига не хэш, а просто id владельца
def find_users_items(user_id):
    db = sqlite.connect("clientbase.db")
    cur = db.cursor()
    cur.execute("SELECT * FROM items WHERE hash = ?", (str(user_id),))
    result = cur.fetchall()
    return result
