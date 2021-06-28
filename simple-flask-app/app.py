import sys
import sqlite3


# @app.route('/')
# def hello():
#     return 'Hello, World!'

def connect_database(database_name):
    db_connection = sqlite3.connect(database_name)
    return db_connection


def database_test_population(cursor, table_name, username, password, email, number, pcm, pt, pmg):
    cursor.execute("""CREATE TABLE IF NOT EXISTS {}(
        login_username VARCHAR(20) PRIMARY KEY,
        password VARCHAR(50),
        e_mail VARCHAR(30),
        phone_number VARCHAR(10),
        preferred_comm_method CHAR(1),
        favorite_theater VARCHAR(10),
        favorite_movie_genre VARCHAR (10));""".format(table_name))

    cursor.execute("""INSERT INTO {} (login_username, password, e_mail, phone_number, preferred_comm_method, 
       favorite_theater, favorite_movie_genre) VALUES (?,?,?,?,?,?,?)""".format(table_name),
                   (username, password, email, number, pcm, pt, pmg))


def commit_table_updates(db_connection):
    db_connection.commit()
    db_connection.close()


if __name__ == "__main__":
    database_name = sys.argv[1] if len(sys.argv) > 1 else "testDB.db"
    database_connection = connect_database(database_name)

    crsr = database_connection.cursor()
    print("Please enter: Table Name, username, password, email, phone number, preferred comm method, "
          "favorite theater, favorite movie genre")
    # database_test_population(crsr, input(), input(), input(), input(), input(), input(), input(), input())

    crsr.execute("Select * FROM credentials")
    ans = crsr.fetchall()
    print(ans)

    # This is to make it happen for real
    # commit_table_updates(database_connection)
