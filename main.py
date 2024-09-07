async def main():
    activity_name = "Bread 🍞"
    
    from disnake.ext import commands
    from disnake import Status, Activity, ActivityType, Intents, utils
    import sqlite3
    import logging
    intents = Intents.default()
    intents.message_content = True
    intents.members = True
    intents.guilds = True
    bot = commands.Bot(command_prefix="dsfgdsdfg", intents=intents)
    
    logging.basicConfig()
    
    bot.sqlite_connection = sqlite3.connect("database.db")
    bot.sqlite_cursor = bot.sqlite_connection.cursor()
    bot.sqlite_cursor.execute("CREATE TABLE IF NOT EXISTS Admins (id INTEGER PRIMARY KEY UNIQUE)")
    bot.sqlite_cursor.execute("CREATE TABLE IF NOT EXISTS Config (log INTEGER, role INTEGER, freddie INTEGER)")
    bot.sqlite_cursor.execute("CREATE TABLE IF NOT EXISTS Admins (id INTEGER PRIMARY KEY UNIQUE)")
    bot.sqlite_cursor.execute("INSERT INTO Config (log, role, freddie) VALUES (?, ?, ?)", (0, 0, 0))
    try:
        bot.sqlite_cursor.execute("INSERT INTO Admins (id) VALUES (?)", (855948446540496896,))
    except sqlite3.IntegrityError:
        pass

    bot.sqlite_connection.commit()
    @bot.event
    async def on_ready():
        print("ready")
        await bot.change_presence(status=Status.idle)


    bot.reload = True

    bot.load_extensions("plugins/")

    TOKEN = open("token.txt", 'r').read()
    await bot.start(TOKEN)
if __name__ == "__main__":
    from asyncio import run
    run(main())