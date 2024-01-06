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


##################################################################################
# CONFIGURATION DOTENV
##################################################################################
load_dotenv()


# Initialiser le client OpenAI
client = OpenAI(
    api_key=os.environ.get("OPENAI_API_KEY"),
)


##################################################################################
# DEFINITIONS
##################################################################################

def prompt_to_chat_gpt_api(prompt):


    chatCompletion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": "Vous êtes un assistant capable de générer des questions de quiz au format JSON."},
            {"role": "user", "content": prompt}
        ],
        model="gpt-3.5-turbo",
    )

    responseMessage = chatCompletion.choices[0].message
    responseContent = responseMessage.content

    print(f"[INFO] - responseContent : {responseContent}")

    return responseContent


def chose_random_from_list(mainList):
    return  random.choice(mainList)

def select_random_question_categorie_sous_categorie():
    categories = ["Géographie","Histoire", "Science et Nature","Art et Littérature","Sports","Cinéma et Télévision","Musique","Technologie et Informatique","Gastronomie", "Langues et Culture"]
    sousCategories = [
        ["Pays et Capitales", "Montagnes et Rivières", "Climat et Écosystèmes", "Cartographie et Navigation"], # Géographie
        ["Histoire Ancienne", "Moyen Âge", "Histoire Moderne", "Histoire Contemporaine"], # Histoire
        ["Biologie et Écologie", "Physique et Chimie", "Astronomie", "Géologie"], # Science et Nature
        ["Peinture et Sculpture", "Littérature Classique", "Mouvements Artistiques", "Théâtre et Poésie"], # Art et Littérature
        ["Sports Collectifs", "Sports Individuels", "Sports d'Hiver", "Sports Extrêmes"], # Sports
        ["Films Classiques", "Séries Télévisées", "Réalisation et Production", "Genres Cinématographiques"], # Cinéma et Télévision
        ["Musique Classique", "Rock et Pop", "Jazz et Blues", "Musique Électronique"], # Musique
        ["Informatique", "Réseaux et Internet", "Intelligence Artificielle", "Nouvelles Technologies"], # Technologie et Informatique
        ["Cuisine du Monde", "Techniques Culinaires", "Pâtisserie et Boulangerie", "Boissons et Cocktails"], # Gastronomie
        ["Langues du Monde", "Traditions Culturelles", "Études Linguistiques", "Diversité et Interculturalité"] # Langues et Culture
    ]

    choiceOfCategorie = chose_random_from_list(categories)
    index_choice_of_categorie = categories.index(choiceOfCategorie)
    choiceOfSousCategorie = chose_random_from_list(sousCategories[index_choice_of_categorie])

    print(f"[INFO] - choiceOfCategorie : {choiceOfCategorie}")
    print(f"[INFO] - choiceOfSousCategorie : {choiceOfSousCategorie}")
    return choiceOfCategorie, choiceOfSousCategorie

def select_difficulty(difficultyInput):

    listDiffulty =  ["facile","intermediaire","difficile","très difficile","impossible"]

    if difficultyInput:
        print(f"[INFO] - choiceOfDiffculty : {listDiffulty[difficultyInput+1]}")
        return listDiffulty[difficultyInput+1]
    else :
        choiceOfDifficulty = chose_random_from_list(listDiffulty)
        print(f"[INFO] - choiceOfDiffculty : {choiceOfDifficulty}")
        return choiceOfDifficulty
 


def prompt_creation(categorieChosen,sousCategorieChosen,difficultyChosen):

    prompt = \
    f'''
    Génère une question de quiz de catégorie \
    {categorieChosen} \
    et de sous catégorie \
    {sousCategorieChosen} \
    qui sera de difficulté \
    {difficultyChosen} \
    avec des options de réponse multiples au format JSON. \
    La question doit être suivie de quatre options de réponse et indiquer la réponse correcte. \
    La question doit être conçue pour être répondue en 3 secondes. \
    Ne met pas de le terme "json" avant la réponse sous forme de Json. \
    Ne met pas de A) ou de A. devant les réponses \
    les noms des clés du Json seront : question, reponses, solution, temps. \
    les réponses serront dans un array.
    '''
    print(f"[INFO] : choiceOfDiffculty : {prompt}")

    return prompt


def json_lecture(jsonAnswer):
    
    # Essayez de convertir le contenu en JSON
    try:

        if jsonAnswer[0] == "j" :
            jsonAnswer = jsonAnswer[3:]
            
        responseData = json.loads(jsonAnswer)

        # Supprimer la clé 'answer'
        if 'solution' in responseData:
            solution = responseData['solution']
        else : 
            solution = None
        
        if 'question' in responseData:
            question = responseData['question']
        else : 
            question = None
        
        reponsesList = []
        if 'reponses' in responseData:
            reponsesList.append(responseData['reponses'][0])
            reponsesList.append(responseData['reponses'][1])
            reponsesList.append(responseData['reponses'][2])
            reponsesList.append(responseData['reponses'][3])

        temps = 5

        print(f"[INFO] - question : {question}")
        print(f"[INFO] - reponsesList : {reponsesList}")
        print(f"[INFO] - solution : {solution}")
        print(f"[INFO] - temps : {temps}")
        
        return question , reponsesList , solution,temps

    except json.JSONDecodeError:
        print(f"[ERROR] - question")
        print(f"[ERROR] - reponsesList")
        print(f"[ERROR] - solution")
        print(f"[ERROR] - temps")
        return None,None,None,None


def creation_embed(question,reponsesList,categorie,sousCategorie,difficulty):
    
    image_path = "images/bk.png"   
    colors = [0x1abc9c, 0x3498db, 0x9b59b6, 0xe74c3c, 0xf1c40f, 0x2ecc71]
    random_color = chose_random_from_list(colors)



    embed = Embed(title="🌎 GEOBOT 🐬", description='', color=random_color)  # Vous pouvez changer la couleur

    embed.add_field(name="**Catégories **", value=categorie, inline=True)
    embed.add_field(name="**Sous-Catégories**", value=sousCategorie, inline=True)
    embed.add_field(name="**Difficulté**", value=difficulty + "\n", inline=True)

    embed.add_field(name="**Question**", value=question, inline=False)

    # Ajouter les réponses à l'embed, deux par ligne
    embed.add_field(name="REPONSE A)", value=reponsesList[0] + "\n", inline=True)
    embed.add_field(name="REPONSE B)", value=reponsesList[1] + "\n", inline=True)
    embed.add_field(name="REPONSE C)", value=reponsesList[2] + "\n", inline=True)
    embed.add_field(name="REPONSE D)", value=reponsesList[3] + "\n", inline=True)

    embed.add_field(name="**TIMER**", value=str(0), inline=True)


    embed.set_image(url='attachment://image.jpg')
        
    # Création de l'objet File
    file = File(image_path, filename='image.jpg')
    return embed,file




##################################################################################
# CLASS
##################################################################################

class MyView(discord.ui.View):
    def __init__(self,reponsesList,solution):
        super().__init__()


        self.reponsesList = reponsesList
        self.solution = solution
        self.alreadyAnswered = set()  # Utiliser un ensemble pour enregistrer les utilisateurs qui ont déjà répondu

        # Ajouter les boutons avec des styles différents
        self.add_item(discord.ui.Button(style=discord.ButtonStyle.grey, custom_id=reponsesList[0], label="A"))
        self.add_item(discord.ui.Button(style=discord.ButtonStyle.green, custom_id=reponsesList[1], label="B"))
        self.add_item(discord.ui.Button(style=discord.ButtonStyle.blurple, custom_id=reponsesList[2], label="C"))
        self.add_item(discord.ui.Button(style=discord.ButtonStyle.red, custom_id=reponsesList[3], label="D"))


    async def interaction_check(self, interaction: discord.Interaction) -> bool:

        user_id = interaction.user.id
        userName =  interaction.user

        # Vérifier si l'utilisateur a déjà répondu
        if user_id in self.alreadyAnswered:
            await interaction.response.send_message("Vous avez déjà répondu à cette question sale merde.", ephemeral=True)
            return False

        self.alreadyAnswered.add(user_id)  # Marquer l'utilisateur comme ayant répondu

        # Vérifier si la réponse est correcte
        if interaction.data['custom_id'] == self.solution:
            await interaction.response.send_message(f"{userName} ✅ Bonne réponse! ✅", ephemeral=False)
        else:
            await interaction.response.send_message(f"{userName} ❌Mauvaise réponse!❌", ephemeral=False)

        return True