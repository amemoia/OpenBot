import discord
import random
import cogs.tools as tools
from cogs.tools import client_role_color
from datetime import datetime
from utils.dataIO import fileIO
from discord.ext import commands

class Merit(commands.Cog, name="merit"):
    def __init__(self, client):
        self.client = client
        self.path = "data/write/merits.json"
        self.db = fileIO(self.path, "load")

    @commands.command()
    @commands.guild_only()
    async def merit(self, ctx, user: discord.Member = None, *args):
        """CATEG_MOD Append a note to a server member, which may be viewed by anyone at any time. Good for noting down good behaviors."""
        if ctx.message.author.guild_permissions.manage_messages == False:
            embed=discord.Embed(title="🔴 Error", description="You do not have the necessary permissions.", color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
            return

        channel = ctx.message.channel
        author = ctx.message.author
        guild = ctx.message.guild

        if user == None:
            embed=discord.Embed(title="🔴 Error", description="Provide a user for this to work.", color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
            return
        if user == author:
            embed=discord.Embed(title="🔴 Error", description="You can't merit yourself! :eyes:", color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
            return
        if user == self.client.user:
            embed=discord.Embed(title="🔴 Error", description="I can't merit myself! :eyes:", color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
            return

        reason = " ".join(args)
        if reason == "":
            reason = "No reason provided."

        dm = user.dm_channel

        maxID = 999999999999999999
        minID = 100000000000000000
        meritID = random.randint(minID, maxID)
        time = datetime.now()
        fmt = "%d %b %Y %H:%M"
        timestamp = time.strftime(fmt)

        guildstr = str(guild.id)
        userstr = str(user.id)
        meritstr = str(meritID)

        merit_data = {"Reason" : reason,
                       "Date" : timestamp,
                       "Author" : str(author)}

        embed=discord.Embed(title=":warning: {}".format(self.client.user.name), description="Are you sure you want to merit {}?".format(user.mention), color=0xffcd4c, timestamp=datetime.utcnow())
        embed.set_footer(icon_url=self.client.user.avatar_url,text="Reply with yes to continue.")
        await ctx.send(embed=embed)

        def check(m):
            return m.channel == channel and m.author == author

        msg = await self.client.wait_for('message', check=check)
        if msg.content == "yes" or msg.content == "y":

            if guildstr in self.db:
                for x in self.db[guildstr]:
                    while meritstr in self.db[guildstr][x]:
                        meritID = random.randint(minID, maxID)
                        meritstr = str(meritID)
                if userstr not in self.db[guildstr]:
                    self.db[guildstr][userstr] = {}
            if guildstr not in self.db:
                self.db[guildstr] = {}
                self.db[guildstr][userstr] = {}

            self.db[guildstr][userstr][meritstr] = merit_data

            fileIO(self.path, "save", self.db)
            await tools.log_merit(self, ctx, user, merit_data, meritID)
            embed = discord.Embed(title="🌟 Merit", description="{} has recieved a merit.".format(user.mention), color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)

            try:
                replyembed = discord.Embed(title="🌟 {}".format(self.client.user.name), description="You recieved a merit in {} for the following:\n```{}```".format(guild.name, reason), color=0xffcd4c, timestamp=datetime.utcnow())
                replyembed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
                replyembed.set_thumbnail(url=guild.icon_url)
                if dm == None:
                    await user.create_dm()
                    dm = user.dm_channel
                await dm.send(embed=replyembed)
            except discord.errors.Forbidden:
                pass
        else:
            embed = discord.Embed(title="🌟 Merit", description="Cancelling...", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def merits(self, ctx, user: discord.Member = None):
        """CATEG_MOD List someone's merits."""
        if user == None:
            user = ctx.message.author
        guild = ctx.message.guild
        guildstr = str(guild.id)
        userstr = str(user.id)

        if not self.db or not self.db[guildstr] or guildstr not in self.db or userstr not in self.db[guildstr]:
            embed = discord.Embed(title="{} has no merits in {}.".format(user.name, guild.name), color=client_role_color(self, ctx), timestamp=datetime.utcnow())
        
        elif userstr in self.db[guildstr]:
            embed = discord.Embed(title="🌟 Merits", description="{} has {} merit(s) in {}".format(user.mention, len(self.db[guildstr][userstr]), guild.name), color=client_role_color(self, ctx))
            for x in self.db[guildstr][userstr]:
                embed.add_field(name=str(x), value="```Reason: {}\nAuthor: {}\nDate: {}```".format(self.db[guildstr][userstr][str(x)]["Reason"], self.db[guildstr][userstr][str(x)]["Author"], self.db[guildstr][userstr][str(x)]["Date"]), inline=False)
        
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def rmmerit(self, ctx, meritID: int=0):
        """CATEG_MOD Delete a merit."""
        if ctx.message.author.guild_permissions.manage_messages == False:
            embed=discord.Embed(title="🔴 Error", description="You do not have the necessary permissions.", color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
            return
        if meritID < 100000000000000000 or meritID > 9999999999999999999:
            embed=discord.Embed(title="🔴 Error", description="Invalid merit ID.", color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
            return

        channel = ctx.message.channel
        author = ctx.message.author
        guild = ctx.message.guild
        guildstr = str(guild.id)
        meritstr = str(meritID)

        embed=discord.Embed(title=":warning: {}".format(self.client.user.name), description="Are you sure you want to delete this merit?", color=0xffcd4c, timestamp=datetime.utcnow())
        embed.set_footer(icon_url=self.client.user.avatar_url,text="Reply with yes to continue.")
        await ctx.send(embed=embed)

        def check(m):
            return m.channel == channel and m.author == author

        msg = await self.client.wait_for('message', check=check)
        if msg.content == "yes" or msg.content == "y":
            for x in self.db[guildstr]:
                if meritstr in self.db[guildstr][x]:
                    del self.db[guildstr][x][meritstr]
                    fileIO(self.path, "save", self.db)
                    embed = discord.Embed(title="🌟 Merit", description="Successfully removed the merit.", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
                    embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
                    await ctx.send(embed=embed)
                    
                    if not self.db[guildstr][x]:
                        del self.db[guildstr][x]
                        if not self.db[guildstr]:
                            del self.db[guildstr]
                        fileIO(self.path, "save", self.db)
                    return
            embed=discord.Embed(title="🔴 Error", description="merit not found.", color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="🌟 Merit", description="Cancelling...", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def clearmerits(self, ctx, user: discord.Member = None):
        """CATEG_MOD Clear someone's merits."""

        channel = ctx.message.channel
        author = ctx.message.author
        guild = ctx.message.guild
        guildstr = str(guild.id)
        userstr = str(user.id)

        if ctx.message.author.guild_permissions.manage_messages == False:
            embed=discord.Embed(title="🔴 Error", description="You do not have the necessary permissions.", color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
            return
        if user == None:
            embed=discord.Embed(title="🔴 Error", description="You need to provide a user.", color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
            return
        if user == author:
            embed=discord.Embed(title="🔴 Error", description="You can't clear your own merits!", color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
            return

        embed=discord.Embed(title=":warning: {}".format(self.client.user.name), description="Are you sure you want to clear {}'s merits?".format(user.mention), color=0xffcd4c, timestamp=datetime.utcnow())
        embed.set_footer(icon_url=self.client.user.avatar_url,text="Reply with yes to continue.")
        await ctx.send(embed=embed)

        def check(m):
            return m.channel == channel and m.author == author

        msg = await self.client.wait_for('message', check=check)
        if msg.content == "yes" or msg.content == "y":
            if self.db[guildstr][userstr]:
                del self.db[guildstr][userstr]
                fileIO(self.path, "save", self.db)
                embed = discord.Embed(title="🌟 Merit", description="Successfully cleared {}'s merits.".format(user.mention), color=client_role_color(self, ctx), timestamp=datetime.utcnow())
                embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
                await ctx.send(embed=embed)
                
                if not self.db[guildstr]:
                    del self.db[guildstr]
                fileIO(self.path, "save", self.db)
                return

            embed = discord.Embed(title="🌟 Merit", description="{} didn't have any merits to clear.".format(user.mention), color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title="🌟 Merit", description="Cancelling...", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)

def setup(client):
    tools.jsoncheck()
    client.add_cog(Merit(client))