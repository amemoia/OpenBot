import discord
import cogs.tools as tools
from discord.ext import commands
from cogs.tools import client_role_color
from utils.dataIO import fileIO

class Help(commands.Cog, name="help"):
    def __init__(self, client):
        self.client = client

    @commands.group()
    async def help(self, ctx):
        if ctx.invoked_subcommand == None:

            def get_prefix(client, message):
                tools.prefixcheck()
                prefixes = fileIO("data/prefix/prefix.json", "load")
                settings = fileIO("settings.json", "load")
                default_prefix = settings["DEFAULT_PREFIX"]

                if not message.guild:
                    return default_prefix
                elif str(message.guild.id) not in prefixes:
                    return default_prefix
                else:
                    prefix = prefixes[str(message.guild.id)]
                    return prefix

            general = "`invite` `ping`"
            fun = "`say`"
            mod = ""
            admin = "`prefix`"

            embed = discord.Embed(title="📕 Help", description="My prefix on this server is `{pre}`. Alternatively, just @ me. \nFor more information on a command, send `{pre}help [command]`".format(pre=get_prefix(self.client, ctx.message)), color=client_role_color(self, ctx))
            embed.add_field(name="🔷 General", value=general)
            embed.add_field(name="🕹️ Fun", value=fun)
            embed.add_field(name="⚖️ Moderation", value=mod)
            embed.add_field(name="🔶 Server Admin", value=admin)
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Help(client))