import discord
from Util import is_member_allowed, save_data
from constant import guildIds
from discord.ext import commands

class ChannelCogs(commands.Cog):
    
    def __init__(self, bot: discord.Bot, servers):
        self.bot = bot
        self.servers = servers
        
    channel = discord.SlashCommandGroup("channel", "Commands related to channel picture")
    
    @channel.command(guild_ids=guildIds,  description="Add a channel to receive pictures")
    async def add(self, ctx: discord.ApplicationContext, channel: discord.Option(discord.TextChannel, "The channel where the picture will be sent")):
        await ctx.defer()
        if not await is_member_allowed(ctx, self.servers):
            return
        if not ctx.guild.id in self.servers:
            self.servers[ctx.guild.id] = {
                "pictures": [],
                "channels": {channel.id},
                "pictures_list": {},
                "roles": set()
            }
        else:
            self.servers[ctx.guild.id]["channels"].add(channel.id)
        save_data(self.servers)
        await ctx.respond("Channel added !")
        
    @channel.command(guild_ids=guildIds,  description="Remove a channel to receive pictures")
    async def remove(self, ctx: discord.ApplicationContext, channel: discord.Option(discord.TextChannel, "The channel where the picture will be sent")):
        await ctx.defer()
        if not await is_member_allowed(ctx, self.servers):
            return
        if not ctx.guild.id in self.servers or len(self.servers[ctx.guild.id]["channels"]) == 0:
            embed = discord.Embed(title="Remove fail", description="You don't have any picture channels in your server")
        else:
            if channel.id in self.servers[ctx.guild.id]["channels"]:
                self.servers[ctx.guild.id]["channels"].remove(channel.id)
                save_data(self.servers)
                embed = discord.Embed(title="Remove success", description="The channel was removed !")
            else:
                embed = discord.Embed(title="Remove fail", description="The channel does not exist in your picture channel")
        await ctx.respond(embed=embed)
        
    @channel.command(guild_ids=guildIds,  description="Show channel to receive pictures")
    async def show(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        if not ctx.guild.id in self.servers or self.servers[ctx.guild.id]["channels"] is None:
            await ctx.respond("No channel !")
        else:
            text = ""
            i = 1
            for channel_id in self.servers[ctx.guild.id]["channels"]:
                channel = await discord.utils.get_or_fetch(ctx.guild, "channel", channel_id)
                text += "{}) {} \n".format(i, channel.mention)
                i += 1
            embed = discord.Embed(title="Here are your channels !", description=text)
            await ctx.respond(embed=embed)