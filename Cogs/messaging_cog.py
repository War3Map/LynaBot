import codecs
import random
from random import randint

import discord
import requests
from discord.ext import commands

import re

GREETINGS_DIC = {
    0: 'Привет, {name}!',
    1: 'Мне кажется, или я реально тебя вижу, {name}!',
    2: 'Приветушечки, {name}!',
    3: 'Не может быть! Это же {name}!',
    4: 'Хай, {name}!',
    5: 'Хеллоу, {name}!',
    6: 'Ого! {name} ли это? ',
    7: 'Рада тебя видеть, {name}!',
    8: 'Доброго дня, {name}!',
    9: 'Поприветствуйте, сам {name} почтил нас!',

}

RANDOM_FACT = [
    'Добрая рука, как лучик света!',
    'Няяя! Не нравится? Ну так не смотри!',
    'Мир да любовь!'

]

ABOUT = [
    'Я - Лина. Бот для дискорда.',
    'Мой создатель - Иван Моржов.',
    'Набери !help если хочешь узнать что я могу',
    'На латинском языке имя Лина означает «сирена»',
    'Моё любимое аниме - Bleach',
    'Мой любимый мужской персонаж - Ичимару Гин',
    'Мой любимый женский персонаж - Рукия Кучики'
]

FUCKS_LIST = [
    r'https://tenor.com/view/mr-bean-fuck-you-finger-middle-finger-fuck-off-gif-3528631',
    r'https://tenor.com/view/fuck-fuck-off-fuckity-pissed-off-gif-9736688',
    r'https://tenor.com/view/middlefinger-ryan-stiles-pocket-whose-gif-3863927',
    r'https://tenor.com/view/fuck-you-middle-finger-flipping-off-flip-off-jack-nicholson-gif-5326673',
    r'https://tenor.com/view/middle-finger-the-bird-flip-the-bird-flipping-the-bird-fuck-you-gif-5633646',
    r'.!.',


]

FACT_SITE = 'https://randstuff.ru/fact/'


def parse_html_to_fact():
    message = "К сожалению мне не удалось найти ничего интересного"
    response = requests.get(FACT_SITE)
    pattern = r"""<table[^>]*?>(.*?)<\/td>"""
    content = codecs.decode(response.content, 'UTF-8')
    searched_result = re.search(pattern, content)
    message_list = searched_result.group(0).split(">")
    if len(message_list) > 4:
        message = message_list[3].split("<")[0]
    return message


class MessagingCog(commands.Cog):
    """
    Messaging functionality for bot
    """
    discord_bot = None

    def __init__(self, bot):
        self.discord_bot = bot

    @commands.command()
    async def here(self, context):
        """Basic Testing command"""
        await context.send("Приветик! Я тут!")

    @commands.command(help="вежеливо поприветствую тебя")
    async def hello(self, context):  # Создаём функцию и передаём аргумент context.
        """Says hello to addressee"""
        author = context.message.author  # Объявляем переменную author и записываем туда информацию об авторе.
        greeting = GREETINGS_DIC[randint(0, len(GREETINGS_DIC))]
        await context.send(greeting.format(name=author.mention))

    @commands.command(help="случайная фраза")
    async def phrase(self, context):
        """Says random phrase"""
        response = random.choice(RANDOM_FACT)
        await context.send(response)

    @commands.command(help="случайный факт из интернета")
    async def fact(self, context):
        """Prints random fact"""
        await context.send(parse_html_to_fact())

    @commands.command(aliases=['fac', 'f'],
                      help="отправлю факулечки")
    async def fuc(self, context):
        """Sends a fuck sign gif"""
        await context.send(random.choice(FUCKS_LIST))

    @commands.command(aliases=['me', 'about'])
    async def info(self, context):
        """ Writes Info About Bot"""
        response = random.choice(ABOUT)
        await context.send(response)

    @commands.command(aliases=['presence', 'status'])
    @commands.has_role('admin')
    async def change_status(self, context, message):
        """ Changes bot status"""
        game = discord.Game(message)
        await self.discord_bot.change_presence(status=discord.Status.online, activity=game)

    @commands.Cog.listener()
    async def on_message(self, message):
        pass
