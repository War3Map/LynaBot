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