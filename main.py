
##################################################################################
# IMPORTATIONS
##################################################################################

import requests
import json
from dotenv import load_dotenv
import os
from openai import OpenAI
import discord
from discord.ext import commands
import logging
import random

##################################################################################
# CONFIGURATION DOTENV
##################################################################################
load_dotenv()



# Initialiser le client OpenAI
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)



############
    
token = os.getenv("TOKEN")

intents = discord.Intents.default() # Creating default intents
intents.members = True
intents.message_content = True # Giving our bot permission to send and read messages


logger = logging.getLogger(__name__)
logging.basicConfig(
    format="[%(asctime)s] [%(filename)s:%(lineno)d] %(message)s", level=logging.INFO
)


bot = commands.Bot(command_prefix="/",intents=intents) # Creating bot

bot.remove_command('help')


@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user.name}")
    await bot.tree.sync()
    

@bot.tree.command(name="test", description="test")
async def slash_command(interaction: discord.Interaction):

    await interaction.response.defer()

    categories = ["Géographie","Histoire", "Science et Nature","Art et Littérature","Sports","Cinéma et Télévision","Musique","Technologie et Informatique","Gastronomie", "Langues et Culture"]
    categorieChosen = random.choice(categories)
    difficulty = ["très difficile","presque impossible"]
    difficultyChosen = random.choice(difficulty)
    # Votre prompt
    prompt_division = f'''
    Génère une question de quiz de {categorieChosen} {difficultyChosen} avec des options de réponse multiples au format JSON. La question doit être suivie de quatre options de réponse et indiquer la réponse correcte. La question doit être conçue pour être répondue en 3 secondes.
    '''


    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "Vous êtes un assistant capable de générer des questions de quiz au format JSON."},
            {"role": "user", "content": prompt_division}
        ],
        model="gpt-3.5-turbo",
    )
    # Affichage de la réponse
    print(chat_completion)

    # Obtenez la réponse
    response_message = chat_completion.choices[0].message

    # Accédez au contenu de la réponse
    response_content = response_message.content
    print(response_content)

     # Envoyez un message supplémentaire avec la catégorie choisie
    await interaction.followup.send(f"Catégorie choisie : {categorieChosen}")
    await interaction.followup.send(f"Difficulté choisie : {difficultyChosen}")


  # Essayez de convertir le contenu en JSON
    try:
        response_data = json.loads(response_content)
        print("Données JSON extraites :")
        print(response_data)

        # Convertir le JSON en une chaîne de caractères formatée pour l'affichage
        formatted_json = json.dumps(response_data, indent=4, ensure_ascii=False)
        await interaction.followup.send(f"```json\n{formatted_json}\n```")
    except json.JSONDecodeError:
        await interaction.followup.send("erreur la team")


 

bot.run(token)