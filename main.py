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
import time


from views import *
from functions import *
from embed import *
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
last_call_time = 0

@bot.event
async def on_ready():
    await bot.tree.sync()
    logger.info(f"Logged in as {bot.user.name}")   
    


@bot.tree.command(name="question", description="question creation")
async def slash_command_question(interaction: discord.Interaction, newquestionproba : float):

    ###############################################################################################################
    #Time check
    if not can_execute_command():
        await interaction.response.send_message("Veuillez attendre une minute avant de réutiliser cette commande.")
        return
    
    await interaction.response.defer()

    ################################################################################################################
    #choice question
    question , reponsesList , solution , isNewQuestion =  creation_question_answers_solutions(newquestionproba)


    if question : 

        timer_value = 10

        view = MyView(reponsesList,solution,timer_value)
        viewAnswer = MyViewAnswer(question,reponsesList,solution,timer_value,isNewQuestion)

        embed,file = creation_embed(question,reponsesList)
        message = await interaction.followup.send(embed=embed, view=view, file =file)


        for i in range(timer_value - 1, 0, -1):
            if i%2 == 0 : 
                embed.set_field_at(2, name="**TIMER**", value=transform_number_to_emoji_2_digits(i) + "⌛" , inline=True)
            else :
                embed.set_field_at(2, name="**TIMER**", value=transform_number_to_emoji_2_digits(i) + "⏳" , inline=True)

            await message.edit(embed=embed)
            await asyncio.sleep(1)

        embed.set_field_at(2, name="**TIMER**", value="🛑", inline=True)
        for item in view.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True

        # Mettre à jour le message avec la vue désactivée
        await message.edit(embed=embed, view=view)


        solutionList = creation_results(view)

        embed_answer,file = creation_embed_answer(solution,solutionList,timer_value)


        await interaction.followup.send(embed=embed_answer, view = viewAnswer,file =file)

    else : 

        await interaction.followup.send("error")

bot.run(token)