import os
import logging

from random import choice

import discord
import discord.ext.commands

from cogs import (
    messaging_cog,
    entertainment_cog,
    voice_cog,
    manage_cog
)

import additional.config_loader
from additional.config_loader import get_setting

# TODO: Сохранить в json и загружать из json
TOKEN = os.getenv("TOKEN")


# TODO: настроить логирование


def start_bot():
    """
    Starts a bot.
    """

    prefix = get_setting("PREFIX")
    # intents = discord.Intents.default()
    # intents.members = True

    discord_bot = discord.ext.commands.Bot(command_prefix=prefix,
                                           help_command=None,
                                           case_insensitive=True)
    bot_name = get_setting("BOT_NAME")

    bot_names = [bot_name]
    bot_names.extend(get_setting("ALTERNATIVE_NAMES"))

    appear_phrases = get_setting("APPEAR")


    @discord_bot.command()
    async def repeat(ctx, times: int, content='repeating...'):
        """Repeats a message multiple times."""
        for i in range(times):
            await ctx.send(content)

    @discord_bot.event
    async def on_ready():
        print(f'{discord_bot.user.name}: Бот готов к работе!')

    @discord_bot.event
    async def on_message(message):
        # no need to reply on own messages
        call_bot = False
        if message.author == discord_bot.user:
            return

        for name in bot_names:
            if name in message.content:
                call_bot = True
                break

        if call_bot:
            appear_phrase = choice(appear_phrases)
            await message.channel.send(appear_phrase)
        # run command processing
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

        print(f"{context.author.name} запросил справку!")
        # Отображает: ctx.author.name - Имя отправителя, ctx.author.avatar_url - Аватар отправителя
        emb.add_field(name='Управление каналом',
                      value=f'`{prefix}move user channel`  - перемещю пользователя в указанный канал)\n'
                            f'`{prefix}crtc name`  - создам новый текстовый канал с именем name)\n'
                            f'`{prefix}crvc name`  - создам новый голосовой канал с именем name)\n'
                            f'`{prefix}create [v/t] name,name1...`  - создам сразу несколько голосовых'
                            f' или текстовых каналов\n'
                            f'`{prefix}createm [v/t] name [start_num end_num]` - создам сразу несколько голосовых'
                            f' или текстовых каналов с приписками справа)\n'
                            f'`{prefix}deletem name [start_num end_num]`  - удалю каналы с приписками справа)\n'
                            f'`{prefix}del name`  - удалю канал с именем name)\n'
                            f'`{prefix}rename member_name new` - сменю ник\n'
                            f'`{prefix}kick member_name` - выкину нехорошего человека с сервера\n'
                            f'`{prefix}ban member_name` - забаню нехорошего человека\n'
                            f'`{prefix}unban member_name` - разбаню того, кто это заслужил\n',
                      inline=False)
        emb.add_field(name='Текстовые',
                      value=f'`{prefix}hello` - поприветствую тебя\n'
                            f'`{prefix}phrase` - не хочешь крутую фразочку?)\n'
                            f'`{prefix}here`  - отвечу тебе, если я тут)\n'
                            f'`{prefix}fact` - отправлю случайный факт из интернета\n'
                            f'`{prefix}quote` - отправлю цитату из интернета\n'
                            f'`{prefix}fuc`, `{prefix}f`  - хочешь факулечку?)\n'
                            f'`{prefix}me`, `{prefix}info`  - расскажу тебе факт обо мне\n'
                            f'`{prefix}status`, `{prefix}presence new`  - изменю свой статус на новый (для админов)\n',
                      inline=False)
        emb.add_field(name='Развлекающие',
                      value=f'`{prefix}dice n m` - брошу кубик c m-гранями n раз  \n'
                            f'`{prefix}choose c1 c2 ...` - выберу один из вариантов \n'
                            f'`{prefix}rand`, `{prefix}r`, `{prefix}random [startn endn]`'
                            '- выберу случайное число \n'
                            f'`{prefix}image`, `{prefix}img`, `{prefix}im`, `{prefix}i`'
                            ' - отправлю случайную картинку из интернета\n'
                            f'`{prefix}gif`, `{prefix}gff`, `{prefix}gf`'
                            ' - отправлю случайную gif - картинку из интернета\n'
                            f'`{prefix}girl`, `{prefix}g`'
                            ' - отправлю случайную картинку девушки из интернета\n'
                            f'`{prefix}anime`, `{prefix}a`'
                            ' - отправлю случайную картинку аниме-девушки из интернета\n',
                      inline=False)
        emb.add_field(name='Голосовые',
                      value=f'`{prefix}join` - подключусь к голосовому каналу\n'
                            f'`{prefix}leave` - покину голосовой канал\n'
                            f'`{prefix}playf file`, `{prefix}play_file file`,'
                            f' `{prefix}plf file` - проиграю файл, если он у меня есть)\n'
                            f'`{prefix}playnow link`, `{prefix}play_now link`,'
                            f' `{prefix}playn link`, `{prefix}pln link` - ТОЛЬКО ДЛЯ АДМИНОВ:'
                            f' проиграю файл по ссылке(с предзагрузкой)\n'
                            f'`{prefix}stream link`, `{prefix}strm link`- ТОЛЬКО ДЛЯ АДМИНОВ:'
                            f' проиграю файл по ссылке\n'
                            f'`{prefix}play link`, `{prefix}addp link`,'
                            f' `{prefix}pladd link`, `{prefix}ppl link` - добавлю файл в плейлист'
                            f' и проиграю его когда прийдёт его время)\n'
                            f'`{prefix}list`, `{prefix}pls` - покажу содержимое плейлиста)\n'
                            f'`{prefix}stop` - перестану проигрывать музыку\n'
                            f'`{prefix}volume level` - поменяю уровень громкости\n',
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

        print(f'[Logs:info] Справка по командам была успешно выведена | {prefix}help ')

    # Adding functionality as  cogs
    discord_bot.add_cog(messaging_cog.MessagingCog(discord_bot))
    discord_bot.add_cog(entertainment_cog.EntertainmentCog(discord_bot))
    discord_bot.add_cog(voice_cog.VoiceCog(discord_bot))
    discord_bot.add_cog(manage_cog.ManageCog(discord_bot))
    discord_bot.run(TOKEN)

    cog = discord_bot.get_cog('MessagingCog')
    commands = cog.get_commands()
    print([c.name for c in commands])

    bot_id = get_setting("ID")
    print(f"Бот {bot_name}:{bot_id} запущен!")


start_bot()

# if __name__ == '__main__':
#     start_bot()
