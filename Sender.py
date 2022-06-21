from datetime import datetime
import discord
from discord.ext import commands, tasks

from Util import get_random_gif, save_data



class Sender(commands.Cog):
    def __init__(self, bot: discord.Bot, servers):
        self.bot: discord.Bot = bot
        self.servers = servers
        self.isLooping = False     

    def cog_unload(self):
        self.timeChecker.cancel()
        
        
    def start(self):
        self.timeChecker.start()
        

    @tasks.loop(seconds=30)
    async def timeChecker(self):
        changed = False
        if not self.isLooping:
            self.isLooping = True
            for guid_id, info in self.servers.items():
                for pictureDisplay in info["pictures"]:
                    now = datetime.now()
                    if now - pictureDisplay.lastSent  >= pictureDisplay.timedelta:
                        pictureDisplay.lastSent = now
                        changed = True
                        await self.send_image(get_random_gif(pictureDisplay.search, pictureDisplay.max_search), info["channels"], guid_id, pictureDisplay.search)
            self.isLooping = False
        if changed:
            save_data(self.servers)
            
    async def send_image(self, url, channels, guild_id, search):
        guild = await discord.utils.get_or_fetch(self.bot, "guild", guild_id)
        if guild is not None:
            for channel_id in channels:
                channel = await discord.utils.get_or_fetch(guild, "channel", channel_id)
                if channel is not None:
                    embed = discord.Embed(title="Here is a picture of {}".format(search))
                    embed.set_image(url=url)
                    await channel.send(embed=embed)
            