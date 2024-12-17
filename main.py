from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message, File, app_commands, Interaction, Attachment, Object
from responses import get_response, target_angela
from dataManagement import save_user_gems, load_gems

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
        # if response == 'asstarion':
        #     await message.channel.send(file=File('./gachaPullImages/asstarion.jpg'))
        #     return
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
#TODO: have it also take in a target user
@tree.command(
        name="grant_gems",
        description="Give a user some number of gems (can also be negative)",
        guild=Object(id=GUILD_ID)
) 
async def grant_gems(interaction: Interaction, user: str, added: int) -> None:
    print('is anything print???:::?')
    gemCount = save_user_gems(user, added)
    try:
        await interaction.response.send_message(f'new gem count is {gemCount}!')
    except Exception as e:
        print(e)

@tree.command(
        name="check_gems",
        description="check a users gem count",
        guild=Object(id=GUILD_ID)
)
async def check_gems(interaction: Interaction, user: str) -> None:
    gemCount = load_gems(user)
    try:
        await interaction.response.send_message(f'User {user} has {gemCount} gems!')
    except Exception as e:
        print(e)

#TODO: pull
#each pull will need 20 gems

#TODO: addImage (takes in picture and star level)
@tree.command(
        name="add_image",
        description="Upload a new image and give it a star rating",
        guild=Object(id=GUILD_ID)
)
async def add_image(interaction: Interaction, file: Attachment, star: int) -> None:
    try:
        await interaction.response.send_message(f'image added with star rating {star}!')
    except Exception as e:
        print(e)

#TODO: dailyLogin (2 gems)

#TODO: roll_d20

#step 5: main entry point
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()