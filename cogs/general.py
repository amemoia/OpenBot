import discord
import math
from math import sqrt
from cogs.tools import client_role_color
from utils.dataIO import fileIO
from discord.ext import commands
from datetime import datetime

class General(commands.Cog, name='general'):
    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['profile'])
    async def userinfo(self, ctx, *, user: discord.Member = None):
        """CATEG_GEN Sends some information about a given user."""
        author = ctx.message.author
        guild = ctx.message.guild

        if not user:
            user = author

        try:
            dbs = fileIO("data/write/strikedata.json", "load")
        except FileNotFoundError:
            dbs = None
        try:
            dbm = fileIO("data/write/meritdata.json", "load")
        except FileNotFoundError:
            dbm = None

        roles = [x.name for x in user.roles if x.name != '@everyone']

        if not dbs:
            scount = 0
        elif not dbs[str(guild.id)]:
            scount = 0
        elif str(user.id) in dbs[str(guild.id)]:
            scount = len(dbs[str(guild.id)][str(user.id)])
        elif str(user.id) not in dbs[str(guild.id)] or str(guild.id) not in dbs:
            scount = 0

        if not dbm:
            mcount = 0
        elif not dbm[str(guild.id)]:
            mcount = 0
        elif str(user.id) in dbm[str(guild.id)]:
            mcount = len(dbm[str(guild.id)][str(user.id)])
        elif str(user.id) not in dbm[str(guild.id)] or str(guild.id) not in dbm:
            mcount = 0

        if scount == 0:
            sres = "None"
        else:
            sres = str(scount)
        if mcount == 0:
            mres = "None"
        else:
            mres = str(mcount)
            

        joined_at = user.joined_at
        since_created = (ctx.message.created_at - user.created_at).days
        since_joined = (ctx.message.created_at - joined_at).days
        user_joined = joined_at.strftime("%d %b %Y, %H:%M")
        user_created = user.created_at.strftime("%d %b %Y, %H:%M")

        created_on = "{} ({} days ago)".format(user_created, since_created)
        joined_on = "{} ({} days ago)".format(user_joined, since_joined)

        #    Bots cannot fetch profiles as of writing
        if 69 == 0:
            #nitro_since = "Not subscribed."
            badgelist = []
            profile = await user.profile()
            if profile.staff == True:
                badgelist.append("Staff")
            if profile.partner == True:
                badgelist.append("Discord Partner")
            if profile.nitro == True:
                badgelist.append("Nitro")
                #nitro_days = (ctx.message.created_at - profile.premium_since).days
                #nitro_since = "Since {}\n({} days ago)".format(profile.premium_since, nitro_days)
            if profile.bug_hunter == True:
                badgelist.append("Bug Hunter")
            if profile.early_supporter == True:
                badgelist.append("Early Supporter")
            if profile.hypesquad == True:
                house = ", ".join(profile.hypesquad_houses)
                badgelist.append(house)
            #badges = ", ".join(badgelist)

        if user.status == discord.Status.online:
            game = "Online"
        if user.status == discord.Status.offline:
            game = "Offline"
        if user.status == discord.Status.dnd:
            game = "Busy"
        if user.status == discord.Status.idle:
            game = "Idle"

        if user.activity != None:
            if user.activity.type.name == "playing":
                game = "Playing {}".format(user.activity.name)
            if user.activity.type.name == "streaming":
                game = "Streaming: [{}]({})".format(user.activity.name, user.activity.url)

        if roles:
            roles = sorted(roles, key=[x.name for x in guild.roles
                                   if x.name != "@everyone"].index, reverse=True)
            roles = ", ".join(roles)
        else:
            roles = "None"

        name = str(user)
        if user.nick:
            name = "{} ({})".format(str(user), user.nick)

        data = discord.Embed(title=name, description=game, colour=client_role_color(self, ctx))
        data.add_field(name="📅 Joined Discord on", value=created_on, inline=False)
        data.add_field(name="🗓️ Joined this server on", value=joined_on, inline=False)
        data.add_field(name="🔨 Strikes", value=sres, inline=False)
        data.add_field(name="🌟 Merits", value=mres, inline=False)
        data.add_field(name="💍 Married to", value="Marriage isn't implemented yet!", inline=False)
        data.add_field(name="🔧 Roles", value=roles, inline=False)
        data.set_footer(text="User ID: {}".format(user.id))

        if user.avatar_url:
            data.set_thumbnail(url=user.avatar_url)
        try:
            await ctx.send(embed=data)
        except discord.HTTPException:
            await ctx.send("I need the `Embed links` permission "
                               "to send this")

    @commands.command(aliases=['hinfo', 'hackinfo'])
    async def getuser(self, ctx, uid: int=0):
        """CATEG_GEN Finds info about a user based on their ID. Works on people that aren't in the current guild, but sends less info. The bot needs to share a guild with that user."""
        if uid == 0 or len(str(uid)) != 18:
            embed=discord.Embed(title="🔴 Error", description="Invalid ID.", color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
            return

        user = self.client.get_user(id=uid)
        if user == None:
            embed=discord.Embed(title="🔴 Error", description="I couldn't find that user. Please check if I share any servers with them.", color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
            return

        since_created = (ctx.message.created_at - user.created_at).days
        user_created = user.created_at.strftime("%d %b %Y, %H:%M")
        created_on = "{} ({} days ago)".format(user_created, since_created)

        data = discord.Embed(title=str(user), colour=client_role_color(self, ctx))
        data.add_field(name="📅 Joined Discord on", value=created_on, inline=False)
        data.add_field(name="🤖 Bot", value=str(user.bot), inline=False)
        data.add_field(name="💍 Married to", value="Marriage isn't implemented yet!", inline=False)
        data.add_field(name="#️⃣ User ID", value=str(user.id), inline=False)

        if user.avatar_url:
            data.set_thumbnail(url=user.avatar_url)
        try:
            await ctx.send(embed=data)
        except discord.HTTPException:
            await ctx.send("I need the `Embed links` permission to send this")

    @commands.command(aliases=['server', 'guild', 'guildinfo'])
    @commands.guild_only()
    async def serverinfo(self, ctx):
        """CATEG_GEN Returns information on the current server."""
        guild = ctx.message.guild
        text_channels = len([x for x in guild.text_channels])
        voice_channels = len([x for x in guild.voice_channels])
        passed = (ctx.message.created_at - guild.created_at).days
        created_at = ("Since {}. That's over {} days ago!"
                      "".format(guild.created_at.strftime("%d %b %Y %H:%M"),
                                passed))

        bot_count = 0
        for member in guild.members:
            if member.bot == True:
                bot_count = bot_count + 1
        total_users = len(guild.members) - bot_count
        boosters = len(guild.premium_subscribers)

        if boosters < 2:
            boost_level = 0
        if boosters >= 2 and boosters < 15:
            boost_level = 1
        if boosters >= 15 and boosters < 30:
            boost_level = 2
        if boosters >= 30:
            boost_level = 3

        if guild.region == discord.VoiceRegion.amsterdam:
            fancyregion = "🇳Amsterdam"
        elif guild.region == discord.VoiceRegion.brazil:
            fancyregion = "Brazil"
        elif guild.region == discord.VoiceRegion.eu_central:
            fancyregion = "Central Europe"
        elif guild.region == discord.VoiceRegion.eu_west:
            fancyregion = "West Europe"
        elif guild.region == discord.VoiceRegion.frankfurt:
            fancyregion = "Frankfurt"
        elif guild.region == discord.VoiceRegion.hongkong:
            fancyregion = "Hong Kong"
        elif guild.region == discord.VoiceRegion.japan:
            fancyregion = "Japan"
        elif guild.region == discord.VoiceRegion.london:
            fancyregion = "London"
        elif guild.region == discord.VoiceRegion.russia:
            fancyregion = "Russia"
        elif guild.region == discord.VoiceRegion.singapore:
            fancyregion = "Singapore"
        elif guild.region == discord.VoiceRegion.southafrica:
            fancyregion = "South Africa"
        elif guild.region == discord.VoiceRegion.sydney:
            fancyregion = "Sydney"
        elif guild.region == discord.VoiceRegion.us_central:
            fancyregion = "US Central"
        elif guild.region == discord.VoiceRegion.us_east:
            fancyregion = "US East"
        elif guild.region == discord.VoiceRegion.us_south:
            fancyregion = "US South"
        elif guild.region == discord.VoiceRegion.us_west:
            fancyregion = "US West"
        elif guild.region == discord.VoiceRegion.vip_amsterdam:
            fancyregion = "VIP Amsterdam"
        elif guild.region == discord.VoiceRegion.vip_us_east:
            fancyregion = "VIP US East"
        elif guild.region == discord.VoiceRegion.vip_us_west:
            fancyregion = "VIP US West"
        elif guild.region == "europe":
            fancyregion = "Europe"

        data = discord.Embed(title=guild.name, description=created_at, colour=client_role_color(self, ctx))
        data.add_field(name="🌍 Region", value=str(fancyregion), inline=False)
        data.add_field(name="👥 Members", value="{} members, {} bots".format(total_users, bot_count), inline=False)
        data.add_field(name="💬 Text Channels", value=text_channels, inline=False)
        data.add_field(name="🔊 Voice Channels", value=voice_channels, inline=False)
        data.add_field(name="💠 Boosting", value="Level {}, {} boosters".format(boost_level, boosters), inline=False)
        data.add_field(name="🔧 Roles", value=len(guild.roles), inline=False)
        data.add_field(name="👑 Owner", value=str(guild.owner), inline=False)
        data.set_footer(text="Server ID: " + str(guild.id))

        if guild.icon_url:
            data.set_thumbnail(url=guild.icon_url)

        try:
            await ctx.send(embed=data)
        except discord.HTTPException:
            await ctx.send("I need the `Embed links` permission to do this.")

    @commands.command(aliases=['hguild', 'hackguild'])
    async def getguild(self, ctx, uid: int = 0):
        """CATEG_GEN Returns information on a guild with the given ID. The bot has to be a member of the guild."""
        if uid == 0 or len(str(uid)) != 18:
            embed=discord.Embed(title="🔴 Error", description="Invalid ID.", color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
            return

        guild = self.client.get_guild(id=uid)
        if guild == None:
            embed=discord.Embed(title="🔴 Error", description="Couldn't find a guild. Please check if I'm in that server.", color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
            return
        text_channels = len([x for x in guild.text_channels])
        voice_channels = len([x for x in guild.voice_channels])
        passed = (ctx.message.created_at - guild.created_at).days
        created_at = ("Since {}. That's over {} days ago!"
                      "".format(guild.created_at.strftime("%d %b %Y %H:%M"),
                                passed))

        bot_count = 0
        for member in guild.members:
            if member.bot == True:
                bot_count = bot_count + 1
        total_users = len(guild.members) - bot_count
        boosters = len(guild.premium_subscribers)

        if boosters < 2:
            boost_level = 0
        if boosters >= 2 and boosters < 15:
            boost_level = 1
        if boosters >= 15 and boosters < 30:
            boost_level = 2
        if boosters >= 30:
            boost_level = 3

        if guild.region == discord.VoiceRegion.amsterdam:
            fancyregion = "🇳Amsterdam"
        elif guild.region == discord.VoiceRegion.brazil:
            fancyregion = "Brazil"
        elif guild.region == discord.VoiceRegion.eu_central:
            fancyregion = "Central Europe"
        elif guild.region == discord.VoiceRegion.eu_west:
            fancyregion = "West Europe"
        elif guild.region == discord.VoiceRegion.frankfurt:
            fancyregion = "Frankfurt"
        elif guild.region == discord.VoiceRegion.hongkong:
            fancyregion = "Hong Kong"
        elif guild.region == discord.VoiceRegion.japan:
            fancyregion = "Japan"
        elif guild.region == discord.VoiceRegion.london:
            fancyregion = "London"
        elif guild.region == discord.VoiceRegion.russia:
            fancyregion = "Russia"
        elif guild.region == discord.VoiceRegion.singapore:
            fancyregion = "Singapore"
        elif guild.region == discord.VoiceRegion.southafrica:
            fancyregion = "South Africa"
        elif guild.region == discord.VoiceRegion.sydney:
            fancyregion = "Sydney"
        elif guild.region == discord.VoiceRegion.us_central:
            fancyregion = "US Central"
        elif guild.region == discord.VoiceRegion.us_east:
            fancyregion = "US East"
        elif guild.region == discord.VoiceRegion.us_south:
            fancyregion = "US South"
        elif guild.region == discord.VoiceRegion.us_west:
            fancyregion = "US West"
        elif guild.region == discord.VoiceRegion.vip_amsterdam:
            fancyregion = "VIP Amsterdam"
        elif guild.region == discord.VoiceRegion.vip_us_east:
            fancyregion = "VIP US East"
        elif guild.region == discord.VoiceRegion.vip_us_west:
            fancyregion = "VIP US West"
        elif guild.region == "europe":
            fancyregion = "Europe"

        data = discord.Embed(title=guild.name, description=created_at, colour=client_role_color(self, ctx))
        data.add_field(name="🌍 Region", value=str(fancyregion), inline=False)
        data.add_field(name="👥 Members", value="{} members, {} bots".format(total_users, bot_count), inline=False)
        data.add_field(name="💬 Text Channels", value=text_channels, inline=False)
        data.add_field(name="🔊 Voice Channels", value=voice_channels, inline=False)
        data.add_field(name="💠 Boosting", value="Level {}, {} boosters".format(boost_level, boosters), inline=False)
        data.add_field(name="🔧 Roles", value=len(guild.roles), inline=False)
        data.add_field(name="👑 Owner", value=str(guild.owner), inline=False)
        data.set_footer(text="Server ID: " + str(guild.id))

        if guild.icon_url:
            data.set_thumbnail(url=guild.icon_url)

        try:
            await ctx.send(embed=data)
        except discord.HTTPException:
            await ctx.send("I need the `Embed links` permission to do this.")

    @commands.command()
    async def calc(self, ctx, *, maths):
        """CATEG_GEN Does the math for you"""
        equation = maths.strip().replace('^', '**').replace('x', '*')
        try:
            if '=' in equation:
                left = eval(equation.split('=')[0], {"__builtins__": None}, {"sqrt": sqrt})
                right = eval(equation.split('=')[1], {"__builtins__": None}, {"sqrt": sqrt})
                answer = str(left == right)
            else:
                answer = str(eval(equation, {"__builtins__": None}, {"sqrt": sqrt}))
        except TypeError:
            return await ctx.send("Invalid calculation query.")
        try: 
            em = discord.Embed(title='🧮 Calculator', color=client_role_color(self, ctx))
            em.add_field(name='Input:', value=maths.replace('**', '^').replace('x', '*'), inline=False)
            em.add_field(name='Output:', value=answer, inline=False)
            await ctx.send(embed=em)
        except discord.HTTPException:
            await ctx.send("I need the `Embed links` permission to do this.")

    @commands.command(aliases=['assign'], pass_context=True)
    @commands.guild_only()
    async def role(self, ctx, *, role: discord.Role = None):
        """CATEG_GEN Assigns you a role that is below your highest one."""
        user = ctx.message.author
        if role is None:
            embed=discord.Embed(title="🔴 Error", description="You haven't specified a role!", color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
        if role not in ctx.message.guild.roles:
            embed=discord.Embed(title="🔴 Error", description="That role doesn't exist.", color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
        if role.position < user.top_role.position:
            if role not in ctx.message.author.roles:
                await user.add_roles(role, reason='Role add requested by {}'.format(str(user)))
                embed=discord.Embed(title="✅ Role", description="``{}`` has been added to {}.".format(role, user.mention), color=client_role_color(self, ctx), timestamp=datetime.utcnow())
                embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
                await ctx.send(embed=embed)
            elif role in ctx.message.author.roles:
                await user.remove_roles(role, reason='Role removal requested by {}'.format(str(user)))
                embed=discord.Embed(title="✅ Role", description="``{}`` has been removed from {}.".format(role, user.mention), color=client_role_color(self, ctx), timestamp=datetime.utcnow())
                embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
                await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="🔴 Error", description="That role is higher than your top role.", color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)

    @commands.command(aliases=['pfp', 'icon'])
    async def avatar(self, ctx, user: discord.User = None):
        """CATEG_GEN Returns a user's avatar."""
        if not user:
            user = ctx.message.author
        icon = user.avatar_url
        embed=discord.Embed(title="🖼️ Here's **{}'s** avatar.".format(user), color=client_role_color(self, ctx), timestamp=datetime.utcnow())
        embed.set_image(url=str(icon))
        embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
        await ctx.send(embed=embed)

    @commands.command(aliases=['guildicon'])
    @commands.guild_only()
    async def servericon(self, ctx):
        """CATEG_GEN Returns the server's icon."""
        user = ctx.message.guild
        icon = user.icon_url
        if icon._url == None:
            embed=discord.Embed(title="🔴 Error", description="**{}** has no icon.".format(user), colour=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            embed.set_image(url=str(icon))
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="🖼️ Here's **{}'s** icon.".format(user), color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_image(url=str(icon))
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def banner(self, ctx):
        """CATEG_GEN Returns the server's banner."""
        user = ctx.message.guild
        icon = user.banner_url
        if icon._url == None:
            embed=discord.Embed(title="🔴 Error", description="**{}** has no banner.".format(user), colour=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            embed.set_image(url=str(icon))
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="🖼️ Here's **{}'s** banner.".format(user), color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_image(url=str(icon))
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)

    @commands.command()
    @commands.guild_only()
    async def splash(self, ctx):
        """CATEG_GEN Returns the server's invite splash."""
        user = ctx.message.guild
        icon = user.splash_url
        if icon._url == None:
            embed=discord.Embed(title="🔴 Error", description="**{}** has no invite splash.".format(user), colour=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            embed.set_image(url=str(icon))
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="🖼️ Here's **{}'s** invite splash.".format(user), color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_image(url=str(icon))
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(General(client))