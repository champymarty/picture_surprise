import uuid
from Confirm import Confirm
from Util import save_data
from constant import guildIds
import discord
from discord.ext import commands, pages
import validators

class ListCogs(commands.Cog):
    
    def __init__(self, bot: discord.Bot, servers):
        self.bot = bot
        self.servers = servers

    list = discord.SlashCommandGroup("list", "Commands related to url picture list")
    
    @list.command(guild_ids=guildIds, description="View all picture of a list")
    async def view(self, ctx: discord.ApplicationContext, 
                                 list_name: discord.Option(str, "The name of the list to view"),
                                 start_picture: discord.Option(int, "The picture number were to start", min_value=1, default=1)
                                 ):
        await ctx.defer()
        if not ctx.guild.id in self.servers or len(self.servers[ctx.guild.id]["pictures_list"]) == 0:
            await ctx.respond("You dont have any list !")
        else:
            if list_name in self.servers[ctx.guild.id]["pictures_list"]:
                pageList = []
                i = 1
                for url_info in self.servers[ctx.guild.id]["pictures_list"][list_name]:
                    if validators.url(url_info["url"]):
                        embed = discord.Embed(title="Picture {}".format(i) )
                        embed.set_image(url=url_info["url"])
                    else:
                        embed = discord.Embed(title="Picture " + str(i), description="Invalid url")
                    if validators.url(url_info["url"]):
                        embed.set_image(url=url_info["url"])
                    embed.set_footer(text="To delete the picture: /remove_picture_in_list list_name: {} picture_id: {}".format(list_name, url_info["id"]))
                    pageList.append(pages.Page(
                        embeds=[
                            embed
                        ],
                    ))
                    i += 1
                paginator = pages.Paginator(pages=pageList, timeout=60 * 5)
                paginator.current_page = start_picture - 1
                await paginator.respond(ctx.interaction, ephemeral=False)
            else:
                embed = discord.Embed(title="Remove fail !", description="This list name does not exist in your url picture list")
                await ctx.respond(embed=embed)
                
    @list.command(guild_ids=guildIds,  description="Create a list of url pictures")
    @discord.option(
        "attachment",
        discord.Attachment,
        description="A file with all the pictures url on each line",
        required=False  # The default value will be None if the user doesn't provide a file.
    )
    @discord.option(
        "url_separator",
        str,
        description="The file separator (default is next line)",
        default="\n",
        required=False
    )
    @discord.option(
        "encoding",
        str,
        description="The encoding of the file",
        default=None,
        required=False
    )
    async def create(self, ctx: discord.ApplicationContext, list_name: str, attachment: discord.Attachment,
                                url_separator: str, encoding: str):
        await ctx.defer()
        if attachment is not None:
            file_read = await attachment.read()
            file_content = None
            if encoding is None:
                file_content = file_read.decode()
            else:
                file_content = file_read.decode(encoding=encoding)
            
            urls = file_content.strip().split(url_separator)
            urls_pic = []
            for url in urls:
                url = url.strip()
                urls_pic.append({
                    "id": str(uuid.uuid4()),
                    "url": url 
                })
        else:
            urls_pic = []
        if not ctx.guild.id in self.servers:
            self.servers[ctx.guild.id] = {
                "pictures": [],
                "channels": None,
                "pictures_list": {
                    list_name: urls_pic
                }
            }
            save_data(self.servers)
            await ctx.respond("The list was created with {} items !".format(len(urls_pic)))
        else:
            if list_name in self.servers[ctx.guild.id]["pictures_list"]:
                await ctx.respond("That list already exist !")
            else:
                self.servers[ctx.guild.id]["pictures_list"][list_name] = urls_pic
                save_data(self.servers)
                await ctx.respond("The list was created with {} items !".format(len(urls_pic)))
                
                
    @list.command(guild_ids=guildIds,  description="Show all the url picture list")
    async def show(self, ctx: discord.ApplicationContext):
        await ctx.defer()
        if not ctx.guild.id in self.servers or len(self.servers[ctx.guild.id]["pictures_list"]) == 0:
            await ctx.respond("You dont have any list !")
        else:
            text = ""
            i = 1
            for list_name, urls in self.servers[ctx.guild.id]["pictures_list"].items():
                text += "{}) {} with {} items\n".format(i, list_name, len(urls))
                i += 1
            embed = discord.Embed(title="Here are your url picture list !", description=text)
            await ctx.respond(embed=embed)
            
    @list.command(guild_ids=guildIds, name="add_url", description="Add a url picture to a list")
    async def add_url(self, ctx: discord.ApplicationContext, 
                                    list_name: discord.Option(str, "The name of the list to delete"),
                                    url: discord.Option(str, "The url of the picture")):
        await ctx.defer()
        if not ctx.guild.id in self.servers or len(self.servers[ctx.guild.id]["pictures_list"]) == 0:
            await ctx.respond("You dont have any list !")
        else:
            if list_name in self.servers[ctx.guild.id]["pictures_list"]:
                if not validators.url(url):
                    await ctx.respond("Invalid url format")
                isIn = False
                for pic_info in self.servers[ctx.guild.id]["pictures_list"][list_name]:
                    if pic_info["url"] == url:
                        isIn = True
                        break
                if isIn:
                    await ctx.respond("Url already in this list !")
                else:
                    view = Confirm()
                    embed = discord.Embed()
                    embed.set_image(url=url)
                    embed.set_footer(text="If you dont see your image, you have a bad url")
                    await ctx.respond("Do you want to add that picture ?", embed=embed, view=view)
                    await view.wait()
                    if view.value:
                        self.servers[ctx.guild.id]["pictures_list"][list_name].append({
                            "id": str(uuid.uuid4()),
                            "url": url 
                        })
                        save_data(self.servers)
                        await ctx.send_followup("Url added !")
            
    @list.command(guild_ids=guildIds, name="remove", description="Remove all a url picture list")
    async def remove_list(self, ctx: discord.ApplicationContext, 
                                    list_name: discord.Option(str, "The name of the list to delete")):
        await ctx.defer()
        if not ctx.guild.id in self.servers or len(self.servers[ctx.guild.id]["pictures_list"]) == 0:
            await ctx.respond("You dont have any list !")
        else:
            if list_name in self.servers[ctx.guild.id]["pictures_list"]:
                embed = discord.Embed(title="Remove success !", description="The list was removed !")
                del self.servers[ctx.guild.id]["pictures_list"][list_name]
                save_data(self.servers)
            else:
                embed = discord.Embed(title="Remove fail !", description="This list name does not exist in your url picture list")
            await ctx.respond(embed=embed)
            
    @list.command(guild_ids=guildIds,  description="Remove all a url picture list")
    async def remove_picture(self, ctx: discord.ApplicationContext, 
                                    list_name: discord.Option(str, "The name of the list to delete"), 
                                    picture_id: discord.Option(int, "The picture number to delete")):
        await ctx.defer()
        if not ctx.guild.id in self.servers or len(self.servers[ctx.guild.id]["pictures_list"]) == 0:
            await ctx.respond("You dont have any list !")
        else:
            pass
            # todo