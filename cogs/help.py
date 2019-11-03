import discord
import inspect
import cogs.tools as tools
from discord.ext import commands
from cogs.tools import client_role_color, get_prefix
from utils.dataIO import fileIO
from datetime import datetime

#
#    =help takes a command's doc / help text (the """text""" at the start of each command)
#    in order to determine their description and category.
#    the category is determined by the FIRST 10 CHARACTERS of the help text (includes a whitespace)
#    the rest is used for the description.
#    
#    valid categories are: CATEG_GEN, CATEG_FUN, CATEG_MOD, CATEG_ADM, CATEG_OWN
#                          (general, fun, guild moderator, guild admin, bot owner)
#    CATEG_OWN commands do not show in -help, they can be found on the website or in the readme
#    
#    example:
#
#    """CATEG_GEN This is a cool command for cool people"""
#      |CATEGORY|              DESCRIPTION              |
#


class Help(commands.Cog, name="help"):
    def __init__(self, client):
        self.client = client

    @commands.group()
    async def help(self, ctx, cmd: str = "None"):
        """CATEG_GEN Sends this message."""
        self.pre = get_prefix(self, ctx)

        all_aliases = []
        for x in self.client.commands:
            all_aliases.append(x.aliases)

        mcommand = None
        if cmd != "None":
            mcommand = discord.utils.get(self.client.commands, name=cmd)
        if mcommand == None:
            for x in all_aliases:
                if cmd in x:
                    mcommand = discord.utils.get(self.client.commands, aliases=x)

        if mcommand == None:

            general_list = []
            fun_list = []
            mod_list = []
            admin_list = []

            for x in self.client.commands:
                desc = x.help if x.help is not None else "No description provided."
                desc_categ = desc[0:9]
                name = "`" + x.name + "`"
                if desc_categ == "CATEG_GEN":
                    general_list.append(name)
                if desc_categ == "CATEG_FUN":
                    fun_list.append(name)
                if desc_categ == "CATEG_MOD":
                    mod_list.append(name)
                if desc_categ == "CATEG_ADM":
                    admin_list.append(name)
                if desc_categ == "CATEG_OWN" or desc_categ == "CATEG_NON" or desc_categ == "CATEG_SUB":
                    pass

            general = " ".join(general_list)
            fun = " ".join(fun_list)
            mod = " ".join(mod_list)
            admin = " ".join(admin_list)

            embed = discord.Embed(title="📕 Help", description="My prefix on this server is `{pre}`. Alternatively, just @ me. \nFor more information on a command, send `{pre}help [command]`".format(pre=self.pre), color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.add_field(name="🔷 General", value=general, inline=False)
            embed.add_field(name="🎮 Fun", value=fun, inline=False)
            embed.add_field(name="🔨 Moderation", value=mod, inline=False)
            embed.add_field(name="🔶 Server Admin", value=admin, inline=False)
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
        else:
            if mcommand.aliases == None:
                aliases = "None"
            elif len(mcommand.aliases) == 0:
                aliases = "None"
            else:
                xlist = []
                for x in mcommand.aliases:
                    xlist.append("`{}`".format(x))
                aliases = " ".join(xlist)

            ####                                TAKEN FROM DISCORD/EXT/COMMANDS/FORMATTER.PY                                ####
            params = mcommand.clean_params
            if len(params) > 0:
                result = []
                for name, param in params.items():
                    if param.default is not param.empty:
                        should_print = param.default if isinstance(param.default, str) else param.default is not None
                        if should_print:
                            result.append('[{}={}]'.format(name, param.default))
                        else:
                            result.append('[{}]'.format(name))
                    elif param.kind == param.VAR_POSITIONAL:
                        result.append('[{}...]'.format(name))
                    else:
                        result.append('<{}>'.format(name))
                out = " ".join(result)
                usage = "{}{} {}".format(self.pre, mcommand.name, out)
            else:
                usage = "{}{}".format(self.pre, mcommand.name)
            ####                                                                                                            ####


            info = {
                "cmd_name" : "{}{}".format(self.pre, mcommand.name),
                "cmd_desc" : "",
                "cmd_alias" : aliases,
                "cmd_format" : "`{}`".format(usage)
            }
            await tools.send_cmdinfo(self, ctx, info)

    @commands.command(aliases = ['info', 'about'])
    async def botinfo(self, ctx):
        """CATEG_GEN Information about the bot."""
        embed = discord.Embed(title="🤖 About", description="Based on [OpenBot](https://github.com/notLeM/OpenBot), an open-source discord bot by [notLeM](https://github.com/notLeM).", timestamp=datetime.utcnow(), color=client_role_color(self, ctx))
        embed.add_field(name="OpenBot version", value="Alpha 5.1")
        embed.add_field(name="Servers", value=len(self.client.guilds))
        embed.add_field(name="Commands", value=len(self.client.commands))
        embed.add_field(name="\u200b", value="[Invite]({}) • [OpenBot Website](https://notlem.github.io/)".format(discord.utils.oauth_url(client_id=self.client.user.id, permissions=discord.Permissions(permissions=1609952503))), inline=False)
        embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Help(client))