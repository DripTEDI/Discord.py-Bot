import discord
from discord.ext import commands
intents = discord.Intents.all()
import asyncio
import datetime
import traceback, sys
import sqlite3, os


f = open("regoleds.txt", "r")
rules = f.readlines()

bot = commands.Bot(command_prefix='!', case_insensitive=True, intents=intents)
bot.remove_command('help')

@bot.event
async def on_ready():
    print("I am online!")
    return await bot.change_presence(activity=discord.Activity(type=1, name='connecting...', url="http://207.180.214.184:5111/"))

initial_extensions = ['cogs.moderation', 
                        'cogs.welcome',
                        'cogs.levelling',
                        'cogs.error']

if __name__ == '__main__':
    for extension in initial_extensions:
        try:
            bot.load_extension(extension)
        except Exception as e:
            print(f"failed to load extension {extension}", file=sys.stderr)
            traceback.print_exc()

@bot.command()
async def ping(ctx):
    await ctx.send(f'Per risponderti ho impiegato: {round(bot.latency * 1000)}ms della mia inutile vita')

@bot.command(aliases=['regole'])
async def rule(ctx, *, number):
    await ctx.send(rules[int(number)-1])
    await ctx.send('visita <#760838028213092372> per le regole complete')

@bot.command(aliases=['i'])
async def info(ctx):
    embed = discord.Embed(title='**Informazioni**', description=f'{ctx.author.mention} ecco qui le cose che puoi fare con me!\n Il mio prefix è `!`\n:one:`!ping`\n:two: `!rule` + il numero(1-9)\n:three: `!rank` (senza altri argomenti restituisce il proprio **rank**\n\n**I comandi successivi neccessitano di permessi da modder/admin**\n\n:four: `!purge` + numero di messaggi che vuoi cancellare\n:five: `!kick` + utente\n:six: `!ban` +utente', colur=0xFF00FF)
    embed.set_thumbnail(url="https://media.giphy.com/media/NuJr20CtZERCrPjZDV/giphy.gif")
    embed.set_footer(icon_url = ctx.author.avatar_url, text=f'Richiesto da {ctx.author.name}.')
    embed.timestamp = datetime.datetime.utcnow()
    await ctx.send(embed=embed)



bot.run("BOT")