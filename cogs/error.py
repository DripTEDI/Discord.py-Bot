import discord
from discord import embeds
from discord.ext import commands
intents = discord.Intents.default()
import asyncio
import datetime

class ErrorCog(commands.Cog, name="error"):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        try:
            if hasattr(ctx.command, 'on_error'):
                return
            else:
                embed = discord.Embed(title=f"Error in {ctx.command}", description=f'`{ctx.command.qualified_name} {ctx.command.signature}`\n{error}', colour=0xFF00FF)
                await ctx.send(embed=embed)
        except:
            embed = discord.Embed(title=f"Error in {ctx.command}", description=f'{error}', colour=0xFF00FF)
            await ctx.send(embed=embed)


def setup(bot):
    bot.add_cog(ErrorCog(bot))
    print('Error loaded')