from disnake.ext import plugins, tasks
from disnake import Embed, Color,  utils
from mcstatus import BedrockServer
from asyncio import sleep
ORIGINS_MESSAGE = None
COUNCIL_MESSAGE = None
first_itteration = True
plugin = plugins.Plugin()

@plugin.register_loop()
@tasks.loop(seconds=30)
async def check_status():
    global first_itteration
    await plugin.bot.wait_until_ready()
    if first_itteration:
        await sleep(5)
        first_itteration = False
        
    global ORIGINS_MESSAGE, COUNCIL_MESSAGE
    embed = Embed()
    timestamp = f"<t:{int(utils.utcnow().timestamp())}:R>"
    try:
        server = BedrockServer("OriginsBE.duckdns.org", 19225)
        status = server.status()
        embed.title = ":green_circle: Server is online"
        embed.description = f"Version: `{status.version.name}`\nPlayers: `{status.players_online}/{status.players_max}`\nlatency (from west Canada)): `{status.latency}`\n-# Last updated: {timestamp}"
        embed.color = Color.green()
    except TimeoutError:
        try:
            server = BedrockServer("54.38.29.227", 19225)
            status = server.status()
            embed.title = ":yellow_circle: Server is online"
            embed.description = f" DuckDNS unreachable, use IP: `54.38.29.227` instead.\nVersion: `{status.version.name}`\nPlayers: `{status.players_online}/{status.players_max}`\nlatency (from west Canada)): `{status.latency}`\n-# Last updated: {timestamp}"
            embed.color = Color.yellow()
        except TimeoutError:
            embed.title = ":red_circle: Server unreachable"
            embed.description = f"Server is offline, or incorrect address has been passed\n-# Last updated: {timestamp}"
            embed.color = Color.red()
            embed.add_field(name="Adresses tried", value="`OriginsBE.duckdns.org:19255`, `54.38.29.227:19255`")
    
    try:
        if ORIGINS_MESSAGE == None:
            ORIGINS_MESSAGE = await plugin.bot.get_guild(826685546772168734).get_channel(1161528232965836931).send(embed=embed)
        else:
            await ORIGINS_MESSAGE.edit(embed=embed)
    except Exception:
        pass
    try:
        if COUNCIL_MESSAGE == None:
            COUNCIL_MESSAGE = await plugin.bot.get_guild(1166799644362276967).get_channel(1282534413430689963).send(embed=embed)
        else:
            await COUNCIL_MESSAGE.edit(embed=embed)
    except Exception:
        pass

            
setup, teardown = plugin.create_extension_handlers()
