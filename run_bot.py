import os

import discord
from discord.ext import commands

from Cogs import messaging_cog, entertainment_cog, \
    voice_cog, manage_cog


# TODO: Сохранить в json и загружать из json
SETTINGS = {
    'bot_name': 'Lyna',
    'id': 791651219529531402,
    'prefix': '!'
}

TOKEN = os.getenv("TOKEN")

PREFIX = SETTINGS['prefix']

# TODO: настроить логирование


def start_bot():
    """
    Starts a bot.
    """
    discord_bot = commands.Bot(command_prefix='!', help_command=None, case_insensitive=True)

    @discord_bot.event
    async def on_ready():
        print(f'{discord_bot.user.name}: Приветик! Я снова с вами:)')

    @discord_bot.event
    async def on_message(message):
        if message.author == discord_bot.user:
            return
        if (
                ("Lyna" in message.content) or
                ("Лина" in message.content)

        ):
            await message.channel.send('А вот и я=) Вызывали?')

        await discord_bot.process_commands(message)

    # TODO: Error handling
    # @discord_bot.event
    # async def on_command_error(context, error):
    #     context.send('Ты написал что-то неправильно!', error)
    #     if isinstance(error, commands.errors.CheckFailure):
    #         await context.send('Ты написал что-то неправильно!')

    @discord_bot.command()
    async def help(context):
        emb = discord.Embed(title='Вот что я могу:',
                            description='Я пока ещё многого не умею, но точно научусь!',
                            colour=discord.Color.red())

        emb.set_author(name=context.author.name, icon_url=context.author.avatar_url)

        print(context.author.name)
        # Отображает: ctx.author.name - Имя отправителя, ctx.author.avatar_url - Аватар отправителя
        emb.add_field(name='Управление каналом',
                      value=f'`{PREFIX}move user channel`  - перемещю пользователя в указанный канал)\n'
                            f'`{PREFIX}crtc name`  - создам новый текстовый канал с именем name)\n'
                            f'`{PREFIX}crvc name`  - создам новый голосовой канал с именем name)\n'
                            f'`{PREFIX}create [v/t] name,name1...`  - создам сразу несколько голосовых'
                            f' или текстовых каналов\n'
                            f'`{PREFIX}createm [v/t] name [start_num end_num]` - создам сразу несколько голосовых'
                            f' или текстовых каналов с приписками справа)\n'
                            f'`{PREFIX}deletem name [start_num end_num]`  - удалю каналы с приписками справа)\n'
                            f'`{PREFIX}del name`  - удалю канал с именем name)\n'
                            f'`{PREFIX}rename member_name new` - сменю ник\n'
                            f'`{PREFIX}kick member_name` - выкину нехорошего человека с сервера\n'
                            f'`{PREFIX}ban member_name` - забаню нехорошего человека\n'
                            f'`{PREFIX}unban member_name` - разбаню того, кто это заслужил\n',
                      inline=False)
        emb.add_field(name='Текстовые',
                      value=f'`{PREFIX}hello` - поприветствую тебя\n'
                            f'`{PREFIX}phrase` - не хочешь крутую фразочку?)\n'
                            f'`{PREFIX}here`  - отвечу тебе, если я тут)\n'
                            f'`{PREFIX}fact` - отправлю случайный факт из интернета\n'
                            f'`{PREFIX}quote` - отправлю цитату из интернета\n'
                            f'`{PREFIX}fuc`, `{PREFIX}f`  - хочешь факулечку?)\n'
                            f'`{PREFIX}me`, `{PREFIX}info`  - расскажу тебе факт обо мне\n'
                            f'`{PREFIX}status`, `{PREFIX}presence new`  - изменю свой статус на новый (для админов)\n',
                      inline=False)
        emb.add_field(name='Развлекающие',
                      value=f'`{PREFIX}dice n m` - брошу кубик c m-гранями n раз  \n'
                            f'`{PREFIX}choose c1 c2 ...` - выберу один из вариантов \n'
                            f'`{PREFIX}rand`, `{PREFIX}r`, `{PREFIX}random [startn endn]`'
                            '- выберу случайное число \n'
                            f'`{PREFIX}image`, `{PREFIX}img`, `{PREFIX}im`, `{PREFIX}i`'
                            ' - отправлю случайную картинку из интернета\n'
                            f'`{PREFIX}gif`, `{PREFIX}gff`, `{PREFIX}gf`'
                            ' - отправлю случайную gif - картинку из интернета\n'
                            f'`{PREFIX}girl`, `{PREFIX}g`'
                            ' - отправлю случайную картинку девушки из интернета\n'                            
                            f'`{PREFIX}anime`, `{PREFIX}a`'
                            ' - отправлю случайную картинку аниме-девушки из интернета\n',
                      inline=False)
        emb.add_field(name='Голосовые',
                      value=f'`{PREFIX}join` - подключусь к голосовому каналу\n'
                            f'`{PREFIX}leave` - покину голосовой канал\n'
                            f'`{PREFIX}playf file`, `{PREFIX}play_file file`,'
                            f' `{PREFIX}plf file` - проиграю файл, если он у меня есть)\n'
                            f'`{PREFIX}playnow link`, `{PREFIX}play_now link`,'
                            f' `{PREFIX}playn link`, `{PREFIX}pln link` - ТОЛЬКО ДЛЯ АДМИНОВ:'
                            f' проиграю файл по ссылке(с предзагрузкой)\n'
                            f'`{PREFIX}stream link`, `{PREFIX}strm link`- ТОЛЬКО ДЛЯ АДМИНОВ:'
                            f' проиграю файл по ссылке\n'
                            f'`{PREFIX}play link`, `{PREFIX}addp link`,'
                            f' `{PREFIX}pladd link`, `{PREFIX}ppl link` - добавлю файл в плейлист'
                            f' и проиграю его когда прийдёт его время)\n'
                            f'`{PREFIX}list`, `{PREFIX}pls` - покажу содержимое плейлиста)\n'
                            f'`{PREFIX}stop` - перестану проигрывать музыку\n'
                            f'`{PREFIX}volume level` - поменяю уровень громкости\n',
                      inline=False)

        # Отображаемый блок текста. name - Жирный крупный текст | value - обычный текст под "name"
        # | inline = True - Блоки текста будут в одну строку (https://prnt.sc/uogw2x) / inline = False -
        # Блоки текста будут один под другим (https://prnt.sc/uogx3t)
        emb.set_thumbnail(url=discord_bot.user.avatar_url)
        # emb.set_thumbnail - Добавляет картинку около текста
        # client.user.avatar_url - Отображает аватарку бота

        # emb.set_footer(icon_url=context.guild.owner.avatar_url,
        #                text=f'{context.guild.owner.name} !!!!')

        emb.set_footer(text='Удачки!)')

        # emb.set_thumbnail - Добавляет картинку под текстом
        # | ctx.guild.owner.avatar_url - Аватарка создателя сервера
        # | ctx.guild.owner.name - Имя создателя сервера

        await context.send(embed=emb)
        # Отправляет сообщение и так же преобразует emb в embed

        print(f'[Logs:info] Справка по командам была успешно выведена | {PREFIX}help ')

    # Adding functionality as  cogs
    discord_bot.add_cog(messaging_cog.MessagingCog(discord_bot))
    discord_bot.add_cog(entertainment_cog.EntertainmentCog(discord_bot))
    discord_bot.add_cog(voice_cog.VoiceCog(discord_bot))
    discord_bot.add_cog(manage_cog.ManageCog(discord_bot))
    discord_bot.run(TOKEN)
    print(f"Бот {SETTINGS['bot_name']}:{SETTINGS['id']} запущен")


start_bot()

# if __name__ == '__main__':
#     start_bot()
