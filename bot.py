import discord
from discord.ext import commands
from utils.dataIO import fileIO
import cogs.tools as tools



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
    tools.prefixcheck()
    if not message.guild:
        return commands.when_mentioned_or(default_prefix)(client, message)
    prefixes = fileIO("data/prefix/prefix.json", "load")
    if str(message.guild.id) not in prefixes:
        return commands.when_mentioned_or(default_prefix)(client, message)
    prefix = prefixes[str(message.guild.id)]
    return commands.when_mentioned_or(prefix)(client, message)

extensions = ["admin"]
default_prefix = sett["DEFAULT_PREFIX"]
token = sett["TOKEN"]
presence = sett["PRESENCE"]

#       Startup

client = commands.Bot(command_prefix=get_prefix, case_insensitive=True)

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
        try:
            client.load_extension('cogs.' + extension)
        except Exception as error:
            print("{} cannot be loaded. [{}]".format(extension, error))

    client.run(token)