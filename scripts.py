import sqlite3
import os
import glob

db = sqlite3.connect('users.db')


def all_users_id(sex):
    global db
    cursor = db.cursor()
    cursor.execute('''SELECT user_id FROM users WHERE sex !=? and index_activity=?''', (sex, 1,))
    c = cursor.fetchall()
    db.commit()
    return c


def save_photo(user_id, photo):
    global db
    c = db.cursor()
    c.execute('''UPDATE users SET photo=? WHERE user_id=?''',(photo, user_id))
    db.commit()

def check_photo(user_id):
    global db
    c = db.cursor()
    c.execute("SELECT photo FROM users WHERE user_id=?", (user_id,))
    return c.fetchone()[0]


def user_sex(user_id):
    global db
    c = db.cursor()
    c.execute('SELECT sex FROM users WHERE user_id=?', (user_id,))
    user = c.fetchall()[0][0]
    return user


# Функция для очистки БД
def clear_db():
    global db
    cursor = db.cursor()
    cursor.execute('DROP TABLE users')
    cursor.execute('''CREATE TABLE users(name VARCHAR, user_id INTEGER, age INTEGER, sex VARCHAR, personal_data VARCHAR, chat_id INTEGER)''')
    db.commit()


# Функция, для сохранения данных пользователя в БД
def add_data(chat_id, user_id, user_data, indexes, index_like, index_activity, photo):
    global db
    c = db.cursor()
    c.execute('''INSERT INTO users (chat_id, user_id, name, age, sex, personal_data, indexes, index_like, index_activity, photo) VALUES (?, ?, ?, ?, ?, ?, ?, ?,?, ?)''',
              (chat_id, user_id, user_data['name'], user_data['age'], user_data['sex'], user_data['personal_data'],
               indexes, index_like, index_activity, photo))
    db.commit()


def update_data(user_id, user_data):
    global db
    c = db.cursor()
    c.execute('''UPDATE users SET name=?, age=?, sex=?, personal_data=? WHERE user_id=?''',
              (user_data['name'], user_data['age'], user_data['sex'], user_data['personal_data'], user_id))
    db.commit()


def change_description(user_id, user_data):
    global db
    c = db.cursor()
    c.execute('''UPDATE users SET personal_data=?  WHERE user_id=?''', (user_data, user_id))
    db.commit()


def change_index(user_id, index):
    global db
    c = db.cursor()
    c.execute('''UPDATE users SET indexes=?  WHERE user_id=?''', (index, user_id))
    db.commit()


def change_description(user_id, user_data):
    global db
    c = db.cursor()
    c.execute('''UPDATE users SET personal_data=?  WHERE user_id=?''', (user_data, user_id))
    db.commit()


def check_user_exists(chat_id):
    global db
    c = db.cursor()
    c.execute("SELECT * FROM users WHERE user_id=?", (chat_id,))
    user = c.fetchall()
    if bool(user):
        return True
    else:
        return False


def likes(like, liked):
    global db
    c = db.cursor()
    c.execute('''SELECT COUNT(*) as count_like FROM likes1''')
    x = c.fetchone()[0]
    c.execute('''INSERT INTO likes1 (like1, liked, index_spiska) VALUES (?, ?, ?)''', (like, liked, x+1))
    db.commit()


def index_spiska(liked):
    global db
    c = db.cursor()
    c.execute("SELECT index_spiska FROM likes1 WHERE liked=?", (liked,))
    return c.fetchall()


def delete_for_liked(x):
    global db
    c = db.cursor()
    for i in range(len(x)):
        n = x[i][0]
        c.execute("DELETE FROM likes1 WHERE index_spiska=?", (n,))
    db.commit()


def proverka_like(like, liked):
    global db
    c = db.cursor()
    c.execute('''SELECT liked FROM likes1 WHERE like1=?''', (liked,))
    c = c.fetchall()
    db.commit()
    for i in range(len(c)):
        c[i] = c[i][0]
    if like in c:
        return True
    else:
        return False


def delete_like(like, liked):
    global db
    c = db.cursor()
    c.execute('''DELETE FROM likes1 WHERE like1=? and liked=?''', (like, liked,))
    c.execute('''DELETE FROM likes1 WHERE like1=? and liked=?''', (liked, like,))
    db.commit()


def delete_all_like(liked):
    global db
    c = db.cursor()
    c.execute('''DELETE FROM likes1 WHERE liked=?''', (liked,))
    db.commit()


def get_user_by_id(user_id):
    global db
    c = db.cursor()
    c.execute("SELECT * FROM users WHERE user_id=?", (user_id,))
    return c.fetchone()


def proverka_like2(like, liked):
    global db
    c = db.cursor()
    c.execute('''SELECT * from likes1 WHERE like1=? and liked=?''', (like, liked,))
    c = c.fetchone()
    if c != None:
        return False
    else:
        return True


def delete_profile(user_id):
    global db
    c = db.cursor()
    c.execute('''DELETE FROM users WHERE user_id=?''', (user_id,))
    db.commit()


#  все id, которые лайкнули пользователя
def ankets_with_like(user_id):
    global db
    c = db.cursor()
    c.execute('''SELECT like1 FROM likes1 WHERE liked =?''', (user_id,))
    return c.fetchall()


def change_index_like(index, user_id):
    global db
    c = db.cursor()
    c.execute('''UPDATE users SET index_like=?  WHERE user_id=?''', (index, user_id))
    db.commit()


def index_like(user_id):
    global db
    c = db.cursor()
    c.execute('''SELECT index_like FROM users WHERE user_id=?''', (user_id,))
    db.commit()
    return c.fetchone()[0]-1
"""
def delete_user_image(user_id):
    os.rmdir(f'/images/{user_id}')
"""


def user_activity(index_activity, user_id):
    global db
    c = db.cursor()
    c.execute('''UPDATE users SET index_activity=?  WHERE user_id=?''', (index_activity, user_id,))
    db.commit()

"""
def count_pics(folder_path):
    pattern = os.path.join(folder_path, "*.jpg")
    photos = glob.glob(pattern)
    count = len(photos)
    return count"""
