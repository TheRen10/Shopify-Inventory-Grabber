import discord
import json
import random
import time
import requests
from discord.ext.commands import Bot
from discord.ext import commands

intents = discord.Intents.all()
Client = discord.Client(intents=discord.Intents.default())
bot_prefix = "!"
client = commands.Bot(command_prefix=bot_prefix,intents=intents)

TOKEN = 'TOKEN HERE'

@client.event
async def on_ready():
    print("Stock Grabber online")
    print("name: {}".format(client.user.name))
    print("ID: {}".format(client.user.id))

@client.event
async def on_message(message):
    if message.content.startswith('!stock'):
        stock = []
        titles = []
        vars = []
        number = 0
        messageSplit = message.content.split(' ')
        channel = message.channel
        link = messageSplit[1]
        site = link.split('/')
        site = site[2]
        print(site)
        print(link+".json")
        r = requests.get(link+".json")
        r = r.json()
        prodname = r["product"]["title"]
        prodimage = r["product"] ["images"] [0] ["src"]
        for i in r["product"]["variants"]:
            id = i['id']
            vars.append(id)
            inventory_quantity = i['inventory_quantity']
            stock_number = int(inventory_quantity)
            if(stock_number < 0):
                stock_number = stock_number * -1
            number = number + stock_number
            inventory_quantity = str(stock_number)
            stock.append(inventory_quantity)
            title = i['title']
            titles.append(title)
        embed = discord.Embed(title="Stock Numbers, Total Stock: " + str(number), description=prodname, color=0xFF9900, url = "[link]")
        x = 0
        print(number)
        for i in titles:
            embed.add_field(name= "Size " + str(i) + " - " + str(stock[x]), value = "Variant: " + str(vars[x]), inline=True)
            x = x+1
        embed.set_thumbnail(url = prodimage)
        embed.set_footer(text = "Developed by: Renselling", icon_url="https://yt3.ggpht.com/ytc/AKedOLRmu9nwyXCjAXVBjDtS0QyTf5vY6aAZJlQvac2tCA=s900-c-k-c0x00ffffff-no-rj")
        await channel.send(embed = embed)

client.run(TOKEN)