async def main():
    activity_name = "Bread 🍞"
    
    from disnake.ext import commands
    from disnake import Status, Activity, ActivityType, Intents, utils, Message, Embed
    from datetime import datetime, timezone
    import sqlite3
    import logging
    intents = Intents.default()
    intents.message_content = True
    intents.members = True
    intents.guilds = True
    bot = commands.Bot(command_prefix="dsfgdsdfg", intents=intents)
    
    bot.sqlite_connection = sqlite3.connect("database.db")
    bot.sqlite_cursor = bot.sqlite_connection.cursor()
    bot.sqlite_cursor.execute("CREATE TABLE IF NOT EXISTS Admins (id INTEGER PRIMARY KEY UNIQUE)")
    bot.sqlite_cursor.execute("CREATE TABLE IF NOT EXISTS Config (log INTEGER, role INTEGER, freddie INTEGER)")
    bot.sqlite_cursor.execute("SELECT * FROM Config")
    config = bot.sqlite_cursor.fetchall()
    if len(config) < 1:
        bot.sqlite_cursor.execute("INSERT INTO Config (log, role, freddie) VALUES (?, ?, ?)", (0, 0, 0))
    try:
        bot.sqlite_cursor.execute("INSERT INTO Admins (id) VALUES (?)", (855948446540496896,))
    except sqlite3.IntegrityError:
        pass

    bot.sqlite_connection.commit()
    
    @bot.event
    async def on_ready():
        print("ready")
        await bot.wait_until_ready()
        await bot.change_presence(status=Status.idle)
        origins = bot.get_guild(826685546772168734).get_channel(1161528232965836931)
        council = bot.get_guild(1166799644362276967).get_channel(1282534413430689963)
        for message in await origins.history().flatten():
            if message.author.id == bot.user.id:
                await message.delete()
        for message in await council.history().flatten():
            if message.author.id == bot.user.id:
                await message.delete()

    @bot.event
    async def on_message(message:Message):
        if message.channel.id == 1166799644970467411 and not message.author.bot:
            delta_time = datetime.now(timezone.utc) - message.author.joined_at
            if delta_time.days < 8:
                reply = await message.reply(embed=Embed(title="You don't meet requirements!", description=f"You must have been in this server for 7 days. you have been in for {delta_time.days} days"))
                await sleep(5)
                try:
                    await message.delete()
                    await reply.delete()
                except Exception:
                    await reply.edit(embed=Embed(title="You don't meet requirements!", description=f"You must have been in this server for 7 days. you have been in for {delta_time.days} days\n-# Failed to delete message chain"))

    bot.reload = True

    bot.load_extensions("plugins/")

    TOKEN = open("token.txt", 'r').read()
    await bot.start(TOKEN)
if __name__ == "__main__":
    from asyncio import run, sleep
    run(main())