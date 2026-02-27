import aiosqlite
import os
import asyncio

async def non_returning_query(query):
    connection = await aiosqlite.connect('data/database.db')
    cursor = await connection.cursor()
    await cursor.execute(query)
    await connection.commit()
    await connection.close()

async def get(table:str, item_id:int, field):
    connection = await aiosqlite.connect('data/database.db')
    cursor = await connection.cursor()
    command=f"SELECT {field} FROM {table} WHERE {table[:-1]+"ID"} = {item_id}"
    await cursor.execute(command)
    data= await cursor.fetchall()
    await connection.close()
    return data

async def create(table:str, data: tuple):
    command=f"INSERT INTO {table} VALUES {data}"
    asyncio.run(non_returning_query(command))

async def update(table, item_id, field, data):
    command=f"UPDATE {table} SET {field} = '{data}'  WHERE {table[:-1]+"ID"} = {item_id}"
    asyncio.run(non_returning_query(command))

async def delete(table, item_id):
    command=f"DELETE FROM {table} WHERE {table[:-1]+"ID"} = {item_id}"
    asyncio.run(non_returning_query(command))


if __name__ == '__main__':
    os.chdir(os.getcwd().replace("server", ""))
