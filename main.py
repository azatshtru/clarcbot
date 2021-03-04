import discord
import process
import os

from PIL import Image
from io import BytesIO

client = discord.Client()

@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$wordle'):
        msg = message.content[8:]
        txt = process.process_text(msg)
        im = process.process_image(txt)

        with BytesIO() as output:
            im.save(output, format="PNG")
            output.seek(0)
            await message.channel.send(file=discord.File(output, 'wordle.png'))

client.run('TOKEN') #replace token with your own token