import datetime
import discord
from PictureDisplay import PictureDisplay
from Util import save_data
from constant import guildIds
from discord.ext import commands

class PictureSenderCogs(commands.Cog):
    
    def __init__(self, bot: discord.Bot, servers):
        self.bot = bot
        self.servers = servers
        
    pictureSender = discord.SlashCommandGroup("picture_sender", "Commands related to sending picture to channels")
    
    @pictureSender.command(guild_ids=guildIds, description="Show help window")
    async def add(self, ctx: discord.ApplicationContext, search: discord.Option(str, "The search string"),
                            days: discord.Option(int, "The number of days before next pic", min_value=0),
                            picture_pool:  discord.Option(int, "The number of images", min_value=1, max_value = 200, default=100),
                            hours : discord.Option(int, "The number of hours days before next pic (is adding time on top of days)", min_value=0, default=0), 
                            minutes : discord.Option(int, "The number of minutes before next pic (is adding time on top of days and hours)", min_value=0, default=0)):
        await ctx.defer()
        if not ctx.guild.id in self.servers or self.servers[ctx.guild.id]["channels"] is None:
            await ctx.respond("You need to set your channels to received pictures first !")
            return
        timedelta = datetime.timedelta(days=days, hours=hours, minutes=minutes)
        if ctx.guild.id in self.servers:
            self.servers[ctx.guild.id]["pictures"].append(PictureDisplay(search, timedelta, picture_pool))
        else:
            self.servers[ctx.guild.id] = {
                "pictures": [PictureDisplay(search, timedelta, picture_pool)],
                "channels": None,
                "pictures_list": {}
            }
        channels = ""
        for channel_id in self.servers[ctx.guild.id]["channels"]:
            channel = await discord.utils.get_or_fetch(ctx.guild, "channel", channel_id)
            channels += ", {}".format(channel.mention)
        if channels != "":
            channels = channels[2:]
        save_data(self.servers)
        await ctx.respond("You will receive a picture of {} each {} in channel {}".format(search, timedelta, channels))

    @pictureSender.command(guild_ids=guildIds,  description="Show all the pictures sender of your server")
    async def show(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        if not ctx.guild.id in self.servers or len(self.servers[ctx.guild.id]["pictures"]) == 0:
            await ctx.respond("You dont have any picture sender !")
        else:
            text = ""
            i = 1
            for picture_sender in self.servers[ctx.guild.id]["pictures"]:
                text += "{}) search: {} with timedelta of {} and a poll of {}\n".format(i, picture_sender.search,
                                                                                    picture_sender.timedelta,
                                                                                    picture_sender.max_search)
                i += 1
            embed = discord.Embed(title="Here are your picture senders !", description=text)
            await ctx.respond(embed=embed)
            
    @pictureSender.command(guild_ids=guildIds,  description="Remove a picture sender")
    async def remove(self, ctx: discord.ApplicationContext, search: discord.Option(str, "The search string")):
        await ctx.defer()
        if not ctx.guild.id in self.servers or len(self.servers[ctx.guild.id]["pictures"]) == 0:
            await ctx.respond("You dont have any picture sender !")
        else:
            i = 0
            found = False
            for picture_sender in self.servers[ctx.guild.id]["pictures"]:
                if search == picture_sender.search:
                    found = True
                    break
                i += 1
            if found:
                del self.servers[ctx.guild.id]["pictures"][i]
                save_data(self.servers)
                embed = discord.Embed(title="Remove success", description="The picture sender was removed !")
            else:
                embed = discord.Embed(title="Remove fail", description="The search term does not exist in your picture sender")
            await ctx.respond(embed=embed)