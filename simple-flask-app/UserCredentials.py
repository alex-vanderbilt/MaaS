import sys
import sqlite3
import string
from werkzeug.security import check_password_hash


class UserCredentials:
    def __init__(self, database, database_table_name):
        self.__password_key = "WOOO!!!!!!!!!!"
        self.__database_to_connect = database
        self.__table_to_access = database_table_name
        self.__cursor = None
        self.__db_connection = None

    def access_database(self, master_password):
        if self.__password_key == master_password:
            print("Master Password successful, returning connection to the database")
            self.__db_connection = sqlite3.connect(self.__database_to_connect)
            self.__cursor = self.__db_connection.cursor()
            self.create_table()
            return "Connection Successful"
        else:
            print("Incorrect Master Password")
            return -1

    def authenticate_user(self, username, password):
        database_keys = self.fetch_table_duo_column("login_username", "password")
        for db_username, db_password in database_keys:
            if username == db_username:
                if check_password_hash(db_password, password):
                    print("Successfully authenticated, Logging in")
                    return True
        return False

    def populate_table(self, username, password, email, first_name="None", last_name="None", number="None", pcm="None",
                       pt="None", pmg="None"):
        self.__cursor.execute("""INSERT INTO {} (login_username, password, e_mail, first_name, last_name, 
                phone_number, preferred_comm_method, favorite_theater, favorite_movie_genre) 
                VALUES (?,?,?,?,?,?,?,?,?)""".format(self.__table_to_access), (username, password,
                                                                               email, first_name, last_name, number,
                                                                               pcm, pt, pmg))

    def fetch_entire_table(self):
        self.__cursor.execute("SELECT * FROM {}".format(self.__table_to_access))
        return self.__cursor.fetchall()

    def fetch_table_column(self, column):
        self.__cursor.execute("SELECT {} FROM {}".format(column, self.__table_to_access))
        return self.__cursor.fetchall()

    def fetch_table_duo_column(self, column1, column2):
        self.__cursor.execute("SELECT {}, {} FROM {}".format(column1, column2, self.__table_to_access))
        return self.__cursor.fetchall()

    def delete_table_entry(self, username):
        self.__cursor.execute("DELETE FROM {} WHERE login_username={}".format(self.__table_to_access, username))

    def commit_changes(self):
        self.__db_connection.commit()
        # self.__db_connection.close()

    def close_database(self):
        self.__db_connection.close()

    def create_table(self):
        self.__cursor.execute("""CREATE TABLE IF NOT EXISTS {}(
                            login_username VARCHAR(20) PRIMARY KEY,
                            password VARCHAR(255),
                            e_mail VARCHAR(30),
                            first_name VARCHAR(20),
                            last_name VARCHAR(30),
                            phone_number VARCHAR(10),
                            preferred_comm_method CHAR(1),
                            favorite_theater VARCHAR(10),
                            favorite_movie_genre VARCHAR (10));""".format(self.__table_to_access))

    def truncate_table(self):
        print(self.fetch_entire_table())
        self.__cursor.execute("DELETE FROM {}".format(self.__table_to_access))
        self.commit_changes()
        print(self.fetch_entire_table())
