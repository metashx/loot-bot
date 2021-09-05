import discord
from discord import activity
from discord.ext import tasks
from dotenv import load_dotenv
import os
import re
import json
import requests

load_dotenv()
SECRET = os.getenv('DISCORD_TOKEN')
CONTRACT = "0xff9c1b15b16263c61d017ee9f65c50e4ae0113d7"
XCONTRACT = "0x8bf2f876e2dcd2cae9c3d272f325776c82da366d"
OPENSEA_URL = f"https://opensea.io/assets"
OPENSEA_API = f"https://api.opensea.io/api/v1/asset"

lootIdPattern = re.compile("^#\d{1,5}$")

client = discord.Client()

@tasks.loop(minutes=10)
async def checkFloor():
    try:
        # Can't get floor via contract request so we check dummy asset
        response = requests.get(f'{OPENSEA_API}/{CONTRACT}/69')
        
        # Retrieve from response https://docs.opensea.io/reference/retrieving-a-single-asset
        price = response.json()
        price = price['collection']['stats']['floor_price']
        price = str(price)

        floorActivity = discord.Activity(name=f"Floor Ξ {price}", type=3)
        await client.change_presence(activity=floorActivity)
    except Exception as e:
        print(repr(e))

@checkFloor.before_loop
async def before_checkFloor():
    await client.wait_until_ready()

@client.event
async def on_message(message):
    if lootIdPattern.search(message.content):
        lootId = int(message.content[1:])
        if lootId < 1 or lootId > 16000:
            return

        isXloot = False if lootId < 8001 else True

        lootDict = loot if not isXloot else xloot
        rareDict = rare if not isXloot else xrare
        lootIdx = lootId if not isXloot else lootId - 8000
        lootContract = CONTRACT if not isXloot else XCONTRACT
        lootFooter = "" if not isXloot else "(Extension Loot)"

        # Get dict for this bag
        bag = lootDict[lootIdx-1][f'{lootId}']

        # Turn bag values into list, and order to match sales bot
        bagItems = [ 
            bag['weapon'], bag['chest'], bag['head'], bag['waist'], 
            bag['foot'], bag['hand'], bag['neck'], bag['ring']
        ]

        # Get rarity for this bag
        rareId = list(filter(lambda l: l['lootId'] == lootId, rareDict))[0]
        rareRank = rareId['rarest']
        
        msg = discord.Embed(
            title = f'**Bag #{lootId}**', 
            url=f'{OPENSEA_URL}/{lootContract}/{lootId}'
        )
        msg.add_field(
            name='—',
            value=('\n').join(bagItems),
            inline=True
        )
        msg.set_footer(text=f'Rarity Rank {rareRank} {lootFooter}')

        await message.channel.send(embed=msg)
        
with open("lib/dhof-loot/output/loot.json", "r") as f:
    loot = json.load(f)

with open("lib/dhof-loot/derivatives/extension-loot/output/xLoot.json", "r") as f:
    xloot = json.load(f)

with open("lib/dhof-loot/output/rare.json", "r") as f:
    rare = json.load(f)

with open("lib/dhof-loot/derivatives/extension-loot/output/probability.json", "r") as f:
    xrare = json.load(f)

checkFloor.start()
client.run(SECRET)