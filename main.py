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
        lootItems = loot[lootId]
        lootItems = json.dumps(lootItems, indent=4)
        await message.channel.send(lootItems)
        
with open("loot.json", "r") as f:
    loot = json.load(f)

client.run(SECRET)