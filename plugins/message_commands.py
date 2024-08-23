from disnake.ext import commands, plugins
from disnake import Embed, Color, MessageCommandInteraction, Message
plugin = plugins.Plugin()


@plugin.message_command(name="Allowlist add")
async def allowlist_add(inter:MessageCommandInteraction, message:Message):
    plugin.bot.sqlite_cursor.execute("SELECT * FROM Admins WHERE id = ?", (inter.author.id,))
    if plugin.bot.sqlite_cursor.fetchone():
        plugin.bot.sqlite_cursor.execute("SELECT role, log FROM Config")
        role, log = plugin.bot.sqlite_cursor.fetchall()[0]
        if role != 0:
            try:
                await message.author.add_roles(inter.guild.get_role(role))
                try:
                    await message.author.send(embed=Embed(title=f"From Origins BE", description=f"Your application to join the Origins BE SMP has been accepted", color=Color.green()))
                except Exception:
                    pass
                await inter.response.send_message(embed=Embed(title="Allowlist add", description="The operation as sucessful"), ephemeral=True)
                if log != 0:
                    await inter.guild.get_channel(log).send(embed=Embed(title="Allowlist add", description=f"{inter.author.global_name} ({inter.author.id}) has added {message.author.global_name} ({message.author.id}) to the allowlist"))
            except Exception as error:
                print(error)
        else:
            await inter.response.send_message(embed=Embed(title="Role ID not set, use `/configure role:roleid config:role`"))
    else:
        await inter.response.send_message(embed=Embed(title="You do not have permission to do this", color=Color.red()))

@plugin.message_command(name="Allowlist remove")
async def allowlist_remove(inter:MessageCommandInteraction, message:Message):
    plugin.bot.sqlite_cursor.execute("SELECT * FROM Admins WHERE id = ?", (inter.author.id,))
    if plugin.bot.sqlite_cursor.fetchone():
        plugin.bot.sqlite_cursor.execute("SELECT role, log FROM Config")
        role, log = plugin.bot.sqlite_cursor.fetchall()[0]
        if role != 0:
            try:
                await message.author.remove_roles(inter.guild.get_role(role))
                try:
                    await message.author.send(embed=Embed(title=f"From Origins BE", description=f"You have been removed from the allowlist", color=Color.red()))
                except Exception:
                    pass
                await inter.response.send_message(embed=Embed(title="Allowlist remove", description="The operation as sucessful"), ephemeral=True)
                if log != 0:
                    await inter.guild.get_channel(log).send(embed=Embed(title="Allowlist remove", description=f"{inter.author.global_name} ({inter.author.id}) has removed {message.author.global_name} ({message.author.id}) from the allowlist"))
            except Exception as error:
                print(error)
        else:
            await inter.response.send_message(embed=Embed(title="Role ID not set, use `/configure role:roleid config:role`"))
    else:
        await inter.response.send_message(embed=Embed(title="You do not have permission to do this", color=Color.red()))


setup, teardown = plugin.create_extension_handlers()