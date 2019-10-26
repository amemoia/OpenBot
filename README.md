<p align="center">
  <strong>OpenBot</strong> Is WIP a open-source, cog-based discord.py bot with a variety of commands ranging from moderation to completely random, fun stuff. Takes some elements from the Red discord bot.
  <br>
  The default prefixes are <code>=[command]</code> and <code>@OpenBot [command]</code>
  <br>
</p>

## Planned Features
- ⚖️ Moderation
- 📋 Logging
- 📝 Per-Server strike / merit system
- 🎮 Fun and games
- 💍 Cross-Server marriage system
- 🔊 Music playback
- ⁉️ Custom prefixes
- 🎶 Osu! integration

Right now a full command list is only available through `=help`

## Owner-only commands
- `=status` set the bot's status message
- `=guildlist` sends a list of guilds the bot is in alongside their IDs
- `=leaveguild [guild.id]` leaves the guild with the given ID
- `=eval [code]` runs the given code, DMs you if there's any errors

## Hosting

#### Requirements
- <a href="https://www.python.org/downloads/"> Python </a> (duh)
- <a href="https://github.com/Rapptz/discord.py">Discord.py</a> (voice support is not required right now)
- An IDE, for example <a href="https://code.visualstudio.com">Visual Studio Code</a> is highly recommended

#### How to host
- Clone the repository
- Create a `.bat` file which runs `bot.py` and open it
- When prompted, paste your bot token into the window

Default prefix and status can be changed within `settings.json`
