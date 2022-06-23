import discord
from Util import is_member_allowed, save_data
from constant import guildIds
from discord.ext import commands

class PermissionCogs(commands.Cog):
    
    def __init__(self, bot: discord.Bot, servers):
        self.bot = bot
        self.servers = servers
        
    permission = discord.SlashCommandGroup("permission", "Commands related to who can use them")
    
        
    @permission.command(guild_ids=guildIds, description="Add a role who can execute the commands")
    async def add_role(self, ctx: discord.ApplicationContext,
                       role: discord.Option(discord.Role, description="The role to be allow to run the commands")):
        await ctx.defer()
        if not await is_member_allowed(ctx, self.servers):
            return
        if not ctx.guild.id in self.servers:
            self.servers[ctx.guild.id] = {
                "pictures": [],
                "channels": set(),
                "pictures_list": {},
                "roles": set()
            }
            self.servers[ctx.guild.id]["roles"].add(str(role.id))
            save_data(self.servers)
            await ctx.respond("The role {} was added to the permissions".format(role.mention))
        elif role.id in self.servers[ctx.guild.id]["roles"]:
            await ctx.respond("The role {} already exist in the permissions !".format(role.mention))
        else:
            self.servers[ctx.guild.id]["roles"].add(str(role.id))
            save_data(self.servers)
            await ctx.respond("The role {} was added to the permissions".format(role.mention))
        
    @permission.command(guild_ids=guildIds, description="Remove a role from the allowed member")
    async def remove_role(self, ctx: discord.ApplicationContext,
                          role: discord.Option(discord.Role, description="The role who cant run the commands anymore")):
        await ctx.defer()
        if not await is_member_allowed(ctx, self.servers):
            return
        if not ctx.guild.id in self.servers or not str(role.id) in self.servers[ctx.guild.id]["roles"]:
            await ctx.respond("The role {} does not exist in your permissions".format(role.mention))
        else:
            self.servers[ctx.guild.id]["roles"].remove(str(role.id))
            save_data(self.servers)
            await ctx.respond("The role {} was remove from the permissions".format(role.mention))
        
    @permission.command(guild_ids=guildIds, description="Remove a role from the allowed member")
    async def show_role(self, ctx: discord.ApplicationContext):
        if not ctx.guild.id in self.servers or len(self.servers[ctx.guild.id]["roles"]) == 0:
            await ctx.respond("You don't have any permission roles")
        else:
            i = 1
            text = ""
            for role_id in self.servers[ctx.guild.id]["roles"]:
                role: discord.Role = await discord.utils.get_or_fetch(ctx.guild, "role", int(role_id))
                text += "{}) {} \n".format(i, role.mention)
                i += 1
            await ctx.respond(embed=discord.Embed(title="Your permission roles", description=text))
                
        