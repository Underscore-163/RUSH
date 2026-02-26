import sqlite3
import os





def get(table:str, item_id:int, field):
    connection = sqlite3.connect('data/database.db')
    cursor = connection.cursor()
    command=f"SELECT {field} FROM {table} WHERE {table[:-1]+"ID"} = {item_id}"
    cursor.execute(command)
    data= cursor.fetchall()
    connection.close()
    return data

def create(table:str, data: tuple):
    connection = sqlite3.connect('data/database.db')
    cursor = connection.cursor()
    command=f"INSERT INTO {table} VALUES {data}"
    cursor.execute(command)
    connection.commit()
    connection.close()

def update(table, item_id, field, data):
    connection = sqlite3.connect('data/database.db')
    cursor = connection.cursor()
    command=f"UPDATE {table} SET {field} = '{data}'  WHERE {table[:-1]+"ID"} = {item_id}"
    print(command)
    cursor.execute(command)
    connection.commit()
    connection.close()

def delete(table, item_id):
    connection = sqlite3.connect('data/database.db')
    cursor = connection.cursor()
    command=f"DELETE FROM {table} WHERE {table[:-1]+"ID"} = {item_id}"
    cursor.execute(command)
    connection.commit()
    connection.close()


if __name__ == '__main__':
    os.chdir(os.getcwd().replace("server", ""))
    print((get("Users",1234,"Username")))