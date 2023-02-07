import os
import logging
import random

from random import choice

import discord
import discord.ext.commands

from cogs import (
    messaging_cog,
    entertainment_cog,
    voice_cog,
    manage_cog,
    field_of_dream_cog
)

import additional.config_loader
from additional.config_loader import get_setting

TOKEN = os.getenv("TOKEN")
DREAM_HELP = "".join(get_setting("DREAM_HELP"))
MANAGE_HELP = "".join(get_setting("MANAGE_HELP"))
TEXT_HELP = "".join(get_setting("TEXT_HELP"))
ENTERTAINMENT_HELP = "".join(get_setting("ENTERTAINMENT_HELP"))
VOICE_HELP = "".join(get_setting("VOICE_HELP"))
APPEARS = get_setting("APPEAR")
WELCOME_CHAT_ID = get_setting("WELCOME_CHAT_ID")


# TODO: настроить логирование
def log_exp(info: str):
    """
    Temp func for logging
    :param info:
    :return:
    """
    print(info)


async def send_welcome_to_channel(bot: discord.ext.commands.Bot):
    """
    Set welcome message to chat in config
    :param bot:
    :return:
    """
    channel = bot.get_channel(WELCOME_CHAT_ID)
    random_welcome = random.choice(APPEARS)
    await channel.send(random_welcome)


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
        try:
            await send_welcome_to_channel(discord_bot)
        except Exception as ex:
            log_exp(f'Сообщение не отправлено в чат{ex}')

        log_exp(f'{discord_bot.user.name}: Бот готов к работе!')

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

        author = context.author.name
        emb.set_author(name=author, icon_url=context.author.avatar_url)

        # print(f"{author} запросил справку!")
        # Отображает: ctx.author.name - Имя отправителя, ctx.author.avatar_url - Аватар отправителя
        emb.add_field(name='Управление каналом',
                      value=MANAGE_HELP.format(prefix=prefix),
                      inline=False)
        emb.add_field(name='Текстовые',
                      value=TEXT_HELP.format(prefix=prefix),
                      inline=False)
        emb.add_field(name='Развлекающие',
                      value=ENTERTAINMENT_HELP.format(prefix=prefix),
                      inline=False)
        emb.add_field(name='Голосовые',
                      value=VOICE_HELP.format(prefix=prefix),
                      inline=False)
        emb.add_field(name='Игра поле чудес',
                      value=DREAM_HELP.format(prefix=prefix),
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
    discord_bot.add_cog(field_of_dream_cog.DreamGameCog(discord_bot))
    try:
        discord_bot.run(TOKEN)
    except RuntimeError:
        print("Бот выключен")

    # cog = discord_bot.get_cog('MessagingCog')
    # commands = cog.get_commands()
    # print([c.name for c in commands])
    #
    # bot_id = get_setting("ID")
    # print(f"Бот {bot_name}:{bot_id} запущен!")


start_bot()

# if __name__ == '__main__':
#     start_bot()
