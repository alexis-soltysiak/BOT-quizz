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
            jsonAnswer = jsonAnswer[4:]
        elif jsonAnswer[0] == "\n" :
            jsonAnswer = jsonAnswer[5:]
        
        print(jsonAnswer)
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


def creation_results(view):

    listResult = view.listAnswer

    print(listResult)

    def tri_key(element):
        return (0 if element[1] else 1, element[2])

    sorted_results = sorted(listResult, key=tri_key)

    return sorted_results


def creation_embed(question,reponsesList,categorie,sousCategorie,difficulty):
    
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


def r_just_string(string,size):
    return string.rjust(size)


def transform_number_to_emoji_5_digits(score):
    listEmojiDigit = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]

    score_int = int(round(score))  # Arrondissez le score si c'est un nombre à virgule flottante
    score_str = str(score_int).zfill(5)

    score_str = score_str.lstrip('0').rjust(5, '⬛')

    emoji_score = ''.join(listEmojiDigit[int(digit)] if digit.isdigit() else digit for digit in score_str)

    return emoji_score



def transform_number_to_emoji_2_digits(score):
    listEmojiDigit = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]

    score_int = int(round(score))  # Arrondissez le score si c'est un nombre à virgule flottante
    score_str = str(score_int).zfill(2)

    # Remplacer les zéros de tête par l'emoji ⬛
    score_str = score_str.lstrip('0').rjust(2, '⬛')

    # Remplacer chaque chiffre par son emoji correspondant
    emoji_score = ''.join(listEmojiDigit[int(digit)] if digit.isdigit() else digit for digit in score_str)

    return emoji_score

def transform_number_to_emoji(score):

    listEmojiDigit = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]
    score_str = str(score)
    emoji_score = ''.join(listEmojiDigit[int(digit)] for digit in score_str)

    return emoji_score

def score_calculation(reponse,temps):
    if reponse == False:
        return transform_number_to_emoji_5_digits(0)
    else :
        score = 1000 * (11-temps)
        if score < 0 :
            score = 0
        print(temps,score)
        return transform_number_to_emoji_5_digits(1000 * (10-temps)) 


def creation_embed_answer(solution,solutionList):
    
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
        score = score_calculation(reponse,temps)
        reponseEmoji = "✅" if reponse == True else "❌"

        embed.add_field(name=" ", value= f"{transform_number_to_emoji_2_digits(index)}" , inline=True)
        embed.add_field(name=" ", value= f"{str(nom.name)}" , inline=True)
        embed.add_field(name=" ", value= f"{score} " , inline=True)

  
    embed.set_image(url='attachment://image.jpg')
        
    # Création de l'objet File
    file = File(image_path, filename='image.jpg')
    return embed,file



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
        if datetime.datetime.now() - self.start_time > timer_value_delta : 
            return True
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
                  
                  
        await interaction.response.send_message(f"Tu as voté {interaction.data['custom_id']} en {response_time_seconds}s" , ephemeral=True)

        return True
    
