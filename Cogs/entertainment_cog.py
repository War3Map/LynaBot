import random

import discord
from discord.ext import commands


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

    @commands.Cog.listener()
    async def on_message(self, message):
        pass
