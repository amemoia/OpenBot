import discord
import cogs.tools
from utils.dataIO import fileIO
from discord.ext import commands
from datetime import datetime
from cogs.tools import client_role_color, get_prefix, modlog_toggle_messages

class Setup(commands.Cog, name="setup"):
    def __init__(self, client):
        self.client = client
        self.path = "data/write/setup.json"
        self.db = fileIO(self.path, "load")
        self.template = {"JOINLEAVE" : None,
                        "STARBOARD" : None,
                        "TRUST" : None,
                        "VIP" : None,
                        "AGREE" : {"CHANNEL" : None, "ROLE" : None},
                        "MODLOG" : {"CHANNEL" : None, "MESSAGES" : True},
                        "COLORS" : []}
        self.coloremoji = ['💖', '💛', '💚', '💙', '💜']

    @commands.guild_only()
    @commands.command()
    async def settings(self, ctx):
        """CATEG_ADM Shows the bot's settings for the current guild."""
        guild = ctx.message.guild
        guildstr = str(guild.id)
        disabled = []
        if not self.db[guildstr]["AGREE"]["CHANNEL"]:
            disabled.append("agree")
        if not self.db[guildstr]["MODLOG"]["CHANNEL"]:
            disabled.append("modlog")
        if not self.db[guildstr]["JOINLEAVE"]:
            disabled.append("joinleave")
        if not self.db[guildstr]["STARBOARD"]:
            disabled.append("starboard")
        if not self.db[guildstr]["TRUST"]:
            disabled.append("trust")
        if not self.db[guildstr]["VIP"]:
            disabled.append("vip")

        embed = discord.Embed(title="⚙️ Server Settings", description="Bot feature settings for this server:", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
        if self.db[guildstr]["AGREE"]["CHANNEL"]:
            channel = guild.get_channel(int(self.db[guildstr]["AGREE"]["CHANNEL"]))
            embed.add_field(name="Agree channel:", value=channel.mention)
        if self.db[guildstr]["MODLOG"]["CHANNEL"]:
            channel = guild.get_channel(int(self.db[guildstr]["MODLOG"]["CHANNEL"]))
            embed.add_field(name="Modlog channel:", value=channel.mention)
        
        if self.db[guildstr]["JOINLEAVE"]:
            channel = guild.get_channel(int(self.db[guildstr]["JOINLEAVE"]))
            embed.add_field(name="Join / Leave message channel:", value=channel.mention)
        if self.db[guildstr]["STARBOARD"]:
            channel = guild.get_channel(int(self.db[guildstr]["STARBOARD"]))
            embed.add_field(name="Starboard channel:", value=channel.mention)
        if self.db[guildstr]["TRUST"]:
            role = guild.get_role(int(self.db[guildstr]["TRUST"]))
            embed.add_field(name="Trusted user role:", value=role.name)
        if self.db[guildstr]["VIP"]:
            role = guild.get_role(int(self.db[guildstr]["VIP"]))
            embed.add_field(name="VIP user role:", value=role.name)

        embed.add_field(name="Disabled features:", value=", ".join(disabled), inline=False)
        await ctx.send(embed=embed)

    @commands.guild_only()
    @commands.group()
    async def setup(self, ctx):
        """CATEG_ADM Sets up commands that require specific channels or roles. Valid subcommands are: `agree` `joinleave` `modlog` `starboard` `colorroles` `trust` `vip` `reset`"""
        self.pre = get_prefix(self, ctx)
        if ctx.message.author.guild_permissions.manage_guild == False:
            embed=discord.Embed(title="🔴 Error", description="You do not have the required permissions for this command.", color=0xdd2e44, timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
            return
        if ctx.invoked_subcommand == None:
            embed=discord.Embed(title="🔴 Error", description="You didn't provide a valid subcommand.\nAvailable options are: `agree` `joinleave` `modlog` `starboard` `reset`.", color=0xdd2e44, timestamp=datetime.utcnow())
            await ctx.send(embed=embed)
            return

    @setup.command()
    @commands.has_permissions(manage_guild=True)
    async def agree(self, ctx, channel: discord.TextChannel = None):
        """CATEG_SUB """
        author = ctx.message.author
        rechannel = ctx.message.channel
        guild = ctx.message.guild
        guildstr = str(guild.id)

        perm_member = discord.Permissions()
        perm_member.update(create_instant_invite=True,
        add_reactions=True, read_messages=True,
        send_messages=True, embed_links=True,
        attach_files=True, read_message_history=True,
        external_emojis=True, connect=True, speak=True,
        use_voice_activation=True, change_nickname=True)

        def check(m):
                return m.channel == rechannel and m.author == author

        if guild.me.guild_permissions.manage_channels == False:
            await ctx.send("I require the `manage channels` permissions to do this.")
            return
        if guild.me.guild_permissions.manage_roles == False:
            await ctx.send("I require the `manage roles` permissions to do this.")
            return

        if channel == None:
            embed=discord.Embed(title=":warning: {}".format(self.client.user.name), description="You didn't give me a channel, would you like me to create a new one?", color=0xffcd4c, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url,text="Reply with yes to continue.")
            await ctx.send(embed=embed)

            msg = await self.client.wait_for('message', check=check)
            if msg.content == "yes" or msg.content == "y":
                await guild.create_text_channel(name="agree")
                channel = discord.utils.get(guild.text_channels, name="agree")
            else:
                embed = discord.Embed(title="⚙️ Setup", description="Cancelling...", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
                embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
                return await ctx.send(embed=embed)

        if guildstr not in self.db:
            self.db[guildstr] = self.template
        self.db[guildstr]["AGREE"]["CHANNEL"] = str(channel.id)

        memberrole = discord.utils.get(guild.roles, name="Member")
        if memberrole == None:
            guild.create_role(name="Member", permissions=perm_member)
            memberrole = discord.utils.get(guild.roles, name="Member")

        self.db[guildstr]["AGREE"]["ROLE"] = str(memberrole.id)

        memberlist = guild.members
        memberlist.remove(guild.me)
        for x in memberlist:
            if memberrole not in x.roles:
                await x.add_roles(memberrole)

        await guild.default_role.edit(permissions=discord.Permissions.none())

        await channel.set_permissions(target=memberrole, read_messages=False)
        await channel.set_permissions(target=guild.default_role, read_messages=True, send_messages=True, read_message_history=True)

        welcome = discord.Embed(title="🔵 {}".format(self.client.user.name), description="Welcome to {}! If you agree with our rules, type ``{}agree`` to unlock the rest of the server.".format(guild.name, self.pre), colour=client_role_color(self, ctx), timestamp=datetime.utcnow())
        welcome.set_thumbnail(url=ctx.message.guild.icon_url)
        await channel.send(embed=welcome)

        embed=discord.Embed(title=":warning: {}".format(self.client.user.name), description="What is your rules channel?", color=0xffcd4c, timestamp=datetime.utcnow())
        embed.set_footer(icon_url=self.client.user.avatar_url,text="Mention a channel to continue.")
        await ctx.send(embed=embed)

        msg = await self.client.wait_for('message', check=check)
        if msg.content == "cancel" or msg.content == "no" or msg.content == "n":
            await ctx.send("Cancelling...")
            await guild.default_role.edit(permissions=discord.Permissions(permissions=104193089))
        while len(msg.channel_mentions) != 1:
            await ctx.send("Please mention a channel.")
            msg = await self.client.wait_for('message', check=check)
        if len(msg.channel_mentions) == 1:
            for TextChannel in msg.channel_mentions:
                await TextChannel.set_permissions(target=guild.default_role, send_messages=False, read_messages=True, read_message_history=True, add_reactions=False)
                await TextChannel.set_permissions(target=memberrole, send_messages=False, read_messages=True, read_message_history=True, add_reactions=False)

        fileIO(self.path, "save", self.db)
        embed = discord.Embed(title="⚙️ Setup", description="`{}agree` setup complete".format(self.pre), color=client_role_color(self, ctx), timestamp=datetime.utcnow())
        embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
        return await ctx.send(embed=embed)

    @commands.command(name="agree")
    @commands.guild_only()
    async def _agree(self, ctx):
        """CATEG_NONE"""
        guild = ctx.message.guild
        author = ctx.message.author
        guildstr = str(guild.id)
        channelstr = str(ctx.message.channel.id)
        if guildstr not in self.db:
            return
        if self.db[guildstr]["AGREE"]["CHANNEL"] == channelstr:
            memberrole = discord.utils.get(guild.roles, name="Member")
            if self.db[guildstr]["AGREE"]["ROLE"] == str(memberrole.id):
                await author.add_roles(memberrole)
                await ctx.message.delete()

    @setup.command()
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    async def joinleave(self, ctx, channel: discord.TextChannel = None):
        """CATEG_SUB """
        guildstr = str(ctx.message.guild.id)
        if channel == None:
            embed=discord.Embed(title=":warning: {}".format(self.client.user.name), description="You didn't give me a channel, would you like me set up here?", color=0xffcd4c, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url,text="Reply with yes to continue.")
            await ctx.send(embed=embed)

            def check(m):
                return m.channel == ctx.channel and m.author == ctx.message.author

            msg = await self.client.wait_for('message', check=check)
            if msg.content == "yes" or msg.content == "y":
                channel = ctx.channel
            else:
                embed = discord.Embed(title="⚙️ Setup", description="Cancelling...", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
                embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
                return await ctx.send(embed=embed)

        if guildstr not in self.db:
            self.db[guildstr] = self.template
        self.db[guildstr]["JOINLEAVE"] = str(channel.id)

        fileIO(self.path, "save", self.db)
        embed = discord.Embed(title="⚙️ Setup", description="Set join / leave message channel.", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
        embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
        return await ctx.send(embed=embed)

    @setup.command()
    @commands.has_permissions(manage_guild=True)
    @commands.guild_only()
    async def starboard(self, ctx, channel: discord.TextChannel = None):
        """CATEG_SUB """
        guild = ctx.message.guild
        guildstr = str(guild.id)

        if channel == None:
            embed=discord.Embed(title=":warning: {}".format(self.client.user.name), description="You didn't give me a channel, would you like me to make a new one?", color=0xffcd4c, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url,text="Reply with yes to continue.")
            await ctx.send(embed=embed)

            def check(m):
                return m.channel == ctx.channel and m.author == ctx.message.author

            msg = await self.client.wait_for('message', check=check)
            if msg.content == "yes" or msg.content == "y":
                await guild.create_text_channel(name="starboard")
                channel = discord.utils.get(guild.text_channels, name="starboard")
            else:
                embed = discord.Embed(title="⚙️ Setup", description="Cancelling...", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
                embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
                return await ctx.send(embed=embed)

            memberrole = discord.utils.get(guild.roles, name="Member")
            if memberrole is not None:
                await channel.set_permissions(target=memberrole, send_messages=False, read_messages=True, read_message_history=True, add_reactions=False)
            await channel.set_permissions(target=guild.default_role, send_messages=False, read_messages=True, read_message_history=True, add_reactions=False)

        if guildstr not in self.db:
            self.db[guildstr] = self.template
        self.db[guildstr]["STARBOARD"] = str(channel.id)

        fileIO(self.path, "save", self.db)
        embed = discord.Embed(title="⚙️ Setup", description="Set starboard channel.", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
        embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
        return await ctx.send(embed=embed)

#
#               COMMANDS BELOW ARE TAKEN STRAIGHT FROM YEETBOT WITH MINOR CHANGES
#               SOME THINGS MIGHT NOT BE FULLY FUNCTIONAL
#

    @setup.group()
    @commands.has_permissions(manage_guild=True)
    async def modlog(self, ctx):
        """CATEG_SUB """
        if ctx.invoked_subcommand == None:
            embed=discord.Embed(title="🔴 Error", description="You didn't provide a valid subcommand.\nAvailable options are: `channel` `messages` `disable`.", color=0xdd2e44)
            return await ctx.send(embed=embed)

    @modlog.command()
    @commands.has_permissions(manage_guild=True)
    async def disable(self, ctx):
        """CATEG_SUB """
        guild = ctx.message.guild
        
        if not str(guild.id) in self.db:
            embed=discord.Embed(title="🔴 Error", description="This server already has modlogs disabled.", color=0xdd2e44)
            await ctx.send(embed=embed)
            return
        elif str(guild.id) in self.db:
            self.db[str(guild.id)]["MODLOG"]["CHANNEL"] = None
            self.db[str(guild.id)]["MODLOG"]["MESSAGES"] = None
            fileIO(self.path, "save", self.db)
            embed=discord.Embed(title="🔵 {}".format(self.client.user.name), description="I will no longer send modlog notifications to this server.", color=client_role_color(self, ctx))
            await ctx.send(embed=embed)

    @modlog.command()
    @commands.has_permissions(manage_guild=True)
    async def channel(self, ctx, channel: discord.TextChannel = None):
        """CATEG_SUB """
        guild = ctx.message.guild
        channel = ctx.message.channel
        author = ctx.message.author
        

        if channel == None:
            embed=discord.Embed(title="🔵 {}".format(self.client.user.name), description="Where would you like me to send my modlogs?", color=client_role_color(self, ctx))
            embed.set_footer(text="Mention a channel to continue.")
            await ctx.send(embed=embed)

            def check(m):
                return m.channel == channel and m.author == author

            msg = await self.client.wait_for('message', check=check)
            if msg.channel_mentions:
                if len(msg.channel_mentions) > 1:
                    await ctx.send("You cannot provide more than one channel, try again.")
                    msg = await self.client.wait_for('message', check=check)
                    if not msg.channel_mentions or len(msg.channel_mentions) > 1:
                        await ctx.send("You failed a second time. Closing setup...")
                        return
                if len(msg.channel_mentions) == 1:
                    for TextChannel in msg.channel_mentions:
                        chn = discord.utils.get(guild.text_channels, name=TextChannel.name)
                    if guild.me.permissions_in(chn).send_messages and guild.me.permissions_in(chn).embed_links:
                        if str(guild.id) in self.db:
                            self.db[str(guild.id)]["MODLOG"]["CHANNEL"] = str(chn.id)
                            fileIO(self.path, "save", self.db)
                            embed=discord.Embed(title="🔵 {}".format(self.client.user.name), description="Channel changed to {}.".format(chn.mention), color=client_role_color(self, ctx))
                            await ctx.send(embed=embed)
                        elif str(guild.id) not in self.db or self.db[str(guild.id)]["MODLOG"] == None:
                            self.db[str(guild.id)] = self.template
                            self.db[str(guild.id)]["MODLOG"]["CHANNEL"] = str(chn.id)
                            self.db[str(guild.id)]["MODLOG"]["MESSAGES"] = str(chn.id)
                            fileIO(self.path, "save", self.db)
                            embed=discord.Embed(title="🔵 {}".format(self.client.user.name), description="I will now send modlog notifications in {}.".format(chn.mention), color=client_role_color(self, ctx))
                            await ctx.send(embed=embed)
            else:
                await ctx.send("No channel provided, cancelling...")

        else:
            if len(ctx.message.channel_mentions) == 1:
                for TextChannel in ctx.message.channel_mentions:
                    chn = discord.utils.get(guild.text_channels, name=TextChannel.name)
                if guild.me.permissions_in(chn).send_messages and guild.me.permissions_in(chn).embed_links:
                    if str(guild.id) in self.db:
                        self.db[str(guild.id)]["MODLOG"]["CHANNEL"] = str(chn.id)
                        fileIO(self.path, "save", self.db)
                        embed=discord.Embed(title="🔵 {}".format(self.client.user.name), description="Channel changed to {}.".format(chn.mention), color=client_role_color(self, ctx))
                        await ctx.send(embed=embed)
                    elif str(guild.id) not in self.db:
                        self.db[str(guild.id)] = self.template
                        self.db[str(guild.id)]["MODLOG"]["CHANNEL"] = str(chn.id)
                        fileIO(self.path, "save", self.db)
                        embed=discord.Embed(title="🔵 {}".format(self.client.user.name), description="I will now send modlog notifications in {}.".format(chn.mention), color=client_role_color(self, ctx))
                        await ctx.send(embed=embed)

    @modlog.command()
    @commands.has_permissions(manage_guild=True)
    async def messages(self, ctx):
        """CATEG_SUB """
        msg = "deleted and edited message logging"
        await modlog_toggle_messages(self, ctx, msg)

    @setup.command()
    @commands.has_permissions(manage_guild=True)
    async def trust(self, ctx, role: discord.Role = None):
        """CATEG_SUB """
        guild = ctx.guild
        guildstr = str(guild.id)
        if role == None:
            embed = discord.Embed(title="⚙️ Setup", description="You didn't give me a role! Please try again.", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            return await ctx.send(embed=embed)
        if role not in ctx.guild.roles:
            embed = discord.Embed(title="⚙️ Setup", description="I couldn't find that role.", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            return await ctx.send(embed=embed)

        if guildstr not in self.db:
            self.db[guildstr] = self.template
        self.db[guildstr]["TRUST"] = str(role.id)

        fileIO(self.path, "save", self.db)
        embed = discord.Embed(title="⚙️ Setup", description="Set `{}trust` role.".format(get_prefix(self, ctx)), color=client_role_color(self, ctx), timestamp=datetime.utcnow())
        embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
        return await ctx.send(embed=embed)

    @commands.command(name="trust", aliases=['verify'])
    @commands.guild_only()
    async def _trust(self, ctx, user: discord.Member = None):
        """CATEG_MOD """
        guildstr = str(ctx.guild.id)
        if user == None:
            embed = discord.Embed(title=":white_check_mark: Trust", description="You need to provide a user.", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            return await ctx.send(embed=embed)
        if user == ctx.message.author:
            embed = discord.Embed(title=":white_check_mark: Trust", description="You can't do that to yourself!", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            return await ctx.send(embed=embed)
        if guildstr not in self.db:
            embed = discord.Embed(title=":white_check_mark: Trust", description="This server didn't setup `trust`.", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            return await ctx.send(embed=embed)
        if self.db[guildstr]["TRUST"] == None:
            embed = discord.Embed(title=":white_check_mark: Trust", description="This server didn't setup `trust`.", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            return await ctx.send(embed=embed)

        role = discord.utils.get(ctx.guild.roles, id=int(self.db[guildstr]["TRUST"]))
        if role == None:
            embed = discord.Embed(title=":white_check_mark: Trust", description="There was a problem finding the trust role, if you're an admin please run `setup trust`.", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            return await ctx.send(embed=embed)
        
        await user.add_roles(role)
        embed = discord.Embed(title=":white_check_mark: Trust", description="{} is now verified!".format(user.mention), color=client_role_color(self, ctx), timestamp=datetime.utcnow())
        embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
        return await ctx.send(embed=embed)

    @setup.command()
    @commands.has_permissions(manage_guild=True)
    async def vip(self, ctx, role: discord.Role = None):
        """CATEG_SUB """
        guild = ctx.guild
        guildstr = str(guild.id)
        if role == None:
            embed = discord.Embed(title="⚙️ Setup", description="You didn't give me a role! Please try again.", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            return await ctx.send(embed=embed)
        if role not in ctx.guild.roles:
            embed = discord.Embed(title="⚙️ Setup", description="I couldn't find that role.", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            return await ctx.send(embed=embed)

        if guildstr not in self.db:
            self.db[guildstr] = self.template
        self.db[guildstr]["VIP"] = str(role.id)

        fileIO(self.path, "save", self.db)
        embed = discord.Embed(title="⚙️ Setup", description="Set `{}vip` role.".format(get_prefix(self, ctx)), color=client_role_color(self, ctx), timestamp=datetime.utcnow())
        embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
        return await ctx.send(embed=embed)

    @commands.command(name="vip")
    @commands.guild_only()
    async def _vip(self, ctx, user: discord.Member = None):
        """CATEG_MOD """
        guildstr = str(ctx.guild.id)
        if user == None:
            embed = discord.Embed(title=":white_check_mark: Trust", description="You need to provide a user.", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            return await ctx.send(embed=embed)
        if user == ctx.message.author:
            embed = discord.Embed(title=":white_check_mark: Trust", description="You can't do that to yourself!", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            return await ctx.send(embed=embed)
        if guildstr not in self.db:
            embed = discord.Embed(title=":white_check_mark: Trust", description="This server didn't setup `vip`.", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            return await ctx.send(embed=embed)
        if self.db[guildstr]["TRUST"] == None:
            embed = discord.Embed(title=":white_check_mark: Trust", description="This server didn't setup `vip`.", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            return await ctx.send(embed=embed)

        role = discord.utils.get(ctx.guild.roles, id=int(self.db[guildstr]["VIP"]))
        if role == None:
            embed = discord.Embed(title=":white_check_mark: Trust", description="There was a problem finding the VIP role, if you're an admin please run `setup trust`.", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            return await ctx.send(embed=embed)
        
        await user.add_roles(role)
        embed = discord.Embed(title=":white_check_mark: Trust", description="{} is now a VIP!".format(user.mention), color=client_role_color(self, ctx), timestamp=datetime.utcnow())
        embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
        return await ctx.send(embed=embed)

    @setup.command()
    async def colorroles(self, ctx):
        """CATEG_SUB """
        # :heart::yellow_heart::green_heart::blue_heart::purple_heart:
        red = discord.utils.get(ctx.guild.roles, name="Red", color=discord.Color.red())
        yellow = discord.utils.get(ctx.guild.roles, name="Yellow", color=discord.Color.gold())
        green = discord.utils.get(ctx.guild.roles, name="Green", color=discord.Color.green())
        blue = discord.utils.get(ctx.guild.roles, name="Blue", color=discord.Color.blue())
        purple = discord.utils.get(ctx.guild.roles, name="Purple", color=discord.Color.purple())

        if red == None:
            await ctx.guild.create_role(name="Red", color=discord.Color.red())
        if yellow == None:
            await ctx.guild.create_role(name="Yellow", color=discord.Color.gold())
        if green == None:
            await ctx.guild.create_role(name="Green", color=discord.Color.green())
        if blue == None:
            await ctx.guild.create_role(name="Blue", color=discord.Color.blue())
        if purple == None:
            await ctx.guild.create_role(name="Purple", color=discord.Color.purple())

        await ctx.send("Color roles created! Send `{}colorroles` in a channel to let members change their display color by reacting to a message. Also please remember to set up the role hierarchy in a way that makes the colors show up.".format(get_prefix(self, ctx)))

    @commands.command(name="colorroles")
    @commands.has_permissions(manage_messages=True)
    async def _colorroles(self, ctx):
        """CATEG_MOD allows members who react to the sent message to get a chosen color-role"""
        guildstr = str(ctx.guild.id)
        red = discord.utils.get(ctx.guild.roles, name="Red", color=discord.Color.red())
        yellow = discord.utils.get(ctx.guild.roles, name="Yellow", color=discord.Color.gold())
        green = discord.utils.get(ctx.guild.roles, name="Green", color=discord.Color.green())
        blue = discord.utils.get(ctx.guild.roles, name="Blue", color=discord.Color.blue())
        purple = discord.utils.get(ctx.guild.roles, name="Purple", color=discord.Color.purple())

        roles = []
        roles.append(red)
        roles.append(green)
        roles.append(yellow)
        roles.append(blue)
        roles.append(purple)
        for x in roles:
            if x == None:
                await ctx.send("This server hasn't set up color roles.")
                break
        
        embed = discord.Embed(title="Color roles (non-staff)", description="Add one of the following colored role to your current default role without affecting permissions.", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
        msg = await ctx.send(embed=embed)

        for x in self.coloremoji:
            await msg.add_reaction(x)

        await ctx.message.delete()

        if guildstr not in self.db:
            self.db[guildstr] = self.template
        self.db[guildstr]["COLORS"].append(str(msg.id))
        fileIO(self.path, "save", self.db)


        





#################################################################################
#################################### EVENTS #####################################
#################################################################################








#   starboard and colors
    @commands.Cog.listener()
    @commands.guild_only()
    async def on_reaction_add(self, reaction, user):
        message = reaction.message
        guild = message.guild
        guildstr = str(guild.id)
        if not str(guild.id) in self.db:
            return

        if reaction.emoji == "⭐":
            if self.db[str(guild.id)]["STARBOARD"] == None:
                return
            if reaction.me:
                return
            if reaction.count < 3:
                return
            
            channelid = self.db[str(guild.id)]["STARBOARD"]
            channel = guild.get_channel(int(channelid))

            try:
                msgcheck = await channel.fetch_message(message.id)
                if msgcheck != None:
                    return
                if msgcheck == None:
                    pass
            except discord.NotFound:
                pass

            embed = discord.Embed(title="New star! :star:", color=0xffcd4c, timestamp=datetime.utcnow())
            embed.add_field(name="Author", value=str(message.author))
            embed.add_field(name="Channel", value=message.channel.mention)
            embed.add_field(name="Message", value="[Jump]({})".format(message.jump_url))
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)

            if message.content != '' and message.content != None:
                content = message.content
                embed.add_field(name="Content", value=content, inline=False)

            if len(message.attachments) == 1:
                for x in message.attachments:
                    if x.filename.endswith(".png") or x.filename.endswith(".gif") or x.filename.endswith(".jpg") or x.filename.endswith(".jpeg"):
                        embed.set_image(url=x.url)

            await channel.send(embed=embed)
            pass

        elif reaction.emoji in self.coloremoji: #['❤️', '💛', '💚', '💙', '💜']

            if str(reaction.message.id) not in self.db[guildstr]["COLORS"]:
                return

            role = None

            if reaction.emoji == '💖':
                role = discord.utils.get(message.guild.roles, name="Red", color=discord.Color.red())
            if reaction.emoji == '💛':
                role = discord.utils.get(message.guild.roles, name="Yellow", color=discord.Color.gold())
            if reaction.emoji == '💚':
                role = discord.utils.get(message.guild.roles, name="Green", color=discord.Color.green())
            if reaction.emoji == '💙':
                role = discord.utils.get(message.guild.roles, name="Blue", color=discord.Color.blue())
            if reaction.emoji == '💜':
                role = discord.utils.get(message.guild.roles, name="Purple", color=discord.Color.purple())
    
            if role != None:
                if role not in user.roles:
                    await user.add_roles(role)

            pass

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_reaction_remove(self, reaction, user):
        message = reaction.message
        guild = message.guild
        guildstr = str(guild.id)
        if not str(guild.id) in self.db:
            return
        if reaction.emoji in self.coloremoji: #['❤️', '💛', '💚', '💙', '💜']

            if str(reaction.message.id) not in self.db[guildstr]["COLORS"]:
                return

            role = None

            if reaction.emoji == '❤️':
                role = discord.utils.get(message.guild.roles, name="Red", color=discord.Color.red())
            if reaction.emoji == '💛':
                role = discord.utils.get(message.guild.roles, name="Yellow", color=discord.Color.gold())
            if reaction.emoji == '💚':
                role = discord.utils.get(message.guild.roles, name="Green", color=discord.Color.green())
            if reaction.emoji == '💙':
                role = discord.utils.get(message.guild.roles, name="Blue", color=discord.Color.blue())
            if reaction.emoji == '💜':
                role = discord.utils.get(message.guild.roles, name="Purple", color=discord.Color.purple())
    
            if role != None:
                if role in user.roles:
                    await user.remove_roles(role)

            pass

#    message delete
    @commands.Cog.listener()
    @commands.guild_only()
    async def on_message_delete(self, message):
        guild = message.guild
        
        if not str(guild.id) in self.db:
            return
        if self.db[str(guild.id)]["MODLOG"]["MESSAGES"] == False:
            return
        if message.author.bot == True:
            return
            
        channelid = self.db[str(guild.id)]["MODLOG"]["CHANNEL"]
        channel = guild.get_channel(int(channelid))
        
        name = str(message.author)
        logmsg = ":warning: A message by {} was deleted in #{}".format(name, message.channel.name)

        if message.content == '':
            return
        elif message.content != '':
            before = message.content
        elif len(message.attachments) > 0:
            before = "The message contained only an attachment, but since that is now deleted I can't display it."
            embed = discord.Embed(title=logmsg, description=before, colour=0xffcd4c, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await channel.send(embed=embed)
            return

        for i in message.mentions:
            before = before.replace(i.mention, str(i))

        embed = discord.Embed(title=logmsg, colour=0xffcd4c, timestamp=datetime.utcnow())
        embed.add_field(name="Content:", value=before)
        embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
        await channel.send(embed=embed)
        pass

#    message edit
    @commands.Cog.listener()
    @commands.guild_only()
    async def on_message_edit(self, before, after):
        guild = before.guild
        
        try:
            if str(guild.id) not in self.db:
                return
            if self.db[str(guild.id)]["MODLOG"]["CHANNEL"] == None:
                return
        except AttributeError:
            return
        if self.db[str(guild.id)]["MODLOG"]["MESSAGES"] == False:
            return
        if before.content == after.content:
            return
        if before.author.bot == True:
            return
        if before.pinned != after.pinned:
            return
        
        for i in before.mentions:
            before.content = before.content.replace(i.mention, str(i))
        for i in after.mentions:
            after.content = after.content.replace(i.mention, str(i))

        channelid = self.db[str(guild.id)]["MODLOG"]["CHANNEL"]
        channel = guild.get_channel(int(channelid))
        
        
        name = str(before.author)
        logmsg = ":warning: A message by {} was edited in {}".format(name, before.channel.name)

        embed = discord.Embed(title=logmsg, colour=0xffcd4c, timestamp=datetime.utcnow())
        embed.add_field(name="Before edit:", value=before.content, inline=False)
        embed.add_field(name="After edit:", value=after.content, inline=False)
        embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
        await channel.send(embed=embed)
        pass

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_member_join(self, member):
        guild = member.guild
        guildstr = str(guild.id)
        name = str(member)

        if str(guild.id) not in self.db:
            return
        if self.db[str(guild.id)]["MODLOG"]["CHANNEL"] == None:
            return

        if self.db[guildstr]["JOINLEAVE"] != None:
            strwelcome = self.db[str(guild.id)]["JOINLEAVE"]
            welcome = guild.get_channel(int(strwelcome))
            logmsg = '**{}** has joined **{}**'.format(name, guild.name)
            embed = discord.Embed(title=":wave: Member Joined", description=logmsg, color=discord.Color.green(), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await welcome.send(embed=embed)

        if member != None:
            channelid = self.db[str(guild.id)]["MODLOG"]["CHANNEL"]
            channel = guild.get_channel(int(channelid))
            logmsg = '{} has joined {}'.format(name, guild.name)
            embed = discord.Embed(title=logmsg, color=discord.Color.green(), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await channel.send(embed=embed)
            
        pass

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_member_remove(self, member):
        guild = member.guild
        guildstr = str(guild.id)
        name = str(member)

        if str(guild.id) not in self.db:
            return
        if self.db[str(guild.id)]["MODLOG"]["CHANNEL"] == None:
            return
            
        if self.db[guildstr]["JOINLEAVE"] != None:
            strwelcome = self.db[str(guild.id)]["JOINLEAVE"]
            welcome = guild.get_channel(int(strwelcome))
            logmsg = '**{}** has left **{}**'.format(name, guild.name)
            embed = discord.Embed(title=":wave: Member Left", description=logmsg, color=discord.Color.red(), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await welcome.send(embed=embed)

        if member != None:
            channelid = self.db[str(guild.id)]["MODLOG"]["CHANNEL"]
            channel = guild.get_channel(int(channelid))
            logmsg = '{} has left {}'.format(name, guild.name)
            embed = discord.Embed(title=logmsg, color=discord.Color.green(), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await channel.send(embed=embed)
            
        pass

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_member_ban(self, guild, user):
        self.db = fileIO(self.path, 'load')
        if not str(guild.id) in self.db:
            return
        channelid = self.db[str(guild.id)]["MODLOG"]["CHANNEL"]
        channel = guild.get_channel(int(channelid))
        
        
        name = str(user)

        logmsg = '{} has been banned from the server'.format(name)
        embed = discord.Embed(title=logmsg, color=0xdd2e44, timestamp=datetime.utcnow())
        embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
        await channel.send(embed=embed)
        pass

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_member_unban(self, guild, user):
        self.db = fileIO(self.path, 'load')
        if not str(guild.id) in self.db:
            return
        channelid = self.db[str(guild.id)]["MODLOG"]["CHANNEL"]
        channel = guild.get_channel(int(channelid))
        
        
        name = str(user)

        logmsg = '{} has been unbanned'.format(name)
        embed = discord.Embed(title=logmsg, color=0xdd2e44, timestamp=datetime.utcnow())
        embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
        await channel.send(embed=embed)
        pass

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_guild_update(self, before, after):
        guild = before
        
        if str(guild.id) not in self.db:
            return
        if self.db[str(guild.id)]["MODLOG"]["CHANNEL"] == None:
            return

        channelid = self.db[str(guild.id)]["MODLOG"]["CHANNEL"]
        channel = guild.get_channel(int(channelid))
        
        

###################################################################

        if guild.region == discord.VoiceRegion.amsterdam:
            fancyregion = "🇳🇱 Amsterdam"
        elif guild.region == discord.VoiceRegion.brazil:
            fancyregion = "🇧🇷 Brazil"
        elif guild.region == discord.VoiceRegion.eu_central:
            fancyregion = "🇪🇺 Central Europe"
        elif guild.region == discord.VoiceRegion.eu_west:
            fancyregion = "🇪🇺 West Europe"
        elif guild.region == discord.VoiceRegion.frankfurt:
            fancyregion = "🇩🇪 Frankfurt"
        elif guild.region == discord.VoiceRegion.hongkong:
            fancyregion = "🇨🇳 Hong Kong"
        elif guild.region == discord.VoiceRegion.japan:
            fancyregion = "🇯🇵 Japan"
        elif guild.region == discord.VoiceRegion.london:
            fancyregion = "🇬🇧 London"
        elif guild.region == discord.VoiceRegion.russia:
            fancyregion = "🇷🇺 Russia"
        elif guild.region == discord.VoiceRegion.singapore:
            fancyregion = "🇸🇬 Singapore"
        elif guild.region == discord.VoiceRegion.southafrica:
            fancyregion = "🇿🇦 South Africa"
        elif guild.region == discord.VoiceRegion.sydney:
            fancyregion = "🇦🇺 Sydney"
        elif guild.region == discord.VoiceRegion.us_central:
            fancyregion = "🇺🇸 US Central"
        elif guild.region == discord.VoiceRegion.us_east:
            fancyregion = "🇺🇸 US East"
        elif guild.region == discord.VoiceRegion.us_south:
            fancyregion = "🇺🇸 US South"
        elif guild.region == discord.VoiceRegion.us_west:
            fancyregion = "🇺🇸 US West"
        elif guild.region == discord.VoiceRegion.vip_amsterdam:
            fancyregion = "🌟 VIP Amsterdam"
        elif guild.region == discord.VoiceRegion.vip_us_east:
            fancyregion = "🌟 VIP US East"
        elif guild.region == discord.VoiceRegion.vip_us_west:
            fancyregion = "🌟 VIP US West"

        if after.region == discord.VoiceRegion.amsterdam:
            fancyregion_a = "🇳🇱 Amsterdam"
        elif after.region == discord.VoiceRegion.brazil:
            fancyregion_a = "🇧🇷 Brazil"
        elif after.region == discord.VoiceRegion.eu_central:
            fancyregion_a = "🇪🇺 Central Europe"
        elif after.region == discord.VoiceRegion.eu_west:
            fancyregion_a = "🇪🇺 West Europe"
        elif after.region == discord.VoiceRegion.frankfurt:
            fancyregion_a = "🇩🇪 Frankfurt"
        elif after.region == discord.VoiceRegion.hongkong:
            fancyregion_a = "🇨🇳 Hong Kong"
        elif after.region == discord.VoiceRegion.japan:
            fancyregion_a = "🇯🇵 Japan"
        elif after.region == discord.VoiceRegion.london:
            fancyregion_a = "🇬🇧 London"
        elif after.region == discord.VoiceRegion.russia:
            fancyregion_a = "🇷🇺 Russia"
        elif after.region == discord.VoiceRegion.singapore:
            fancyregion_a = "🇸🇬 Singapore"
        elif after.region == discord.VoiceRegion.southafrica:
            fancyregion_a = "🇿🇦 South Africa"
        elif after.region == discord.VoiceRegion.sydney:
            fancyregion_a = "🇦🇺 Sydney"
        elif after.region == discord.VoiceRegion.us_central:
            fancyregion_a = "🇺🇸 US Central"
        elif after.region == discord.VoiceRegion.us_east:
            fancyregion_a = "🇺🇸 US East"
        elif after.region == discord.VoiceRegion.us_south:
            fancyregion_a = "🇺🇸 US South"
        elif after.region == discord.VoiceRegion.us_west:
            fancyregion_a = "🇺🇸 US West"
        elif after.region == discord.VoiceRegion.vip_amsterdam:
            fancyregion_a = "🌟 VIP Amsterdam"
        elif after.region == discord.VoiceRegion.vip_us_east:
            fancyregion_a = "🌟 VIP US East"
        elif after.region == discord.VoiceRegion.vip_us_west:
            fancyregion_a = "🌟 VIP US West"

        if before.default_notifications == discord.NotificationLevel.all_messages:
            notifbefore = "all messages"
        if after.default_notifications == discord.NotificationLevel.all_messages:
            notifafter = "all messages"
        if before.default_notifications == discord.NotificationLevel.only_mentions:
            notifbefore = "only mentions"
        if after.default_notifications == discord.NotificationLevel.only_mentions:
            notifafter = "only mentions"

        if before.explicit_content_filter == discord.ContentFilter.disabled:
            beforefilter = "disabled"
        if before.explicit_content_filter == discord.ContentFilter.no_role:
            beforefilter = "members without a role"
        if before.explicit_content_filter == discord.ContentFilter.all_members:
            beforefilter = "all members"
        if after.explicit_content_filter == discord.ContentFilter.disabled:
            afterfilter = "disabled"
        if after.explicit_content_filter == discord.ContentFilter.no_role:
            afterfilter = "members without a role"
        if after.explicit_content_filter == discord.ContentFilter.all_members:
            afterfilter = "all members"

        if before.verification_level == discord.VerificationLevel.none:
            beforeverif = "none"
        if before.verification_level == discord.VerificationLevel.low:
            beforeverif = "low"
        if before.verification_level == discord.VerificationLevel.medium:
            beforeverif = "medium"
        if before.verification_level == discord.VerificationLevel.high:
            beforeverif = "high"
        if before.verification_level == discord.VerificationLevel.extreme:
            beforeverif = "extreme"
        if after.verification_level == discord.VerificationLevel.none:
            afterverif = "none"
        if after.verification_level == discord.VerificationLevel.low:
            afterverif = "low"
        if after.verification_level == discord.VerificationLevel.medium:
            afterverif = "medium"
        if after.verification_level == discord.VerificationLevel.high:
            afterverif = "high"
        if after.verification_level == discord.VerificationLevel.extreme:
            afterverif = "extreme"

        timeout_b = before.afk_timeout / 60
        timeout_a = after.afk_timeout / 60

###################################################################

        #guild.region
        logmsg_region = "Server region has been changed from **{}** to **{}**.".format(fancyregion, fancyregion_a)
        #guild.name
        logmsg_name = "Server name has been changed from **{}** to **{}**.".format(before.name, after.name)
        #guild.afk_channel
        logmsg_afk = "Server AFK Channel has been changed from **{}** to **{}**.".format(str(before.afk_channel), str(after.afk_channel))
        #guild.afk_timeout
        logmsg_timeout = "Server AFK Timeout has been changed from **{}min** to **{}min**.".format(str(timeout_b), str(timeout_a))
        #guild.default_notifications
        logmsg_notif = "Server default notification setting has been changed from **{}** to **{}**.".format(notifbefore, notifafter)
        #guild.verification_level
        logmsg_veriflevel = "Server verification level has been changed from **{}** to **{}**.".format(beforeverif, afterverif)
        #guild.explicit_content_filter
        logmsg_filter = "Server explicit content filter setting has been changed from **{}** to **{}**.".format(beforefilter, afterfilter)
        #guild.mfa_level
        logmsg_mfa_true = "Server Two-Factor Authentication requirement has been **enabled**."
        logmsg_mfa_false = "Server Two-Factor Authentication requirement has been **disabled**."
        #guild.icon
        logmsg_icon = "Server icon has been changed."

###################################################################

        if before.region != after.region:
            embed = discord.Embed(title="🔴 Server settings have been changed", description=logmsg_region, color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await channel.send(embed=embed)
            pass
        if before.name != after.name:
            embed = discord.Embed(title="🔴 Server settings have been changed", description=logmsg_name, color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await channel.send(embed=embed)
            pass
        if before.afk_channel != after.afk_channel:
            embed = discord.Embed(title="🔴 Server settings have been changed", description=logmsg_afk, color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await channel.send(embed=embed)
            pass
        if before.afk_timeout != after.afk_timeout:
            embed = discord.Embed(title="🔴 Server settings have been changed", description=logmsg_timeout, color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await channel.send(embed=embed)
            pass
        if before.default_notifications != after.default_notifications:
            embed = discord.Embed(title="🔴 Server settings have been changed", description=logmsg_notif, color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await channel.send(embed=embed)
            pass
        if before.verification_level != after.verification_level:
            embed = discord.Embed(title="🔴 Server settings have been changed", description=logmsg_veriflevel, color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await channel.send(embed=embed)
            pass
        if before.explicit_content_filter != after.explicit_content_filter:
            embed = discord.Embed(title="🔴 Server settings have been changed", description=logmsg_filter, color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await channel.send(embed=embed)
            pass
        if before.mfa_level != after.mfa_level:
            if before.mfa_level == 0:
                logmsg_mfa = logmsg_mfa_true
            if before.mfa_level == 1:
                logmsg_mfa = logmsg_mfa_false
            embed = discord.Embed(title="🔴 Server settings have been changed", description=logmsg_mfa, color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await channel.send(embed=embed)
            pass
        if before.icon_url != after.icon_url:
            embed = discord.Embed(title="🔴 Server settings have been changed", description=logmsg_icon, color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await channel.send(embed=embed)
            pass
        pass

###################################################################


    @commands.Cog.listener()
    @commands.guild_only()
    async def on_guild_role_create(self, role):
        guild = role.guild
        
        if str(guild.id) not in self.db:
            return
        if self.db[str(guild.id)]["MODLOG"]["CHANNEL"] == None:
            return

        channelid = self.db[str(guild.id)]["MODLOG"]["CHANNEL"]
        channel = guild.get_channel(int(channelid))
        
        
        logmsg = 'A new role has been created'

        embed = discord.Embed(title=logmsg, color=0xdd2e44, timestamp=datetime.utcnow())
        embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_guild_role_delete(self, role):
        guild = role.guild
        
        if str(guild.id) not in self.db:
            return
        if self.db[str(guild.id)]["MODLOG"]["CHANNEL"] == None:
            return

        channelid = self.db[str(guild.id)]["MODLOG"]["CHANNEL"]
        channel = guild.get_channel(int(channelid))
        
        
        logmsg = 'The {} role has been deleted'.format(role.name)

        embed = discord.Embed(title=logmsg, color=0xdd2e44, timestamp=datetime.utcnow())
        embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
        await channel.send(embed=embed)

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_guild_role_update(self, before, after):
        #    things we check for: name, color, hoist, mentionable
        guild = before.guild
        
        if str(guild.id) not in self.db:
            return
        if self.db[str(guild.id)]["MODLOG"]["CHANNEL"] == None:
            return
        channelid = self.db[str(guild.id)]["MODLOG"]["CHANNEL"]
        channel = guild.get_channel(int(channelid))
        

        

        logmsg_name = "The **{}** role has been renamed to **{}**.".format(before.name, after.name)
        logmsg_color = "The **{}** has been recolored from `{}` to `{}`.".format(after.name, before.color, after.color)
        logmsg_hoist_on = "The **{}** role now shows members seperately from online members.".format(after.name)
        logmsg_hoist_off = "The **{}** role no longer shows members seperately from online members.".format(after.name)
        logmsg_mention_on = "The **{}** role can now be mentioned.".format(after.name)
        logmsg_mention_off = "The **{}** role can no longer be mentioned.".format(after.name)

        if after.hoist == False:
            logmsg_hoist = logmsg_hoist_off
        if after.hoist == True:
            logmsg_hoist = logmsg_hoist_on
        if after.mentionable == False:
            logmsg_mention = logmsg_mention_off
        if after.mentionable == True:
            logmsg_mention = logmsg_mention_on

        if before.name != after.name:
            embed = discord.Embed(title="🔴 A role has been updated", description=logmsg_name, color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await channel.send(embed=embed)
            pass
        if before.color != after.color:
            embed = discord.Embed(title="🔴 A role has been updated", description=logmsg_color, color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await channel.send(embed=embed)
            pass
        if before.hoist != after.hoist:
            embed = discord.Embed(title="🔴 A role has been updated", description=logmsg_hoist, color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await channel.send(embed=embed)
            pass
        if before.mentionable != after.mentionable:
            embed = discord.Embed(title="🔴 A role has been updated", description=logmsg_mention, color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await channel.send(embed=embed)
            pass

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_guild_channel_create(self, channel):
        #    channel = abc.GuildChannel
        guild = channel.guild
        
        if str(guild.id) not in self.db:
            return
        if self.db[str(guild.id)]["MODLOG"]["CHANNEL"] == None:
            return
        channelid = self.db[str(guild.id)]["MODLOG"]["CHANNEL"]
        send = guild.get_channel(int(channelid))
        
        

        if isinstance(channel, discord.TextChannel) == True:
            chntype = "text channel"
        elif isinstance(channel, discord.VoiceChannel) == True:
            #
            chntype = "voice channel"
        elif isinstance(channel, discord.CategoryChannel) == True:
            #
            chntype = "channel category"
        else:
            print("Error in modlog, on_guild_channel_create: channel type not determined")
            return

        logmsg = "A new {} called {} has been created".format(chntype, channel.name)

        embed = discord.Embed(title=logmsg, color=0xdd2e44, timestamp=datetime.utcnow())
        embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
        await send.send(embed=embed)

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_guild_channel_delete(self, channel):
        #    channel = abc.GuildChannel
        guild = channel.guild
        
        if str(guild.id) not in self.db:
            return
        if self.db[str(guild.id)]["MODLOG"]["CHANNEL"] == None:
            return
        channelid = self.db[str(guild.id)]["MODLOG"]["CHANNEL"]
        send = guild.get_channel(int(channelid))
        
        

        if isinstance(channel, discord.TextChannel) == True:
            chntype = "text channel"
        elif isinstance(channel, discord.VoiceChannel) == True:
            #
            chntype = "voice channel"
        elif isinstance(channel, discord.CategoryChannel) == True:
            #
            chntype = "channel category"
        else:
            print("Error in modlog, on_guild_channel_delete: channel type not determined")
            return

        logmsg = "A {} called {} has been deleted".format(chntype, channel.name)

        embed = discord.Embed(title=logmsg, color=0xdd2e44, timestamp=datetime.utcnow())
        embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
        await send.send(embed=embed)

    @commands.Cog.listener()
    @commands.guild_only()
    async def on_guild_channel_update(self, before, after):
        guild = before.guild
        
        if str(guild.id) not in self.db:
            return
        if self.db[str(guild.id)]["MODLOG"]["CHANNEL"] == None:
            return
        channelid = self.db[str(guild.id)]["MODLOG"]["CHANNEL"]
        channel = guild.get_channel(int(channelid))
        
        

        if isinstance(before, discord.TextChannel) == True:
            chntype = "text"
            cleantype = "text channel"
        elif isinstance(before, discord.VoiceChannel) == True:
            #
            chntype = "voice"
            cleantype = "voice channel"
        elif isinstance(before, discord.CategoryChannel) == True:
            #
            chntype = "categ"
            cleantype = "category"
        else:
            print("Error in modlog, on_guild_channel_delete: channel type not determined")
            return

        #    things we check for: name, category, topicTEXT, slowmode_delayTEXT, nsfw
        
        logmsg_name = "The **{}** {} has been renamed to **{}**.".format(before.name, cleantype, after.name)

        if before.name != after.name:
            embed = discord.Embed(title="🔴 A channel has been updated", description=logmsg_name, color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await channel.send(embed=embed)
            pass
        if chntype == "text":

            if before.category == None:
                bcategname = "None"
            else:
                bcategname = before.category.name
            if after.category == None:
                acategname = "None"
            else:
                acategname = after.category.name

            logmsg_category = "The **{}** {} has been moved from the **{}** category to the **{}** category.".format(after.name, cleantype, bcategname, acategname)
            logmsg_topic = "The topic of the **{}** {} has been updated.".format(after.name, cleantype)
            logmsg_slow = "The slowmode delay for the **{}** {} has been changed from **{}s** to **{}s**.".format(after.name, cleantype, before.slowmode_delay, after.slowmode_delay)
            logmsg_nsfw_off = "The **{}** {} is no longer marked NSFW.".format(after.name, cleantype)
            logmsg_nsfw_on = "The **{}** {} is now marked NSFW.".format(after.name, cleantype)

            if before.category != after.category:
                embed = discord.Embed(title="🔴 A channel has been updated", description=logmsg_category, color=0xdd2e44, timestamp=datetime.utcnow())
                embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
                await channel.send(embed=embed)
                pass
            if before.topic != after.topic:
                embed = discord.Embed(title="🔴 A channel has been updated", description=logmsg_topic, color=0xdd2e44, timestamp=datetime.utcnow())
                if before.topic != '':
                    embed.add_field(name="Before:", value=before.topic, inline=False)
                elif before.topic == '':
                    embed.add_field(name="Before:", value="No topic", inline=False)
                if after.topic != '':
                    embed.add_field(name="After:", value=after.topic, inline=False)
                elif after.topic == '':
                    embed.add_field(name="After:", value="No topic", inline=False)
                embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
                await channel.send(embed=embed)
                pass
            if before.slowmode_delay != after.slowmode_delay:
                embed = discord.Embed(title="🔴 A channel has been updated", description=logmsg_slow, color=0xdd2e44, timestamp=datetime.utcnow())
                embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
                await channel.send(embed=embed)
                pass
            if before.nsfw != after.nsfw:
                if after.nsfw == False:
                    logmsg_nsfw = logmsg_nsfw_off
                if after.nsfw == True:
                    logmsg_nsfw = logmsg_nsfw_on
                embed = discord.Embed(title="A channel has been updated", description=logmsg_nsfw, color=0xdd2e44, timestamp=datetime.utcnow())
                embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
                await channel.send(embed=embed)
                pass
        elif chntype == "voice":
            bitbefore = before.bitrate / 1000
            bitafter = after.bitrate / 1000
            logmsg_category = "The **{}** {} has been moved from the **{}** category to the **{}** category.".format(after.name, cleantype, before.category.name, after.category.name)
            logmsg_bit = "The bitrate of the **{}** channel has been changed from **{}kbps** to **{}kbps**.".format(after.name, bitbefore, bitafter)

            if before.category != after.category:
                embed = discord.Embed(title="A channel has been updated", description=logmsg_category, color=0xdd2e44, timestamp=datetime.utcnow())
                embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
                await channel.send(embed=embed)
                pass
            if before.bitrate != after.bitrate:
                embed = discord.Embed(title="A channel has been updated", description=logmsg_bit, color=0xdd2e44, timestamp=datetime.utcnow())
                embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
                await channel.send(embed=embed)
                pass
            if before.user_limit != after.user_limit:
                if before.user_limit == 0:
                    limit = "no limit"
                elif after.user_limit == 0:
                    limita = "no limit"
                if before.user_limit != 0:
                    limit = before.user_limit
                if after.user_limit != 0:
                    limita = after.user_limit

                logmsg_limit = "The user limit of the **{}** channel has been changed from **{}** to **{}** users.".format(after.name, limit, limita)
                embed = discord.Embed(title="A channel has been updated", description=logmsg_limit, color=0xdd2e44, timestamp=datetime.utcnow())
                embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
                await channel.send(embed=embed)
                pass

def setup(client):
    cogs.tools.jsoncheck()
    client.add_cog(Setup(client))