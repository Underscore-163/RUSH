import json
import sys
import aiosqlite
# noinspection PyUnusedImports
import sqlite3
import os
import asyncio
import uuid
import tempfile
import zipremove as zipfile
import secrets
import time
import utils

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
    UserID
        a user id
    GroupID
        a group id that the user is in
Assignments
    AssignmentID
        a unique id for the assignment
    Assignee
        the id of the group or user that the assignment was assigned to
    Creator
        the id of the user that created the assignment
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

    await cursor.execute("""CREATE TABLE Groups
                            (
                                GroupID    varchar(255),
                                GroupName  varchar(255),
                                GroupAdmin varchar(255)
                            )""")

    await cursor.execute("""CREATE TABLE UsersInGroups
                            (   
                                UserID varchar(255),
                                GroupID varchar(255)  
                            )""")

    await cursor.execute("""CREATE TABLE Assignments
                            (
                                AssignmentID varchar(255),
                                AssigneeID   varchar(255),
                                CreatorID    varchar(255)
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
    print(command)
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

    if await check_exists(table, table[:-1] + "ID", id):
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
        "ClientID": None,
    }
    if not await check_exists("Users", "Username", username):
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




async def check_db_exists():
    if not os.path.exists('data/database.db'):
        log.critical("Database not found. This could be due to data corruption.")
        if input("would you like to create a new database? (this could remove the old one, if it exists)[y,n]") == "y":
            await create_db()
        else:
            log.warning("Aborting startup...")
            sys.exit()


async def check_exists(table, field, data_to_be_checked):
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

async def create_auth(username, password, client_id):
    lifespan=config["authentication"]["token_lifespan"]

    # check that the user exists
    if await check_exists("Users", "Username", username):
        # get the userid and hashed password by searching for the username
        user_id,stored_password =await get(table="Users",
                  field="UserID, HashedPassword",
                  query=f"Username='{username}'",)

        # if the userid or the client id already has a token associated with it,
        # kill the old token, then continue
        if await check_exists("Authentication", "UserID", user_id) :
            await update("Authentication",
                   "Alive",
                   False,
                   f"UserID='{user_id}'",)
        if await check_exists("Authentication", "ClientID", client_id):
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
            return 1
    # if the user doesn't exist, return False
    else:
        return 2

async def check_auth(token, user_id, client_id):

    # check that the token exists
    if await check_exists("Authentication", "Token", token):
        print("token exists")

        # get the token from the database
        token_record=await get(table="Authentication",
                  query=f"Token='{token}'")
        token_info=dict(alive=token_record[1],
                        tod=token_record[3],
                        user_id=token_record[4],
                        client_id=token_record[5])

        # check that the token is valid
        if (token_info["alive"] and
            token_info["tod"]>int(time.time()) and
            token_info["user_id"]==user_id and
            token_info["client_id"]==client_id):
                print("token valid")
                return 0 # normal response; the token exists and is valid
        else:
            print("token exists, but not valid")
            # if the token is not valid, kill it just to be safe
            await update("Authentication",
                   "Alive",
                   False,
                   f"Token='{token}'",)
            return 1 # token exists but is invalid
    else:
        return 2 # token does not exist

async def add_assignment(assignment,creator_id):
    id=await generate_unique_id("Assignment")
    with open(f"data/files/assignments/{id}.rushzip","wb") as f:
        f.write(assignment.read())
    with zipfile.ZipFile(f"data/files/assignments/{id}.rushzip").open("manifest.json") as manifest_file:
        manifest=json.load(manifest_file)
    with zipfile.ZipFile(f"data/files/assignments/{id}.rushzip","a")as assignment_file:
        manifest["assignment_id"]=id
        assignment_file.remove("manifest.json")
        assignment_file.writestr("manifest.json",json.dumps(manifest))
    await create(table="Assignments",
                 fields="AssignmentID,AssigneeID,CreatorID",
                 data=f"\"{id}\",\"{manifest["assignees"][0]}\",\"{creator_id}\"")

async def list_assignments(user_id):
    group_ids= await get("UsersInGroups",f"UserID=\"{user_id}\"","GroupID")
    if group_ids == []:
        group_ids=[user_id]
    query="SELECT AssignmentID FROM Assignments WHERE"
    for group_id in group_ids:
        query+=f" AssigneeID = \"{group_id}\" "
        if group_ids.index(group_id) != len(group_ids)-1:
            query+="OR"
    connection= await aiosqlite.connect("data/database.db")
    cursor = await connection.cursor()
    await cursor.execute(query)
    assignment_ids=await cursor.fetchall()
    await connection.close()
    return assignment_ids

async def check_assigned(assignment_id,user_id):
    group_query=f"SELECT GroupID From UsersInGroups WHERE UserID=\"{user_id}\""
    connection= await aiosqlite.connect("data/database.db")
    cursor = await connection.cursor()
    await cursor.execute(group_query)
    group_ids=await cursor.fetchall()
    query = "SELECT AssignmentID FROM Assignments WHERE"
    for group_id in group_ids:
        query += f" AssigneeID = \"{group_id}\" "
        if group_ids.index(group_id) != len(group_ids) - 1:
            query += "OR"
    await cursor.execute(query)
    assignment_ids=await cursor.fetchall()
    if assignment_id in assignment_ids:
        return True
    else:
        return False


if __name__=="__main__":
    log,config=asyncio.run(utils.full_setup())
else:
    log,config=asyncio.run(utils.part_setup())

asyncio.run(check_db_exists())


