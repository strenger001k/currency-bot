import os
import sqlite3


def creat_table():
    if not os.path.exists('chek.db'):
        table = """CREATE TABLE User (
                                        id           INTEGER PRIMARY KEY ASC
                                                             UNIQUE
                                                             NOT NULL,
                                        user_id      INT     UNIQUE
                                                             NOT NULL,
                                        username     STRING,
                                        user_name    STRING  NOT NULL,
                                        user_surname STRING,
                                        is_block     BOOLEAN NOT NULL
                                                             DEFAULT (False),
                                        is_scheduler BOOLEAN DEFAULT (False)
                                                             NOT NULL
                                     )"""
        conn = sqlite3.connect('chek.db', check_same_thread=False)
        cursor_obj = conn.cursor()
        cursor_obj.execute(table)
        print("===DataBase created===")
        conn.close()
    else:
        print("===DataBase already exists===")


if __name__ == '__main__':
    creat_table()
