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
        if lootId > 7999:
            return
        
        # Get dict for this bag
        bag = loot[lootId][f'{lootId}']
        # Get rarity for this bag
        rareId = list(filter(lambda l: l['lootId'] == lootId, rare))[0]
        rareRank = rareId['rarest']
        rareScore = rareId['score']
        
        msg = discord.Embed(
            title = f'**Bag #{lootId}**', 
            description = f'Rarest {rareRank}, Score {rareScore}'
        )

        msg.add_field(
            name='-',
            value=('\n').join(list(bag.values())),
            inline=True
        )

        await message.channel.send(embed=msg)
        
with open("loot.json", "r") as fLoot:
    loot = json.load(fLoot)

with open("rare.json", "r") as fRare:
    rare = json.load(fRare)

client.run(SECRET)