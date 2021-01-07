import codecs
import random
import re

import discord
import requests

from discord.ext import commands
from bs4 import BeautifulSoup


ANIME_IMAGE_URL = 'https://animepicsx.net/random'

RANDOM_IMAGE_SITE = 'https://www.generatormix.com'
GIRL_URL = 'https://www.generatormix.com/random-beautiful-women'
RIMAGE_URL = 'https://www.generatormix.com/random-image-generator'


def get_image():
    message = "К сожалению мне не удалось найти ничего интересного"

    response = requests.get(RIMAGE_URL)

    soup = BeautifulSoup(response.text, 'lxml')
    res = soup.find_all("img", class_="lazy thumbnail")
    
    if res is None:
        return message

    for image in res:
        message = image['data-src']
        break

    return message


def get_anime_image():
    message = "К сожалению мне не удалось найти ничего интересного"

    response = requests.get(ANIME_IMAGE_URL)
    soup = BeautifulSoup(response.text, 'lxml')
    res = soup.find_all("a", class_="_random_pic")
    if res is None:
        return message

    soup = BeautifulSoup(str(res), 'lxml')
    res = soup.find_all("img")
    for image in res:
        message = image['src']

    # way 2
    # src_element = re.search('src="(.*?)"', str(res))
    # src_parts = src_element.group(0).split('"')
    # if len(src_parts) == 3:
    #     message = src_parts[1]

    # print(res)
    # content = codecs.decode(response.content, 'UTF-8')

    return message


def get_girl_image():
    message = "К сожалению мне не удалось найти ничего интересного"

    response = requests.get(GIRL_URL)
    soup = BeautifulSoup(response.text, 'lxml')
    res = soup.find_all("img", class_='lazy thumbnail aspect-tall-contain')
    if res is None:
        return message

    image_list = list()
    for image in res:
        # print(str(image))
        image_list.append(image['data-src'])
    message = random.choice(image_list)

    return RANDOM_IMAGE_SITE + message


class EntertainmentCog(commands.Cog):
    """
    Entertainment bot functions
    """
    discord_bot = None

    def __init__(self, bot):
        self.discord_bot = bot

    @commands.command(help='Брошу кубик столько раз сколько попросите=)')
    async def dice(self, context, number_of_dice: int, number_of_sides: int):
        dice_result = [
            str(random.choice(range(1, number_of_sides + 1)))
            for _ in range(number_of_dice)
        ]
        await context.send(', '.join(dice_result))

    @commands.command(description='For when you wanna settle the score some other way')
    async def choose(self, context, *choices: str):
        """Chooses between multiple choices."""
        await context.send(random.choice(choices))

    @commands.command(aliases=['rand', 'r'],
                      description='For when you wanna settle the score some other way')
    async def random(self, context, start_num=0, end_num=100):
        """Generates random number from start_num to end_num(exclude)"""
        await context.send(random.randint(start_num, end_num))

    @commands.command(aliases=['img', 'im', 'i'],
                      description='Отправлю случайную аниме картинку')
    async def image(self, context, start_num=0, end_num=100):
        """Gets random image from RIMAGE_URL"""
        await context.send(get_image())

    @commands.command(aliases=['a', 'anime', 'waifu', 'w'],
                      description='Отправлю случайную аниме картинку c девушкой')
    async def anime_image(self, context, start_num=0, end_num=100):
        """Gets random image from ANIME_IMAGE_URL"""
        await context.send(get_anime_image())

    @commands.command(name="girl",
                      aliases=['g'],
                      description='Отправлю случайную картинку')
    async def girl_image(self, context, start_num=0, end_num=100):
        """Gets random image from GIRL_URL"""
        await context.send(get_girl_image())

    @commands.Cog.listener()
    async def on_message(self, message):
        pass
