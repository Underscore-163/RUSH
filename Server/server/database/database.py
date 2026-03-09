import os
if __name__ == '__main__':
    os.chdir(os.getcwd().replace("server/database", ""))
import asyncio
import checks
import create


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



print(os.getcwd())
from server.logger import get_main_logger
log=get_main_logger()

asyncio.run(checks.check_db_exists())
asyncio.run(create.create_assignment("assignment1234567898765.tar",
                              1234567890)
            )
