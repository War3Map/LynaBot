import random
from random import randint

import discord
from discord.ext import commands
from additional.config_loader import get_setting
from additional.web_parser import get_info_from_url, parse_from_html_test, get_quote_result, get_fact_result

GREETINGS = get_setting("GREETINGS")
RANDOM_FACTS = get_setting("RANDOM_FACTS")
ABOUT_FACTS = get_setting("ABOUT_FACTS")
ALIVE_PHASES = get_setting("ALIVE_PHASES")
FUCKS_LIST = get_setting("FUCKS_LIST")
BOT_INFO = get_setting("BOT_INFO")
FACT_SITE = get_setting("FACT_SITE")
QUOTE_SITE = get_setting("QUOTE_SITE")


def choice_random_phrase(pharases: list):
    """Choices random phrase from list"""
    return random.choice(pharases)


class MessagingCog(commands.Cog):
    """
    Messaging functionality for bot
    """
    discord_bot = None

    def __init__(self, bot):
        self.discord_bot = bot

    @commands.command(aliases=['lyna'])
    async def here(self, context):
        """Basic Testing command"""
        await context.send(choice_random_phrase(ALIVE_PHASES))

    @commands.command(help="вежеливо поприветствую тебя")
    async def hello(self, context):  # Создаём функцию и передаём аргумент context.
        """Says hello to addressee"""
        # Объявляем переменную author и записываем туда информацию об авторе.
        author = context.message.author
        random_phrase = choice_random_phrase(GREETINGS)
        greeting = random_phrase.format(name=author.mention)
        await context.send(greeting)

    @commands.command(help="случайная фраза")
    async def phrase(self, context):
        """Says random phrase"""
        response = random.choice(ABOUT_FACTS)
        await context.send(response)

    @commands.command(help="случайный факт из интернета", aliases=['ft'])
    async def fact(self, context):
        """Prints random fact"""
        # info = parse_from_html_test(get_fact_result, FACT_SITE)
        info = await get_info_from_url(FACT_SITE, "fact")
        await context.send(info)
                
    @commands.command(help="цитата из интернета", aliases=['q'])
    async def quote(self, context):
        """Prints random quote"""
        info = await get_info_from_url(QUOTE_SITE, "quote")
        await context.send(info)

    @commands.command(aliases=['fac', 'f'],
                      help="отправлю факулечки")
    async def fuc(self, context, count=1):
        """Sends a fuck sign gif"""
        for _ in range(count):
            await context.send(random.choice(FUCKS_LIST))

    @commands.command(aliases=['me', 'about'])
    async def info(self, context):
        """ Writes Info About Bot"""
        response = random.choice(BOT_INFO)
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
