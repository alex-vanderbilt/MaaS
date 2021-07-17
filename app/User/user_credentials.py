import sys
import sqlite3
import string

import pyotp
from werkzeug.security import check_password_hash
import random


class UserCredentials:
    def __init__(self, database, database_table_name):
        self.__password_key = "WOOO!!!!!!!!!!"
        self.__database_to_connect = database
        self.__table_to_access = database_table_name
        self.__cursor = None
        self.__db_connection = None

    def access_database(self, master_password):
        if self.__password_key == master_password:
            # print("Master Password successful, returning connection to the database")
            self.__db_connection = sqlite3.connect(self.__database_to_connect)
            self.__cursor = self.__db_connection.cursor()
            self.create_table()
            return "Connection Successful"
        else:
            # print("Incorrect Master Password")
            return -1

    def authenticate_user(self, username, password):
        database_keys = self.fetch_table_duo_column("login_username", "password")
        for db_username, db_password in database_keys:
            # print(db_username)
            # print(db_password)
            if username == db_username:
                if check_password_hash(db_password, password):
                    # print("Successfully authenticated, Logging in")
                    return True
        return False

    def populate_table(self, username, password, email, first_name="None", last_name="None", number="None",
                       zipcode="None", pcm="None", pt="None", pmg="None", weekday="None", tod="None",
                       theater_name="None"):
        enrolled = "false"
        user_otp = pyotp.random_base32()
        self.__cursor.execute("""INSERT INTO {} (login_username, password, e_mail, first_name, last_name, 
                phone_number, zipcode, preferred_comm_method, favorite_theater, favorite_movie_genre, tfa_enrolled,
                tfa_otp, weekday, time_of_day, theater_name) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)""".format(
            self.__table_to_access),
            (username, password,
             email, first_name,
             last_name,
             number, zipcode,
             pcm, pt, pmg, enrolled,
             user_otp, weekday, tod,
             theater_name))

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
                            zipcode INTEGER,
                            preferred_comm_method CHAR(1),
                            favorite_theater VARCHAR(255),
                            favorite_movie_genre VARCHAR (10),
                            tfa_enrolled VARCHAR(5),
                            tfa_otp VARCHAR(255),
                            weekday VARCHAR (30),
                            time_of_day VARCHAR (30));""".format(self.__table_to_access))

    def truncate_table(self):
        # print(self.fetch_entire_table())
        self.__cursor.execute("DELETE FROM {}".format(self.__table_to_access))
        self.commit_changes()
        # print(self.fetch_entire_table())

    def update_user_enrollment(self, username):
        self.__cursor.execute("UPDATE {} SET tfa_enrolled = 'true' WHERE login_username = '{}'".format(
            self.__table_to_access, username))

    def update_user_favorite_theater(self, username, updated_theater_information):
        name, address, city, state, zipcode = updated_theater_information.split(",")
        self.__cursor.execute("UPDATE {} SET favorite_theater = '{}' WHERE login_username = '{}'".format(
            self.__table_to_access, updated_theater_information, username))
        self.commit_changes()
        self.__cursor.execute("UPDATE {} SET theater_name = '{}' WHERE login_username = '{}'".format(
            self.__table_to_access, name, username))
        self.commit_changes()

    def fetch_users_favorited_theater(self, username):
        theater = (self.__cursor.execute("SELECT favorite_theater FROM {} WHERE login_username = '{}'".format(
            self.__table_to_access, username)).fetchone())
        for address in theater:
            return_value = address
        return return_value

    def fetch_user_theater_name(self, username):
        theater = (self.__cursor.execute("SELECT theater_name FROM {} WHERE login_username = '{}'".format(
            self.__table_to_access, username)).fetchone())
        for name in theater:
            return_value = name
        return return_value

    def create_movie_trailer_table(self):
        self.__cursor.execute("""CREATE TABLE IF NOT EXISTS trailer_links(
                                    movie_name VARCHAR(100) PRIMARY KEY,
                                    links VARCHAR(150));""")

    def populate_movie_trailer_table(self):
        self.__cursor.execute("""INSERT INTO trailer_links VALUES('Mortal Kombat',
                'https://www.youtube.com/embed/NYH2sLid0Zc')""")
        self.commit_changes()
        self.__cursor.execute("""INSERT INTO trailer_links VALUES('Raya and the Last Dragon',
                'https://www.youtube.com/embed/1VIZ89FEjYI')""")
        self.commit_changes()
        self.__cursor.execute("""INSERT INTO trailer_links VALUES('The Misfits',
                'https://www.youtube.com/embed/XaXanCUXnJM')""")
        self.commit_changes()
        self.__cursor.execute("""INSERT INTO trailer_links VALUES('A Quiet Place Pt. 2',
                'https://www.youtube.com/embed/BpdDN9d9Jio')""")
        self.commit_changes()

    def update_notification_day(self, weekday, username):
        self.__cursor.execute("UPDATE {} SET weekday = '{}' WHERE login_username = '{}'".format(self.__table_to_access,
                                                                                                weekday, username))
        self.commit_changes()

    def update_time_of_day(self, tod, username):
        self.__cursor.execute("UPDATE {} SET time_of_day = '{}' WHERE login_username = '{}'".format(
            self.__table_to_access,
            tod, username))

    def get_new_movie_trailer(self):
        movie_trailers = self.__cursor.execute("SELECT * FROM trailer_links")
        i = 0
        random_trailer = random.randint(0, 3)
        for trailer_name, trailer_link in movie_trailers:
            if i == random_trailer:
                return trailer_link
            i += 1
