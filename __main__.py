import datetime
import discord
from cogs.ChannelCogs import ChannelCogs
from cogs.ListCogs import ListCogs
from PictureDisplay import PictureDisplay
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

sender = None
@bot.event
async def on_ready():
    global sender
    sender = Sender(bot, servers)
    sender.start()
    print("We have logged in as {0.user}".format(bot))
    


@bot.slash_command(guild_ids=guildIds,  description="Show help window")
async def get_random_pics(ctx: discord.ApplicationContext , search: discord.Option(str, "The search string"),
                          picture_pool:  discord.Option(int, "The number of images", min_value=1, max_value = 200, default=100)):
    await ctx.defer()
    get_random_gif(search, picture_pool)
    await ctx.respond(get_random_gif(search, picture_pool))

 
bot.run(TOKEN)