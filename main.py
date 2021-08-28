import discord
from dotenv import load_dotenv
import os
import re
import json

load_dotenv()
SECRET = os.getenv('DISCORD_TOKEN')
lootIdPattern = re.compile("^#\d{1,4}$")

client = discord.Client()

@client.event
async def on_message(message):
    if lootIdPattern.search(message.content):
        lootId = int(message.content[1:])
        if lootId < 1 or lootId > 8000:
            return
        
        # Get dict for this bag
        bag = loot[lootId-1][f'{lootId}']

        # Turn bag values into list, and order to match sales bot
        bagItems = [ 
            bag['weapon'], bag['chest'], bag['head'], bag['waist'], 
            bag['foot'], bag['hand'], bag['neck'], bag['ring']
        ]

        # Get rarity for this bag
        rareId = list(filter(lambda l: l['lootId'] == lootId, rare))[0]
        rareRank = rareId['rarest']
        
        msg = discord.Embed(title = f'**Bag #{lootId}**')
        msg.add_field(
            name='-',
            value=('\n').join(bagItems),
            inline=True
        )
        msg.set_footer(text=f'Rarity Rank {rareRank}')

        await message.channel.send(embed=msg)
        
with open("loot.json", "r") as fLoot:
    loot = json.load(fLoot)

with open("rare.json", "r") as fRare:
    rare = json.load(fRare)

client.run(SECRET)