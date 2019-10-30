import discord
from discord.ext import commands
from utils.dataIO import fileIO
import cogs.tools as tools
from datetime import datetime



#       Customization options can be found in settings.json!
#       Please do not touch anything else unless
#       you know what you're doing!



tools.settingscheck()
sett = fileIO("settings.json", "load")

if sett["TOKEN"] == "None":
    answ = input("Please paste in your bot token and hit enter.\n")
    sett["TOKEN"] = str(answ)
    fileIO("settings.json", "save", sett)

def get_prefix(client, message):
    tools.jsoncheck()
    if not message.guild:
        return commands.when_mentioned_or(default_prefix)(client, message)
    prefixes = fileIO("data/write/prefix.json", "load")
    if str(message.guild.id) not in prefixes:
        return commands.when_mentioned_or(default_prefix)(client, message)
    prefix = prefixes[str(message.guild.id)]
    return commands.when_mentioned_or(prefix)(client, message)

extensions = ["help", "admin", "fun", "general"]
default_prefix = sett["DEFAULT_PREFIX"]
token = sett["TOKEN"]
presence = sett["PRESENCE"]

client = commands.Bot(command_prefix=get_prefix, case_insensitive=True, help_command=None)

#       Cog Loading

@client.command()
async def unload(ctx, extension):
    if await client.is_owner(ctx.message.author) == True:
        try:
            client.unload_extension(extension)
            print(">>>Unloaded {}".format(extension))
            embed=discord.Embed(title="🔵 {}".format(client.user.name), description="Unloaded {}.".format(extension), color=0x55acee, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=client.user.avatar_url, text="{}".format(client.user.name))
            await ctx.send(embed=embed)
        except Exception as error:
            print("{} cannot be unloaded. [{}]".format(extension, error))
            embed=discord.Embed(title="🔴 Error", description="{} cannot be unloaded.\n[{}]".format(extension, error), color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=client.user.avatar_url, text="{}".format(client.user.name))
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="🔴 Error", description="Only my owner can do that.", color=0xdd2e44, timestamp=datetime.utcnow())
        embed.set_footer(icon_url=client.user.avatar_url, text="{}".format(client.user.name))
        await ctx.send(embed=embed)

@client.command()
async def reload(ctx, extension):
    if await client.is_owner(ctx.message.author) == True:
        try:
            client.reload_extension("cogs." + extension)
            print(">>>Reloaded {}".format(extension))
            embed=discord.Embed(title="🔵 {}".format(client.user.name), description="Reloaded {}.".format(extension), color=0x55acee, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=client.user.avatar_url, text="{}".format(client.user.name))
            await ctx.send(embed=embed)
        except Exception as error:
            print("{} cannot be reloaded. [{}]".format(extension, error))
            embed=discord.Embed(title="🔴 Error", description="{} cannot be reloaded.\n[{}]".format(extension, error), color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=client.user.avatar_url, text="{}".format(client.user.name))
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="🔴 Error", description="Only my owner can do that.", color=0xdd2e44, timestamp=datetime.utcnow())
        embed.set_footer(icon_url=client.user.avatar_url, text="{}".format(client.user.name))
        await ctx.send(embed=embed)

@client.command()
async def load(ctx, extension):
    if await client.is_owner(ctx.message.author) == True:
        try:
            client.load_extension("cogs." + extension)
            print(">>>Loaded {}".format(extension))
            embed=discord.Embed(title="🔵 {}".format(client.user.name), description="Loaded {}.".format(extension), color=0x55acee, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=client.user.avatar_url, text="{}".format(client.user.name))
            await ctx.send(embed=embed)
        except Exception as error:
            print("{} cannot be loaded. [{}]".format(extension, error))
            embed=discord.Embed(title="🔴 Error", description="{} cannot be loaded.\n[{}]".format(extension, error), color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=client.user.avatar_url, text="{}".format(client.user.name))
            await ctx.send(embed=embed)
    else:
        embed=discord.Embed(title="🔴 Error", description="Only my owner can do that.", color=0xdd2e44, timestamp=datetime.utcnow())
        embed.set_footer(icon_url=client.user.avatar_url, text="{}".format(client.user.name))
        await ctx.send(embed=embed)

#       Startup

@client.event
async def on_ready():
    print(" ")
    print("--------------------------------------------------")
    print(" ")
    print("OpenBot online!")
    print(" ")
    print("Client user name:")
    print(str(client.user))
    print(" ")
    print("Default prefix:")
    print(default_prefix)
    print(" ")
    print("Currently in {} guilds.".format(len(client.guilds)))
    print(" ")
    print("--------------------------------------------------")
    print(" ")
    await client.change_presence(status=discord.Status.online, activity=discord.Streaming(name=presence, url='https://www.twitch.tv/directory', twitch_name="directory"))

if __name__ == "__main__":
    for extension in extensions:
        #try:
        client.load_extension("cogs." + extension)
        #except Exception as error:
        #    print("{} cannot be loaded. [{}]".format(extension, error))

    client.run(token)