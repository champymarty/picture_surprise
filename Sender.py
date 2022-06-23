from datetime import datetime
import logging
import os
import random
import discord
from discord.ext import commands, tasks

from Util import get_random_gif, save_data

logger = logging.getLogger("discord_sender")
logger.setLevel(logging.INFO)
fileDir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "logs")
if not os.path.isdir(fileDir):
    os.mkdir(fileDir)
file = os.path.join(fileDir, "sender.log")
handler = logging.FileHandler(filename=file, encoding="utf-8", mode="w")
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

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
        try:
            changed = False
            if not self.isLooping:
                self.isLooping = True
                for guid_id, info in self.servers.items():
                    for pictureDisplay in info["pictures"]:
                        now = datetime.now()
                        if now - pictureDisplay.lastSent  >= pictureDisplay.timedelta:
                            pictureDisplay.lastSent = now
                            changed = True
                            if pictureDisplay.isListSearch():
                                if not info["pictures_list"][pictureDisplay.list_name] is None:
                                    pic_info = random.choice(info["pictures_list"][pictureDisplay.list_name])
                                    await self.send_image(pic_info["url"], 
                                                        info["channels"], guid_id, pictureDisplay.list_name,
                                                        footer_text="To delete the picture: /list remove_picture list_name: {} picture_id: {}".format(pictureDisplay.list_name, pic_info["id"]))
                            else:
                                await self.send_image(await get_random_gif(pictureDisplay.search, pictureDisplay.max_search),
                                                    info["channels"], guid_id, pictureDisplay.search)
                self.isLooping = False
            if changed:
                save_data(self.servers)
        except Exception as e:
            logger.exception("exception in loop")
            self.isLooping = False
            
    async def send_image(self, url, channels, guild_id, search, footer_text: None):
        guild = await discord.utils.get_or_fetch(self.bot, "guild", guild_id)
        if guild is not None:
            for channel_id in channels:
                channel = await discord.utils.get_or_fetch(guild, "channel", channel_id)
                if channel is not None:
                    embed = discord.Embed(title="Here is a picture of {}".format(search))
                    embed.set_image(url=url)
                    if not footer_text is None:
                        embed.set_footer(text=footer_text)
                    await channel.send(embed=embed)
            