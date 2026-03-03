import sys

import aiosqlite
import sqlite3
import os
import asyncio
import uuid


"""
Users
    UserID
        a unique id for the user
        starts with 10 : student
        starts with 20 : teacher
        starts with 3x : parent
        the parent UserID is the same as the student, 
        but starts with 30 or 31
    Username
        the username used to log in, e.g. an email address
    HashedPassword
        the hashed password for that user
    FriendlyName
        the name the user should be called by
    ClientID
        holds the ClientID of the client that the user uses
Clients
    ClientID
        a unique id for the client
        created when installed on a system
Groups
    GroupID
        a unique id for the group. 
        as groups behave similarly to users, 
        these ids will start with 40
    GroupName
        name of the group
    GroupAdmin
        UserID of the administrator of the group
UsersInGroups
    GroupID
        the id of each group from the Groups table
    All other fields
        every user in the group
Assignments
    AssignmentID
        a unique id for the assignment
    AssignmentName
        the title of the assignment
    Assignee
        the id of the group or user that the assignment was assigned to
    Path
        a path to a directory on the filesystem 
        that holds all the files for the assignment,
        including the md file for the body text
Authentication
    Token
        an auth token
    Alive
        boolean - is the token currently accepted, regardless of time of death
    TimeOfBirth
        when was the token created (Unix time)
    TimeOfDeath
        when will the token no longer be valid (Unix time)
    UserID
        the id of the user that this token belongs to
    ClientID
        the id of the client that uses this token. 
        if either the user or client ids do not match, the token is killed.
"""

async def create_db():
    log.info("Creating new database...")
    connection = await aiosqlite.connect('data/database.db')
    cursor= await connection.cursor()

    await cursor.execute("""CREATE TABLE Users (
    UserID varchar(255),
    Username varchar(255),
    HashedPassword varchar(255),
    FriendlyName varchar(255),
    ClientID int
    )""")

    await cursor.execute("""CREATE TABLE Clients (
    ClientID varchar(255)
    )""")

    await cursor.execute("""CREATE TABLE Groups (
    GroupID varchar(255),
    GroupName varchar(255),
    GroupAdmin int
    )""")

    await cursor.execute("""CREATE TABLE UsersInGroups (
    GroupID varchar(255)
    )""")

    await cursor.execute("""CREATE TABLE Assignments (
    AssignmentID varchar(255),
    AssignmentName varchar(255),
    Assignee int,
    Path varchar(255)
    )""")

    await cursor.execute("""CREATE TABLE Authentication (
    Token varchar(512),
    Alive bool,
    TimeOfBirth int,
    TimeOfDeath int,
    UserID int,
    ClientID int
    )""")
    log.info("Database successfully created")




async def non_returning_query(query):
    connection = await aiosqlite.connect('data/database.db')
    cursor = await connection.cursor()
    await cursor.execute(query)
    await connection.commit()
    await connection.close()

async def get(table:str, item_id:int, field:str="*"):
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

async def generate_unique_id(id_type):
    log.debug("Generating new id")
    id=uuid.uuid4().hex
    if id_type == "Student":
        id="10"+str(id)
    elif id_type == "Teacher":
        id="20"+str(id)
    elif id_type == "Group":
        id="40"+str(id)
    elif id_type == "Assignment":
        id="50"+str(id)
    elif id_type == "Client":
        id="60"+str(id)
    else:
        raise ValueError("unknown id type '"+id_type+"'")

    if id_type == "Student" or "Teacher":
        table="Users"
    else:
        table=id_type+"s"

    connection = await aiosqlite.connect('data/database.db')
    cursor = await connection.cursor()

    #SELECT COUNT(*) FROM users WHERE username = 'john_doe'
    query=f"""
    SELECT COUNT(*)
    FROM {table}
    WHERE {table[:-1]+"ID"}='{id}'"""

    result=await cursor.execute(query)
    exists=await result.fetchone()
    exists=exists[0]

    if exists:
        id=await generate_unique_id(id_type)
    return id


async def create_user(username:str,user_type):

    user_id=await generate_unique_id(user_type)

    user_info={
        "UserID":user_id,
        "Username":username,
        "HashedPassword":username,
        "FriendlyName":None,
        "ClientID":"test",
        }

    connection = await aiosqlite.connect('data/database.db')
    cursor = await connection.cursor()



    query=f"""INSERT INTO Users(UserID,Username,HashedPassword,FriendlyName,ClientID)
     VALUES (
    '{user_info["UserID"]}', 
    '{user_info["Username"]}', 
    '{user_info["HashedPassword"]}', 
    '{user_info["FriendlyName"]}', 
    '{user_info["ClientID"]}')"""

    await cursor.execute(query)

    await connection.commit()
    await connection.close()

async def check_db_exists():
    if not os.path.exists('data/database.db'):
        log.critical("Database not found. This could be due to data corruption.")
        if input("would you like to create a new database? (this could remove the old one, if it exists)[y,n]")=="y":
            await create_db()
        else:
            log.warning("Aborting startup...")
            sys.exit()


if __name__ == '__main__':
    os.chdir(os.getcwd().replace("server", ""))
from logger import get_main_logger
log=get_main_logger()

asyncio.run(check_db_exists())
asyncio.run(create_user("reuben","Student"))
