async def check_db_exists():
    if not os.path.exists('data/database.db'):
        log.critical("Database not found. This could be due to data corruption.")
        if input("would you like to create a new database? (this could remove the old one, if it exists)[y,n]")=="y":
            await create_db()
        else:
            log.warning("Aborting startup...")
            sys.exit()

async def check_unique(table,field,data_to_be_checked):
    connection = await aiosqlite.connect('data/database.db')
    cursor = await connection.cursor()

    #SELECT COUNT(*) FROM users WHERE username = 'john_doe'
    query=f"""
    SELECT COUNT(*)
    FROM {table}
    WHERE {field}='{data_to_be_checked}'"""

    result=await cursor.execute(query)
    exists=await result.fetchone()
    exists=bool(exists[0])

    return exists
