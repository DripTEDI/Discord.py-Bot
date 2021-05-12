import discord
from discord.ext import commands
intents = discord.Intents.default()
import asyncio
import datetime
import sqlite3
import math

class LvlCog(commands.Cog, name="levelling"):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id FROM levels WHERE guild_id = '{message.author.guild.id}' and user_id = '{message.author.id}'")
        result = cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO levels(guild_id, user_id, exp, lvl) VALUES(?,?,?,?)")
            val = (message.author.guild.id, message.author.id, 2, 0)
            cursor.execute(sql, val)
            db.commit()
        else:
            cursor.execute(f"SELECT user_id, exp, lvl FROM levels WHERE guild_id = '{message.author.guild.id}' and user_id = '{message.author.id}'")
            result1 = cursor.fetchone()
            exp = int(result1[1])
            sql = ("UPDATE levels SET exp = ? WHERE guild_id = ? AND user_id = ?")
            val = (exp+2, str(message.guild.id), str(message.author.id))
            cursor.execute(sql, val)
            db.commit()

            cursor.execute(f"SELECT user_id, exp, lvl FROM levels WHERE guild_id = '{message.author.guild.id}' and user_id = '{message.author.id}'")
            result2 = cursor.fetchone()

            xp_start = int(result2[1])
            lvl_start = int(result2[2])
            xp_end = math.floor(5 * (lvl_start ^ 2)+50 *lvl_start+100)
            if xp_end < xp_start:
                channel = self.bot.get_channel(id=799937314217525259)
                await channel.send(f'{message.author.mention} has leveled up to level {lvl_start+1}')
                sql = ("UPDATE levels SET lvl = ? WHERE guild_id = ? AND user_id = ?")
                val = (int(lvl_start+1), str(message.guild.id), str(message.author.id))
                cursor.execute(sql, val)
                db.commit()
                sql = ("UPDATE levels SET exp = ? WHERE guild_id = ? AND user_id = ?")
                val = (0, str(message.guild.id), str(message.author.id))
                cursor.execute(sql, val)
                db.commit()
                cursor.close()
                db.close()

    @commands.command()
    async def rank(self, ctx):
        db = sqlite3.connect('main.sqlite')
        cursor = db.cursor()
        cursor.execute(f"SELECT user_id, exp, lvl FROM levels WHERE guild_id = '{ctx.message.author.guild.id}' AND user_id = '{ctx.message.author.id}'")
        result = cursor.fetchone()
        if result is None:
            await ctx.send('That user in not yet ranked')
        else:
            xp = int(result[1])
            lvl = int(result[2])
            if lvl == 0:
                embed = discord.Embed(title="{}, ecco le tue stats!".format(ctx.author.name), colour=0xFF00FF)
                embed.add_field(name="Name", value=ctx.author.mention, inline=True)
                embed.add_field(name="XP", value=f"{xp}", inline=True)
                embed.add_field(name="LEVEL", value=f"{lvl}", inline=True)
                embed.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.channel.send(embed=embed)
            else:
                boxes = int((xp/(200*(1/2*lvl)))*10)
                embed = discord.Embed(title="{}, ecco le tue stats!".format(ctx.author.name), colour=0xFF00FF)
                embed.add_field(name="Name", value=ctx.author.mention, inline=True)
                embed.add_field(name="XP", value=f"{xp}", inline=True)
                embed.add_field(name="LEVEL", value=f"{lvl}", inline=True)
                embed.add_field(name="Progress Bar [lvl]", value=boxes * ":blue_square:" + (10-boxes) * ":white_large_square:", inline=True)
                embed.set_thumbnail(url=ctx.author.avatar_url)
                await ctx.channel.send(embed=embed)
        cursor.close()
        db.close()

def setup(bot):
    bot.add_cog(LvlCog(bot))
    print('Levelling loaded')