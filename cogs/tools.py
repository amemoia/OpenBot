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

def prefixcheck():
    if not os.path.exists('data/payrespects'):
        print('Creating data/payrespects folder...')
        os.makedirs('data/payrespects')
    if not fileIO('data/payrespects/data.json', 'check'):
        print('Creating default data.json...')
        fileIO('data/payrespects/data.json', 'save', {})

def client_role_color(self, ctx):
    ClientMember = discord.utils.get(ctx.message.guild.members, id=self.client.user.id)
    if ClientMember.color == discord.Color.default:
        return 0x7289da
    else:
        return ClientMember.color
    
def settingscheck():
    content = {
    "TOKEN" : "None",
    "DEFAULT_PREFIX" : "=",
    "PRESENCE" : "=help"
    }
    if not fileIO('settings.json', 'check'):
        print('Creating default prefix.json...')
        fileIO('settings.json', 'save', content)