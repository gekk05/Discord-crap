#!/usr/bin/python3
import discord
from discord_webhook import DiscordWebhook, DiscordEmbed

hook_endpoint = ""

alt_token = ""
client = discord.Client()
main_channel = ""       # Channel name to delete and remake

@client.event
async def on_ready():  #
    print(f'We have logged in as {client.user}')  # notification of login
    for guild in client.guilds: 
        for x in guild.channels     # Can probably derive guild channel object directly instead of iterating and comparing
            if x.name == main_channel:
                new_channel = await x.clone(name=x.name + "TEMP")       # Clones and deletes 
                await new_channel.edit(name=main_channel)
                await x.delete()

client.run(alt_token)


