<p align="center">
  <strong>OpenBot</strong> Is WIP an unfinished cog-based discord.py bot with a variety of commands ranging from moderation to completely random, fun stuff. Takes some elements from the Red discord bot.
  <br>
  The default prefixes are <code>=[command]</code> and <code>@OpenBot [command]</code>
  <br>
</p>

### Discontinued
While I've moved onto other projects meant to replace the mess that this bot was, feel free to frankenstein it into something of your own.
Follow the guide below to get started,

#### Requirements
- <a href="https://www.python.org/downloads/"> Python </a>
- <a href="https://github.com/Rapptz/discord.py">Discord.py</a> (voice support is not required right now)
- A code editor, for example <a href="https://code.visualstudio.com">Visual Studio Code</a> is required if you want to change stuff or add your own things

#### How to host
- Clone the repository
- Create a `.bat` file which runs `bot.py` and open it
- When prompted, paste your bot token into the window

#### Owner-only commands
- `=status [str]` set the bot's status message without changing the default status
- `=guildlist` sends a list of guilds the bot is in alongside their IDs
- `=leaveguild [guild.id]` leaves the guild with the given ID
- `=eval [code]` runs the given code, DMs you if there's any errors

Default prefix and status can be changed within `settings.json`
