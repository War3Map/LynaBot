from datetime import datetime, timedelta

import discord
from discord.ext import commands

from player import YTDLSource


def get_duration_str(duration_in_seconds):
    """
    Returns duration as str in format "%H:%M:%S"
    :param duration_in_seconds: duration in seconds
    :type duration_in_seconds: int
    :rtype:  str
    """
    duration = (datetime.min + timedelta(seconds=duration_in_seconds)).time()
    duration_str = duration.strftime("%H:%M:%S")
    return duration_str


class VoiceCog(commands.Cog):
    """
    Voice commands for bot
    """
    discord_bot = None

    def __init__(self, bot):
        self.discord_bot = bot

    @commands.command()
    async def join(self, context):
        """Bot joins to current voice channel"""
        channel = context.author.voice.channel
        if channel:
            print("Joining channel {id}".format(
                id=channel.id))
            await channel.connect(reconnect=False)
        else:
            await context.send('Такого канала не существует!')

    @commands.command()
    async def leave(self, context):
        """bot Leaves a channel"""
        channel = context.author.voice.channel
        if channel:
            print("Leaving channel".format(
                id=channel.id))
            await context.guild.voice_client.disconnect()

    @commands.command()
    async def play(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send('Now playing: {}'.format(query))

    @commands.command()
    async def yt(self, context, *, url):
        """Plays from a url (almost anything youtube_dl supports)"""

        async with context.typing():
            player = await YTDLSource.from_url(url, loop=self.discord_bot.loop)

            duration_str = get_duration_str(int(player.data.get('duration')))

            context.voice_client.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

        await context.send('Сейчас проигрывается: {}'
                           ' продолжительность - {}'.format(
                            player.title,
                            duration_str
                           ))

    @commands.command()
    async def stream(self, context, *, url):
        """Streams from a url (same as yt, but doesn't predownload)"""

        async with context.typing():
            player = await YTDLSource.from_url(url, loop=self.discord_bot.loop, stream=True)
            player.data
            duration_str = get_duration_str(int(player.data.get('duration')))

            context.voice_client.play(player,
                                      after=lambda e: print('Player error: %s' % e) if e else None)

        await context.send('Сейчас проигрывается: {}'
                           ' продолжительность - {}'.format(
            player.title,
            duration_str
        ))

    @commands.command()
    async def stop(self, context):
        """Plays from a url (almost anything youtube_dl supports)"""

        if context.voice_client.is_playing():
            context.voice_client.stop()

    @commands.command()
    async def volume(self,  ctx, volume_val: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume_val / 100
        await ctx.send("Changed volume to {}%".format(volume_val))

    @play.before_invoke
    @yt.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, ctx):
        if ctx.voice_client is None:
            if ctx.author.voice:
                await ctx.author.voice.channel.connect()
            else:
                await ctx.send("Ты не подключен к голосовому каналу!")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif ctx.voice_client.is_playing():
            ctx.voice_client.stop()

    @commands.Cog.listener()
    async def on_message(self, message):
        pass
