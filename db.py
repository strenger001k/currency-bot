from xlsxwriter.workbook import Workbook
from config import DB_URI
import messages
import psycopg2
import sqlite3

# conn = psycopg2.connect(DB_URI, sslmode="require")
# cursor = conn.cursor()
conn = sqlite3.connect('database.db', check_same_thread=False)
cursor = conn.cursor()

def create_user(user_id: int, username: str, user_name: str, user_surname: str):
    cursor.execute('INSERT INTO Users (user_id, username, user_name, user_surname) VALUES (%d, %s, %s, %s)',
                   (user_id, username, user_name, user_surname))
    conn.commit()


def check_registration(user_id: int):
    get_user_id = cursor.execute('SELECT * FROM Users WHERE user_id=?', (user_id, ))
    if get_user_id.fetchone() is None:
        return False
    else:
        return True


def get_all_user():
    list_all_users = []
    get_users = cursor.execute('SELECT * FROM Users ORDER BY username ASC')  # The ASC keyword means ascending. And the DESC keyword means descending.
    users = get_users.fetchall()
    for user in users:
        list_all_users.append(messages.ALL_USERS.format(user[1], user[2], user[3], user[4], user[5], user[6]))
    return ''.join(list_all_users)


def get_all_id():
    list_all_id = []
    get_users = cursor.execute('SELECT * FROM Users')
    users = get_users.fetchall()
    for user in users:
        if not is_block(user[1]):
            list_all_id.append(user[1])
    return list_all_id


def block_user(user_id: int):
    get_user = cursor.execute("""SELECT * FROM Users WHERE user_id=?""", (user_id, ))
    user = get_user.fetchone()
    if user is not None:
        cursor.execute("UPDATE Users SET is_block=? WHERE user_id=?", (True, user_id))
        conn.commit()
        return messages.BLOCK_SUCCESS
    else:
        return messages.ERROR_SEARCH

def unblock_user(user_id: int):
    get_user = cursor.execute("""SELECT * FROM Users WHERE user_id=?""", (user_id, ))
    user = get_user.fetchone()
    if user is not None:
        cursor.execute("UPDATE Users SET is_block=? WHERE user_id=?", (False, user_id))
        conn.commit()
        return messages.UNBLOCK_SUCCESS
    else:
        return messages.ERROR_SEARCH


def search_user_id(username: str):
    get_user = cursor.execute("""SELECT * FROM Users WHERE username = ?""", (username, ))
    user = get_user.fetchone()
    if user is not None:
        return user[1]
    else:
        return 0


def search_user(user_id: int):
    get_user = cursor.execute("""SELECT * FROM Users WHERE user_id = ?""", (user_id, ))
    user = get_user.fetchone()
    if user is not None:
        return messages.ALL_USERS.format(user[1], user[2], user[3], user[4], user[5], user[6])
    else:
        return messages.ERROR_SEARCH


def is_block(user_id: int):
    get_user = cursor.execute("""SELECT * FROM Users WHERE user_id = ?""", (user_id, ))
    user = get_user.fetchone()
    return user[5]


def is_scheduler(user_id: int):
    get_user = cursor.execute("""SELECT * FROM Users WHERE user_id = ?""", (user_id, ))
    user = get_user.fetchone()
    return user[6]


def scheduler_user_on(user_id: int):
    cursor.execute("UPDATE Users SET is_scheduler=? WHERE user_id=?", (True, user_id))
    conn.commit()


def scheduler_user_off(user_id: int):
    cursor.execute("UPDATE Users SET is_scheduler=? WHERE user_id=?", (False, user_id))
    conn.commit()


def to_excel():
    workbook = Workbook('database.xlsx')
    worksheet = workbook.add_worksheet()

    cell_format = workbook.add_format()
    cell_format.set_align('center')
    cell_format.set_bold()
    worksheet.set_column('A:A', 5)
    worksheet.set_column('B:E', 15)

    get_users = cursor.execute('SELECT * FROM Users')

    worksheet.write(0, 0, "#", cell_format)
    worksheet.write(0, 1, "ID", cell_format)
    worksheet.write(0, 2, "USERNAME", cell_format)
    worksheet.write(0, 3, "NAME", cell_format)
    worksheet.write(0, 4, "BLOCK", cell_format)
    worksheet.write(0, 5, "MAILING", cell_format)

    for i, row in enumerate(get_users):
        if row[5] == 1:
            cell_format = workbook.add_format()
            cell_format.set_bold()
            cell_format.set_align('center')
            cell_format.set_font_color('red')
        else:
            cell_format = workbook.add_format()
            cell_format.set_font_color('black')
            cell_format.set_align('center')

        worksheet.write(i+1, 0, i+1, cell_format)
        worksheet.write(i+1, 1, row[1], cell_format)
        worksheet.write_url(i+1, 2, f'https://t.me/{row[2]}', string='@' + row[2], cell_format=cell_format, tip='Click')  # worksheet.write(i+1, 2, '@' + row[2], cell_format)
        worksheet.write(i+1, 3, row[3], cell_format)
        worksheet.write(i+1, 4, row[5], cell_format)
        worksheet.write(i+1, 5, row[6], cell_format)

    workbook.close()
