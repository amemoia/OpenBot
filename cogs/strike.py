import discord
import random
import cogs.tools as tools
from cogs.tools import client_role_color
from datetime import datetime
from utils.dataIO import fileIO
from discord.ext import commands

class Strike(commands.Cog, name="strike"):
    def __init__(self, client):
        self.client = client
        self.path = "data/write/strikes.json"
        self.db = fileIO(self.path, "load")

    @commands.command()
    @commands.guild_only()
    async def strike(self, ctx, user: discord.Member = None, *args):
        """CATEG_MOD Append a note to a server member, which may be viewed by anyone at any time. Good for noting down bad behaviors and using strikes as a warning."""
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
            embed=discord.Embed(title="🔴 Error", description="You can't strike yourself! :eyes:", color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
            return
        if user == self.client.user:
            embed=discord.Embed(title="🔴 Error", description="I can't strike myself! :eyes:", color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
            return

        reason = " ".join(args)
        if reason == "":
            reason = "No reason provided."

        dm = user.dm_channel

        maxID = 999999999999999999
        minID = 100000000000000000
        strikeID = random.randint(minID, maxID)
        time = datetime.now()
        fmt = "%d %b %Y %H:%M"
        timestamp = time.strftime(fmt)

        guildstr = str(guild.id)
        userstr = str(user.id)
        strikestr = str(strikeID)

        strike_data = {"Reason" : reason,
                       "Date" : timestamp,
                       "Author" : str(author)}

        embed=discord.Embed(title=":warning: {}".format(self.client.user.name), description="Are you sure you want to strike {}?".format(user.mention), color=0xffcd4c, timestamp=datetime.utcnow())
        embed.set_footer(icon_url=self.client.user.avatar_url,text="Reply with yes to continue.")
        await ctx.send(embed=embed)

        def check(m):
            return m.channel == channel and m.author == author

        msg = await self.client.wait_for('message', check=check)
        if msg.content == "yes" or msg.content == "y":

            if guildstr in self.db:
                for x in self.db[guildstr]:
                    while strikestr in self.db[guildstr][x]:
                        strikeID = random.randint(minID, maxID)
                        strikestr = str(strikeID)
                if userstr not in self.db[guildstr]:
                    self.db[guildstr][userstr] = {}
            if guildstr not in self.db:
                self.db[guildstr] = {}
                self.db[guildstr][userstr] = {}

            self.db[guildstr][userstr][strikestr] = strike_data

            fileIO(self.path, "save", self.db)
            await tools.log_strike(self, ctx, user, strike_data, strikeID)
            embed = discord.Embed(title=":warning: Strike", description="{} has recieved a strike.".format(user.mention), color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)

            try:
                replyembed = discord.Embed(title=":warning: {}".format(self.client.user.name), description="You recieved a strike in {} for the following:\n```{}```".format(guild.name, reason), color=0xffcd4c, timestamp=datetime.utcnow())
                replyembed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
                replyembed.set_thumbnail(url=guild.icon_url)
                if dm == None:
                    await user.create_dm()
                    dm = user.dm_channel
                await dm.send(embed=replyembed)
            except discord.errors.Forbidden:
                pass
        else:
            embed = discord.Embed(title=":warning: Strike", description="Cancelling...", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def strikes(self, ctx, user: discord.Member = None):
        """CATEG_MOD List someone's strikes."""
        if user == None:
            user = ctx.message.author
        guild = ctx.message.guild
        guildstr = str(guild.id)
        userstr = str(user.id)

        if not self.db or not self.db[guildstr] or guildstr not in self.db or userstr not in self.db[guildstr]:
            embed = discord.Embed(title="{} has no strikes in {}.".format(user.name, guild.name), color=client_role_color(self, ctx), timestamp=datetime.utcnow())
        
        elif userstr in self.db[guildstr]:
            embed = discord.Embed(title=":warning: Strikes", description="{} has {} strike(s) in {}".format(user.mention, len(self.db[guildstr][userstr]), guild.name), color=client_role_color(self, ctx))
            for x in self.db[guildstr][userstr]:
                embed.add_field(name=str(x), value="```Reason: {}\nAuthor: {}\nDate: {}```".format(self.db[guildstr][userstr][str(x)]["Reason"], self.db[guildstr][userstr][str(x)]["Author"], self.db[guildstr][userstr][str(x)]["Date"]), inline=False)
        
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def rmstrike(self, ctx, strikeID: int=0):
        """CATEG_MOD Delete a strike."""
        if ctx.message.author.guild_permissions.manage_messages == False:
            embed=discord.Embed(title="🔴 Error", description="You do not have the necessary permissions.", color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
            return
        if strikeID < 100000000000000000 or strikeID > 9999999999999999999:
            embed=discord.Embed(title="🔴 Error", description="Invalid strike ID.", color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
            return

        channel = ctx.message.channel
        author = ctx.message.author
        guild = ctx.message.guild
        guildstr = str(guild.id)
        strikestr = str(strikeID)

        embed=discord.Embed(title=":warning: {}".format(self.client.user.name), description="Are you sure you want to delete this strike?", color=0xffcd4c, timestamp=datetime.utcnow())
        embed.set_footer(icon_url=self.client.user.avatar_url,text="Reply with yes to continue.")
        await ctx.send(embed=embed)

        def check(m):
            return m.channel == channel and m.author == author

        msg = await self.client.wait_for('message', check=check)
        if msg.content == "yes" or msg.content == "y":
            for x in self.db[guildstr]:
                if strikestr in self.db[guildstr][x]:
                    del self.db[guildstr][x][strikestr]
                    fileIO(self.path, "save", self.db)
                    embed = discord.Embed(title=":warning: Strike", description="Successfully removed the strike.", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
                    embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
                    await ctx.send(embed=embed)
                    
                    if not self.db[guildstr][x]:
                        del self.db[guildstr][x]
                        if not self.db[guildstr]:
                            del self.db[guildstr]
                        fileIO(self.path, "save", self.db)
                    return
            embed=discord.Embed(title="🔴 Error", description="Strike not found.", color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=":warning: Strike", description="Cancelling...", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def clearstrikes(self, ctx, user: discord.Member = None):
        """CATEG_MOD Clear someone's strikes."""

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
            embed=discord.Embed(title="🔴 Error", description="You can't clear your own strikes!", color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
            return

        embed=discord.Embed(title=":warning: {}".format(self.client.user.name), description="Are you sure you want to clear {}'s strikes?".format(user.mention), color=0xffcd4c, timestamp=datetime.utcnow())
        embed.set_footer(icon_url=self.client.user.avatar_url,text="Reply with yes to continue.")
        await ctx.send(embed=embed)

        def check(m):
            return m.channel == channel and m.author == author

        msg = await self.client.wait_for('message', check=check)
        if msg.content == "yes" or msg.content == "y":
            if self.db[guildstr][userstr]:
                del self.db[guildstr][userstr]
                fileIO(self.path, "save", self.db)
                embed = discord.Embed(title=":warning: Strike", description="Successfully cleared {}'s strikes.".format(user.mention), color=client_role_color(self, ctx), timestamp=datetime.utcnow())
                embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
                await ctx.send(embed=embed)
                
                if not self.db[guildstr]:
                    del self.db[guildstr]
                fileIO(self.path, "save", self.db)
                return

            embed = discord.Embed(title=":warning: Strike", description="{} didn't have any strikes to clear.".format(user.mention), color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(title=":warning: Strike", description="Cancelling...", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)

def setup(client):
    tools.jsoncheck()
    client.add_cog(Strike(client))