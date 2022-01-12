import asyncio
from datetime import datetime, timedelta
from collections import deque

import discord
from discord.ext import commands

from additional.player import YTDLSource
from threading import Timer

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
        self.playing_playlist = False
        self.duration_song = 0
        self.playlist_timer = None
        self.current_song = None

    @commands.command()
    async def join(self, context):
        """Bot joins to current voice channel"""
        channel = context.author.voice.channel
        if channel:
            print(f"Joining channel {channel.id}")
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

            context.voice_client.play(player, after=lambda e: print(f'Player error: {e}') if e else None)

        await context.send('Сейчас проигрывается: {}'
                           ' продолжительность - {}'.format(
            player.title,
            duration_str
        ))

    # @tasks.loop(seconds=self.duration_song)
    # async def run_new_song(self):
    #
    #     print("Next cause")
    #     self.player = None
    #     asyncio.run_coroutine_threadsafe(voice_cog.play_from_playlist(context, url), event_loop)

    def stop_song(self, context):
        print("Таймер тик!")
        if len(self.playlist) == 0:
            print("Плейлист закончен!")
            self.playing_playlist = False
            self.player = None
        else:
            asyncio.run_coroutine_threadsafe(self.play_next(context), event_loop)
            # self.play()

        self.playlist_timer.cancel()

    async def play_song(self, client):
        await client.play(self.player)

    async def play_next(self, context):
        """
        Stop the player and prepare to start new song

        :param context: Message context

        :param url: Next url to play

        :type url: str or None

        """
        print("запуск следующей композиции")
        current_url = self.playlist.popleft() if self.playlist else None

        if current_url is not None:
            # asyncio.run_coroutine_threadsafe(self.play_from_playlist(context, new_url), event_loop)
            print(f"Starting play song at url {current_url}")
            self.player = await YTDLSource.from_url(current_url, loop=self.discord_bot.loop)
            self.duration_song = int(self.player.data.get('duration'))
            await context.send(f'Сейчас проигрывается: {self.player.title}'
                               f' продолжительность - {self.duration_song} c')
            self.playing_playlist = True
            # asyncio.create_task()

            # context.voice_client.play(self.player)

            # asyncio.create_task(self.play_song(context.voice_client))




            self.playlist_timer = Timer(self.duration_song,
                                        self.stop_song,
                                        args=[context])
            self.playlist_timer.start()
            print("Таймер запущен")

        # self.run_new_song.start()

    @commands.command(aliases=['play', 'addp', 'pladd', 'ppl'])
    async def play_from_playlist(self, context, url):
        """Adds song to playlist. Plays song from a url(with predownload). """

        if url is not None:
            self.playlist.appendleft(url)

        print(f"Adding to queue {url}")
        print(f"Playlist: {self.playlist}")
        await context.send(f'Добавлено в очередь {url}')
        if not self.playing_playlist:
            print("Запуск проигрывания ")
            await self.play_next(context)

    @commands.command(aliases=['pls', ])
    async def list(self, context):
        """Sends content of playlist"""
        playlist_content = "\n".join(self.playlist) if not self.playlist else "Пусто!"
        await context.send(f'Содержимое плейлиста: {playlist_content}')

    @commands.command(aliases=['сls', ])
    async def clear_list(self, context):
        """Sends content of playlist"""

        await self.playlist.clear()
        await context.send(f'Плейлист очищен!')

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
    async def volume(self, ctx, volume_val: int):
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

    # @commands.command(aliases=['play', 'addp', 'pladd', 'ppl'])
    # async def old_playlist(self, context, url):
        # cur_url = ""
        # if len(self.playlist) > 0:

        # if self.player is None:
        #     print(f"Starting play song at url {url}")
        #     cur_url = self.playlist.popleft()
        #     self.player = await YTDLSource.from_url(cur_url, loop=self.discord_bot.loop)
        #     context.voice_client.play(self.player, after=lambda e: play_next(self, context, None))
        # elif context.voice_client.is_playing:
        #     print(f"Adding to queue {url}")
        #     print(f"Playlist: {self.playlist}")
        #     await context.send('Добавлено в очередь {url}'.format(
        #         url=url
        #     ))
        #     duration_str = get_duration_str(int(self.player.data.get('duration')))
        #
        #     await context.send(f'Сейчас проигрывается: {self.player.title}'
        #                        f' продолжительность - {duration_str}')
        # else:
        #     cur_url = self.playlist.popleft()
        #     print(f"Playing song at url {cur_url}")
        #     self.player = await YTDLSource.from_url(cur_url, loop=self.discord_bot.loop)
        #     context.voice_client.play(self.player, after=lambda e: play_next(self, context, cur_url))