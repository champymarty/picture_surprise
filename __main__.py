import logging
import os
import discord
from cogs.ChannelCogs import ChannelCogs
from cogs.ListCogs import ListCogs
from cogs.PermissionsCogs import PermissionCogs
from Sender import Sender
from cogs.PictureSenderCogs import PictureSenderCogs
from constant import TOKEN, guildIds
from Util import get_random_gif, load_data, save_data

# id {
#    pictures: []
#    channels: set(),
#    pictures_list: {
#           list_name: [
#                    {
#                        id
#                        url
#                    }
#                   ]
#    }
# }
servers = {}
servers = load_data()

intents = discord.Intents.default()
bot: discord.ext.commands.Bot = discord.ext.commands.Bot(intents=intents)
bot.add_cog(ListCogs(bot, servers))
bot.add_cog(ChannelCogs(bot, servers))
bot.add_cog(PictureSenderCogs(bot, servers))
bot.add_cog(PermissionCogs(bot, servers))

logger = logging.getLogger("discord_commands")
logger.setLevel(logging.INFO)
fileDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "logs")
if not os.path.isdir(fileDir):
    os.mkdir(fileDir)
file = os.path.join(fileDir, "command.log")
handler = logging.FileHandler(filename=file, encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

sender = None
@bot.event
async def on_ready():
    global sender
    sender = Sender(bot, servers)
    sender.start()
    logger.info("We have logged in as {0.user}".format(bot))
    print("We have logged in as {0.user}".format(bot))
    


@bot.slash_command(guild_ids=guildIds,  description="Show help window")
async def get_random_pics(ctx: discord.ApplicationContext , search: discord.Option(str, "The search string"),
                          picture_pool:  discord.Option(int, "The number of images", min_value=1, max_value = 200, default=100)):
    await ctx.defer()
    await ctx.respond(await get_random_gif(search, picture_pool))
    
@bot.event
async def on_application_command_error(ctx, error: Exception):
    embed = discord.Embed(title="Unexpected error (this error will be log and look into)", description=error);
    await ctx.respond(embed=embed)
    logger.exception("On {} Exception: {}".format(ctx.guild, error))

 
bot.run(TOKEN)