import discord
from discord.ext import commands
from datetime import datetime
from cogs.tools import client_role_color

class Mod(commands.Cog, name="mod"):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.guild_only()
    async def kick(self, ctx, user: discord.Member = None, *args):
        """Kicks someone from the server."""
        author = ctx.message.author
        channel = ctx.message.channel
        if author.guild_permissions.kick_members == False:
            embed=discord.Embed(title="🔴 Error", description="You do not have the necessary permissions.", color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
            return
        if user == author:
            embed=discord.Embed(title="🔴 Error", description="You cannot kick yourself.", color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
            return
        
        if user == self.client.user:
            embed=discord.Embed(title=":warning: {}".format(self.client.user.name), description="Are you sure you want me to leave this server?", color=0xffcd4c, timestamp=datetime.utcnow())
            selfkick = True
        else:
            userdm = user.dm_channel
            embed=discord.Embed(title=":warning: {}".format(self.client.user.name), description="Are you sure you want to kick {}?".format(user.mention), color=0xffcd4c, timestamp=datetime.utcnow())
            selfkick = False
        embed.set_footer(icon_url=self.client.user.avatar_url, text="Reply with yes to continue.")
        await ctx.send(embed=embed)

        def check(m):
            return m.channel == channel and m.author == author

        msg = await self.client.wait_for('message', check=check)
        if msg.content == "yes" or msg.content == "y":
            if selfkick == True:
                embed=discord.Embed(title="👢 Leaving...", description="Okay, see you later! :wave:", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
                embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
                await ctx.send(embed=embed)
                await msg.guild.leave()
                return
            else:

                reason = ' '.join(args)
                if reason == None or reason == "" or reason == " ":
                    reason = 'No reason provided | Kicked by {}.'.format(str(author))
                else:
                    reason = reason + " | Kicked by {}".format(str(author))

                try:
                    replyembed = discord.Embed(title=":warning: {}".format(self.client.user.name), description="You have been kicked from {} for: \n{}".format(msg.guild.name, reason), color=0xffcd4c, timestamp=datetime.utcnow())
                    replyembed.set_thumbnail(url=ctx.message.guild.icon_url)
                    replyembed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
                    if userdm == None:
                        await user.create_dm()
                        userdm = user.dm_channel
                        pass
                    await userdm.send(embed=replyembed)
                except discord.errors.Forbidden:
                    pass

                try:
                    await msg.guild.kick(user=user, reason=reason)
                    embed=discord.Embed(title="👢 Kick", description="Successfully kicked {}.".format(user.name), color=client_role_color(self, ctx), timestamp=datetime.utcnow())
                    embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
                    await ctx.send(embed=embed)

                except discord.errors.Forbidden:
                    embed=discord.Embed(title="🔴 Error", description="I need the ``Kick Members`` permission to do this.", color=0xdd2e44, timestamp=datetime.utcnow())
                    embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
                    await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="👢 Kick", description="Cancelling...", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def ban(self, ctx, user:discord.Member, *args):
        """Bans someone from the server."""
        author = ctx.message.author
        channel = ctx.message.channel

        if author.guild_permissions.ban_members == False:
            embed=discord.Embed(title="🔴 Error", description="You do not have the necessary permissions.", color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
            return
        if user == author:
            embed=discord.Embed(title="🔴 Error", description="You cannot ban yourself.", color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
            return

        elif user == self.client.user:
            embed=discord.Embed(title=":warning: {}".format(self.client.user.name), description="Are you sure you want me to leave this server?", color=0xffcd4c, timestamp=datetime.utcnow())
            selfkick = True
        else:
            userdm = user.dm_channel
            embed=discord.Embed(title=":warning: {}".format(self.client.user.name), description="Are you sure you want to ban {}?".format(user.mention), color=0xffcd4c, timestamp=datetime.utcnow())
            selfkick = False

        embed.set_footer(icon_url=self.client.user.avatar_url, text="Reply with yes to continue.")
        await ctx.send(embed=embed)

        def check(m):
            return m.channel == channel and m.author == author

        msg = await self.client.wait_for('message', check=check)
        if msg.content == "yes" or msg.content == "y":
            if selfkick == True:
                embed=discord.Embed(title="🔨 {}".format(self.client.user.name), description="Okay, see you later! :wave:", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
                embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
                await ctx.send(embed=embed)
                await msg.guild.leave()
                return
            else:
                reason = ' '.join(args)
                if reason == None or reason == "" or reason == " ":
                    reason = 'No reason provided | Banned by {}.'.format(str(author))
                else:
                    reason = reason + " | Banned by {}".format(str(author))

                try:
                    replyembed = discord.Embed(title=":warning: {}".format(self.client.user.name), description="You've been banned from {} for: \n{}".format(msg.guild.name, reason), color=0xffcd4c, timestamp=datetime.utcnow())
                    replyembed.set_thumbnail(url=ctx.message.guild.icon_url)
                    replyembed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
                    if userdm == None:
                        await user.create_dm()
                        userdm = user.dm_channel
                        pass
                    await userdm.send(embed=replyembed)
                except discord.errors.Forbidden:
                    pass

                try:
                    await msg.guild.ban(user=user, reason=reason)
                    embed=discord.Embed(title="🔨 Ban", description="Successfully banned {}.".format(user.name), color=client_role_color(self, ctx), timestamp=datetime.utcnow())
                    embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
                    await ctx.send(embed=embed)

                except discord.errors.Forbidden:
                    embed=discord.Embed(title="🔴 Error", description="I need the ``Ban Members`` permission to do this.", color=0xdd2e44, timestamp=datetime.utcnow())
                    embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
                    await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="🔨 Ban", description="Cancelling...", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)

    @commands.command(aliases=['hban'])
    @commands.guild_only()
    async def hackban(self, ctx, user_id: int):
        """Can ban someone even if they're not in the server."""
        author = ctx.message.author
        guild = author.guild

        reason = "Hackbanned by {}".format(str(author))

        if author.guild_permissions.ban_members == False:
            embed=discord.Embed(title="🔴 Error", description="You do not have the necessary permissions.", color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
            return

        ban_list = await guild.bans()
        for entry in ban_list:
            if entry.user.id == user_id:
                embed=discord.Embed(title="🔴 Error", description="That user is already banned.", color=0xdd2e44, timestamp=datetime.utcnow())
                embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
                await ctx.send(embed=embed)
                return

        user = guild.get_member(user_id)
        if user is not None:
            await ctx.invoke(self.ban, user=user, reason=reason)
            return

        try:
            await self.client.http.ban(user_id, guild.id, 0, reason=reason)
        except discord.NotFound:
            msg = "User not found. Have you provided the correct user ID?"
        except discord.Forbidden:
            msg = "I lack the permissions to do this."

        else:
            msg = "Done. That user will not be able to join this server."

        embed=discord.Embed(title="🔨 Hackban", description=msg, color=client_role_color(self, ctx), timestamp=datetime.utcnow())
        embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
        await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def embed(self, ctx, *args):
        """Sends your message in an embed."""
        author = ctx.message.author

        if author.guild_permissions.manage_messages == False:
            embed=discord.Embed(title="🔴 Error", description="You do not have the necessary permissions.", color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
            return

        mesg = ' '.join(args)
        user = ctx.message.author
        name = user.name
        embed=discord.Embed(description=mesg, colour=client_role_color(self, ctx), timestamp=datetime.utcnow())
        embed.set_author(name=name)
        embed.set_thumbnail(url=user.avatar_url)
        await ctx.send(embed=embed)

    @commands.command(aliases=['nuke'])
    @commands.guild_only()
    async def clear(self, ctx, amnt=10):
        """Deletes a set amount of messages"""
        author = ctx.message.author
        if author.guild_permissions.manage_messages == False:
            embed=discord.Embed(title="🔴 Error", description="You do not have the necessary permissions.", color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
            return

        await ctx.message.delete()
        messages = []
        async for message in ctx.channel.history(limit=int(amnt)):
            messages.append(message)
        if amnt > 100:
            embed=discord.Embed(title="🔴 Error", description="You cannot delete more than 100 messages at a time.", color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
        elif amnt == 0:
            embed=discord.Embed(title="🔴 Error", description="The limit cannot be 0.", color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
        else:
            try:
                await ctx.channel.delete_messages(messages)
                embed=discord.Embed(title="🗑️ Clear", description="Successfully deleted {} messages.".format(amnt), color=client_role_color(self, ctx), timestamp=datetime.utcnow())
                embed.set_footer(text="This message will be deleted in 5 seconds.")
                await ctx.send(embed=embed, delete_after=5.00)
            except:
                embed=discord.Embed(title="🔴 Error", description="Something went wrong, please check my permissions.", color=0xdd2e44, timestamp=datetime.utcnow())
                embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
                await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Mod(client))
