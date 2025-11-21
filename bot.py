import csv
import datetime
import logging
import random

import discord
from discord.ext import commands

import credentials

bot = commands.Bot(command_prefix="!wirus ", intents=discord.Intents.all())
logging.basicConfig(
    filename="logs",
    filemode="a",
    format="%(asctime)s,%(msecs)03d %(name)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    level=logging.DEBUG,
)

# Load bites.csv to memory
bites = dict()
with open("bites.csv", newline="") as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        bites.update({row["user"]: int(row["count_of_bites"])})
    print(bites)


def update_bites_csv():
    with open("bites.csv", "w", newline="") as csvfile:
        fieldnames = ["user", "count_of_bites"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for user, count_of_bites in bites.items():
            writer.writerow({fieldnames[0]: user, fieldnames[1]: count_of_bites})


@bot.event
async def on_ready():
    print(f"Wirus.exe just started at {datetime.datetime.now()}")
    channel = bot.get_channel(credentials.TEST_CHANNEL)
    await channel.send(f"Wirus.exe just started at {datetime.datetime.now()}")


@bot.command()
async def ugryź(ctx, user_id: discord.Member = None):
    # Set variables
    flavour_text = ""
    emoji = "😼"
    print(user_id)

    # Choose user to bite
    if random.randint(1, 10) < 3:
        # 1 in 5 chance that bot will bite the sender instead of target
        user_id = ctx.author
    elif user_id is None:
        user_id = random.choice(ctx.guild.members)

    # Change flavour_text and/or emoji based on scenarios
    if user_id == bot.user:
        flavour_text = "Coś poszło nie tak, ten gamoń ugryzł sam sb! \n"
        emoji = "🙀"

    if user_id == ctx.author:
        flavour_text = "Próbował_ś kogoś ugryźć, ale się nie udało! Wirus ugryzł Cb!\n"

    # Check if this user was bitten before, if not add them to directory
    # If they exist increment amount of bites
    if user_id.name in bites.keys():
        bites[user_id.name] += 1
    else:
        bites.update({user_id.name: 1})

    # Save bites to file
    update_bites_csv()

    # Send messages
    await ctx.send(f"{flavour_text}ugryzłem {user_id.mention} {emoji}")
    await ctx.send(f"W sumie ugryzłem tego użytkownika już: {bites[user_id.name]}")


@bot.command()
async def ugryź_scoreboard(ctx):
    embed = discord.Embed(
        title="Najcześciej gryzione osoby",
        description="Scoreboard najczęściej gryzionych osób, wyniki dzielone są miedzy serwerami.",
        colour=0xE1E100,
    )
    embed.set_author(name="Wirus")
    place = 1
    sorted_bits = dict(sorted(bites.items(), reverse=True, key=lambda item: item[1]))
    for user, count_of_bites in sorted_bits.items():
        match place:
            case 1:
                place_print = "🥇"
            case 2:
                place_print = "🥈"
            case 3:
                place_print = "🥉"
            case _:
                place_print = str(place) + "."
        embed.add_field(
            name=f"**{place_print} {user}** - Ugryziona_ny: {count_of_bites}",
            value="",
            inline=False,
        )
        place += 1
        if place > 15:
            break
    await ctx.send(embed=embed)


@bot.event
async def on_command_error(ctx: commands.Context, error: commands.CommandError):
    # Dumb little event, that just sends back any error as a message
    await ctx.send(f"Error: {error}")


if __name__ == "__main__":
    bot.run(credentials.BOT_TOKEN)
