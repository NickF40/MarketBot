import sqlite3 as sqlite
import config, const, temp


def give_menu():
    db = sqlite.connect(const.DB_PATH)
    cur = db.cursor()
    cur.execute("SELECT name FROM categories")
    temp_items = cur.fetchall()
    categories = []
    for item in temp_items:
        categories.append(item[0])
    return categories


def define_type(item_type):
    db = sqlite.connect(const.DB_PATH)
    cur = db.cursor()
    cur.execute("SELECT * id FROM categories WHERE name = ?", (item_type,))
    type1 = cur.fetchone()
    return type1[0]


def type_finder(item_type):
    db = sqlite.connect(const.DB_PATH)
    cur = db.cursor()
    cur.execute("SELECT id FROM items WHERE type = ?", (item_type,))
    temp_items = cur.fetchall()
    items = []
    for item in temp_items:
        items.append(item_finder(item[0]))
    return items


def get_users():
    db = sqlite.connect(const.DB_PATH)
    cur = db.cursor()
    cur.execute("SELECT user_id FROM users")
    return cur.fetchall()


def item_finder(item_id):
    db = sqlite.connect(const.DB_PATH)
    cur = db.cursor()
    cur.execute("SELECT * FROM items WHERE id = ?", (str(item_id),))
    item = temp.Item()
    item.set_full_data(*cur.fetchone())
    print(item.get_data())
    return item


def is_seller(user_id):
    db = sqlite.connect(const.DB_PATH)
    cur = db.cursor()
    cur.execute('SELECT user_id FROM clients WHERE user_id = (?)', (str(user_id),))
    if cur.fetchone():
        return True
    else:
        return False


def add_user(message):
    db = sqlite.connect(const.DB_PATH)
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
    db = sqlite.connect(const.DB_PATH)
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


def add_item(item, user):
    db = sqlite.connect(const.DB_PATH)
    cur = db.cursor()
    cur.execute("SELECT * FROM items WHERE (name) = (?)", (item.description,))
    print(cur.fetchone())
    if not cur.fetchone():
        try:
            cur.execute("INSERT INTO items "
                        "(type, description, hash, seller_name) "
                        "VALUES (?,?,?,?)",
                        (
                            item.type,
                            item.description,
                            user.id,
                            user.username))
            print('\nadded\n')
            db.commit()
        except Exception as e:
            config.log(Error=e, Text='ADDING_NEW_ITEM_ERROR')


def add_kat(message):
    db = sqlite.connect(const.DB_PATH)
    cur = db.cursor()
    cur.execute("SELECT * FROM categories WHERE (name) = (?)", (message.text,))
    if not cur.fetchone():
        try:
            cur.execute("INSERT INTO categories"
                        "(name)"
                        "VALUES (?)",
                        ((message.text),))
            db.commit()
            print("added")
        except Exception as e:
            config.log(Error=e, Text='ADDING_NEW_CATEGORY_ERROR')


def get_user_step(user_id):
    if user_id in const.user_adding_item_step.keys():
        return const.user_adding_item_step[user_id]
    else:
        return False


def add_item_category(message):
    if message.text in give_menu():
        new_item = const.new_items_user_adding[message.chat.id]
        new_item.type = message.text


def add_item_description(message):
    new_item = const.new_items_user_adding[message.chat.id]
    new_item.description = message.text
    add_item(new_item, message.chat)
    new_item.delete()


def find_users_items(user_id):
    db = sqlite.connect(const.DB_PATH)
    cur = db.cursor()
    cur.execute("SELECT * FROM items WHERE hash = ?", (str(user_id),))
    result = cur.fetchall()
    return result
