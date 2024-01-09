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



from functions import *



    
##################################################################################
# CLASS
##################################################################################

class MyView(discord.ui.View):
    def __init__(self,reponsesList,solution,timer_value):
        super().__init__()


        self.reponsesList = reponsesList
        self.solution = solution
        self.alreadyAnswered = set() 
        self.listAnswer = []
        self.start_time = datetime.datetime.now()
        self.timer_value = timer_value

        # Ajouter les boutons avec des styles différents
        self.add_item(discord.ui.Button(style=discord.ButtonStyle.grey, custom_id=reponsesList[0], label="A"))
        self.add_item(discord.ui.Button(style=discord.ButtonStyle.green, custom_id=reponsesList[1], label="B"))
        self.add_item(discord.ui.Button(style=discord.ButtonStyle.blurple, custom_id=reponsesList[2], label="C"))
        self.add_item(discord.ui.Button(style=discord.ButtonStyle.red, custom_id=reponsesList[3], label="D"))


    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        
        time_of_answer = datetime.datetime.now() - self.start_time
        timer_value_delta = datetime.timedelta(seconds=self.timer_value)
        """
        if datetime.datetime.now() - self.start_time > timer_value_delta : 
            return True
        """
        user_id = interaction.user.id
        userName =  interaction.user

        # Vérifier si l'utilisateur a déjà répondu
        if user_id in self.alreadyAnswered:
            await interaction.response.send_message("Vous avez déjà répondu à cette question", ephemeral=True)
            return False

        self.alreadyAnswered.add(user_id)  # Marquer l'utilisateur comme ayant répondu


        response_time_seconds = time_of_answer.total_seconds()  # Temps de réponse en secondes

        # Vérifier si la réponse est correcte
        if interaction.data['custom_id'] == self.solution:
            self.listAnswer.append([userName,True,response_time_seconds])
            #await interaction.response.send_message(f"{userName} ✅ Bonne réponse! ✅", ephemeral=True)

        else:
            self.listAnswer.append([userName,False,response_time_seconds])
                  
                  
        await interaction.response.send_message(f"Tu as voté {interaction.data['custom_id']} en {response_time_seconds - 1}s" , ephemeral=True)

        return True
    

class MyViewAnswer(discord.ui.View):

    def __init__(self,question,reponsesList,solution,timer_value,isNewQuestion):
        super().__init__()

        self.question = question
        self.reponsesList = reponsesList
        self.solution = solution
        self.start_time = datetime.datetime.now()
        self.timer_value = timer_value
        self.isNewQuestion = isNewQuestion

        if (isNewQuestion) : 
            self.add_item(discord.ui.Button(style=discord.ButtonStyle.green, custom_id="True", label="ADD"))
            self.add_item(discord.ui.Button(style=discord.ButtonStyle.red, custom_id="False", label="DEL"))

    def disable_all_buttons(self):
        """Désactiver tous les boutons dans la vue."""
        for item in self.children:
            if isinstance(item, discord.ui.Button):
                item.disabled = True


    async def interaction_check(self, interaction: discord.Interaction) -> bool:

        
        if interaction.data['custom_id'] == "True":
            add_question_answers_solution_to_db(self.question, self.reponsesList, self.solution)
            self.disable_all_buttons()

            await interaction.message.edit(view=self)
            await interaction.response.send_message(f" ✅ Question ajoutée ✅", ephemeral=True)

        else:
            self.disable_all_buttons()
            await interaction.message.edit(view=self)
            await interaction.response.send_message(f"  Question nulle ", ephemeral=True)

        return True