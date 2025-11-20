import logging
import random
import datetime

import discord
from discord.ext import commands

import credentials

bot = commands.Bot(command_prefix='!wirus ', intents=discord.Intents.all())
logging.basicConfig(filename='logs',
                    filemode='a',
                    format='%(asctime)s,%(msecs)03d %(name)s %(levelname)s %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG)


@bot.event
async def on_ready():
    print(f"Wirus.exe just started at {datetime.datetime.now()}")

    channel = bot.get_channel(credentials.TEST_CHANNEL)
    await channel.send(f"Wirus.exe just started at {datetime.datetime.now()}")


@bot.command()
async def ugryź(ctx, user_id = None):
    channel = ctx.channel
    flavour_text = ''
    emoji = '😼'
    if random.randint(1,10) < 3:
        user_id = ctx.author
        flavour_text = 'Próbował_ś kogoś ugryźć, ale się nie udało! Wirus ugryzł Cb!\n'
    elif user_id is None:
        user_id = random.choice(channel.guild.members)
        print(user_id, bot.user)
        if user_id == bot.user:
            flavour_text = 'Coś poszło nie tak, ten gamoń ugryzł sam sb! \n'
            emoji = '🙀'
    await channel.send(f'{flavour_text}ugryzłem {user_id.mention} {emoji}')

if __name__ == "__main__":
    bot.run(credentials.BOT_TOKEN)
