import discord
from discord.ext import commands
intents = discord.Intents.default()
import asyncio
import datetime

class ModCog(commands.Cog, name="moderation"):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def purge(self, ctx, *, number:int=None):
        if ctx.message.author.guild_permissions.manage_messages:
            try:
                if number is None:
                    await ctx.send("Inserisci un numero!")
                else:
                    deleted = await ctx.message.channel.purge(limit=number)
                    await ctx.send(f"Messaggi cancellati da {ctx.message.author.mention}: {len(deleted)}.")
            except:
                await ctx.send("Non lo posso fare.")
        else:
            await ctx.send("Non lo puoi fare.")

    @commands.command()
    async def kick(self, ctx, user:discord.Member, *, reason=None):
        if ctx.message.author.guild_permissions.kick_members:
            if reason is None:
                embed = discord.Embed(title=f'Membro Espulso', description=(f'{user.name} è stao espulso da {user.guild.name}!.'), colour=0xFF00FF)
                embed.set_thumbnail(url = user.avatar_url)
                embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Richiesto da {ctx.author.name}.")
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.guild.kick(user=user, reason='none')
                await ctx.send(embed=embed)
            else:
                embed= discord.Embed(title=f'Membro Espulso', description=f'{user.name} è stato espulso da {user.guild.name} perché {reason}!', colour=0xFF00FF)
                embed.set_thumbnail(url = user.avatar_url)
                embed.set_footer(icon_url = ctx.author.avatar_url, text=f'Richiesto da {ctx.author.name}.')
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.guild.kick(user=user, reason=reason)
                await ctx.send(embed=embed)
        else:
            await ctx.send("Non lo puoi fare.")

    @commands.command()
    async def ban(self, ctx, user:discord.Member, *, reason=None):
        if ctx.message.author.guild_permissions.ban_members:
            if reason is None:
                embed = discord.Embed(title=f'Membro Bannato', description=(f'{user.name} è stao bannato da {user.guild.name}!.'), colour=0xFF00FF)
                embed.set_thumbnail(url = user.avatar_url)
                embed.set_footer(icon_url = ctx.author.avatar_url, text = f"Richiesto da {ctx.author.name}.")
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.guild.ban(user=user, reason='none')
                await ctx.send(embed=embed)
            else:
                embed= discord.Embed(title=f'Membro Bannato', description=f'{user.name} è stato bannato da {user.guild.name} perché {reason}!', colour=0xFF00FF)
                embed.set_thumbnail(url = user.avatar_url)
                embed.set_footer(icon_url = ctx.author.avatar_url, text=f'Richiesto da {ctx.author.name}.')
                embed.timestamp = datetime.datetime.utcnow()
                await ctx.guild.ban(user=user, reason=reason)
                await ctx.send(embed=embed)
        else:
            await ctx.send("Non lo puoi fare.")

def setup(bot):
    bot.add_cog(ModCog(bot))
    print('Modaration loaded')