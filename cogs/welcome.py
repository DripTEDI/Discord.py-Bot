import discord
from discord.ext import commands
intents = discord.Intents.default()
import asyncio
import datetime
import sqlite3

class WelcomeCog(commands.Cog, name="welcome"):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id FROM main WHERE guild_id = {member.guild.id}")
        result = cursor.fetchone()
        if result is None:
            return
        else:
            cursor.execute(f"SELECT msg FROM main WHERE guild_id = {member.guild.id}")
            result1 = cursor.fetchone()
            members = len(list(member.guild.members))
            mention = member.mention
            user = member.name
            guild = member.guild
            embed = discord.Embed(colour=0xFF00FF, description=str(result1[0]).format(members=members, mention=mention, user=user, guild=guild))
            embed.set_thumbnail(url=member.avatar_url)
            embed.set_footer(text=member.name, icon_url=member.guild.icon_url)
            embed.timestamp = datetime.datetime.utcnow()

            channel = self.bot.get_channel(id=int(result[0]))

            await channel.send(embed=embed)
            await member.send(f'Benvenuto {member.name} in {member.guild.name}!')

    @commands.group(invoke_without_commands=True)
    async def welcome(self, ctx):
        embed = discord.Embed(title="Welcoming Message", description='**Available Setup Commands:** \n :one: welcome channel <#channel>\n :two: welcome text <message>.')
        await ctx.send(embed=embed)


    @welcome.command()
    async def channel(self, ctx, channel:discord.TextChannel):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT channel_id FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO main(guild_id, channel_id) VALUES(?, ?)")
                val = (ctx.guild.id, channel.id)
                await ctx.send(f'Channel has been set to {channel.mention}.')
            elif result is not None:
                sql = ("UPDATE main SET channel_id = ? WHERE guild_id = ?")
                val = (channel.id, ctx.guild.id)
                await ctx.send(f'Channel has been updated to **{channel.mention}**.')
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

    @welcome.command()
    async def text(self, ctx, *, text):
        if ctx.message.author.guild_permissions.manage_messages:
            db = sqlite3.connect('main.sqlite')
            cursor = db.cursor()
            cursor.execute(f"SELECT msg FROM main WHERE guild_id = {ctx.guild.id}")
            result = cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO main(guild_id, msg) VALUES(?,?)")
                val = (ctx.guild.id, text)
                await ctx.send(f"Message has been set to **{text}**")
            elif result is not None:
                sql = ("UPDATE main SET msg = ? WHERE guild_id = ?")
                val = (text, ctx.guild.id)
                await ctx.send(f"Message has been updated to **{text}**")
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            db.close()

def setup(bot):
    bot.add_cog(WelcomeCog(bot))
    print('Welcome loaded')