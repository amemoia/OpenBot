import discord
import random
import json
from discord.ext import commands
from datetime import datetime
from cogs.tools import client_role_color
from utils.dataIO import fileIO


class Fun(commands.Cog, name="fun"):
    def __init__ (self, client):
        self.client = client

    @commands.command()
    async def kill(self, ctx, user: discord.Member = None):
        """CATEG_FUN Murder someone."""
        author = ctx.message.author
        if user == None:
            user = ctx.message.author

        kills = []
        kills.append('{killer} shoves a double barreled shotgun into {user}\'s mouth and squeezes the trigger of the gun, causing {user}\'s head to horrifically explode like a ripe pimple, splattering the young person\'s brain matter, gore, and bone fragments all over the walls and painting it a crimson red.')
        kills.append('Screaming in sheer terror and agony, {user} is horrifically dragged into the darkness by unseen forces, leaving nothing but bloody fingernails and a trail of scratch marks in the ground from which the young person had attempted to halt the dragging process.')
        kills.append('{killer} takes a machette and starts hacking away on {user}, chopping {user} into dozens of pieces.')
        kills.append('{killer} pours acid over {user}. *"Well don\'t you look pretty right now?"*')
        kills.append('{user} screams in terror as a giant creature with huge muscular arms grab {user}\'s head; {user}\'s screams of terror are cut off as the creature tears off the head with a sickening crunching sound. {user}\'s spinal cord, which is still attached to the dismembered head, is used by the creature as a makeshift sword to slice a perfect asymmetrical line down {user}\'s body, causing the organs to spill out as the two halves fall to their respective sides.')
        kills.append('{killer} grabs {user}\'s head and tears it off with superhuman speed and efficiency. Using {user}\'s head as a makeshift basketball, {killer} expertly slams dunk it into the basketball hoop, much to the applause of the audience watching the gruesome scene.')
        kills.append('{killer} uses a shiv to horrifically stab {user} multiple times in the chest and throat, causing {user} to gurgle up blood as the young person horrifically dies.')
        kills.append('{user} screams as {killer} lifts {user} up using his superhuman strength. Before {user} can even utter a scream of terror, {killer} uses his superhuman strength to horrifically tear {user} into two halves; {user} stares at the monstrosity in shock and disbelief as {user} gurgles up blood, the upper body organs spilling out of the dismembered torso, before the eyes roll backward into the skull.')
        kills.append('{user} steps on a land mine and is horrifically blown to multiple pieces as the device explodes, the {user}\'s entrails and gore flying up and splattering all around as if someone had thrown a watermelon onto the ground from the top of a multiple story building.')
        kills.append('{user} is killed instantly as the top half of his head is blown off by a Red Army sniper armed with a Mosin Nagant, {user}\'s brains splattering everywhere in a horrific fashion.')

        if user == author:
            embed=discord.Embed(title="💀 Kill", description="I won't let you kill yourself!", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            return await ctx.send(embed=embed)
        elif user.id == self.client.user.id:
            embed=discord.Embed(title="💀 Kill", description="I refuse to kill myself!", color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            return await ctx.send(embed=embed)
        else:
            message = str(random.choice(kills)).format(user=user.display_name, killer=author.display_name)
            embed=discord.Embed(title="💀 Kill", description=message, color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            return await ctx.send(embed=embed)
    
    @commands.command()
    async def insult(self, ctx, user: discord.Member = None):
        """CATEG_FUN Insult someone."""
        if user == None:
            user = ctx.message.author
        insults = fileIO("data/read/insults.json", "load")

        if user.id == self.client.user.id:
            user = ctx.message.author
            msg = "How original. No one else had thought of trying to get the bot to insult itself. I applaud your creativity. Yawn. Perhaps this is why you don't have friends. You don't add anything new to any conversation. You are more of a bot than me, predictable answers, and absolutely dull to have an actual conversation with."
            embed=discord.Embed(title="😡 Insult", description=msg, color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            return await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="😡 Insult", description=user.mention + " " + random.choice(insults), color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            return await ctx.send(embed=embed)

    @commands.command(aliases=['cuddle'])
    async def hug(self, ctx, user: discord.Member=None):
        """CATEG_FUN Free hugs!"""
        author = ctx.message.author

        choices = fileIO("data/read/links.json", "load")
        image = random.choice(choices["hug"])

        def msg():
            if user == None:
                return None
            if user != None:
                return "{} hugged {}!".format(author, user)
        
        embed = discord.Embed(title="🤗 Hug", description=msg(), colour=client_role_color(self, ctx))
        embed.set_image(url=image)

        return await ctx.send(embed=embed) 

    @commands.command(aliases=['8ball'])
    async def ask8(self, ctx):
        """CATEG_FUN Ask the almighty 8ball a question."""
        response=(random.choice(["It is certain.",
                                "It is decidedly so.",
                                "Without a doubt.",
                                "Yes, definitely.",
                                "You may rely on it.",
                                "As I see it, yes.",
                                "Most likely.",
                                "Outlook good.",
                                "Yes.",
                                "Signs point to yes.",
                                "Don't count on it.",
                                "My reply is no.",
                                "My sources say no.",
                                "Outlook not so good.",
                                "Very doubtful."]))
        embed=discord.Embed(title="🎱 8ball", description=response, color=client_role_color(self, ctx), timestamp=datetime.utcnow())
        embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
        await ctx.send(embed=embed)

    @commands.command()
    async def roll(self, ctx, number : int = 20):
        """CATEG_FUN Roll some dice."""
        author = ctx.message.author
        if number > 1:
            n = random.randint(1, number)
            embed=discord.Embed(title="🎲 Roll", description="{}".format(n), color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="🎲 Roll", description="{} Maybe higher than 1?".format(author.mention), color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)

    @commands.command(aliases=['pick'])
    async def choose(self, ctx, *choices: str):
        """CATEG_FUN Chooses between given options at random."""
        if len(choices) < 2:
            embed=discord.Embed(title="🔴 Error", description='Not enough choices to pick from.', color=0xdd2e44, timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)
        else:
            embed=discord.Embed(title="🔮 Choose", description="I'd pick {}.".format(random.choice(choices)), color=client_role_color(self, ctx), timestamp=datetime.utcnow())
            embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
            await ctx.send(embed=embed)

    @commands.command(aliases=['coinflip'])
    async def flip(self, ctx):
        """CATEG_FUN Flip a coin."""
        embed=discord.Embed(title="📀 Coinflip", description=random.choice(["Heads!", "Tails!"]), color=client_role_color(self, ctx), timestamp=datetime.utcnow())
        embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
        await ctx.send(embed=embed)

    @commands.command()
    async def rapname(self, ctx, user: discord.Member=None):
        """CATEG_FUN Start off your Soundcloud career with a cool nickname."""
        if user == None:
            user = ctx.message.author

        with open("data/read/rap_first.json") as json.file:
            rap1 = json.load(json.file)
        with open("data/read/rap_last.json") as json.file:
            rap2 = json.load(json.file)

        result = random.choice(rap1) + " " + random.choice(rap2)
        embed=discord.Embed(title="🎤 Rapname", description="{}'s rap name is: **{}**".format(user.mention, result), color=client_role_color(self, ctx), timestamp=datetime.utcnow())
        embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
        await ctx.send(embed=embed)

    @commands.command()
    async def gay(self, ctx, user: discord.Member=None):
        """CATEG_FUN Measures how gay you are."""
        if not user:
            user = ctx.message.author

        value = int(100)
        n = random.randint(1, value)

        #    Check if user is bot
        if user.id == self.client.user.id:
            n = int(100)
        #    Check if user is owner
        elif user.id == 254204775497859073:
            n = int(0)

        embed=discord.Embed(title="🏳️‍🌈 Gay", description="{} is **{}% gay.**".format(user, n), color=client_role_color(self, ctx), timestamp=datetime.utcnow())
        embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
        await ctx.send(embed=embed)

    @commands.command(aliases=['dick', 'dong'])
    async def penis(self, ctx, user: discord.Member=None):
        """CATEG_FUN Measures your dick size. 100% accurate"""
        if not user:
            user = ctx.message.author

        msg = ""
        state = random.getstate()

        if user.id == 254204775497859073:
            dong = "8{}D".format("=" * 30)
        elif user.id == self.client.user.id:
            dong = "8{}D".format("=")
        else:
            random.seed(user.id)
            dong = "8{}D".format("=" * random.randint(0, 30))

        random.setstate(state)
        msg = "**{}'s size:**\n{}\n".format(user.display_name, dong)
        await ctx.send(msg)

    @commands.command(aliases=['f'])
    async def payrespects(self, ctx):
        """CATEG_FUN Send `=f` to pay respects"""
        db = fileIO("data/write/payrespects.json", "load")
        db[str(ctx.message.id)] = datetime.today().strftime('%Y-%m-%d') 
        fileIO("data/write/payrespects.json", "save", db)

        dbtoday = []
        for entry in db:
            if db[entry] == datetime.today().strftime('%Y-%m-%d'):
                dbtoday.append(entry)
        TodayLen = len(dbtoday)
        TotalLen = len(db)

        embed=discord.Embed(title="{} has paid their respects".format(ctx.message.author.name), description="{} Today, {} Total".format(TodayLen, TotalLen), color=client_role_color(self, ctx), timestamp=datetime.utcnow())
        embed.set_footer(icon_url=self.client.user.avatar_url, text=self.client.user.name)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Fun(client))