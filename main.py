from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message, File, app_commands, Interaction, Object
from responses import get_response, target_angela

#step 0: load our token from somewhere safe
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
BULLY: Final[str] = os.getenv('BULLY_TARGET')
GUILD_ID: Final[int] = os.getenv('SERVER_ID')

#step 1: bot setup
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)
tree = app_commands.CommandTree(client)

#TODO: when bot closes, need to save the gem count data to a txt file
gemCount:int = 0

#step 2: message functionality
async def send_message(username: str, message: Message, user_message: str) -> None:
    if not user_message:
        print('Message was empty; intents not enabled')
        return
    
    if username == BULLY:
        try:
            response: str = target_angela()
            await message.add_reaction('👎')
            await message.channel.send(response)
        except Exception as e:
            print(e)
        return

    if is_private:= user_message[0] == '?':
        user_message = user_message[1:]

    try:
        response: str = get_response(user_message)
        if response == 'asstarion':
            await message.channel.send(file=File('./gachaPullImages/asstarion.jpg'))
            return
        await message.add_reaction('❤')
        await message.author.send(response) if is_private else await message.channel.send(response)
    except Exception as e:
        print(e)

#step 3: handling startup for bot
@client.event
async def on_ready() -> None:
    await tree.sync(guild=Object(id=GUILD_ID))
    print(f'{client.user} is now running!')

#step 4: handling incoming messages
@client.event
async def on_message(message: Message) -> None:
    if message.author == client.user:
        return
    
    username: str = str(message.author)
    user_message: str = message.content
    channel: str = str(message.channel)

    print(f'[{channel}] {username}: "{user_message}"')

    await send_message(username, message, user_message)

#slash commands
@tree.command(
        name="get_gem",
        description="Add a gacha gem",
        guild=Object(id=GUILD_ID)
) 
async def add_gem(interaction: Interaction) -> None:
    global gemCount
    gemCount += 1
    try:
        await interaction.response.send_message(f'new gem count is {gemCount}!')
    except Exception as e:
        print(e)

#step 5: main entry point
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()