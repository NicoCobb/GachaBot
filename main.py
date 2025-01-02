from typing import Final
import os
from dotenv import load_dotenv
from discord import Intents, Client, Message, app_commands, Interaction, Attachment, Object, File
from responses import bully_target_response
from random import randint
from dataManagement import save_user_gems, load_gems, save_new_image, attempt_create_json, load_star_total

#step 0: load our token from somewhere safe
load_dotenv()
TOKEN: Final[str] = os.getenv('DISCORD_TOKEN')
BULLY: Final[str] = os.getenv('BULLY_TARGET')
GUILD_ID: Final[int] = os.getenv('SERVER_ID')
ACCEPTED_FILE_TYPES = ['jpg', 'jpeg', 'png', 'mov', 'mp4']

#bot setup
intents: Intents = Intents.default()
intents.message_content = True
client: Client = Client(intents=intents)
tree = app_commands.CommandTree(client)

#message functionality
async def send_message(username: str, message: Message, user_message: str) -> None:
    if not user_message:
        print('Message was empty; intents not enabled')
        return
    
    if username == BULLY:
        if randint(1, 20) >= 18:
            try:
                response: str = bully_target_response()
                await message.add_reaction('👎')
                await message.channel.send(response)
            except Exception as e:
                print(e)
            return

#handling startup for bot
@client.event
async def on_ready() -> None:
    #check the correct folder system exists
    nested_folders = ['GachaImages/1',
                      'GachaImages/2',
                      'GachaImages/3',
                      'GachaImages/4',
                      'GachaImages/5']
    for folder in nested_folders:
        os.makedirs(folder, exist_ok=True)

    attempt_create_json()
    
    await tree.sync(guild=Object(id=GUILD_ID))
    print(f'{client.user} is now running!')

#handling incoming messages
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
#---------------------------------------------------------------------------------
@tree.command(
        name="add_gems",
        description="Give a user some number of gems (can also be negative)",
        guild=Object(id=GUILD_ID)
)
async def grant_gems(interaction: Interaction, user: str, added: int) -> None:
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

#TODO: add duplicate protection for V2.0
@tree.command(
        name="pull",
        description="PULLLLLLLLLLLLLLLLL!!!! costs 20 gems",
        guild=Object(id=GUILD_ID)
)
async def pull_image(interaction: Interaction) -> None:
    user = interaction.user.name
    print(user)
    currentGems = load_gems(user)
    if currentGems < 20:
        await interaction.response.send_message(f'you have {currentGems} and need at least 20!')
    else:
        save_user_gems(user, -20)
        star = randomize_star()
        total = load_star_total(star)
        while total == 0 and star > 0:
            star = star - 1
            total = load_star_total(star)

        if star == 0:
            await interaction.response.send_message('No images available!')
            return
        chosen = randint(1, total)
        #scan file extension possibilities
        for i in range(len(ACCEPTED_FILE_TYPES)):
            selectedFile = f"GachaImages/{star}/{chosen}.{ACCEPTED_FILE_TYPES[i]}"
            if os.path.isfile(selectedFile):
                break
        await interaction.response.send_message(f'{star} star!', file=File(selectedFile))
    

#TODO: addImage (takes in picture and star level)
@tree.command(
        name="add_media",
        description="Upload a new image or video and give it a star rating",
        guild=Object(id=GUILD_ID)
)
@app_commands.choices(star=[
    app_commands.Choice(name='⭐', value=1),
    app_commands.Choice(name='⭐⭐', value=2),
    app_commands.Choice(name='⭐⭐⭐', value=3),
    app_commands.Choice(name='⭐⭐⭐⭐', value=4),
    app_commands.Choice(name='🌟🌟🌟🌟🌟‼️‼️', value=5),
])
async def add_image(interaction: Interaction, file: Attachment, star: app_commands.Choice[int]) -> None:
    #func to check how many files exist of a given star rating for naming
    imageType = file.content_type.split('/')
    if not ('image' in imageType[0] or 'video' in imageType[0]):
        try:
            await interaction.response.send_message(f'attachment must be an image or video!')
        except Exception as e:
            print(e)
        return
    
    total = save_new_image(star.value)
    #hard code weird quicktime video thing
    if imageType[1] == 'quicktime':
        imageType[1] = 'mov'
    filename = f"{total}." + imageType[1]
    await file.save(fp="GachaImages/{}/{}".format(star.value,filename))
    try:
        await interaction.response.send_message(f'image added with star rating {star.value}!')
    except Exception as e:
        print(e)

@tree.command(
        name="roll_d20",
        description="roll a d20",
        guild=Object(id=GUILD_ID)
)
async def roll_d20(interaction: Interaction) -> None:
    try:
        await interaction.response.send_message(f'you rolled: {randint(1,20)}!')
    except Exception as e:
        print(e)

#end slash commands
#----------------------------------------------------------------------------------

def randomize_star() -> int:
    num = randint(1, 100)
    if num < 40:
        return 1
    if num >=40 and num < 65:
        return 2
    if num >=65 and num < 80:
        return 3
    if num >=80 and num < 91:
        return 4
    if num >=91:
        return 5

#main entry point
def main() -> None:
    client.run(token=TOKEN)

if __name__ == '__main__':
    main()