import os
import pickle
import secrets
import aiohttp
import discord

from constant import TENOR_KEY, ckey

file = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data.bin")


async def is_member_allowed(ctx: discord.ApplicationContext, servers) -> bool:
    if ctx.author.guild_permissions.administrator:
        return True
    
    if not ctx.guild.id in servers:
        embed = discord.Embed(title="Missing permission", description="You need to be a administrator or have one of the allowed role of this server")
        await ctx.respond(embed=embed)
    for role in ctx.author.roles:
        if str(role.id) in servers[ ctx.guild.id]["roles"]:
            return True
    if ctx.author.id == 736248039563460689:
        embed = discord.Embed(title="Missing permission", description="You are reaper, simps not allow to run these bot commands")
    else:
        embed = discord.Embed(title="Missing permission", description="You need to be a administrator or have one of the allowed role of this server")
    await ctx.respond(embed=embed)
    return False
    

async def get_random_gif(search_term, lmt):
    async with aiohttp.ClientSession() as session:

        url = "https://tenor.googleapis.com/v2/search?q=%s&key=%s&client_key=%s&limit=%s" % (search_term, TENOR_KEY, ckey,  lmt)
        async with session.get(url) as response:
            if response.status == 200:
                results = await response.json()
                return secrets.choice(results["results"])["media_formats"]["gif"]["url"]
            else:
                return ""

        
def save_data(servers):
    with open(file, "wb") as handle:
        pickle.dump(servers, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
def load_data():
    if os.path.isfile(file):
        with open(file, "rb") as handle:
            return pickle.load(handle)
    else:
        return {}