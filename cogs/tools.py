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
    embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
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
    embed = discord.Embed(title="📕 Help", color=0x7289da, timestamp=datetime.utcnow())
    embed.add_field(name=info["cmd_name"], value=info["cmd_desc"], inline=False)
    embed.add_field(name="Aliases", value=info["cmd_alias"], inline=False)
    embed.add_field(name="Usage", value=info["cmd_format"], inline=False)
    embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
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

async def modlog_toggle_messages(self, ctx, msg):
    guild = ctx.message.guild
    db = fileIO(self.path, "load")
    if db[str(guild.id)]["MODLOG"]["MESSAGES"] == False:
        db[str(guild.id)]["MODLOG"]["MESSAGES"] = True
        fileIO(self.path, "save", db)
        embed=discord.Embed(title=":notepad_spiral: Modlog", description="Enabled {}.".format(msg), color=client_role_color(self, ctx))
        await ctx.send(embed=embed)
    elif db[str(guild.id)]["MODLOG"]["MESSAGES"] == True:
        db[str(guild.id)]["MODLOG"]["MESSAGES"] = False
        fileIO(self.path, "save", db)
        embed=discord.Embed(title=":notepad_spiral: Modlog", description="Disabled {}.".format(msg), color=client_role_color(self, ctx))
        await ctx.send(embed=embed)
    elif db[str(guild.id)]["MODLOG"]["MESSAGES"] == None:
        db[str(guild.id)]["MODLOG"]["MESSAGES"] = True
        fileIO(self.path, "save", db)
        embed=discord.Embed(title=":notepad_spiral: Modlog", description="Enabled {}.".format(msg), color=client_role_color(self, ctx))
        await ctx.send(embed=embed)


async def log_strike(self, ctx, user, strike_data, strikeID):
    guild = ctx.guild
    guildstr = str(ctx.guild.id)
    meriter = strike_data["Author"]
    reason = strike_data["Reason"]
    if str(guild.id) not in self.db:
        return
    if self.db[guildstr]["MODLOG"]["CHANNEL"] == False:
        return
    if user == None:
        return
    channelid = self.db[guildstr]["MODLOG"]["CHANNEL"]
    logchannel = guild.get_channel(int(channelid))
    name = str(user)
        
    logmsg = '{} has recieved a strike from {}'.format(name, meriter)
    embedmsg = discord.Embed(title=logmsg, color=discord.Color.green(), timestamp=datetime.utcnow())
    embedmsg.add_field(name="Reason:", value=reason, inline=False)
    embedmsg.add_field(name="Strike ID:", value=str(strikeID), inline=False)
    embedmsg.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
    await logchannel.send(embed=embedmsg)
    return

async def log_merit(self, ctx, user, merit_data, meritID):
    guild = ctx.guild
    guildstr = str(ctx.guild.id)
    meriter = merit_data["Author"]
    reason = merit_data["Reason"]
    if str(guild.id) not in self.db:
        return
    if self.db[guildstr]["MODLOG"]["CHANNEL"] == False:
        return
    if user == None:
        return
    channelid = self.db[guildstr]["MODLOG"]["CHANNEL"]
    logchannel = guild.get_channel(int(channelid))
    name = str(user)
        
    logmsg = '{} has recieved a merit from {}'.format(name, meriter)
    embedmsg = discord.Embed(title=logmsg, color=discord.Color.green(), timestamp=datetime.utcnow())
    embedmsg.add_field(name="Reason:", value=reason, inline=False)
    embedmsg.add_field(name="Merit ID:", value=str(meritID), inline=False)
    embedmsg.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
    await logchannel.send(embed=embedmsg)
    return

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
    #    STRIKE
    if not fileIO('data/write/strikes.json', 'check'):
        print('Creating default strikes.json...')
        fileIO('data/write/strikes.json', 'save', {})
    #    MERIT
    if not fileIO('data/write/merits.json', 'check'):
        print('Creating default merits.json...')
        fileIO('data/write/merits.json', 'save', {})
    if not fileIO('data/write/setup.json', 'check'):
        print('Creating default setup.json...')
        fileIO('data/write/setup.json', 'save', {})
    
def settingscheck():
    content = {
    "TOKEN" : "None",
    "DEFAULT_PREFIX" : "=",
    "PRESENCE" : "=help"
    }
    if not fileIO('settings.json', 'check'):
        print('Creating default prefix.json...')
        fileIO('settings.json', 'save', content)

def get_prefix(self, ctx):
    jsoncheck()
    prefixes = fileIO("data/write/prefix.json", "load")
    settings = fileIO("settings.json", "load")
    default_prefix = settings["DEFAULT_PREFIX"]

    if not ctx.guild:
        return default_prefix
    elif str(ctx.guild.id) not in prefixes:
        return default_prefix
    else:
        prefix = prefixes[str(ctx.guild.id)]
        return prefix
