import discord
from discord.ext import commands


class ManageCog(commands.Cog):
    """
    Contains command to manage channel

    Attributes:
        bot (commands.Bot)
    """

    discord_bot = None

    def __init__(self, bot):
        self.discord_bot = bot

    @commands.command(name='crtc', help='Создам текстовый канал) Только для админчиков)')
    @commands.has_role('admin')
    async def create_text_channel(self, context, channel_name):
        """
        Creates a new text channel

        :param context: discord bot context object

        :param channel_name: name of channel

        """
        guild = context.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if not existing_channel:
            print(f'Создаю новый тестовый канал: {channel_name}')
            await guild.create_text_channel(channel_name)

    @commands.command(name='crvc', help='Создам голосовой канал) Только для админчиков)')
    @commands.has_role('admin')
    async def create_voice_channel(self, context, channel_name):
        guild = context.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if not existing_channel:
            print(f'Создаю новый голосовой канал: {channel_name}')
            await guild.create_voice_channel(channel_name)

    @commands.command(name='create',
                      help='Создам каналы (голосовой или текстовый) Только для админчиков)')
    @commands.has_role('admin')
    async def create_channels(self, context, channel_type, *channels):
        """ Creates voice or text channel"""
        guild = context.guild
        creation_dict = {
            "t": guild.create_text_channel,
            "v": guild.create_voice_channel
        }

        creation_func = creation_dict.get(channel_type)

        if creation_func is None:
            return

        for channel_str in channels:
            channel_list = channel_str.split(",")
            for channel in channel_list:
                existing_channel = discord.utils.get(guild.channels, name=channel)
                if not existing_channel:
                    print(f'Создаю новый канал: {channel}')
                    await creation_func(channel)

    @commands.command(name='createm',
                      help='Создам каналы. Только для админчиков)')
    @commands.has_role('admin')
    async def create_many_channels(self, context, channel_type, name,
                                   start_ind=0, end_ind=100):
        """Creates many channels with indexes"""

        start_ind = int(start_ind)
        end_ind = int(end_ind)

        guild = context.guild
        creation_dict = {
            "t": guild.create_text_channel,
            "v": guild.create_voice_channel
        }

        creation_func = creation_dict.get(channel_type)

        for number in range(start_ind, end_ind + 1):
            channel_name = "{name}{number}".format(name=name,
                                                   number=number)
            existing_channel = discord.utils.get(guild.channels,
                                                 name=channel_name)

            if not existing_channel:
                print(f'Создаю новый канал: {channel_name}')
                await creation_func(channel_name)

    @commands.command(name='deletem',
                      help='Удалю каналы. Только для админчиков)')
    @commands.has_role('admin')
    async def delete_channels(self, context, name, start_ind=0, end_ind=100):
        """Deletes many channel with indexes"""
        guild = context.guild
        start_ind = int(start_ind)
        end_ind = int(end_ind)

        for number in range(start_ind, end_ind + 1):
            channel_name = "{name}{number}".format(name=name, number=number)
            existing_channel = discord.utils.get(guild.channels, name=channel_name)
            if existing_channel:
                print(f'Удаляю канал: {channel_name}')
                await existing_channel.delete()

    @commands.command(name='del', help='Удалю канал) Только для админчиков)')
    @commands.has_role('admin')
    async def delete_channel(self, context, channel_name):
        """Deletes a channel with name channel_name"""
        guild = context.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if existing_channel:
            print(f'Удаляю канал: {channel_name}')
            await existing_channel.delete()

    @commands.command(aliases=['rename', 'cnick'])
    @commands.has_role('admin')
    async def change_nickname(self, ctx, member: discord.Member, nick):
        """ Changes nickname"""
        previous = member.nick
        print(previous)
        await member.edit(nick=nick)
        await ctx.send(f'Никнейм этого человека: ```ARM\n{previous}``` поменялся на :{member.mention} ')

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, reason=None):
        user = member.nick
        ban_reason = reason if reason is not None else "Админ так сказал!"
        try:
            await member.kick()
            await ctx.send(f'{user} вылетел из сервера! Причина: {ban_reason}')
        except Exception as ex:
            print("Ошибка при удалении", ex)
            await ctx.send('Я не могу этого сделать!')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, reason=None):
        user = member.name
        ban_reason = reason if reason is not None else "Админ так сказал!"
        try:
            await member.ban()
            await ctx.send(f'{user} был забанен! Причина: {ban_reason}')
        except Exception as ex:
            print("Ошибка при бане", ex)
            await ctx.send('Я не могу этого сделать!')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, member_name, reason=None):

        banned_users = await ctx.guild.bans()
        # member_name, member_discriminator = member.split('#')
        user = None
        ban_reason = reason if reason is not None else "Админ так сказал!"
        for ban_entry in banned_users:
            user = ban_entry.user
            if user.name == member_name:
                break
        try:
            await ctx.guild.unban(user)
            await ctx.send(f"{user} был разбанен! Причина: {ban_reason}")
        except Exception as ex:
            print("Ошибка при разбане", ex)
            await ctx.send('Я не могу этого сделать!')

    @commands.command()
    # @commands.has_permissions(move_members=True)
    @commands.has_role('admin')
    async def move(self, context, member: discord.Member, channel_name):
        channel = discord.utils.find(lambda x: x.name == channel_name, context.guild.channels)
        await member.move_to(channel)

    @commands.command()
    async def invite(self, context):
        invitelink = await context.channel.create_invite(max_age=90, max_uses=1, unique=True)
        await context.send(invitelink)

    @commands.command()
    # @commands.has_permissions(administrator=True)
    @commands.has_role('admin')
    async def purge(self, context, count: int):
        await context.channel.purge(limit=count + 1)

    @commands.Cog.listener()
    async def on_message(self, message):
        pass


