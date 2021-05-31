import sqlite3
from contextlib import closing

class PasswordManager:

    def __init__(self, db, table):
        self.conn = sqlite3.connect(db)
        self.db = db.split('.')[0]
        self.table = table
        self.create_password_table()

    def execute_query(self, sql):
        with closing(self.conn.cursor()) as cur:
            try:
                cur.execute(sql)
            except Exception as e:
                print("Error:", e)
            else:
                self.conn.commit()
                print("Query executed successfully")

    def create_password_table(self):
        sql = '''create table if not exists {} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,            
            website VARCHAR(255),
            name VARCHAR(255) NOT NULL UNIQUE,
            username VARCHAR(255) NOT NULL,
            password VARCHAR(255) NOT NULL,
            notes VARCHAR(4000),
            created_ts INT,
            edited_ts INT)'''.format(self.table)
        self.execute_query(sql)

    def add_password(self, Password):
        website = getattr(Password,'website')
        name = getattr(Password,'name')
        username = getattr(Password,'username')
        password = getattr(Password,'password')
        notes = getattr(Password,'notes')
        
        sql = '''insert into {0}(website, name, username, password, notes, created_ts)
        values('{1}', '{2}', '{3}', '{4}', '{5}', strftime('%s','now'));'''.format(self.table,website,name,username,password,notes)
        self.execute_query(sql)

    def search_for_password(self, params):
        print(params)
        sql_base = '''
        select website, name, username, password 
        from passwords'''

        operator = {True: "where", False: " and"}
        filters = ["{} {} like '{}'".format(operator[i == 0], name, value)
                   for i, (name, value) in enumerate(params.items()) if value]
        filter = "".join(filters)
        sql = "{} {}".format(sql_base, filter)

        with closing(self.conn.cursor()) as cur:
            try:
                cur.execute(sql)
            except Exception as e:
                print("Error:", e)
            else:
                r = [dict((cur.description[i][0], value) \
                          for i, value in enumerate(row)) for row in cur.fetchall()]
        print(r)
        return r

    def close(self):
        self.conn.close()

