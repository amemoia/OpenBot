import discord
from discord.ext import commands
import time
from datetime import datetime
from tools import client_role_color
import tools
from utils.dataIO import fileIO
import traceback

class Admin(commands.Cog, name="admin"):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def test(self, ctx):  
        embed=discord.Embed(title="🔵 Test", description="Hello! :wave:", color=0x55acee, timestamp=datetime.utcnow())
        embed.set_footer(icon_url=self.client.user.avatar_url, text="{}".format(self.client.user.name))
        await ctx.send(embed=embed)

    @commands.command()
    async def testerror(self, ctx):
        embed=discord.Embed(title="🔴 Error", description="This is an error.", color=0xdd2e44, timestamp=datetime.utcnow())
        embed.set_footer(icon_url=self.client.user.avatar_url, text="{}".format(self.client.user.name))
        await ctx.send(embed=embed)

    @commands.command()
    async def testwarning(self, ctx):
        embed=discord.Embed(title="⚠️ Warning", description="This is a warning.", color=0xffcd4c, timestamp=datetime.utcnow())
        embed.set_footer(icon_url=self.client.user.avatar_url, text="{}".format(self.client.user.name))
        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        channel = ctx.message.channel
        t1 = time.perf_counter()
        await channel.trigger_typing()
        t2 = time.perf_counter()
  
        embed=discord.Embed(title="🏓 Pong!", description="This took me {}ms.".format(round((t2-t1)*1000)), color=client_role_color(self, ctx), timestamp=datetime.utcnow())
        embed.set_footer(icon_url=self.client.user.avatar_url, text="{}".format(self.client.user.name))
        await ctx.send(embed=embed)

    @commands.command()
    async def say(self, ctx, *args):
        msg = " ".join(args)
        await ctx.send(msg)
        await ctx.message.delete()

    @commands.command()
    @commands.guild_only()
    async def prefix(self, ctx, *, prefix):
        if self.client.is_owner(ctx.message.author) == True or ctx.message.author.guild_permissions.manage_guild == True:
            predata = "data/prefix/prefix.json"
            db = fileIO(predata, "load")
            channel = ctx.message.channel
            author = ctx.message.author

            embed=discord.Embed(title="⚠️ Prefix", description="Are you sure you want to change this server's prefix to `{}`?".format(prefix), color=0xffcd4c, timestamp=datetime.utcnow())
            embed.set_footer(text="Reply with yes to continue.")
            await ctx.send(embed=embed)

            def check(m):
                return m.channel == channel and m.author == author

            msg = await self.client.wait_for('message', check=check)
            if msg.content == "yes" or msg.content == "y":
                db[str(ctx.guild.id)] = prefix
                fileIO(predata, "save", db)
 
                embed=discord.Embed(title="⁉️ Prefix", description="Successfully set this server's prefix to `{}`".format(prefix), color=client_role_color(self, ctx), timestamp=datetime.utcnow())
                embed.set_footer(icon_url=self.client.user.avatar_url, text="{}".format(self.client.user.name))
                await ctx.send(embed=embed)
            else:
                embed=discord.Embed(title="⁉️ Prefix", description="Cancelling...", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
                embed.set_footer(icon_url=self.client.user.avatar_url, text="{}".format(self.client.user.name))
                await ctx.send(embed=embed)
        else:
            return

    @commands.command()
    async def invite(self, ctx):
        url = "https://discordapp.com/api/oauth2/authorize?client_id=635411383554539520&permissions=506981622&scope=bot"
        embed = discord.Embed(title="✉️ Invite Link", description="You can invite me using [this link]({})".format(url))
        embed.set_footer(icon_url=self.client.user.avatar_url, text="{}".format(self.client.user.name))
        await tools.dmauthor(self, ctx, embed)

        embed=discord.Embed(title="✉️ Invite", description="Check your DMs! :page_facing_up:", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
        embed.set_footer(icon_url=self.client.user.avatar_url, text="{}".format(self.client.user.name))
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def status(self, ctx, *args):
        game = " ".join(args)
        if str(game) == "":
            return
        await self.client.change_presence(status=discord.Status.online, activity=discord.Streaming(name=game, url='https://www.twitch.tv/directory', twitch_name="directory"))
        embed=discord.Embed(title="🎮 Status", description='Setting status to "{}".'.format(game), color=client_role_color(self, ctx))
        embed.set_footer(icon_url=self.client.user.avatar_url, text="{}".format(self.client.user.name))
        await ctx.send(embed=embed)

    @commands.command()
    @commands.is_owner()
    async def guildlist(self, ctx):
        msg = discord.Embed(title="📃 Guild list", description="Currently in {} guilds, those are:".format(len(self.client.guilds)), color=client_role_color(self, ctx))
        for x in self.client.guilds:
            msg.add_field(name=x.name, value="ID: `" + str(x.id) + "`, " + str(len(x.members)) + " Members", inline=False)
        msg.set_footer(icon_url=self.client.user.avatar_url, text="{}".format(self.client.user.name))
        await tools.dmauthor(self, ctx, embed=msg)

    @commands.command()
    @commands.is_owner()
    async def leaveguild(self, ctx, id: int = 0000000):
        if id == 0000000:
            embed=discord.Embed(title="🔴 Error", description="You need to provide a valid guild ID.", color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text="{}".format(self.client.user.name))
            await ctx.send(embed=embed)
            return
        guild = discord.utils.get(self.client.guilds, id=id)
        if guild == None:
            embed=discord.Embed(title="🔴 Error", description="You need to provide a valid guild ID.", color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text="{}".format(self.client.user.name))
            await ctx.send(embed=embed)
            return
        await guild.leave()
        embed=discord.Embed(title="👋 Leave Guild", description="Successfully left the guild.", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
        embed.set_footer(icon_url=self.client.user.avatar_url, text="{}".format(self.client.user.name))
        await ctx.send(embed=embed)

    @commands.command(name='eval')
    @commands.guild_only()
    @commands.is_owner()
    async def _eval(self, ctx, *, command):
        if await self.client.is_owner(ctx.message.author) == True:
            try:
                res = eval(command)
                if inspect.isawaitable(res):
                    embed=discord.Embed(title="🤖 Eval", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
                    embed.add_field(name="Output:", value="```py\n{}\n```".format(await res), inline=False)
                    embed.set_footer(icon_url=self.client.user.avatar_url, text="{}".format(self.client.user.name))
                    await ctx.send(embed=embed)
                else:
                    embed=discord.Embed(title="🤖 Eval", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
                    embed.add_field(name="Output:", value="```py\n{}\n```".format(res), inline=False)
                    embed.set_footer(icon_url=self.client.user.avatar_url, text="{}".format(self.client.user.name))
                    await ctx.send(embed=embed)
            except:
                embed=discord.Embed(title="🤖 Eval", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
                embed.add_field(name="Output:", value="```py\n{}\n```".format(traceback.format_exc()), inline=False)
                embed.set_footer(icon_url=self.client.user.avatar_url, text="{}".format(self.client.user.name))
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="🔴 Error", description="Only my owner can do that.", color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text="{}".format(self.client.user.name))
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Admin(client))