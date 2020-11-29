import discord
from discord.ext import commands
from datetime import datetime
import asyncio
import json
import os

TOKEN = ""
basedir = os.path.abspath(os.path.dirname(__file__))
# open dictionary json
with open(basedir + "/birthdays.json", "r+") as myfile:
    birthday_data = json.load(myfile)
# initalise bot
intents = discord.Intents.default()
intents.members = True
client = commands.Bot(command_prefix='>', case_insensitive=True, intents=intents)


@client.command()
async def love(context):
    await context.send("I love you guys :heart:")


@client.command()
async def saoie(context):
    await context.send("Nana's wife <:saoiePeek:759791733490843648>")


@client.command()
async def nana(context):
    await context.send('Did you know Nana is awesome, ' + format(context.author.mention) + "?")


@client.command(pass_context=True)
@commands.has_permissions(manage_roles=True, ban_members=True)
async def addbirthday(context, user, birthday):
    add_json = {user: birthday}
    with open(basedir + "/birthdays.json", "r+") as myfile:
        data = json.load(myfile)
        data.update(add_json)
        myfile.seek(0)
        json.dump(data, myfile)
    await context.send("You added {}'s birthday on {}".format(user, birthday))


@client.command()
@commands.has_permissions(manage_roles=True, ban_members=True)
async def purgebirthdays(context):
    for guild in client.guilds:
        for member in guild.members:
            ids = [member.id for member in guild.members]
    with open(basedir + "/birthdays.json") as myfile:
        data = json.load(myfile)
        for entry in list(data.items()):
            if int(entry[0][3:-1]) not in ids:
                data.pop(entry[0], entry[1])
    with open('basedir + "/birthdays.json"', 'w') as w:
        w.write(json.dumps(data))
    await context.send("You purged the birthday list")


@client.command()
async def birthdaylist(context):
    with open(basedir + "/birthdays.json") as myfile:
        data = json.load(myfile)
        bdays = ""
        for entry in data.items():
            bdays += str(entry[0] + " - " + entry[1] + "\n")
        myEmbed = discord.Embed(title="Birthday list", description=bdays)
        await context.send(embed=myEmbed)


@client.command(pass_context=True)
@commands.has_permissions(manage_roles=True, ban_members=True)
async def deleteone(context, user):
    with open(basedir + "/birthdays.json") as myfile:
        data = json.load(myfile)
        for entry in list(data.items()):
            if entry[0] == user:
                data.pop(entry[0], entry[1])
    with open(basedir + "/birthdays.json", 'w') as w:
        w.write(json.dumps(data))
        await context.send("deleted" + user)


@client.command()
async def commands(context):
    myEmbed = discord.Embed(title="Commandlist", description="These are the commands! \nIf you're struggling to @user you can right click their name and get their id make sure you wrap it like this <@!########>")
    myEmbed.add_field(name="addbirthday", inline=False, value="Adds one birthday to the list use this format '>addbirthday @user ##/##' make sure you tag user")
    myEmbed.add_field(name="birthdaylist", inline=False, value="Displays a list of all users currently added to the list")
    myEmbed.add_field(name="deleteone", inline=False, value="Delete one user from the list use this format'>deleteone @user' make sure you tag user")
    myEmbed.add_field(name="purgebirthdays", inline=False, value="Deletes all birthdays of users who have left the server")
    await context.send(embed=myEmbed)


async def checktime():
    general_channel = client.get_channel(724338025902899354)
    now = datetime.utcnow()
    current_time = now.strftime("%d/%m-%H:%M:%S")
    for entry in birthday_data.items():
        if current_time == entry[1] + "-01:00:00":
            entryid = entry[0]
            myEmbed = discord.Embed(title=" :confetti_ball: HAPPY BIRTHDAY :confetti_ball: ", description="SamihBot loves you " + entryid + " :heart: and wishes you the happiest of birthdays! May you achieve all your dreams and your next year be <:PogChamp:734092872655175730> \nHere have some cake :cake:\n <:atpRtsd:733675921369858190> ", color=0x89DAFF)
            await general_channel.send(embed=myEmbed)


async def background_tasks():
    await client.wait_until_ready()
    while not client.is_closed():
        try:
            await checktime()
            await asyncio.sleep(1)
        except Exception as e:
            print(str(e))
            await asyncio.sleep(20)

client.loop.create_task(background_tasks())
client.run(TOKEN)
