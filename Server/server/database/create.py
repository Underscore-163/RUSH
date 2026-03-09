import os
import aiosqlite
import uuid
import checks
import utils
import tempfile
import tarfile
import json


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

    if await checks.check_unique(table, table[:-1] + "ID", id):
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
    if not await checks.check_unique("Users", "Username", username):
        log.info(f"Creating User '{username}'")
        await utils.create("Users",
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
    "Title": "Assignment Title", 
    "Assignee": "UserID or GroupID",
    "Due_Date": Unix timestamp,
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

    await utils.create(
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

print(os.getcwd())
from server.logger import get_main_logger
log = get_main_logger()
