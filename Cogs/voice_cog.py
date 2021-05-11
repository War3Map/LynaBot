import asyncio
from datetime import datetime, timedelta
from collections import deque

import discord
from discord.ext import commands

from player import YTDLSource

event_loop = asyncio.get_event_loop()


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


def play_next(voice_cog, context, url):
    """
    Stop the player and prepare to start new song

    :param voice_cog: voice cog

    :type voice_cog: VoiceCog

    :param context: Message context

    :param url: Next url to play

    :type url: str or None

    """
    context.voice_client.stop()
    voice_cog.player = None
    print("Next cause")
    asyncio.run_coroutine_threadsafe(voice_cog.play_from_playlist(context, url), event_loop)


class VoiceCog(commands.Cog):
    """
    Voice commands for bot
    """
    discord_bot = None
    player = None
    playlist = None

    def __init__(self, bot):
        self.discord_bot = bot
        self.playlist = deque()

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

    @commands.command(aliases=['playf', 'plf'])
    @commands.has_role('admin')
    async def play_file(self, ctx, *, query):
        """Plays a file from the local filesystem"""

        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(query))
        ctx.voice_client.play(source, after=lambda e: print('Player error: %s' % e) if e else None)

        await ctx.send(f'Now playing: {query}')

    @commands.command(aliases=['playnow', 'playn', 'pln'])
    @commands.has_role('admin')
    async def play_now(self, context, *, url):
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

    @commands.command(aliases=['play', 'addp', 'pladd', 'ppl'])
    async def play_from_playlist(self, context, url):
        """Adds song to playlist. Plays song from a url(with predownload). """

        if url is not None:
            self.playlist.appendleft(url)
        print(self.playlist)

        cur_url = ""
        # if len(self.playlist) > 0:

        if self.player is None:
            print(f"Starting play song at url {url}")
            cur_url = self.playlist.popleft()
            self.player = await YTDLSource.from_url(cur_url, loop=self.discord_bot.loop)
            context.voice_client.play(self.player, after=lambda e: play_next(self, context, None))
        elif context.voice_client.is_playing:
            print(f"Adding to queue {url}")
            await context.send('Добавлено в очередь {url}'.format(
                url=url
            ))
        else:
            cur_url = self.playlist.popleft()
            print(f"Playing song at url {cur_url}")
            self.player = await YTDLSource.from_url(cur_url, loop=self.discord_bot.loop)
            context.voice_client.play(self.player, after=lambda e: play_next(self, context, cur_url))

        duration_str = get_duration_str(int(self.player.data.get('duration')))
        print(self.playlist)
        await context.send(f'Сейчас проигрывается: {self.player .title}'
                           f' продолжительность - {duration_str}')

    @commands.command(aliases=['pls', ])
    async def list(self, context):
        """Sends content of playlist"""
        playlist_content = "\n".join(self.playlist)
        await context.send(f'Содержимое плейлиста: {playlist_content}')

    @commands.command(aliases=['strm', ])
    @commands.has_role('admin')
    async def stream(self, context, *, url):
        """Streams from a url (without predownload).
         The song may suddenly end. Unstable. """

        async with context.typing():
            player = await YTDLSource.from_url(url, loop=self.discord_bot.loop, stream=True)

            duration_str = get_duration_str(int(player.data.get('duration')))

            context.voice_client.play(player,
                                      after=lambda e: print('Player error: %s' % e) if e else None)

        await context.send(f'Сейчас проигрывается: {player.title}'
                           f' продолжительность - {duration_str}')

    @commands.command()
    async def stop(self, context):
        """Stops a song"""

        if context.voice_client.is_playing():
            context.voice_client.stop()

    @commands.command()
    async def volume(self,  ctx, volume_val: int):
        """Changes the player's volume"""

        if ctx.voice_client is None:
            return await ctx.send("Not connected to a voice channel.")

        ctx.voice_client.source.volume = volume_val / 100
        await ctx.send("Changed volume to {}%".format(volume_val))

    @play_now.before_invoke
    @play_file.before_invoke
    @play_from_playlist.before_invoke
    @stream.before_invoke
    async def ensure_voice(self, context):
        if context.voice_client is None:
            if context.author.voice:
                await context.author.voice.channel.connect()
            else:
                await context.send("Ты не подключен к голосовому каналу!")
                raise commands.CommandError("Author not connected to a voice channel.")
        elif context.voice_client.is_playing():
            context.voice_client.stop()

    @commands.Cog.listener()
    async def on_message(self, message):
        pass
