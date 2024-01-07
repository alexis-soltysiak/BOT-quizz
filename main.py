# --------------------------------------------------------------------------------
# @copyright
# Nom du Projet : GEOBOT
# Auteur : Alexis Soltysiak
# Date : 2024
# Description : Main discord bot fuction
# --------------------------------------------------------------------------------

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
from typing import Any
import asyncio
from discord import Embed, File, Button, ButtonStyle
from discord.ui import View


from functions import *
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



##################################################################################
# DISCORD BOT EVENT
##################################################################################

@bot.event
async def on_ready():
    await bot.tree.sync()
    logger.info(f"Logged in as {bot.user.name}")   
    


@bot.tree.command(name="question", description="question creation")
async def slash_command_question(interaction: discord.Interaction):

    await interaction.response.defer()


    ################################################################################################################
    #categorie and diffuclty choice
    categorieChosen, sousCategorieChosen = select_random_question_categorie_sous_categorie()
    difficultyChosen = select_difficulty(None)


    ################################################################################################################
    # PROMPT CREATION
    prompt = prompt_creation(categorieChosen,sousCategorieChosen,difficultyChosen)


    ################################################################################################################
    #PROMPT TO AI
    responseContent = prompt_to_chat_gpt_api(prompt)


    ################################################################################################################
    #LECTURE DU JSON
    question , reponsesList , solution,temps = json_lecture(responseContent)

    if question : 

        timer_value = 11

        view = MyView(reponsesList,solution,timer_value)

        embed,file = creation_embed(question,reponsesList,categorieChosen,sousCategorieChosen,difficultyChosen)

        message = await interaction.followup.send(embed=embed, view=view, file =file)
   


        for i in range(timer_value - 1, 0, -1):
            if i%2 == 0 : 
                embed.set_field_at(2, name="**TIMER**", value=transform_number_to_emoji_2_digits(i) + "⌛" , inline=True)
            else :
                embed.set_field_at(2, name="**TIMER**", value=transform_number_to_emoji_2_digits(i) + "⏳" , inline=True)

            await message.edit(embed=embed)
            await asyncio.sleep(1)

        embed.set_field_at(2, name="**TIMER**", value="🛑", inline=True)
        await message.edit(embed=embed)

        solutionList = creation_results(view)

        print("[INFO]")

        embed_answer,file = creation_embed_answer(solution,solutionList)


        await interaction.followup.send(embed=embed_answer, file =file)

    else : 

        await interaction.followup.send("error")

bot.run(token)