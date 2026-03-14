import json
import sys
import aiosqlite
# noinspection PyUnusedImports
import sqlite3
import os
import asyncio
import uuid
import tempfile
import tarfile
import secrets
import time

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
    Assignee
        the id of the group or user that the assignment was assigned to
    DueDate
        the date the assignment is due in unix time
    Checksum
        the checksum of the assignment file
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
    cursor = await connection.cursor()

    await cursor.execute("""CREATE TABLE Users
                            (
                                UserID         varchar(255),
                                Username       varchar(255),
                                HashedPassword varchar(255),
                                FriendlyName   varchar(255),
                                ClientID       int
                            )""")

    await cursor.execute("""CREATE TABLE Clients
                            (
                                ClientID varchar(255)
                            )""")

    await cursor.execute("""CREATE TABLE Groups
                            (
                                GroupID    varchar(255),
                                GroupName  varchar(255),
                                GroupAdmin int
                            )""")

    await cursor.execute("""CREATE TABLE UsersInGroups
                            (
                                GroupID varchar(255)
                            )""")

    await cursor.execute("""CREATE TABLE Assignments
                            (
                                AssignmentID varchar(255),
                                Assignee     varchar(255),
                                DueDate      int,
                                Checksum     varchar(255)
                            )""")

    await cursor.execute("""CREATE TABLE Authentication
                            (
                                Token       varchar(512),
                                Alive       bool,
                                TimeOfBirth int,
                                TimeOfDeath int,
                                UserID      int,
                                ClientID    int
                            )""")
    await connection.commit()
    await connection.close()
    log.info("Database successfully created")


async def non_returning_query(query):
    connection = await aiosqlite.connect('data/database.db')
    cursor = await connection.cursor()
    await cursor.execute(query)
    await connection.commit()
    await connection.close()

async def get(table:str,query:str,field:str="*",):
    """
    SELECT field
    FROM table
    WHERE record
    """
    connection = await aiosqlite.connect('data/database.db')
    cursor = await connection.cursor()
    command=f"SELECT {field} FROM {table} WHERE {query}"
    await cursor.execute(command)
    data=await cursor.fetchall()
    if len(data) == 1:
        data=data[0]
    await connection.close()
    return data


async def get_by_id(table: str, item_id: str, field: str = "*"):
    connection = await aiosqlite.connect('data/database.db')
    cursor = await connection.cursor()
    command = f"SELECT {field} FROM {table} WHERE {table[:-1] + "ID"} = {item_id}"
    await cursor.execute(command)
    data = await cursor.fetchall()
    await connection.close()
    return data


async def create(table: str, fields, data):
    command = f"INSERT INTO {table}({fields}) VALUES({data})"
    await non_returning_query(command)


async def update(table, fields_to_update, new_data, search_query):
    command = f"UPDATE {table} SET {fields_to_update} = {new_data}  WHERE {search_query}"
    await non_returning_query(command)



async def delete(table, item_id):
    command = f"DELETE FROM {table} WHERE {table[:-1] + "ID"} = {item_id}"
    await non_returning_query(command)


async def generate_unique_id(id_type):
    log.debug("Generating new id")
    id = uuid.uuid4().hex
    if id_type == "Student":
        id = "10" + str(id)
    elif id_type == "Teacher":
        id = "20" + str(id)
    elif id_type == "Group":
        id = "40" + str(id)
    elif id_type == "Assignment":
        id = "50" + str(id)
    elif id_type == "Client":
        id = "60" + str(id)
    else:
        raise ValueError("unknown id type '" + id_type + "'")

    if id_type == "Student" or "Teacher":
        table = "Users"
    else:
        table = id_type + "s"

    if await check_unique(table, table[:-1] + "ID", id):
        log.info("ID already exists. Recreating...")
        id = await generate_unique_id(id_type)
    return id


async def create_user(username: str, user_type):
    log.info("Creating new user")
    user_id = await generate_unique_id(user_type)
    user_info = {
        "UserID": user_id,
        "Username": username,
        "HashedPassword": username,
        "FriendlyName": None,
        "ClientID": "test",
    }
    if not await check_unique("Users", "Username", username):
        log.info(f"Creating User '{username}'")
        await create("Users",
                     "UserID,Username,HashedPassword,FriendlyName,ClientID",
                     f"""'{user_info["UserID"]}',
                     '{user_info["Username"]}',
                     '{user_info["HashedPassword"]}',
                     '{user_info["FriendlyName"]}',
                     '{user_info["ClientID"]}'"""
                     )
        return True
    else:
        log.info(f"Username '{username}' already in use")
        return False


async def create_assignment(temp_file_name, checksum):
    """"""
    """
    {
    "Title": "Sample Title", 
    "Assignee": "20cfaa34559f814ada826f049cbceb1c49",
    "Due_Date": 1772914948
    }
    """
    tempfile.tempdir = f"{os.getcwd()}/data/files/tmp/"
    with tempfile.TemporaryDirectory(dir=f"{os.getcwd()}/data/files/tmp/") as temp_path:
        with tarfile.open(f"{os.getcwd()}/data/files/tmp/{temp_file_name}", "r") as tar:
            data_path = f"{temp_file_name[:-4]}/data.json"
            tar.extract(data_path, path=temp_path)
        with open(f"{temp_path}/{temp_file_name[:-4]}/data.json", "r") as json_file:
            json_data = json.load(json_file)

    assignment_info = {
        "AssignmentID": await generate_unique_id("Assignment"),
        "Assignee": json_data["Assignee"],
        "DueDate": json_data["Due_Date"],
        "Checksum": checksum
    }

    await create(
        "Assignments",
        "AssignmentID,Assignee,DueDate,Checksum",
        f"""
        '{assignment_info["AssignmentID"]}',
        '{assignment_info["Assignee"]}',
        '{assignment_info["DueDate"]}',
        '{assignment_info["Checksum"]}'
"""
    )
    os.rename(f"{os.getcwd()}/data/files/tmp/{temp_file_name}",
              f"{os.getcwd()}/data/files/assignments/{assignment_info['AssignmentID']}.tar")


async def check_db_exists():
    if not os.path.exists('data/database.db'):
        log.critical("Database not found. This could be due to data corruption.")
        if input("would you like to create a new database? (this could remove the old one, if it exists)[y,n]") == "y":
            await create_db()
        else:
            log.warning("Aborting startup...")
            sys.exit()


async def check_unique(table, field, data_to_be_checked):
    connection = await aiosqlite.connect('data/database.db')
    cursor = await connection.cursor()

    # SELECT COUNT(*) FROM users WHERE username = 'john_doe'
    query = f"""
    SELECT COUNT(*)
    FROM {table}
    WHERE {field}='{data_to_be_checked}'"""

    result = await cursor.execute(query)
    exists = await result.fetchone()
    exists = bool(exists[0])

    return exists

async def create_auth(username=None, password=None):
    client_id=None # placeholder
    lifespan=2592000 # this will load from config.yml

    # get the userid and hashed password by searching for the username
    user_id,stored_password =await get(table="Users",
              field="UserID, HashedPassword",
              query=f"Username='{username}'",)

    # if the userid or the client id already has a token associated with it,
    # kill the old token, then continue
    if await check_unique("Authentication","UserID", user_id) :
        await update("Authentication",
               "Alive",
               False,
               f"UserID='{user_id}'",)
    if await check_unique("Authentication","ClientID", client_id):
        await update("Authentication",
                     "Alive",
                     False,
                     f"ClientID='{client_id}'", )

    # check that the password is correct before continuing
    if password==stored_password:

        # generate all the information for the auth
        auth_info={
            "Token": secrets.token_urlsafe(32),
            "UserID": user_id,
            "ClientID": client_id,
            "TimeOfBirth": int(time.time()),
        }
        auth_info["TimeOfDeath"]= auth_info["TimeOfBirth"]+lifespan

        # save the auth into the database
        await create(table="Authentication",
                     fields="Token,Alive,TimeOfBirth,TimeOfDeath,UserID,ClientID",
                     data=f"""
                     '{auth_info["Token"]}',
                     '{True}',
                     '{auth_info["TimeOfBirth"]}',
                     '{auth_info["TimeOfDeath"]}',
                     '{auth_info["UserID"]}',
                     '{auth_info["ClientID"]}'
                    """,)

        # finally, return the auth info for the api to return
        return auth_info

    # if the password is incorrect, return False
    else:
        return False



if __name__ == '__main__':
    os.chdir(os.getcwd().replace("server", ""))
from logger import get_main_logger
log = get_main_logger()

asyncio.run(check_db_exists())

if __name__ == '__main__':
    print(asyncio.run(create_auth("reuben","incorrect")))
