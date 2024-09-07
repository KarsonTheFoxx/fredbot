from disnake.ext import commands, plugins
from disnake import Embed, Color, CommandInteraction, Member
from sqlite3 import IntegrityError
from asyncio import sleep
plugin = plugins.Plugin()

@plugin.slash_command(name="configure", description="Configure the bot for this server")
async def configure(inter:CommandInteraction, id:str, config:str=commands.Param(choices=["log", "role", "freddie"])):
    plugin.bot.sqlite_cursor.execute("SELECT * FROM Admins")
    admins = plugin.bot.sqlite_cursor.fetchall()
    admins = [admin[0] for admin in admins]
    if inter.author.id in admins:
        if not id.isdigit():
            await inter.response.send_message(embed=Embed(title="Failed", description="Input a valid ID.", color=Color.red()), ephemeral=True)
            return

        try:
            if config == "log":
                plugin.bot.sqlite_cursor.execute("UPDATE Config SET log = ?", (id,))
            elif config == "role":
                plugin.bot.sqlite_cursor.execute("UPDATE Config SET role = ?", (id,))
            elif config == "freddie":
                plugin.bot.sqlite_cursor.execute("UPDATE Config SET freddie = ?", (id,))
            plugin.bot.sqlite_connection.commit()
            await inter.response.send_message(embed=Embed(title="Sucess", description=f"The `{config}` was set to `{id}`.", color=Color.green()), ephemeral=True)
        except Exception as error:
            print(error)
            await inter.response.send_message(embed=Embed(title="Failed", description="An error occured, try again or report this to KarsonTheFoxx."), ephemeral=True)
    else:
        await inter.response.send_message(embed=Embed(title="Failed", description="You do not have permission to do this.", color=Color.red()), ephemeral=True)


@plugin.slash_command(name="dm-members", description="Sends a message to all members who have the allowlist role")
async def dm_members(inter:CommandInteraction, message:str):
    await inter.response.defer()
    plugin.bot.sqlite_cursor.execute("SELECT * FROM Admins WHERE id = ?", (inter.author.id,))
    if plugin.bot.sqlite_cursor.fetchone():
        plugin.bot.sqlite_cursor.execute("SELECT role FROM Config")
        role = plugin.bot.sqlite_cursor.fetchone()[0]
        if role == 0:
            await inter.followup.send(embed=Embed(title="Role ID not set, use `/configure role:roleid config:role`"), ephemeral=True)
            return
        
        role = inter.guild.get_role(role)
        for member in role.members:
            try:
                await member.send(embed=Embed(title="From Origins BE", description=f"> {message}\n-# {inter.author.name}"))
            except Exception:
                pass
        
        await inter.followup.send(embed=Embed(title="Message sent"), ephemeral=True)

@plugin.slash_command(name="purge-allowlist", description="Remove the allowlist role from every member who has it")
async def purge_allowlist(inter:CommandInteraction):
    plugin.bot.sqlite_cursor.execute("SELECT * FROM Admins WHERE id = ?", (inter.author.id,))
    if plugin.bot.sqlite_cursor.fetchone():
        await inter.response.defer()
        plugin.bot.sqlite_cursor.execute("SELECT role FROM Config")
        plugin.bot.sqlite_cursor.fetchone()
        role = plugin.bot.sqlite_cursor.fetchone()[0]
        if role == 0:
            await inter.followup.send(embed=Embed(title="Role ID not set, use `/configure role:roleid config:role`"))
            return
        
        role = inter.guild.get_role(role)
        for member in role.members:
            await member.remove_roles(role)
    
        await inter.followup.send(embed=Embed(title="Purge complete"), ephemeral=True)
    else:
        await inter.response.send_message(embed=Embed(title="You do not have permission to do this", color=Color.red()), ephemeral=True)

@plugin.slash_command(name="manage-admins", description="Add/remove admins from the bot")
async def manage_admins(inter:CommandInteraction, id:str, operation=commands.Param(choices=["add", "remove"])):
    plugin.bot.sqlite_cursor.execute("SELECT * FROM Admins WHERE id = ?", (inter.author.id,))
    if plugin.bot.sqlite_cursor.fetchone()[0]:
        if operation == "add":
            try:
                plugin.bot.sqlite_cursor.execute("INSERT INTO Admins (id) VALUES (?)", (id,))
                await inter.response.send_message(embed=Embed(title="Added"), ephemeral=True)
                try:
                    await plugin.bot.get_user(id).send(embed=Embed(title="From Origins BE", description=f"You have been added as a bot admin for FredBot by {inter.author.id}"))
                except Exception:
                    pass
                
            except IntegrityError:
                await inter.response.send_message(embed=Embed(title="Already a bot admin!"), ephemeral=True)
        
        elif operation == "remove":
            plugin.bot.sqlite_cursor.execute("SELECT * FROM Admins WHERE id = ?", (id,))
            if plugin.bot.sqlite_cursor.fetchone()[0]:
                plugin.bot.sqlite_cursor.execute("DELETE FROM Admins WHERE id = ?", (id,))
                plugin.bot.sqlite_connection.commit()

                await inter.response.send_message(embed=Embed(title="Removed"), ephemeral=True)
    else:
        await inter.response.send_message(embed=Embed(title="You do not have permission to do this", color=Color.red()), ephemeral=True)
                
@plugin.slash_command(name="manage-freddie", description="manages the freddie role")
async def give_freddie(inter: CommandInteraction, user:Member, mode=commands.Param(choices=["give", "take"])):
    plugin.bot.sqlite_cursor.execute("SELECT * FROM Admins WHERE id = ?", (inter.author.id,))
    if plugin.bot.sqlite_cursor.fetchone()[0]:
        plugin.bot.sqlite_cursor.execute("SELECT freddie FROM Config")
        freddie_role = plugin.bot.sqlite_cursor.fetchone()[0]
        if freddie_role != 0:
            if mode == "give":
                await user.add_roles(inter.guild.get_role(freddie_role))
                await inter.response.send_message(embed=Embed(title="Gave role to user", color=Color.green()), ephemeral=True)
            else:
                await user.remove_roles(inter.guild.get_role(freddie_role))
                await inter.response.send_message(embed=Embed(title="Removed role from user", color=Color.green()), ephemeral=True)
        else:
            await inter.response.send_message(embed=Embed(title="Role ID not set", color=Color.red()))
    else:
        await inter.response.send_message(embed=Embed(title="You do not have permission to do this", color=Color.red()), ephemeral=True)

@plugin.slash_command(name="bonk", description="Reminds you of something at the time")
async def bonk(inter:CommandInteraction, message:str, duraction:str=commands.Param(description="In seconds")):
    await inter.response.send_message(":bread:")
    await sleep(duraction)
    await inter.channel.send(f"Bonk! {inter.author.mention} wanted me to remind them: {message}")
setup, teardown = plugin.create_extension_handlers()