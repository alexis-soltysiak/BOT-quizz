# --------------------------------------------------------------------------------
# @copyright
# Nom du Projet : GEOBOT
# Auteur : Alexis Soltysiak
# Date : 2024
# Description : Main discord defintions
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
from discord import Embed, File
import datetime
import csv
import time
import pandas as pd

from functions import *

##################################################################################
# Embeded
##################################################################################

def creation_embed(question,reponsesList):
    
    image_path = "images/bk.png"   
    colors = [0x1abc9c, 0x3498db, 0x9b59b6, 0xe74c3c, 0xf1c40f, 0x2ecc71]
    random_color = chose_random_from_list(colors)



    embed = Embed(title="🌎 GEOBOT 🐬", description='', color=random_color) 

    embed.add_field(name=" ", value=" ", inline=True)
    embed.add_field(name=" ", value=" ", inline=True)

    embed.add_field(name="**TIMER**", value=str(0), inline=True)

    #embed.add_field(name="**Catégories **", value=categorie, inline=True)
    #embed.add_field(name="**Sous-Catégories**", value=sousCategorie, inline=True)
    #embed.add_field(name="**Difficulté**", value=difficulty + "\n", inline=True)

    embed.add_field(name="**Question**", value="```" + question + "```" , inline=False)

    embed.add_field(name="A.", value=reponsesList[0] + "\n", inline=True)
    embed.add_field(name="B.", value=reponsesList[1] + "\n", inline=False)
    embed.add_field(name="C.", value=reponsesList[2] + "\n", inline=True)
    embed.add_field(name="D.", value=reponsesList[3] + "\n", inline=False)



    embed.set_image(url='attachment://image.jpg')
        
    # Création de l'objet File
    file = File(image_path, filename='image.jpg')
    return embed,file




def creation_embed_answer(solution,solutionList,temps_max):
    
    image_path = "images/bk.png"   
    colors = [0x1abc9c, 0x3498db, 0x9b59b6, 0xe74c3c, 0xf1c40f, 0x2ecc71]
    random_color = chose_random_from_list(colors)



    embed = Embed(title="🌎 GEOBOT 🐬", description='', color=random_color)  # Vous pouvez changer la couleur


    embed.add_field(name="**Solution**", value="```" + solution + "```" , inline=False)

    embed.add_field(name="**Place**", value= " " , inline=True)
    embed.add_field(name="**Nom**", value=" ", inline=True)
    embed.add_field(name="**Score**", value=" " , inline=True)

    index = 0
    for nom,reponse,temps in solutionList:
            
        index +=1
        score = score_calculation(reponse,temps,temps_max)
        reponseEmoji = "✅" if reponse == True else "❌"

        embed.add_field(name=" ", value= f"{transform_number_to_emoji_2_digits(index)}" , inline=True)
        embed.add_field(name=" ", value= f"{str(nom.name)}" , inline=True)
        embed.add_field(name=" ", value= f"{score} " , inline=True)

  
    embed.set_image(url='attachment://image.jpg')
        
    # Création de l'objet File
    file = File(image_path, filename='image.jpg')
    return embed,file

