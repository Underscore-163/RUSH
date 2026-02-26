import aiosqlite
import os
import asyncio

async def get(table:str, item_id:int, field):
    connection = await aiosqlite.connect('data/database.db')
    cursor = await connection.cursor()
    command=f"SELECT {field} FROM {table} WHERE {table[:-1]+"ID"} = {item_id}"
    await cursor.execute(command)
    data= await cursor.fetchall()
    await connection.close()
    return data

async def create(table:str, data: tuple):
    connection = await aiosqlite.connect('data/database.db')
    cursor = await connection.cursor()
    command=f"INSERT INTO {table} VALUES {data}"
    await cursor.execute(command)
    await connection.commit()
    await connection.close()

async def update(table, item_id, field, data):
    connection = await aiosqlite.connect('data/database.db')
    cursor = await connection.cursor()
    command=f"UPDATE {table} SET {field} = '{data}'  WHERE {table[:-1]+"ID"} = {item_id}"
    await cursor.execute(command)
    await connection.commit()
    await connection.close()

async def delete(table, item_id):
    connection = await aiosqlite.connect('data/database.db')
    cursor = await connection.cursor()
    command=f"DELETE FROM {table} WHERE {table[:-1]+"ID"} = {item_id}"
    await cursor.execute(command)
    await connection.commit()
    await connection.close()


if __name__ == '__main__':
    os.chdir(os.getcwd().replace("server", ""))
    print(asyncio.run(get("Users",1234,"Username")))
