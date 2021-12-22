import discord
from discord_webhook import DiscordWebhook, DiscordEmbed

HOOK_ENDPOINT = ""      # Webhook of another Discord channel to bridge the messages into
DISC_TOKEN = ""         # Discord token of account within server
client = discord.Client()
ANNOYING_PEOPLE = []    # List of user IDs of annoying people to translate messages into "Spongebob talk"
DISC_SERVERS = []       # List of discord server IDs that you would like to log

@client.event
async def on_ready():
    print(f'Bridging as {client.user}')


@client.event
async def on_message(message):

        url = "https://cdn.discordapp.com/avatars/{}/{}".format(str(message.author.id), message.author.avatar)
        author = message.author
        content = "{}".format(message.clean_content)
        
if message.channel.id in DISC_SERVERS:
        if message.author.id in ANNOYING_PEOPLE:
            string_manipulated = ''
            special_cases = '!@?# '
            count = 0
            for i in content:
                if i in special_cases:
                    string_manipulated+=i
                    continue
                if count % 2 == 0:
                    string_manipulated+=i.lower()
                    count +=1
                else:
                    string_manipulated+=i.upper()
                    count +=1
            content = string_manipulated

        x = DiscordWebhook(url=HOOK_ENDPOINT, username=str(message.author).split("#")[0], content=content, avatar_url=url)
        x.execute()




client.run(DISC_TOKEN)
