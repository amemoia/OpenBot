import discord
import __main__ as main
from datetime import datetime
import time
from utils.dataIO import fileIO
from discord.ext import commands
import os
import asyncio

async def errorcheck(self, ctx, error):
    msg = None
    if isinstance(error, commands.BadArgument):
        if ctx.command.name == 'assign' or ctx.command.name == 'role':
            msg="Role not found. Make sure the capitalization matches."
        if ctx.command.name == 'hinfo' or ctx.command.name == 'hackinfo':
            return
        else:
            msg="User not found. Make sure the capitalization matches."
    if isinstance(error, commands.MissingPermissions):
        if ctx.command.name == 'modlog':
            return
        else:
            msg = "You do not have the necessary permissions to run this command."
    if isinstance(error, commands.NoPrivateMessage):
        msg = "This command doesn't work in DMs."
    if isinstance(error, commands.CommandNotFound):
        msg = "I couldn't find that command. Check `@{} help` for the command list.".format(self.client.user.name)
    if isinstance(error, commands.DisabledCommand):
        msg = "This command is currently disabled."
    if isinstance(error, commands.TooManyArguments):
        msg = "You gave me too many arguments, check `@{} help [command]` for details.".format(self.client.user.name)
    if isinstance(error, commands.CommandOnCooldown):
        msg = "This command is on cooldown, try again in {}.".format(error.retry_after)
    if isinstance(error, commands.BotMissingPermissions):
        msg = "I am missing required permissions for this command."
    if isinstance(error, commands.MissingRole) or isinstance(error, commands.MissingAnyRole):
        msg = "You do not have the required role(s) to run this command."
    if isinstance(error, commands.BotMissingRole) or isinstance(error, commands.BotMissingAnyRole):
        msg = "The bot does not have the required role(s) to run this command."
    if isinstance(error, commands.NSFWChannelRequired):
        msg = "This command only works in NSFW channels."
    if isinstance(error, commands.NotOwner):
        msg = "This command is only available to the bot's owner"
    if msg == None:
        msg = "```{}```".format(error)
    embed=discord.Embed(title="🔴 Error", description=msg, color=0xdd2e44)
    embed.set_footer(icon_url=self.client.user.avatar_url, text="{}".format(self.client.user.name))
    await ctx.send(embed=embed)

async def dmauthor(self, ctx, embed):
    user = ctx.message.author
    userdm = user.dm_channel
    if userdm == None:
        await user.create_dm()
        userdm = user.dm_channel
        pass
    await userdm.send(embed=embed)

async def send_cmdinfo(self, ctx, info):
    embed = discord.Embed(title="📕 Help", color=0x7289da)
    embed.add_field(name=info.cmd_name, value=info.cmd_desc, inline=False)
    embed.add_field(name="Aliases", value=info.cmd_alias, inline=False)
    embed.add_field(name="Category", value=info.cmd_categ, inline=False)
    embed.add_field(name="Requirements", value=info.cmd_req, inline=False)
    embed.set_footer(icon_url=self.client.user.avatar_url, text="{}".format(self.client.user.name))
    await ctx.send(embed=embed)

def client_role_color(self, ctx):
    if ctx.message.guild != None:
        ClientMember = discord.utils.get(ctx.message.guild.members, id=self.client.user.id)
        if ClientMember.color == discord.Color.default() or ClientMember.color.value == 0:
            return 0x7289da
        else:
            return ClientMember.color
    else:
        return 0x7289da

def jsoncheck():
    if not os.path.exists('data/write'):
        print('Creating data/write folder...')
        os.makedirs('data/write')
    #    PREFIX
    if not fileIO('data/write/prefix.json', 'check'):
        print('Creating default prefix.json...')
        fileIO('data/write/prefix.json', 'save', {})
    #    PAYRESPECTS
    if not fileIO('data/write/payrespects.json', 'check'):
        print('Creating default payrespects.json...')
        fileIO('data/write/payrespects.json', 'save', {})

    
def settingscheck():
    content = {
    "TOKEN" : "None",
    "DEFAULT_PREFIX" : "=",
    "PRESENCE" : "=help"
    }
    if not fileIO('settings.json', 'check'):
        print('Creating default prefix.json...')
        fileIO('settings.json', 'save', content)
