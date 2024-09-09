from disnake.ext import commands, plugins, tasks
from disnake import Embed, Color, Message
from mcstatus import BedrockServer
from datetime import datetime
from asyncio import sleep
ORIGINS_MESSAGE = None
COUNCIL_MESSAGE = None
plugin = plugins.Plugin()

# @plugin.register_loop()
# @tasks.loop(seconds=30)
# async def check_status():
#     await plugin.bot.wait_until_ready()
#     global ORIGINS_MESSAGE, COUNCIL_MESSAGE
#     embed = Embed()
#     timestamp = f":t:{int(datetime.now().timestamp())}:r:"
#     try:
#         server = BedrockServer("OriginsBE.duckdns.org", 19225)
#         status = server.status()
#         embed.title = ":green_circle: Server is online"
#         embed.description = f"Version: `{status.version}`\nPlayers: `{status.players_online}/{status.players_max}`\nlatency (from west Canada)): `{status.latency}`\n-# Last updated: {timestamp}"
#         embed.color = Color.green()
#     except TimeoutError:
#         try:
#             server = BedrockServer("54.38.29.227", 19225)
#             status = server.status()
#             embed.title = ":yellow_circle: Server is online"
#             embed.description = f" DuckDNS unreachable, use IP: `54.38.29.227` instead.\nVersion: `{status.version}`\nPlayers: `{status.players_online}/{status.players_max}`\nlatency (from west Canada)): `{status.latency}`\n-# Last updated: {timestamp}"
#             embed.color = Color.yellow()
#         except TimeoutError:
#             embed.title = ":red_circle: Server unreachable"
#             embed.description = f"Server is offline, or incorrect address has been passed\n-# Last updated: {timestamp}"
#             embed.color = Color.red()
#             embed.add_field(name="Adresses tried", value="`OriginsBE.duckdns.org:19255`, `54.38.29.227:19255`")
    
#     try:
#         if ORIGINS_MESSAGE == None:
#             ORIGINS_MESSAGE = await plugin.bot.get_guild(826685546772168734).get_channel(1161528232965836931).send(embed=embed)
#         else:
#             await ORIGINS_MESSAGE.edit(embed=embed)
#     except Exception:
#         pass
#     try:
#         print(COUNCIL_MESSAGE)
#         if COUNCIL_MESSAGE == None:
#             COUNCIL_MESSAGE = await plugin.bot.get_guild(1166799644362276967).get_channel(1282534413430689963).send(embed=embed)
#         else:
#             await COUNCIL_MESSAGE.edit(embed=embed)
#     except Exception:
#         pass

            
setup, teardown = plugin.create_extension_handlers()