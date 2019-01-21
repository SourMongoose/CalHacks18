import poker
import tokens
import discord
import asyncio

client = discord.Client()

@client.event
async def on_ready():
    await client.change_presence(game=discord.Game(name='with a fish'))
    print('Ready!')

@client.event
async def on_message(message):
    msg = message.content.lower()
    ch = message.channel
    au = message.author
    
    # ignore own messages
    if au.id == 536822424436473857:
        return
    
    if msg == 'hey':
        await ch.send('waddup')

client.run(tokens.bot_id)