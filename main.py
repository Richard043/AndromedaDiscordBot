import discord
import random
import os
import asyncio
import math
import aiosqlite
import json
import aiofiles
import requests
import googletrans
from googletrans import Translator
from discord.embeds import Embed
from discord.ext import commands
from random import randint
from discord import utils
import aiohttp
import datetime
from utils import fetch
from random import choice
from keep_alive import keep_alive
import music
import animec


async def get_random_gif_by_theme(theme: str):
    async with aiohttp.ClientSession() as session:
        response = await fetch(
            session,
            f"https://api.tenor.com/v1/random?q={theme.replace(' ', '+')}&contentfilter=medium"
        )
        await session.close()
        return response["results"][random.randint(0,
                                                  len(response["results"]) -
                                                  1)]["media"][0]["gif"]["url"]


async def get_random_meme_pic():
    async with aiohttp.ClientSession() as session:
        response = await fetch(session, "https://some-random-api.ml/meme")
        await session.close()
        return response["image"]


async def get_random_joke_text():
    async with aiohttp.ClientSession() as session:
        response = await fetch(
            session, "https://official-joke-api.appspot.com/random_joke")
        await session.close()
        return response["setup"], response["punchline"]


async def get_random_anime_quote():
    async with aiohttp.ClientSession() as session:
        response = await fetch(session,
                               "https://animechan.vercel.app/api/random")
        await session.close()
        return response["quote"], response["character"], response["anime"]


async def get_random_movie_quote():
    async with aiohttp.ClientSession() as session:
        response = await fetch(
            session, "https://movie-quote-api.herokuapp.com/v1/quote/")
        await session.close()
        return response["quote"], response["role"], response["show"]


async def get_random_bad_quote():
    async with aiohttp.ClientSession() as session:
        response = await fetch(
            session, "https://breaking-bad-quotes.herokuapp.com/v1/quotes")
        await session.close()
        return response["quote"], response["author"]


async def get_link_from_API(api):
    async with aiohttp.ClientSession() as session:
        response = await fetch(session, api)
        await session.close()
        return response["link"]


client = commands.Bot(command_prefix=['a!', 'A!'],
                      intents=discord.Intents.all())
client.remove_command("help")
client.ticket_configs = {}

cogs = [music]

for i in range(len(cogs)):
    cogs[i].setup(client)


@client.group(invoke_without_command=True)
async def help(ctx):
    em = discord.Embed(
        title="Help",
        description=
        "Use `prefix` help <command> for extended information on a command.",
        color=ctx.author.color)

    em.add_field(name="Mods", value="purge, kick, ban, unban, poll, WH")
    em.add_field(name="Funs",
                 value="YRN, CF, TOD, truth, dare, TOT, dice, RPS")
    em.add_field(name="Tic Tac Toe", value="TTT, place")
    em.add_field(name="Not So Fun", value="bully, bite, slap, kill")
    em.add_field(name="Socials", value="smug, blush, ship, FR, rate")
    em.add_field(name="Wholesome", value="wink, cuddle, pat, hug, kiss, lick")
    em.add_field(name="Randoms", value="meme, PF, cat, dog, waifu, NSFW")
    em.add_field(name="Anime", value="anime, character, aninews")
    em.add_field(name="Texts", value="AQ, MQ, BQ, advice, yomomma, insult")
    em.add_field(name="Music", value="Join, DC, play, pause, resume")
    em.add_field(name="Counts", value="timer, roll, calc")
    em.add_field(
        name="Specials",
        value="t, dex, movesets, stats, TS, MT, ML, RAG, translate, schedule")
    em.add_field(name="Infos", value="avatar, ping, help")
    em.add_field(name="Developments", value="BI")

    await ctx.send(embed=em)


@help.command()
async def purge(ctx):

    em = discord.Embed(title="Purge",
                       description="Purge messages from a channel!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!purge <amount>")

    await ctx.send(embed=em)


@help.command()
async def kick(ctx):

    em = discord.Embed(title="Kick",
                       description="Kicks a member from the server!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!kick <member> [reason]")

    await ctx.send(embed=em)


@help.command()
async def ban(ctx):

    em = discord.Embed(title="Ban",
                       description="Bans a member from the server!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!ban <member> [reason]")

    await ctx.send(embed=em)


@help.command()
async def unban(ctx):

    em = discord.Embed(title="Unban",
                       description="Unbans a member from the server!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!unban <name#numbers>")

    await ctx.send(embed=em)


@help.command()
async def timer(ctx):

    em = discord.Embed(title="Timer",
                       description="Starts a timer in seconds.",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!cdn <time ammount in seconds>")

    await ctx.send(embed=em)


@help.command()
async def t(ctx):

    em = discord.Embed(title="60sec Timer",
                       description="Starts a 60 seconds timer.",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!t")

    await ctx.send(embed=em)


@help.command()
async def YRN(ctx):

    em = discord.Embed(title="8ball",
                       description="Plays 8ball!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!8ball <questions>")

    await ctx.send(embed=em)


@help.command()
async def CF(ctx):

    em = discord.Embed(title="Coinflip",
                       description="Plays coinflip, shows head or tail!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!cf")

    await ctx.send(embed=em)


@help.command()
async def TOD(ctx):

    em = discord.Embed(
        title="Truth or Dare!",
        description="Gives a random truth or dare questions! :eyes:",
        color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!tod")

    await ctx.send(embed=em)


@help.command()
async def TOT(ctx):

    em = discord.Embed(title="This or That!",
                       description="Gives a random options to choose!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!tot")

    await ctx.send(embed=em)


@help.command()
async def truth(ctx):

    em = discord.Embed(title="Truths!",
                       description="Gives a random truth questions! :eyes:",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!truth")

    await ctx.send(embed=em)


@help.command()
async def dare(ctx):

    em = discord.Embed(title="Dares!",
                       description="Gives a random dare challenges! :eyes:",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!dare")

    await ctx.send(embed=em)


@help.command()
async def RAG(ctx):

    em = discord.Embed(title="Random Alphabet Generator!",
                       description="Generates a random alphabet of A-Z!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!rag")

    await ctx.send(embed=em)


@help.command()
async def dice(ctx):

    em = discord.Embed(title="Dice",
                       description="Rolls the dice!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!dice")

    await ctx.send(embed=em)


@help.command()
async def roll(ctx):

    em = discord.Embed(title="Rolls",
                       description="Rolls a number from the max value!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!roll <max value>")

    await ctx.send(embed=em)


@help.command()
async def AQ(ctx):

    em = discord.Embed(title="Anime Quotes",
                       description="Shows a random anime quotes!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!aq")

    await ctx.send(embed=em)


@help.command()
async def MQ(ctx):

    em = discord.Embed(title="Movie Quotes",
                       description="Shows a random movie quotes!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!mq")

    await ctx.send(embed=em)


@help.command()
async def BQ(ctx):

    em = discord.Embed(title="Bad Quotes",
                       description="Shows a random bad quotes!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!bq")

    await ctx.send(embed=em)


@help.command()
async def advice(ctx):

    em = discord.Embed(title="Advices",
                       description="Shows a random advice!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!advice")

    await ctx.send(embed=em)


@help.command()
async def insult(ctx):

    em = discord.Embed(title="Insults",
                       description="Shows a random insults!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!insult")

    await ctx.send(embed=em)


@help.command()
async def yomomma(ctx):

    em = discord.Embed(title="Yo Momma",
                       description="Shows a random yo momma joke!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!yomomma")

    await ctx.send(embed=em)


@help.command()
async def waifu(ctx):

    em = discord.Embed(title="Waifus",
                       description="Shows a random waifu!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!waifu")

    await ctx.send(embed=em)


@help.command()
async def NSFW(ctx):

    em = discord.Embed(title="NSFW!",
                       description="Shows a random NSFW Stuffs... 😏",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!nsfw")

    await ctx.send(embed=em)


@help.command()
async def poll(ctx):

    em = discord.Embed(title="Polls",
                       description="Send a poll to ask for opinions!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!poll <polls>")

    await ctx.send(embed=em)


@help.command()
async def WH(ctx):

    em = discord.Embed(title="Webhooks!",
                       description="Send a message as a webhooks!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!wh <texts>")

    await ctx.send(embed=em)


@help.command()
async def translate(ctx):

    em = discord.Embed(
        title="Translate!",
        description="Translates the given texts towards the given language!",
        color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!tl <language> <texts>")

    await ctx.send(embed=em)


@help.command()
async def TTT(ctx):

    em = discord.Embed(title="Tic Tac Toe!",
                       description="Starts a tic tac toe game!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!ttt <yourself> <person>")

    await ctx.send(embed=em)


@help.command()
async def place(ctx):

    em = discord.Embed(title="Tic Tac Toe Placings!",
                       description="Place the character to the board!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!place <choose from 1-9>")

    await ctx.send(embed=em)


@help.command()
async def anime(ctx):

    em = discord.Embed(title="Anime!",
                       description="Shows some information about the anime!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!anime <anime title>")

    await ctx.send(embed=em)


@help.command()
async def character(ctx):

    em = discord.Embed(title="Anime Characters!",
                       description="Shows the anime character!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!anime <anime character>")

    await ctx.send(embed=em)


@help.command()
async def aninews(ctx):

    em = discord.Embed(title="Anime News!",
                       description="Shows the latest news about anime!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!aninews")

    await ctx.send(embed=em)


@help.command()
async def avatar(ctx):

    em = discord.Embed(title="Avatar",
                       description="Shows the avatar of a member!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!avatar <member>")

    await ctx.send(embed=em)


@help.command()
async def kill(ctx):

    em = discord.Embed(title="Kill",
                       description="Mention someone to be killed!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!kill <member>")

    await ctx.send(embed=em)


@help.command()
async def bite(ctx):

    em = discord.Embed(title="Bite",
                       description="Mention someone to be bitten!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!bite <member>")

    await ctx.send(embed=em)


@help.command()
async def ship(ctx):

    em = discord.Embed(
        title="Ships!",
        description="Mention 2 people to test their love affinity!",
        color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!ship <person1> <person2>")

    await ctx.send(embed=em)


@help.command()
async def lick(ctx):

    em = discord.Embed(title="Lick",
                       description="Mention someone to be licked!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!lick <member>")

    await ctx.send(embed=em)


@help.command()
async def bully(ctx):

    em = discord.Embed(title="Bully",
                       description="Mention someone to be bullied!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!bully <member>")

    await ctx.send(embed=em)


@help.command()
async def FR(ctx):

    em = discord.Embed(title="Fun Rate",
                       description="Mention someone to be Rated!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!fr <someone>")

    await ctx.send(embed=em)


@help.command()
async def RPS(ctx):

    em = discord.Embed(title="Rock, Paper, Scissors!",
                       description="Play rock paper scissors!",
                       color=ctx.author.color)

    em.add_field(
        name="**Syntax**",
        value="A!rps #and then input choice after the bot sends a message")

    await ctx.send(embed=em)


@help.command()
async def rate(ctx):

    em = discord.Embed(
        title="Ratings!",
        description="Shows a random rating of the person you mention!",
        color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!rate <someone>")

    await ctx.send(embed=em)


@help.command()
async def slap(ctx):

    em = discord.Embed(title="Slap",
                       description="Mention someone to be slapped!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!slap <member>")

    await ctx.send(embed=em)


@help.command()
async def calc(ctx):

    em = discord.Embed(title="Calculator",
                       description="Do simple maths!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!calc")

    await ctx.send(embed=em)


@help.command()
async def ping(ctx):

    em = discord.Embed(title="PING!",
                       description="Shows the bot's latency!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!ping")

    await ctx.send(embed=em)


@help.command()
async def smug(ctx):

    em = discord.Embed(title="Smug",
                       description="Shows a random anime smug gif!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!smug")

    await ctx.send(embed=em)


@help.command()
async def blush(ctx):

    em = discord.Embed(title="Blush",
                       description="Shows a random anime blush gif!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!blush")

    await ctx.send(embed=em)


@help.command()
async def meme(ctx):

    em = discord.Embed(title="Meme",
                       description="Shows a random meme!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!meme")

    await ctx.send(embed=em)


@help.command()
async def wink(ctx):

    em = discord.Embed(title="Wink",
                       description="Gives a wink to someone :smirk:",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!wink <mention>")

    await ctx.send(embed=em)


@help.command()
async def cuddle(ctx):

    em = discord.Embed(title="Cuddle",
                       description="Gives a cuddle to someone :upside_down:",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!cuddle <mention>")

    await ctx.send(embed=em)


@help.command()
async def pat(ctx):

    em = discord.Embed(title="Pat",
                       description="Gives a pat to someone :upside_down:",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!pat <mention>")

    await ctx.send(embed=em)


@help.command()
async def hug(ctx):

    em = discord.Embed(title="Hug",
                       description="Gives a hug to someone :upside_down:",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!hug <mention>")

    await ctx.send(embed=em)


@help.command()
async def kiss(ctx):

    em = discord.Embed(title="Kiss",
                       description="Gives a kiss to someone :upside_down:",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!kiss <mention>")

    await ctx.send(embed=em)


@help.command()
async def join(ctx):

    em = discord.Embed(title="Join",
                       description="Joins the bot to your voice channel!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!join")

    await ctx.send(embed=em)


@help.command()
async def DC(ctx):

    em = discord.Embed(
        title="Disconnect",
        description="Disconnect the bot from your vc :upside_down:",
        color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!dc")

    await ctx.send(embed=em)


@help.command()
async def play(ctx):

    em = discord.Embed(title="Play",
                       description="Plays a youtube audio of your choice!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!play <URL>")

    await ctx.send(embed=em)


@help.command()
async def pause(ctx):

    em = discord.Embed(title="Pause",
                       description="Pauses the bot's audio.",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!pause")

    await ctx.send(embed=em)


@help.command()
async def resume(ctx):

    em = discord.Embed(title="Resume",
                       description="Resume the bot's audio.",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!resume")

    await ctx.send(embed=em)


@help.command()
async def dog(ctx):

    em = discord.Embed(title="Dogs",
                       description="Shows a random dog's picture!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!dog")

    await ctx.send(embed=em)


@help.command()
async def cat(ctx):

    em = discord.Embed(title="Cats",
                       description="Shows a random cat's picture!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!cat")

    await ctx.send(embed=em)


@help.command()
async def PF(ctx):

    em = discord.Embed(title="Pokefusion!",
                       description="Shows a random fused pokemon!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!pf")

    await ctx.send(embed=em)


@help.command()
async def dex(ctx):

    em = discord.Embed(title="Pokedex",
                       description="See the dex of a pokemon!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!dex <pokemon>")

    await ctx.send(embed=em)


@help.command()
async def movesets(ctx):

    em = discord.Embed(title="Movesets",
                       description="See the movesets of a pokemon!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!ms <pokemon>")

    await ctx.send(embed=em)


@help.command()
async def stats(ctx):

    em = discord.Embed(title="Stats",
                       description="See the stats of a pokemon!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!stats <pokemon>")

    await ctx.send(embed=em)


@help.command()
async def TS(ctx):

    em = discord.Embed(title="Type-Stats",
                       description="See the stats of a pokemon-type!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!ts <pokemon-type>")

    await ctx.send(embed=em)


@help.command()
async def MT(ctx):

    em = discord.Embed(title="Moves-Types",
                       description="See the list of moves of a pokemon-type!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!mt <pokemon-type>")

    await ctx.send(embed=em)


@help.command()
async def ML(ctx):

    em = discord.Embed(title="Meeeting's Links",
                       description="Shows a clickable meeting's link",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!ml <subject>")

    await ctx.send(embed=em)


@help.command()
async def schedule(ctx):

    em = discord.Embed(title="Class' Schedule!",
                       description="Shows the schedule of a class",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!s <class>")

    await ctx.send(embed=em)


@help.command()
async def BI(ctx):

    em = discord.Embed(title="Bot-Info",
                       description="Shows the info of this bot!",
                       color=ctx.author.color)

    em.add_field(name="**Syntax**", value="A!bi")

    await ctx.send(embed=em)


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.idle,
                                 activity=discord.Game("ThaRiAn043's codes"))

    async with aiofiles.open("ticket_configs.txt", mode="a") as temp:
        pass

    async with aiofiles.open("ticket_configs.txt", mode="r") as file:
        lines = await file.readlines()
        for line in lines:
            data = line.split(" ")
            client.ticket_configs[int(
                data[0])] = [int(data[1]),
                             int(data[2]),
                             int(data[3])]

    print('bot is ready!')


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('THERE IS NO SUCH A COMMAND! :expressionless:')


@client.command(aliases=['bot-info', 'bi', 'BI', 'botinfo'])
async def bot_info(ctx):
    embed = discord.Embed(title="Bot Informations",
                          colour=discord.Colour.random())
    embed.add_field(
        name="Prefix?",
        value=
        "The prefix of the bot is:\n1. <@899462346827780096>\n2. `a!`\n3. `A!`",
        inline=False)
    embed.add_field(
        name="Developer?",
        value=
        "The developer of this bot is:\n`Thanel Richard Angwarmasse`\nIG: [@tharian_043](https://www.instagram.com/tharian_043/)",
        inline=False)
    embed.set_thumbnail(url="https://i.imgur.com/gQIzQpU.jpeg")
    embed.set_footer(
        text="Created Using Python Programming Language",
        icon_url=
        "https://i.pinimg.com/originals/9d/f1/f8/9df1f82852b0d020ccf6430c17b8ce36.jpg"
    )

    await ctx.send(embed=embed)


@client.command(aliases=['Ping'])
async def ping(ctx):
    await ctx.send(f'pong! {round(client.latency * 1000)}ms',
                   file=discord.File('bonk.png'))


@client.command(aliases=['cdn'])
async def timer(ctx, seconds):
    try:
        secondint = int(seconds)
        if secondint > 1800:
            await ctx.send(
                "Bruhh, i don't think i can go over 30 minutes :sleepy:")
            raise BaseException
        if secondint < 0:
            await ctx.send(
                "Bruhh, how can i count **DOWN** to negatives? :confused:")
            raise BaseException

        message = await ctx.send(f'Timer: {seconds}s')

        while True:
            secondint -= 1
            if secondint == 0:
                await message.edit(content="ENDED!")
                break

            await message.edit(content=f'Timer: {secondint}s')
            await asyncio.sleep(1)
        await ctx.send(f'{ctx.author.mention}, your countdown has been ended!')
    except ValueError:
        await ctx.send('NO NUMBER NO COUNTDOWN! :expressionless:')


@timer.error
async def timer_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('NO NUMBER NO COUNTDOWN! :expressionless:')


@client.command()
async def t(ctx):
    seconds = 60
    try:
        secondint = int(seconds)

        message = await ctx.send(f'Timer: {seconds}s')

        while True:
            secondint -= 1
            if secondint == 0:
                await message.edit(content="Time's up!")
                break

            await message.edit(content=f'Timer: {secondint}s')
            await asyncio.sleep(1)
        await ctx.send(f'This catch is now FFA!')
    except ValueError:
        await ctx.send('Bruhhh :confused:')


@client.command(aliases=['av'])
async def avatar(ctx, member: discord.Member):
    embed = discord.Embed(title=f"{member}'s avatar!",
                          colour=0x0000ff,
                          timestamp=ctx.message.created_at)
    embed.add_field(name="Animated?", value=member.is_avatar_animated())
    embed.set_image(url=member.avatar_url)
    await ctx.send(embed=embed)


@avatar.error
async def avatar_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Mention someone to check their avatar :unamused:')


@client.command(aliases=['kill'])
async def murder(ctx, member: discord.Member):
    replies = [
        "was stabbed by Umbu :smiling_face_with_tear:",
        "was stomped by an elephant to death :smiling_face_with_tear:",
        "gets hit by Truck-kun and got isekai'd :rofl:",
        "was given the millennium problems and died trying :smiling_face_with_tear:",
        "was slapped by Ichad with a slapping speed of 3725.95 mph :rofl:",
        "was falls out of the window :confounded:",
        "was ran over by a reindeer :cry:",
        "trips and dies instantly :pensive:",
        "was ran over by a train :confounded:",
        "goes for skydiving and the parachute fails to open :confounded:",
        "falls of the roof :pensive:", "was poisoned by Ewin :worried:",
        "gets scooped by the scooper and dies instantly :smiling_face_with_tear:",
        "got sold to the black market by Egia :skull:",
        "got chopped by Umbu :slight_smile:", "was burned by Ichad :skull:",
        "got abducted by aliens  :alien::dash:",
        "was stabbed by Ichad with a fork :skull:",
        "got baked in an oven :fire:", "got bonked with a bat :rofl:",
        "was smashed by a clown's hammer :clown:",
        "died from a broken heart :pensive:",
        "was pulled by a monster under their bed :skull:",
        "got attacked by pigs :pig:",
        "died because they're too fabulous :smiling_face_with_tear:",
        "try to swim in accid and die :slight_smile:",
        "got electrified :skull:",
        "got pulled by a mermaid and drowned :skull:",
        "got UwU-ed to the max level and died :rofl:",
        "died because they're single :cold_sweat:",
        "got hit by a lightning :cloud_lightning:",
        "tried to drink gassoline and died :skull:",
        "fell in a hole and died instantly :sweat:",
        "suffocated and die :skull:",
        "got voted out because they're sus af :skull:",
        "was killed by the impostor :skull:",
        "ate too many food and died :rofl:",
        "was executed by michiyo :pensive:",
        "fell out of the world :smiling_face_with_tear:",
        "got squashed by a falling anvil :pensive:",
        "got murdered in an alleyway by some bunny mascots :skull:",
        "tried to kill a titan and died trying :pensive:",
        "Died being fcked by Egia"
    ]
    if member == ctx.author:
        await ctx.send("okay, you died :slight_smile:")
        return
    await ctx.send(f'{member.mention} {random.choice(replies)}')


@murder.error
async def murder_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Who do you wanna kill? :confused:')


@client.command(aliases=['cf'])
async def coinflip(ctx):
    choices = ["Heads.", "Tails."]
    await ctx.send(random.choice(choices))


@client.command(aliases=['8ball'])
async def yrn(ctx, *, question):
    responses = [
        'Yes.', 'No.', 'Maybe.', 'Probably.', 'I think so.', 'It is certain.',
        'without a doubt.', 'Most likely.',
        'The answer have not been founded XD'
    ]
    await ctx.send(f'Question: {question}\nAnswer: {random.choice(responses)}')


@yrn.error
async def yrn_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Gimme a question :expressionless:')


@client.command()
async def roll(ctx, max_value: int):
    await ctx.send(embed=discord.Embed(
        color=0x2F3136,
        description=f"You have rolled a `{randint(1, max_value)}` !"))


@roll.error
async def roll_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Gimme a max value to roll :confused:')


@client.command()
async def dice(ctx):
    await ctx.send(embed=discord.Embed(
        color=0x2F3136, description=f"🎲 You roll a `{randint(1, 6)}` !"))


@client.command()
async def bully(ctx, member: discord.Member):
    if member == ctx.author:
        await ctx.send("Bruhh... :confused:")
        return

    async with ctx.channel.typing():
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://api.waifu.pics/sfw/bully") as r:
                data = await r.json()

                embed = discord.Embed(
                    description=
                    f"**{ctx.author.name}** bullies **{member.name}**",
                    colour=ctx.author.colour)
                embed.set_image(url=data['url'])

                await ctx.send(embed=embed)


@bully.error
async def bully_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Who do you wanna bully? :smiling_face_with_tear:')


@client.command()
async def bite(ctx, member: discord.Member):
    if member == ctx.author:
        await ctx.send("Bruhh... :confused:")
        return

    async with ctx.channel.typing():
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://api.waifu.pics/sfw/bite") as r:
                data = await r.json()

                embed = discord.Embed(
                    description=
                    f"**{ctx.author.name}** bites **{member.name}**",
                    colour=ctx.author.colour)
                embed.set_image(url=data['url'])

                await ctx.send(embed=embed)


@bite.error
async def bite_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Who do you wanna bite? :smiling_face_with_tear:')


@client.command()
async def lick(ctx, member: discord.Member):
    if member == ctx.author:
        await ctx.send("Bruhh... :confused:")
        return

    async with ctx.channel.typing():
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://api.waifu.pics/sfw/lick") as r:
                data = await r.json()

                embed = discord.Embed(
                    description=
                    f"**{ctx.author.name}** licks **{member.name}**",
                    colour=ctx.author.colour)
                embed.set_image(url=data['url'])

                await ctx.send(embed=embed)


@lick.error
async def lick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Who do you wanna lick? :smiling_face_with_tear:')


@client.command()
async def slap(ctx, member: discord.Member):
    if member == ctx.author:
        await ctx.send("Bruhh... :confused:")
        return

    async with ctx.channel.typing():
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://api.waifu.pics/sfw/slap") as r:
                data = await r.json()

                embed = discord.Embed(
                    description=
                    f"**{ctx.author.name}** slaps **{member.name}**",
                    colour=ctx.author.colour)
                embed.set_image(url=data['url'])

                await ctx.send(embed=embed)


@slap.error
async def slap_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Who do you wanna slap? :smiling_face_with_tear:')


@client.command(aliases=['polls'])
@commands.has_permissions(administrator=True)
async def poll(ctx, *, polls):
    await ctx.channel.purge(limit=1)
    channel = client.get_channel(881874747305111573)

    embed = discord.Embed(colour=ctx.author.colour)
    embed.set_author(name=f'poll made by {ctx.message.author}',
                     icon_url=f'{ctx.author.avatar_url}')
    embed.add_field(name='New Poll!', value=f'{polls}')

    message = await ctx.send(embed=embed)

    await message.add_reaction("👍")
    await message.add_reaction("👎")


@client.command(aliases=['purge'])
@commands.has_permissions(administrator=True)
async def clear(ctx, amount: int):
    await ctx.channel.purge(limit=amount + 1)


@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('How many messages you wants to delete? :confused:')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send('YOU ARE NOT WORTHY TO RUN THIS COMMAND :zany_face:')


@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason=None):
    if member == ctx.author:
        await ctx.send("Bruhhh... :confused:")
        return
    await member.kick(reason=reason)


@kick.error
async def kick_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Who do you wanna kick? :confused:')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send('YOU ARE NOT WORTHY TO RUN THIS COMMAND :zany_face:')


@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, *, reason=None):
    if member == ctx.author:
        await ctx.send("Bruhhh... :confused:")
        return
    await member.ban(reason=reason)
    await ctx.send(f'banned {member.mention}')


@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Who do you wanna ban? :confused:')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send('WHO THE FK ARE YOU TO RUN THIS COMMAND :angry:')


@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name,
                                               member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'unbanned {user.mention}')
            return


@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Who do you wanna unban? :confused:')

    if isinstance(error, commands.MissingPermissions):
        await ctx.send('WHO THE FK ARE YOU TO RUN THIS COMMAND :angry:')


@client.command()
async def calc(ctx):
    def check(m):
        return len(m.content) >= 1 and m.author == ctx.author

    await ctx.send(
        embed=discord.Embed(color=0x2F3136, description="1st Numbers:"))
    number_1 = await client.wait_for("message", check=check)
    await ctx.send(embed=discord.Embed(color=0x2F3136, description="operator:")
                   )
    operator = await client.wait_for("message", check=check)
    await ctx.send(
        embed=discord.Embed(color=0x2F3136, description="2nd Numbers:"))
    number_2 = await client.wait_for("message", check=check)
    try:
        number_1 = float(number_1.content)
        operator = operator.content
        number_2 = float(number_2.content)
    except:
        await ctx.send("invalid input")
        return
    output = None
    if operator == "+":
        output = number_1 + number_2
    elif operator == "-":
        output = number_1 - number_2
    elif operator == ":":
        output = number_1 / number_2
    elif operator == "*":
        output = number_1 * number_2
    else:
        await ctx.send("invalid input")
        return
    await ctx.send("Answer: " + str(output))


@client.command()
async def smug(ctx):
    async with ctx.channel.typing():
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://api.waifu.pics/sfw/smug") as r:
                data = await r.json()

                embed = discord.Embed(title="😏", colour=ctx.author.colour)
                embed.set_image(url=data['url'])

                await ctx.send(embed=embed)


@client.command()
async def wink(ctx, member: discord.Member):
    if member == ctx.author:
        await ctx.send("Bruhh... :confused:")
        return

    async with ctx.channel.typing():
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://api.waifu.pics/sfw/wink") as r:
                data = await r.json()

                embed = discord.Embed(
                    description=
                    f"**{ctx.author.name}** winks to **{member.name}**",
                    colour=ctx.author.colour)
                embed.set_image(url=data['url'])

                await ctx.send(embed=embed)


@wink.error
async def wink_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Who do you wanna wink to? :smirk:')


@client.command()
async def meme(ctx):
    meme = choice([True, False])
    await ctx.send(embed=Embed(description=":face_with_raised_eyebrow:",
                               color=0x2F3136).set_image(
                                   url=await get_random_gif_by_theme('meme')
                                   if meme else await get_random_meme_pic()))


@client.command()
async def blush(ctx):
    async with ctx.channel.typing():
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"https://api.waifu.pics/sfw/blush") as r:
                data = await r.json()

                embed = discord.Embed(title="😖", colour=ctx.author.colour)
                embed.set_image(url=data['url'])

                await ctx.send(embed=embed)


@client.command()
async def cuddle(ctx, member: discord.Member):
    if member == ctx.author:
        await ctx.send("Bruhh... :confused:")
        return

    async with ctx.channel.typing():
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://api.waifu.pics/sfw/cuddle") as r:
                data = await r.json()

                embed = discord.Embed(
                    description=
                    f"**{ctx.author.name}** cuddles **{member.name}**",
                    colour=ctx.author.colour)
                embed.set_image(url=data['url'])

                await ctx.send(embed=embed)


@cuddle.error
async def cuddle_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Who do you wanna cuddle? :smirk:')


@client.command()
async def pat(ctx, member: discord.Member):
    if member == ctx.author:
        await ctx.send("Bruhh... :confused:")
        return

    async with ctx.channel.typing():
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://api.waifu.pics/sfw/pat") as r:
                data = await r.json()

                embed = discord.Embed(
                    description=f"**{ctx.author.name}** pats **{member.name}**",
                    colour=ctx.author.colour)
                embed.set_image(url=data['url'])

                await ctx.send(embed=embed)


@pat.error
async def pat_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Who do you wanna pat? :smirk:')


@client.command()
async def kiss(ctx, member: discord.Member):
    if member == ctx.author:
        await ctx.send("Bruhh... :confused:")
        return

    async with ctx.channel.typing():
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://api.waifu.pics/sfw/kiss") as r:
                data = await r.json()

                embed = discord.Embed(
                    description=
                    f"**{ctx.author.name}** kisses **{member.name}**",
                    colour=ctx.author.colour)
                embed.set_image(url=data['url'])

                await ctx.send(embed=embed)


@kiss.error
async def kiss_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Who do you wanna kiss? :smirk:')


@client.command()
async def hug(ctx, member: discord.Member):
    if member == ctx.author:
        await ctx.send("Bruhh... :confused:")
        return

    async with ctx.channel.typing():
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://api.waifu.pics/sfw/hug") as r:
                data = await r.json()

                embed = discord.Embed(
                    description=f"**{ctx.author.name}** hugs **{member.name}**",
                    colour=ctx.author.colour)
                embed.set_image(url=data['url'])

                await ctx.send(embed=embed)


@hug.error
async def hug_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Who do you wanna hug? :upside_down:')


@client.command(aliases=['aq'])
async def animequote(ctx):
    q, c, a = await get_random_anime_quote()
    await ctx.send(
        embed=Embed(title=":slight_smile:",
                    color=0x2F3136,
                    description=f"« {q} » — {c} \n**Anime:** __{a}__"))


@client.command(aliases=['mq'])
async def moviequote(ctx):
    q, r, s = await get_random_movie_quote()
    await ctx.send(
        embed=Embed(title=":slight_smile:",
                    color=0x2F3136,
                    description=f"« {q} » — {r} \n**Show:** __{s}__"))


@client.command()
@commands.has_permissions(administrator=True)
async def approved(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.send(file=discord.File('approvedt.png'))


@client.command()
@commands.has_permissions(administrator=True)
async def denied(ctx):
    await ctx.channel.purge(limit=1)
    await ctx.send(file=discord.File('denied.png'))


@client.event
async def on_raw_reaction_add(payload):
    if payload.member.id != client.user.id and str(payload.emoji) == "🔑":
        msg_id, channel_id, category_id = client.ticket_configs[
            payload.guild_id]

        if payload.message_id == msg_id:
            guild = client.get_guild(payload.guild_id)

            for category in guild.categories:
                if category.id == category_id:
                    break

            channel = guild.get_channel(channel_id)

            ticket_channel = await category.create_text_channel(
                f"room-{payload.member.display_name}",
                topic=f"An incense room for {payload.member.display_name}.",
                permission_synced=True)

            await ticket_channel.set_permissions(payload.member,
                                                 read_messages=True,
                                                 send_messages=True)

            message = await channel.fetch_message(msg_id)
            await message.remove_reaction(payload.emoji, payload.member)

            await ticket_channel.send(
                f"{payload.member.mention} You've opened an incense room! Use **'-close'** to close your room."
            )

            try:
                await client.wait_for(
                    "message",
                    check=lambda m: m.channel == ticket_channel and m.author ==
                    payload.member and m.content == "-close",
                    timeout=10800)

            except asyncio.TimeoutError:
                await ticket_channel.delete()

            else:
                await ticket_channel.delete()


@client.command(aliases=['configticket'])
@commands.has_permissions(administrator=True)
async def configure_ticket(ctx,
                           msg: discord.Message = None,
                           category: discord.CategoryChannel = None):
    if msg is None or category is None:
        await ctx.channel.send(
            "Failed to configure the portal as an argument was not given or was invalid."
        )
        return

    client.ticket_configs[ctx.guild.id] = [
        msg.id, msg.channel.id, category.id
    ]  # this resets the configuration

    async with aiofiles.open("ticket_configs.txt", mode="r") as file:
        data = await file.readlines()

    async with aiofiles.open("ticket_configs.txt", mode="w") as file:
        await file.write(
            f"{ctx.guild.id} {msg.id} {msg.channel.id} {category.id}\n")

        for line in data:
            if int(line.split(" ")[0]) != ctx.guild.id:
                await file.write(line)

    await msg.add_reaction("🔑")
    await ctx.channel.send("Succesfully configured the room portal system.")


@client.command(aliases=['cats', 'meow', 'meows', 'kitten'])
async def cat(ctx):
    async with ctx.channel.typing():
        async with aiohttp.ClientSession() as cs:
            r = await cs.get("https://aws.random.cat/meow")
            data = await r.json()

            embed = discord.Embed(title="🐱", colour=ctx.author.colour)
            embed.set_image(url=data["file"])

            await ctx.send(embed=embed)


@client.command(aliases=['doggo', 'dogs', 'woof', 'woofs', 'puppy'])
async def dog(ctx):
    async with ctx.channel.typing():
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://random.dog/woof.json") as r:
                data = await r.json()

                embed = discord.Embed(title="🐶", colour=ctx.author.colour)
                embed.set_image(url=data['url'])

                await ctx.send(embed=embed)


@client.command(aliases=['waifus'])
async def waifu(ctx):
    async with ctx.channel.typing():
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://api.waifu.pics/sfw/waifu") as r:
                data = await r.json()

                embed = discord.Embed(title="❣️", colour=ctx.author.colour)
                embed.set_image(url=data['url'])

                await ctx.send(embed=embed)


@client.command(aliases=['pf'])
async def pokefusion(ctx):
    poke1 = random.randrange(1, 151)
    poke2 = random.randrange(1, 151)

    embed = discord.Embed(title="WHO'S THAT POKEMON⁉️ :eyes:",
                          colour=ctx.author.colour)
    embed.set_image(
        url=
        f"https://images.alexonsager.net/pokemon/fused/{poke1}/{poke1}.{poke2}.png"
    )
    embed.set_footer(text=f"https://pokemon.alexonsager.net/{poke2}/{poke1}")

    await ctx.send(embed=embed)


@client.command(aliases=['insults'])
async def insult(ctx):
    async with ctx.channel.typing():
        async with aiohttp.ClientSession() as cs:
            async with cs.get(
                    "https://evilinsult.com/generate_insult.php?lang=en&type=json"
            ) as r:
                data = await r.json()

                embed = discord.Embed(title="😌",
                                      description=data["insult"],
                                      colour=ctx.author.colour)

                await ctx.send(embed=embed)


@client.command(aliases=['ymm', 'yomamma', 'yomoma', 'yomomma'])
async def yomama(ctx):
    async with ctx.channel.typing():
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://yomomma-api.herokuapp.com/jokes") as r:
                data = await r.json()

                embed = discord.Embed(title="🤣",
                                      description=data["joke"],
                                      colour=ctx.author.colour)

                await ctx.send(embed=embed)


async def get_random_bad_quote():
    async with aiohttp.ClientSession() as session:
        response = await fetch(
            session, "https://breaking-bad-quotes.herokuapp.com/v1/quotes")
        await session.close()
        return response[0]["quote"], response[0]["author"]


@client.command(aliases=['bq'])
async def badquote(ctx):
    q, a = await get_random_bad_quote()

    embed = discord.Embed(title="🥱",
                          description=f"« {q} » — {a}",
                          color=0x2F3136)

    await ctx.send(embed=embed)


@client.command(aliases=['advices'])
async def advice(ctx):
    async with ctx.channel.typing():
        async with aiohttp.ClientSession() as cs:
            async with cs.get("https://api.adviceslip.com/advice") as r:
                data = await r.text()
                noice = json.loads(data)["slip"]["advice"]

                embed = discord.Embed(title=":slight_smile:",
                                      description=noice,
                                      colour=ctx.author.colour)

                await ctx.send(embed=embed)


URL_API = 'https://pokeapi.co/api/v2/pokemon/'


@client.command(aliases=['dex', 'pd', 'pokedex'])
async def d(ctx, *, args):

    pokeName = args.lower()
    try:
        r = requests.get(f'{URL_API}{pokeName}')
        packages_json = r.json()
        packages_json.keys()

        embed = discord.Embed(title="Pokemon", color=ctx.author.color)
        embed.add_field(name="Name", value=packages_json['name'], inline=True)
        embed.add_field(name="Pokedex Order",
                        value=packages_json['order'],
                        inline=True)
        embed.set_thumbnail(
            url=f'https://play.pokemonshowdown.com/sprites/ani/{pokeName}.gif')
        embed.add_field(name="Weight",
                        value=packages_json['weight'],
                        inline=True)
        embed.add_field(name="Height",
                        value=packages_json['height'],
                        inline=True)
        embed.add_field(name="XP Base",
                        value=packages_json['base_experience'],
                        inline=True)

        types_total = []
        for type in packages_json['types']:
            types_total.append(type['type']['name'])
        embed.add_field(name="Types",
                        value="\n".join(types_total),
                        inline=True)
        embed.set_footer(text="Pokedex - Andromeda ")
        await ctx.send(embed=embed)
    except:
        await ctx.send("Pokemon not found!")


@client.command(aliases=['ms'])
async def moveset(ctx, *, args):

    pokeName = args.lower()
    try:
        r = requests.get(f'{URL_API}{pokeName}')
        packages_json = r.json()
        packages_json.keys()

        embed = discord.Embed(title=f"{packages_json['name']}'s Movesets",
                              color=ctx.author.color)
        embed.set_thumbnail(
            url=f'https://play.pokemonshowdown.com/sprites/ani/{pokeName}.gif')
        for move in packages_json['moves']:
            embed.add_field(
                name=move['move']['name'],
                value=
                f"{move['version_group_details'][0]['level_learned_at']}: *{move['version_group_details'][0]['move_learn_method']['name']}*",
                inline=True)

        embed.set_footer(text="Pokedex - Andromeda ")
        await ctx.send(embed=embed)
    except:
        await ctx.send("Pokemon not found!")


@client.command(aliases=['stat'])
async def stats(ctx, *, args):

    pokeName = args.lower()
    try:
        r = requests.get(f'{URL_API}{pokeName}')
        packages_json = r.json()
        packages_json.keys()

        embed = discord.Embed(title=f"{packages_json['name']}'s Stats",
                              color=ctx.author.color)
        embed.set_thumbnail(
            url=f'https://play.pokemonshowdown.com/sprites/ani/{pokeName}.gif')
        embed.add_field(name=packages_json['stats'][0]['stat']['name'],
                        value=packages_json['stats'][0]['base_stat'],
                        inline=True)
        embed.add_field(name=packages_json['stats'][1]['stat']['name'],
                        value=packages_json['stats'][1]['base_stat'],
                        inline=True)
        embed.add_field(name=packages_json['stats'][2]['stat']['name'],
                        value=packages_json['stats'][2]['base_stat'],
                        inline=True)
        embed.add_field(name=packages_json['stats'][3]['stat']['name'],
                        value=packages_json['stats'][3]['base_stat'],
                        inline=True)
        embed.add_field(name=packages_json['stats'][4]['stat']['name'],
                        value=packages_json['stats'][4]['base_stat'],
                        inline=True)
        embed.add_field(name=packages_json['stats'][5]['stat']['name'],
                        value=packages_json['stats'][5]['base_stat'],
                        inline=True)

        embed.set_footer(text="Pokedex - Andromeda ")
        await ctx.send(embed=embed)
    except:
        await ctx.send("Pokemon not found!")


type_api = 'https://pokeapi.co/api/v2/type/'


@client.command(aliases=['type', 'ts', 'type-stats'])
async def types(ctx, *, arg):

    types = [
        'normal', 'fighting', 'flying', 'poison', 'ground', 'rock', 'bug',
        'ghost', 'steel', 'fire', 'water', 'grass', 'electric', 'psychic',
        'ice', 'dragon', 'dark', 'fairy'
    ]
    typesnum = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]

    for typesnum in range(len(types)):
        types[typesnum]

    r = requests.get(f'{type_api}{arg}')
    packages_json = r.json()
    packages_json.keys()

    damage2xfrom_total = []
    for damage2x in packages_json['damage_relations']['double_damage_from']:
        damage2xfrom_total.append(damage2x['name'])
    if len(damage2xfrom_total) == 0:
        damage2xfrom_total = ["-"]

    damage2xto_total = []
    for damage2x in packages_json['damage_relations']['double_damage_to']:
        damage2xto_total.append(damage2x['name'])
    if len(damage2xto_total) == 0:
        damage2xto_total = ["-"]

    damage12xfrom_total = []
    for damage12x in packages_json['damage_relations']['half_damage_from']:
        damage12xfrom_total.append(damage12x['name'])
    if len(damage12xfrom_total) == 0:
        damage12xfrom_total = ["-"]

    damage12xto_total = []
    for damage12x in packages_json['damage_relations']['half_damage_to']:
        damage12xto_total.append(damage12x['name'])
    if len(damage12xto_total) == 0:
        damage12xto_total = ["-"]

    damagexfrom_total = []
    for damagex in packages_json['damage_relations']['no_damage_from']:
        damagexfrom_total.append(damagex['name'])
    if len(damagexfrom_total) == 0:
        damagexfrom_total = ["-"]

    damagexto_total = []
    for damagex in packages_json['damage_relations']['no_damage_to']:
        damagexto_total.append(damagex['name'])
    if len(damagexto_total) == 0:
        damagexto_total = ["-"]

    embed = discord.Embed(title=f"{arg} Type Stats", color=ctx.author.color)

    embed.add_field(name="Double Damage From:",
                    value="\n".join(damage2xfrom_total))

    embed.add_field(name="Double Damage To:",
                    value="\n".join(damage2xto_total))

    embed.add_field(name="Half Damage From:",
                    value="\n".join(damage12xfrom_total))

    embed.add_field(name="Half Damage To:", value="\n".join(damage12xto_total))

    embed.add_field(name="No Damage From:", value="\n".join(damagexfrom_total))

    embed.add_field(name="No Damage To:", value="\n".join(damagexto_total))

    embed.set_footer(text="Pokedex - TaurosBot ")

    await ctx.send(embed=embed)


@client.command(aliases=['moves-type', 'mt'])
async def moves_type(ctx, *, arg):

    types = [
        'normal', 'fighting', 'flying', 'poison', 'ground', 'rock', 'bug',
        'ghost', 'steel', 'fire', 'water', 'grass', 'electric', 'psychic',
        'ice', 'dragon', 'dark', 'fairy'
    ]
    typesnum = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]

    for typesnum in range(len(types)):
        types[typesnum]

    r = requests.get(f'{type_api}{arg}')
    packages_json = r.json()
    packages_json.keys()

    embed = discord.Embed(title=f"{arg} Type Moves", color=ctx.author.color)

    for move in packages_json['moves']:
        embed.add_field(name=move['name'], value="🔳🔳🔳🔳", inline=True)

    embed.set_footer(text='Pokedex Andromeda')

    await ctx.send(embed=embed)


@client.command(aliases=['wh', 'webhook', 'WH'])
@commands.has_permissions(administrator=True)
async def webhooks(ctx, *, args):
    await ctx.channel.purge(limit=1)
    webhooks = await ctx.channel.webhooks()
    webhook = utils.get(webhooks, name=f"{ctx.author.name} Tauros")
    if webhook is None:
        webhook = await ctx.channel.create_webhook(
            name=f"{ctx.author.name} Andromeda")

    await webhook.send(f'{args}',
                       username=ctx.author.name,
                       avatar_url=ctx.author.avatar_url)


@client.command(aliases=['NSFW'])
async def nsfw(ctx):
    choices = ['neko', 'blowjob', 'waifu']
    async with ctx.channel.typing():
        async with aiohttp.ClientSession() as cs:
            async with cs.get(
                    f"https://api.waifu.pics/nsfw/{random.choice(choices)}"
            ) as r:
                data = await r.json()

                embed = discord.Embed(title="❣️", colour=ctx.author.colour)
                embed.set_image(url=data['url'])

                await ctx.send(embed=embed)


@client.command(aliases=['ships', 'ship'])
async def match(ctx, arg1, arg2):
    if arg1 == arg2:
        await ctx.send("Bruhh... :confused:")
        return

    embed = discord.Embed(Title="Love Meter 💟", colour=ctx.author.colour)
    embed.add_field(
        name="Love Meter 💟",
        value=f"{arg1} + {arg2} = **{random.randint(1, 100)}%** of love ❣️")

    await ctx.send(embed=embed)


@client.command(aliases=['FR'])
async def fr(ctx, arg):

    embed = discord.Embed(title="Fun Rate! 😝", colour=ctx.author.colour)
    embed.add_field(name="Straight?",
                    value=f"{arg} is {random.randint(1, 100)}% straight!",
                    inline=False)
    embed.add_field(name="Gay?",
                    value=f"{arg} is {random.randint(1, 100)}% gay!",
                    inline=False)
    embed.add_field(name="Lesbian?",
                    value=f"{arg} is {random.randint(1, 100)}% lesbian!",
                    inline=False)
    embed.add_field(name="Bisexual?",
                    value=f"{arg} is {random.randint(1, 100)}% bisexual!",
                    inline=False)
    embed.add_field(name="Transgender?",
                    value=f"{arg} is {random.randint(1, 100)}% transgender!",
                    inline=False)
    embed.add_field(name="Cool?",
                    value=f"{arg} is {random.randint(1, 100)}% cool!",
                    inline=False)
    embed.add_field(name="Sexy?",
                    value=f"{arg} is {random.randint(1, 100)}% sexy!",
                    inline=False)

    await ctx.send(embed=embed)


@client.command()
async def rate(ctx, arg):
    choices = [
        'straight', 'gay', 'lesbian', 'bisexual', 'transgender', 'cool',
        'sexy', 'hot', 'smart', 'idiot', 'dumb', 'naughty', 'playboy',
        'masochist', 'sadist', 'genius', 'drug addicted', 'religious'
    ]

    emoji = ['😏', '🗿', '😍', '😝', '🤪', '🤩', '💀', '😶', '🔥', '🙏', '✨', '🌟']

    await ctx.send(
        f"{arg} is {random.randint(1, 100)}% {random.choice(choices)}! {random.choice(emoji)}"
    )


@client.command(aliases=['ML', 'meet'])
async def ml(ctx, arg):

    if arg == "agama":
        embed = discord.Embed(title="Meeting's links!",
                              colour=ctx.author.colour)
        embed.add_field(
            name="Agama",
            value=
            "[meet.google.com/yrx-oykc-jnf](https://meet.google.com/yrx-oykc-jnf)",
            inline=False)

    elif arg == "pkn":
        embed = discord.Embed(title="Meeting's links!",
                              colour=ctx.author.colour)
        embed.add_field(
            name="PPKn",
            value=
            "[meet.google.com/msq-bepz-ndw](https://meet.google.com/msq-bepz-ndw)",
            inline=False)

    elif arg == "bindo":
        embed = discord.Embed(title="Meeting's links!",
                              colour=ctx.author.colour)
        embed.add_field(
            name="Bahasa Indonesia",
            value=
            "[meet.google.com/zcz-vcuh-psh](https://meet.google.com/zcz-vcuh-psh)",
            inline=False)

    elif arg == "bing":
        embed = discord.Embed(title="Meeting's links!",
                              colour=ctx.author.colour)
        embed.add_field(
            name="Bahasa Inggris",
            value=
            "[meet.google.com/prc-fdhr-xph](https://meet.google.com/prc-fdhr-xph)",
            inline=False)

    elif arg == "mw":
        embed = discord.Embed(title="Meeting's links!",
                              colour=ctx.author.colour)
        embed.add_field(
            name="Math Wajib",
            value=
            "[meet.google.com/byh-opvs-abv](https://meet.google.com/byh-opvs-abv)",
            inline=False)

    elif arg == "mm":
        embed = discord.Embed(title="Meeting's links!",
                              colour=ctx.author.colour)
        embed.add_field(
            name="Math Minat",
            value=
            "[meet.google.com/qtk-hhne-mdg](https://meet.google.com/qtk-hhne-mdg)",
            inline=False)

    elif arg == "fisika":
        embed = discord.Embed(title="Meeting's links!",
                              colour=ctx.author.colour)
        embed.add_field(
            name="Fisika",
            value=
            "[meet.google.com/tsh-nspb-yqk](https://meet.google.com/tsh-nspb-yqk)",
            inline=False)

    elif arg == "biologi":
        embed = discord.Embed(title="Meeting's links!",
                              colour=ctx.author.colour)
        embed.add_field(
            name="Biologi",
            value=
            "[meet.google.com/yfi-othh-fad](https://meet.google.com/yfi-othh-fad)",
            inline=False)

    elif arg == "kimia":
        embed = discord.Embed(title="Meeting's links!",
                              colour=ctx.author.colour)
        embed.add_field(
            name="Kimia",
            value=
            "[meet.google.com/qsv-oued-tjh](https://meet.google.com/qsv-oued-tjh)",
            inline=False)

    elif arg == "sindo":
        embed = discord.Embed(title="Meeting's links!",
                              colour=ctx.author.colour)
        embed.add_field(
            name="Sejarah Indonesia",
            value=
            "[meet.google.com/kmf-envs-ppw](https://meet.google.com/kmf-envs-ppw)",
            inline=False)

    elif arg == "ekonomi":
        embed = discord.Embed(title="Meeting's links!",
                              colour=ctx.author.colour)
        embed.add_field(
            name="Ekonomi",
            value=
            "[meet.google.com/kmf-envs-ppw](https://meet.google.com/kmf-envs-ppw)",
            inline=False)

    elif arg == "sbk":
        embed = discord.Embed(title="Meeting's links!",
                              colour=ctx.author.colour)
        embed.add_field(
            name="SBK",
            value=
            "[meet.google.com/qis-gogv-wcy](https://meet.google.com/qis-gogv-wcy)",
            inline=False)

    elif arg == "pjok":
        embed = discord.Embed(title="Meeting's links!",
                              colour=ctx.author.colour)
        embed.add_field(
            name="PJOK",
            value=
            "[meet.google.com/ydn-czth-kvm](https://meet.google.com/ydn-czth-kvm)",
            inline=False)

    elif arg == "pkwu":
        embed = discord.Embed(title="Meeting's links!",
                              colour=ctx.author.colour)
        embed.add_field(
            name="PKWu",
            value=
            "[meet.google.com/oab-rbfr-gae](https://meet.google.com/oab-rbfr-gae)",
            inline=False)

    elif arg == "bk":
        embed = discord.Embed(title="Meeting's links!",
                              colour=ctx.author.colour)
        embed.add_field(
            name="BK",
            value=
            "[meet.google.com/zcz-vcuh-psh](https://meet.google.com/zcz-vcuh-psh)",
            inline=False)

    await ctx.send(embed=embed)


@client.command()
async def truth(ctx):
    choices = [
        'Siapa orang yang paling kamu benci?',
        'Siapa orang yang paling kamu cintai?', 'Crush pas SD?',
        'Berapa banyak mantanmu?',
        'Pernah pacaran dengan 2 atau lebih orang bersamaan?',
        'Sudah punya pacar?', 'Siapa nama pacarmu?',
        'kamu k-popers garis elit atau gak?',
        'Orang terakhir yang kamu searching?', 'Rekor coli sehari?',
        'Hal usil apa yang pernah kamu lakukan ke guru?',
        'Penyesalan terbesar?', 'Pernah kentut di tempat umum?',
        'Pernah ditolak?', 'Pernah terima pernyataan cinta?',
        'Hal paling memalukan yang pernah kamu alami?',
        'Sudah pernah sewa jasa open BO?',
        'Pernah buat fake scenario sebelum tidur?', 'Tempat jalan favorit?',
        'Pernah nangis karena disakiti?',
        'Kapan terakhir kali nangis dan kenapa?', 'Ketakutan terbesar?',
        'Khayalan terbesar?', 'Apa saja Fetishmu?',
        'Hal yang kamu syukuri tidak diketahui mama?'
    ]

    embed = discord.Embed(title='Truth Or Dare!', colour=ctx.author.colour)
    embed.add_field(name='Truth!', value=random.choice(choices))

    await ctx.send(embed=embed)


@client.command()
async def dare(ctx):
    choices = [
        'Confess ke crush!',
        'Gombalin Crush/Pacar/Ex! (tidak perlu sebut nama) (SS)',
        'Gombalin salah satu teman cewek di kelas mu!',
        'Upload foto crush/pacarmu ke SW (SW tidak boleh dihide)!',
        'Joget tiktok dan sw!', 'Dance ‘What is Love’ dan sw!',
        'Selfie gaya Joker!', 'Chat GWS ke kontak random! (RAG)',
        'Telepon kontak random dan tanya apa kabar! (RAG)',
        'Telepon kontak random dan pura-pura dia yang nelpon! (RAG)',
        'Telepon kontak random dan nyanyikan ‘Happy Birthday’! (RAG)',
        'DM Ig Pak Jokowi “Pak Jokowi Jelek”! (SS)',
        'Gombalin teman sesama gender!', 'Gombalin teman lawan gender!',
        'Tambahkan kata ‘meong’ setiap kali kamu bicara sampai giliran kamu berikutnya!',
        'Cium sepatu orang lain!'
    ]

    embed = discord.Embed(title='Truth Or Dare!', colour=ctx.author.colour)
    embed.add_field(name='Dare!', value=random.choice(choices))

    await ctx.send(embed=embed)


@client.command(aliases=['TOD'])
async def tod(ctx):
    tod = ['Truth', 'Dare']

    choices1 = [
        'Siapa orang yang paling kamu benci?',
        'Siapa orang yang paling kamu cintai?', 'Crush pas SD?',
        'Berapa banyak mantanmu?',
        'Pernah pacaran dengan 2 atau lebih orang bersamaan?',
        'Sudah punya pacar?', 'Siapa nama pacarmu?',
        'kamu k-popers garis elit atau gak?',
        'Orang terakhir yang kamu searching?', 'Rekor coli sehari?',
        'Hal usil apa yang pernah kamu lakukan ke guru?',
        'Penyesalan terbesar?', 'Pernah kentut di tempat umum?',
        'Pernah ditolak?', 'Pernah terima pernyataan cinta?',
        'Hal paling memalukan yang pernah kamu alami?',
        'Sudah pernah sewa jasa open BO?',
        'Pernah buat fake scenario sebelum tidur?', 'Tempat jalan favorit?',
        'Pernah nangis karena disakiti?',
        'Kapan terakhir kali nangis dan kenapa?', 'Ketakutan terbesar?',
        'Khayalan terbesar?', 'Apa saja Fetishmu?',
        'Hal yang kamu syukuri tidak diketahui mama?'
    ]

    choices2 = [
        'Confess ke crush!',
        'Gombalin Crush/Pacar/Ex! (tidak perlu sebut nama) (SS)',
        'Gombalin salah satu teman cewek di kelas mu!',
        'Upload foto crush/pacarmu ke SW (SW tidak boleh dihide)!',
        'Joget tiktok dan sw!', 'Dance ‘What is Love’ dan sw!',
        'Selfie gaya Joker!', 'Chat GWS ke kontak random! (RAG)',
        'Telepon kontak random dan tanya apa kabar! (RAG)',
        'Telepon kontak random dan pura-pura dia yang nelpon! (RAG)',
        'Telepon kontak random dan nyanyikan ‘Happy Birthday’! (RAG)',
        'DM Ig Pak Jokowi “Pak Jokowi Jelek”! (SS)',
        'Gombalin teman sesama gender!', 'Gombalin teman lawan gender!',
        'Tambahkan kata ‘meong’ setiap kali kamu bicara sampai giliran kamu berikutnya!',
        'Cium sepatu orang lain!'
    ]

    message = await ctx.send(f"{random.choice(tod)}")

    if message.content == 'Truth':
        await ctx.send(f"{random.choice(choices1)}")

    else:
        await ctx.send(f"{random.choice(choices2)}")


@client.command(aliases=['TOT'])
async def tot(ctx):
    choices = [
        'Lebih pilih jadi KPopers atau Wibu?', 'Mobile Legends atau AoV?',
        'Janda atau Istri orang?', 'Diselingkuhi atau menyelingkuhi?',
        'Lebih sayang bapak atau ibu?', 'PUBG atau FF',
        'Lebih suka kopi atau teh?',
        'Prefer trip ke pegunungan atau ke pantai?',
        'Lebih suka pakai paket data atau WIFI?',
        'Pengen punya adik lawan gender atau kakak lawan gender?',
        'Pengen pacar lebih tua atau lebih muda?', 'Prefer hoodie atau jaket?',
        'Lebih suka menyapu atau mengepel?', 'Horor atau komedi?',
        'Es krim atau yogurt?', 'Mie atau telur?', 'Bali atau Jakarta?',
        'Tempe atau tahu?', 'Lebih suka Marvel atau DC?', 'Komik atau Novel?',
        'Komedi atau Romansa?', 'Sabtu atau Minggu?',
        'Warna-warni atau Monokrom?', 'Kopi atau Coklat?',
        'Telepon atau Chat?', '_Morning Person_ atau _Night Person_?',
        '_Hot Drink_ atau _Cold Drink_?', 'Anjing atau Kucing?',
        'Grab atau Bemo?', 'Mie Goreng atau Mie Kuah?', 'Bakso atau Mie Ayam?',
        'Kuliner atau _Shopping_?', '_Wavy_ atau _Straight_?',
        'Kepanasan atau Kehujanan?', '_Long Hair_ atau _Short Hair_?',
        '_Shaved_ atau _Mustache_?', '_Good Looking_ atau _Intelligent_?',
        'Pendiam atau Humoris?', 'Musik atau Akademik?',
        '_Comfortable_ atau _Dominant_?', '_Good Boy_ atau _Bad Boy_?',
        '_Sport Guy_ atau _Gamer_?', '_Food Date_ atau _Movie Date_?',
        'Romantis atau Realistis?', 'Dijadwalkan atau Jalanin aja?',
        'Kejepit Pintu atau Dilindas Motor?', 'Kalem atau Barbar?',
        'Dikejar Anjing atau Dikejar Banci?',
        'Makan Bubur Pake Tangan Kosong atau Makan Soto Pake Sumpit?',
        'Mandi Pake Rinso atau Cuci Muka Pake Sunlight?',
        'Lidah Kaku atau Gigi Lemas?', 'Jalan-Jalan atau Stay di Rumah?',
        '_Handphone_ Hilang atau Dompet Hilang', 'Ulangan atau Banyak Tugas?',
        'Jajan di Kantin atau Makan Makanan Teman?', 'Jam Kosong atau Libur?',
        '_Scroll Instagram_ atau _Scroll TikTok_?', 'Iron Man atau Thor?',
        'Scarlet Witch atau Dr. Strange?',
        'Captain America atau Winter Soldier?', 'Spider-Man atau Venom?',
        'Deadpool atau Logan?', 'The Avengers atau Eternals?',
        'Quicksilver atau Makkari?', 'Disney atau Pixar?',
        'Twitter atau Instagram?', 'Netflix atau Youtube?'
    ]

    embed = discord.Embed(title='This Or That!', colour=ctx.author.colour)
    embed.add_field(name='Choose!', value=random.choice(choices))

    msg = await ctx.send(embed=embed)

    await msg.add_reaction("<:THIS:932991002724151297>")
    await msg.add_reaction("<:THAT:932991001721733140>")


@client.command(aliases=['RAG'])
async def rag(ctx):
    choices = [
        'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', 'A', 'S', 'D', 'F',
        'G', 'H', 'J', 'K', 'L', 'Z', 'X', 'C', 'V', 'B', 'N', 'M'
    ]

    embed = discord.Embed(title='Random Alphabet Generator!',
                          colour=ctx.author.colour)
    embed.add_field(
        name="Generates:",
        value=f"You've generate the letter `{random.choice(choices)}`!")

    await ctx.send(embed=embed)


@client.command(aliases=['s'])
async def schedule(ctx, arg):

    if arg == 'mia1':
        await ctx.send(file=discord.File('12mia1.jpg'))

    elif arg == 'mia2':
        await ctx.send(file=discord.File('12mia2.jpg'))


@client.command(aliases=['tr', 'Tr', 'TR', 'tl', 'TL'])
async def translate(ctx, lang, *, args):
    t = Translator()
    a = t.translate(args, dest=lang)
    await ctx.send(a.text)


@client.command()
async def anime(ctx, *, query):
    try:

        anime = animec.Anime(query)

    except:
        await ctx.send("No corresponding anime is found in the query!")
        return

    embed = discord.Embed(title=f"{anime.title_jp}/{anime.title_english}",
                          url=anime.url,
                          description=f"{anime.description[:200]}...",
                          colour=ctx.author.colour)
    embed.add_field(name="Episodes", value=str(anime.episodes))
    embed.add_field(name="Ratings", value=str(anime.rating))
    embed.add_field(name="Aired", value=str(anime.aired))
    embed.add_field(name="Broadcast", value=str(anime.broadcast))
    embed.add_field(name="Genres", value=str(anime.genres))
    embed.add_field(name="Type", value=str(anime.type))
    embed.add_field(name="Status", value=str(anime.status))
    embed.set_thumbnail(url=anime.poster)

    await ctx.send(embed=embed)


@client.command(aliases=['char', 'anichar'])
async def character(ctx, *, query):
    try:
        char = animec.Charsearch(query)

    except:
        await ctx.send(
            "No corresponding anime character is found in the query!")
        return

    embed = discord.Embed(title=char.title,
                          url=char.url,
                          colour=ctx.author.colour)
    embed.set_image(url=char.image_url)
    embed.set_footer(text=", ".join(list(char.references.keys())[:2]))

    await ctx.send(embed=embed)


@client.command()
async def aninews(ctx, amount: int = 3):
    news = animec.Aninews(amount)
    links = news.links
    titles = news.titles
    descriptions = news.description

    embed = discord.Embed(title="Latest Anime News",
                          colour=ctx.author.colour,
                          timestamp=datetime.datetime.utcnow())
    embed.set_thumbnail(url=news.images[0])

    for i in range(amount):
        embed.add_field(
            name=f"{i+1}) {titles[i]}",
            value=f"{descriptions[i][:200]}...\n[read more]({links[i]})",
            inline=False)

    await ctx.send(embed=embed)


player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7],
                     [2, 5, 8], [0, 4, 8], [2, 4, 6]]


@client.command(aliases=['ttt', 'TTT'])
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [
            ":white_large_square:", ":white_large_square:",
            ":white_large_square:", ":white_large_square:",
            ":white_large_square:", ":white_large_square:",
            ":white_large_square:", ":white_large_square:",
            ":white_large_square:"
        ]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send(
            "A game is already in progress! Finish it before starting a new one."
        )


@client.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:":
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send(
                    "Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile."
                )
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the !tictactoe command.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[
                condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True


@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send(
            "Please make sure to mention/ping players (ie. <@688534433879556134>)."
        )


@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")


@client.command(aliases=['RPS'])
async def rps(ctx):
    rpsGame = ['rock', 'paper', 'scissors']
    RPS = ['rock', 'paper', 'scissors']
    await ctx.send(f"rock, paper, or scissors? Choose wisely...")

    def check(msg):
        return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower(
        ) in rpsGame

    user_choice = (await client.wait_for('message', check=check)).content

    comp_choice = random.choice(RPS)
    if user_choice == 'rock':
        if comp_choice == 'rock':
            await ctx.send(
                f'Well, that was weird. We tied.\nYour choice: {user_choice}\nMy choice: {comp_choice}'
            )
        elif comp_choice == 'paper':
            await ctx.send(
                f'Nice try, but I won this time!!\nYour choice: {user_choice}\nMy choice: {comp_choice}'
            )
        elif comp_choice == 'scissors':
            await ctx.send(
                f"Aw, you beat me. It won't happen again!\nYour choice: {user_choice}\nMy choice: {comp_choice}"
            )

    elif user_choice == 'paper':
        if comp_choice == 'rock':
            await ctx.send(
                f'The pen beats the sword? More like the paper beats the rock. You won x.x\nYour choice: {user_choice}\nMy choice: {comp_choice}'
            )
        elif comp_choice == 'paper':
            await ctx.send(
                f'Oh, wacky. We just tied. I call a rematch!!\nYour choice: {user_choice}\nMy choice: {comp_choice}'
            )
        elif comp_choice == 'scissors':
            await ctx.send(
                f"LMFAO sucks to be you 'cause I win!!\nYour choice: {user_choice}\nMy choice: {comp_choice}"
            )

    elif user_choice == 'scissors':
        if comp_choice == 'rock':
            await ctx.send(
                f'HAHA!! I JUST CRUSHED YOU!! I rock!!\nYour choice: {user_choice}\nMy choice: {comp_choice}'
            )
        elif comp_choice == 'paper':
            await ctx.send(
                f'Bruh. >:-|\nYour choice: {user_choice}\nMy choice: {comp_choice}'
            )
        elif comp_choice == 'scissors':
            await ctx.send(
                f"Oh well, we tied.\nYour choice: {user_choice}\nMy choice: {comp_choice}"
            )


@client.command()
async def rp(ctx):
  ranpoke = random.randint(1, 905)
  url = "https://pokeapi.co/api/v2/pokemon/"

  try:
    r = requests.get(f"{url}{ranpoke}")
    packages_json = r.json()
    packages_json.keys

    napo = packages_json["name"]

    embed = discord.Embed(title="Who's that pokemon?!", color=discord.Color.random())
    embed.set_image(url=f"https://play.pokemonshowdown.com/sprites/ani/{napo}.gif")
    await ctx.send(embed=embed)

    def check(msg):
      return msg.author == ctx.author and msg.channel == ctx.channel and msg.content.lower()

    user_ans = (await client.wait_for("message", check=check)).content

    if user_ans == napo:
      await ctx.send("You are correct! :)")
    else:
      await ctx.send(f"You are incorrect :v\nThe answer is {napo}")

  except:
    await ctx.send("bruh")



keep_alive()
client.run(os.getenv('TOKEN'))
