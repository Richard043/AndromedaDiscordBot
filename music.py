import discord
from discord.ext import commands
import youtube_dl

class music(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            await ctx.send("Get in the voice channel... :smiling_face_with_tear:")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
        else:
            await ctx.voice_client.move_to(voice_channel)

    @commands.command(aliases=['dc'])
    async def disconnect(self, ctx):
        await ctx.voice_client.disconnect()
        await ctx.send("disconnected!")

    @commands.command()
    async def play(self, ctx, url):
        ctx.voice_client.stop()
        FFMPEG_OPTIONS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
        YDL_OPTIONS = {'format':"bestaudio"}
        vc = ctx.voice_client

        with youtube_dl.YoutubeDL(YDL_OPTIONS) as ydl:
            info = ydl.extract_info(url, download=False)
            url2 = info['formats'][0]['url']
            source = await discord.FFmpegOpusAudio.from_probe(url2, **FFMPEG_OPTIONS)
            vc.play(source)

    @commands.command()
    async def pause(self, ctx):
        await ctx.voice_client.pause()
        await ctx.send("paused :pause_button:")

    @commands.command()
    async def resume(self, ctx):
        await ctx.voice_client.resume()
        await ctx.send("resumed :play_pause:")



def setup(client):
    client.add_cog(music(client))
