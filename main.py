import discord
import random
import aiohttp
from config import TOKEN, WEATHER_API_KEY, GOOGLE_API_KEY, SEARCH_ID
from googleapiclient.discovery import build
from discord import app_commands
from discord.app_commands import Choice
from discord.ext import commands
from eightBall import chooses_answer
from openai_functions import chatgpt_response 
from choices import map_list, nade_list, team_list , game_list


bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())

@bot.event
async def on_ready():
    print(f'{bot.user} is now running')
    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} command(s)')
    except Exception as e:
        print(e)
    

@bot.tree.command(name='magic_8_ball', description='Ask a question to the magic 8 ball')
@app_commands.describe(question = 'Type in your question')
async def magic_8_ball(interaction: discord.Interaction, question: str): 
    await interaction.response.send_message(f"`{interaction.user.display_name}'s question is: {question}`\n{chooses_answer()}")


@bot.tree.command(name='dice_roller', description='Roll a dice')
@app_commands.describe(sides = 'Type in how many sides you wish your dice to have')
async def dice_roller(interaction: discord.Interaction, sides: int): 
    await interaction.response.send_message(f"`{interaction.user.display_name} rolls a {sides} sided dice:`\n{random.randint(1,sides)}")


@bot.tree.command(name='help', description='Learn how to use the bot and its features')
async def help(interaction: discord.Interaction): 
    await interaction.response.send_message(f"Hello, this is JohnnyBot!\nFor a list of commands, type `/commands`",ephemeral=True)


@bot.tree.command(name='commands', description="List of bot's commands")
async def command_list(interaction: discord.Interaction): 
    await interaction.response.send_message(f"`/help\n/magic_8_ball\n/dice_roller\n/coin_flip\n/weather\n/image_search\n/chug\n/patch_notes\n/nades`",ephemeral=True)


flip = ["Heads","Tails"]
@bot.tree.command(name='coin_flip', description="Flip a coin")
async def coin_flip(interaction: discord.Interaction): 
    await interaction.response.send_message(f"`{interaction.user.display_name} flips a coin:`\n{random.choice(flip)}")


@bot.tree.command(name='weather', description="Weather report")
@app_commands.describe(city = 'Enter city or zip code')
async def weather(interaction: discord.Interaction, city: str): 
    url = "http://api.weatherapi.com/v1/current.json"
    params = {"key": WEATHER_API_KEY, "q": city}
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as res:
            data = await res.json()
            location = data["location"]["name"]
            temp_c = data["current"]["temp_c"]
            temp_f = data["current"]["temp_f"]
            humidity = data["current"]["humidity"] 
            wind_kph = data["current"]["wind_kph"] 
            wind_mph = data["current"]["wind_mph"] 
            condition = data["current"]["condition"]["text"]
            uv = data["current"]["uv"]
            feelslike_c = data["current"]["feelslike_c"]
            feelslike_f = data["current"]["feelslike_f"]
            cloud = data["current"]["cloud"]
            image_url = "http:" + data["current"]["condition"]["icon"]
            embed = discord.Embed(title=f"Weather for {location}", description=f"The condition in `{location}` is `{condition}`")
            embed.add_field(name="Temperature", value=f"C: {temp_c} | F: {temp_f}")
            embed.add_field(name="Feels Like", value=f"C: {feelslike_c} | F: {feelslike_f}") 
            embed.add_field(name="Winds Speeds", value=f"KPH: {wind_kph} | MPH: {wind_mph}", inline=False)
            embed.add_field(name="Humidity", value=f"{humidity}%", inline=False)
            embed.add_field(name="Cloud Cover", value=f"{cloud}%", inline=False)
            embed.add_field(name="UV Index", value=f"{uv}", inline=False)
            embed.set_thumbnail(url=image_url)
            await interaction.response.send_message(embed=embed)


@bot.tree.command(name='image_search', description="Search for a image")
@app_commands.describe(image = 'Look up an image')
async def image_search(interaction: discord.Interaction, image: str,):
    ran = random.randint(0,9)
    resource = build("customsearch", "v1", developerKey=GOOGLE_API_KEY).cse()
    result = resource.list(q=f"{image}", cx=SEARCH_ID, searchType="image").execute()
    url = result["items"][ran]["link"]
    embed1 = discord.Embed(title=f"{image.title()}")
    embed1.set_image(url=url)
    await interaction.response.send_message(embed=embed1)


@bot.tree.command(name='chug', description="Your favorite BandLab producer")
async def chug(interaction: discord.Interaction): 
    await interaction.response.send_message("https://www.bandlab.com/the_chug_mindoysh")

@app_commands.choices(game = game_list)
@bot.tree.command(name='patch_notes', description="Latest patch notes for your favorite games")
@app_commands.describe(game = 'Pick a game')
async def patch_notes(interaction: discord.Interaction, game: str): 
    if game == 'CS2':
        await interaction.response.send_message("https://www.counter-strike.net/news/updates")
    elif game == 'Overwatch':
        await interaction.response.send_message("https://overwatch.blizzard.com/en-us/news/patch-notes/")
    elif game == 'Rocket League':
        await interaction.response.send_message("https://www.rocketleague.com/news/?cat=7-5aa1f33-rqfqqm")
    elif game == 'League of Legends':
        await interaction.response.send_message("https://www.rocketleague.com/news/?cat=7-5aa1f33-rqfqqm")
    elif game == 'OSRS':
        await interaction.response.send_message("https://secure.runescape.com/m=news/archive?oldschool=1")
    elif game == 'CSGO':
        await interaction.response.send_message("https://blog.counter-strike.net/index.php/category/updates/")
    elif game == 'Valorant':
        await interaction.response.send_message("https://playvalorant.com/en-gb/news/tags/patch-notes/")
    elif game == 'Apex Legends':
        await interaction.response.send_message("https://www.ea.com/games/apex-legends/news#game-updates")
    elif game == 'Fortnite':
        await interaction.response.send_message("https://www.fortnite.com/news")
    elif game == 'Rainbow Six Siege':
        await interaction.response.send_message("https://www.ubisoft.com/en-us/game/rainbow-six/siege/news-updates?category=patch-notes")
    elif game == 'Final Fantasy XIV':
        await interaction.response.send_message("https://na.finalfantasyxiv.com/lodestone/special/patchnote_log/")
    elif game == 'World of Warcraft':
        await interaction.response.send_message("https://worldofwarcraft.blizzard.com/en-us/content-update-notes")
    elif game == 'Genshin Impact':
        await interaction.response.send_message("https://genshin.hoyoverse.com/en/news")
    elif game == 'Honkai Star Rail':
        await interaction.response.send_message("https://hsr.hoyoverse.com/en-us/news?type=notice")
    

@app_commands.choices(map = map_list, team = team_list, nade = nade_list)
@bot.tree.command(name='nades', description="CS2 nade lineups")
@app_commands.describe(map = 'Choose map',team = 'Choose team', nade='Choose nade type')
async def nades(interaction: discord.Interaction, map: str, team: str, nade: str): 
    await interaction.response.send_message(f"`Map = {map}`\n`Team = {team}`\n`Nade = {nade}`\nhttps://www.csgonades.com/maps/{map}?team={team}&type={nade}")


#@bot.tree.command(name='chat_gpt', description='Get a response from Chat GPT')
#@app_commands.describe(prompt = 'Enter your prompt')
#async def chat_gpt(interaction: discord.Interaction, prompt: str): 
    #await interaction.response.send_message(f"{chatgpt_response(prompt=prompt)}")







bot.run(TOKEN)