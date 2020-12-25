import random

import discord
from discord.ext import commands
# from discord.ext.commands import bot



settings = {
    'token': 'NzkxNjUxMjE5NTI5NTMxNDAy.X-SQpg.xXoj3Q89aNsUZhOHvQKb-fZk7kU',
    'bot': 'Lyna',
    'id': 791651219529531402,
    'prefix': '!'
}

TOKEN = settings['token']
PREFIX = settings['prefix']


def init_bot():
    discord_bot = commands.Bot(command_prefix='!', help_command=None)

    # print(f"The bot {settings['bot']} is started")

    @discord_bot.event
    async def on_ready():
        print(f'{discord_bot.user.name}: Приветик! Я снова с вами:)')

    @discord_bot.command()
    async def test(context, arg):
        await context.send(arg)

    @discord_bot.command(help="вежеливо поприветствую тебя")
    async def hello(context):  # Создаём функцию и передаём аргумент context.
        author = context.message.author  # Объявляем переменную author и записываем туда информацию об авторе.

        await context.send(f'Приветствую тебя, хозяин {author.mention}!')

    @discord_bot.command(help="случайная фраза")
    async def phrase(context):
        random_fact = [
            'Добрая рука, как лучик света!',
            'Няяя! Не нравится? Ну так не смотри!',
            'Мир да любовь!'

        ]

        response = random.choice(random_fact)
        await context.send(response)

    @discord_bot.command(help='Брошу кубик столько раз сколько попросите=)')
    async def dice(context, number_of_dice: int, number_of_sides: int):
        dice_result = [
            str(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)
        ]
        await context.send(', '.join(dice_result))

    @discord_bot.command(name='crt_ch', help='Создам канал) Только для админчиков)')
    @commands.has_role('admin')
    async def create_channel(context, channel_name):
        guild = context.guild
        existing_channel = discord.utils.get(guild.channels, name=channel_name)
        if not existing_channel:
            print(f'Создаю новый канал: {channel_name}')
            await guild.create_text_channel(channel_name)

    # @discord_bot.event
    # async def on_command_error(context, error):
    #     context.send('Ты написал что-то неправильно!', error)
    #     if isinstance(error, commands.errors.CheckFailure):
    #         await context.send('Ты написал что-то неправильно!')

    @discord_bot.command()
    async def help(context):
        emb = discord.Embed(title='Вот что я могу:', description='Я пока ещё многого не умею, но точно научусь!',
                            colour=discord.Color.red())
        # title - Жирный крупный текст (Заголовок) | description - Текст под заголовком | colour - Цвет полоски

        emb.set_author(name=context.author.name, icon_url=context.author.avatar_url)
        
        print(context.author.name)
        # Отображает: ctx.author.name - Имя отправителя, ctx.author.avatar_url - Аватар отправителя
        emb.add_field(name='Все',
                      value=f'`{PREFIX}crt_ch `'
                            f' `{PREFIX}dice   `'
                            f' `{PREFIX}hello`'
                            f' `{PREFIX}help   ` '
                            f'`{PREFIX}phrase ` '
                            f'`{PREFIX}test    ` ',
                      inline=False)


        # Отображаемый блок текста. name - Жирный крупный текст | value - обычный текст под "name"
        # | inline = True - Блоки текста будут в одну строку (https://prnt.sc/uogw2x) / inline = False -
        # Блоки текста будут один под другим (https://prnt.sc/uogx3t)
        emb.set_thumbnail(url=discord_bot.user.avatar_url)
        # emb.set_thumbnail - Добавляет картинку около текста
        # client.user.avatar_url - Отображает аватарку бота

        # emb.set_footer(icon_url=context.guild.owner.avatar_url,
        #                text=f'{context.guild.owner.name} !!!!')

        emb.set_footer(text=f'{PREFIX}crt_ch \n'
                            f' `{PREFIX}dice   `'
                            f' `{PREFIX}hello`'
                            f' `{PREFIX}help   ` '
                            f'`{PREFIX}phrase ` '
                            f'`{PREFIX}test    ` '
                            'Удачки!)')

        # emb.set_thumbnail - Добавляет картинку под текстом
        # | ctx.guild.owner.avatar_url - Аватарка создателя сервера
        # | ctx.guild.owner.name - Имя создателя сервера

        await context.send(embed=emb)
        # Отправляет сообщение и так же преобразует emb в embed

        print(f'[Logs:info] Справка по командам была успешно выведена | {PREFIX}help ')


    # @discord_bot.command()
    # async def __help(ctx):
    #     emb = discord.Embed(title='Вот что я могу:', description='Я пока ещё многого не умею, но точно научусь!',
    #                         colour=discord.Color.red())
    #     # title - Жирный крупный текст (Заголовок) | description - Текст под заголовком | colour - Цвет полоски
    #
    #     emb.set_author(name=ctx.author.name, icon_url=ctx.author.avatar_url)
    #     # Отображает: ctx.author.name - Имя отправителя, ctx.author.avatar_url - Аватар отправителя
    #     emb.add_field(name='Все',
    #                   value=f'`{PREFIX}crt_ch `'
    #                         f' `{PREFIX}dice   `'
    #                         f' `{PREFIX}hello`'
    #                         f' `{PREFIX}help   ` '
    #                         f'`{PREFIX}phrase ` '
    #                         f'`{PREFIX}test    ` ',
    #                   inline=False)
    #
    #     # Отображаемый блок текста. name - Жирный крупный текст | value - обычный текст под "name"
    #     # | inline = True - Блоки текста будут в одну строку (https://prnt.sc/uogw2x) / inline = False -
    #     # Блоки текста будут один под другим (https://prnt.sc/uogx3t)
    #     emb.set_thumbnail(url=discord_bot.user.avatar_url)
    #     # emb.set_thumbnail - Добавляет картинку около текста
    #     # client.user.avatar_url - Отображает аватарку бота
    #     emb.set_footer(icon_url=ctx.guild.owner.avatar_url,
    #                    text=f'{ctx.guild.owner.name} !!!!')
    #     # emb.set_thumbnail - Добавляет картинку под текстом
    #     # | ctx.guild.owner.avatar_url - Аватарка создателя сервера
    #     # | ctx.guild.owner.name - Имя создателя сервера
    #
    #     await ctx.send(embed=emb)
    #     # Отправляет сообщение и так же преобразует emb в embed
    #
    #     print(f'[Logs:info] Справка по командам была успешно выведена | {PREFIX}help ')
    #     # Информация в консоль, что команда "help" была использована
    #     # Итог: https://prnt.sc/uoh6v6


    @discord_bot.event
    async def on_message(message):
        if message.author == discord_bot.user:
            return
        if (
                ("Lyna" in message.content) or
                ("Лина" in message.content)

        ):
            await message.channel.send('А вот и я=)')

        await discord_bot.process_commands(message)

    discord_bot.run(TOKEN)


if __name__ == '__main__':
    init_bot()
