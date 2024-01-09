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

last_call_time = 0

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
        if jsonAnswer[0] != "{": 
            jsonAnswer = jsonAnswer[jsonAnswer.find("{"):]
        """
        elif jsonAnswer[0] == "j" :
            jsonAnswer = jsonAnswer[4:]
        elif jsonAnswer[0] == "\n" :
            jsonAnswer = jsonAnswer[5:]
        """

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

    def tri_key(element):
        return (0 if element[1] else 1, element[2])

    sorted_results = sorted(listResult, key=tri_key)

    return sorted_results



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

def score_calculation(reponse,temps,temps_max):
    if reponse == False:
        return transform_number_to_emoji_5_digits(0)
    else :
        score = 1000 * (temps_max - temps + 2)
        if score < 0 :
            score = 0
        return transform_number_to_emoji_5_digits(score) 


def add_question_answers_solution_to_db(question, reponsesList, solution):
    # Chemins des fichiers CSV
    questionsFilePath = 'bdd/questions.csv'
    answersFilePath = 'bdd/answers.csv'
    solutionsFilePath = 'bdd/solution.csv'

    try:
        df_questions = pd.read_csv(questionsFilePath)
        max_question_id = df_questions['id'].max()
    except FileNotFoundError:
        max_question_id = 0

    new_question_id = max_question_id + 1

    with open(questionsFilePath, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if max_question_id == 0:
            writer.writerow(['id', 'question'])
        writer.writerow([new_question_id, question])

    try:
        df_answers = pd.read_csv(answersFilePath)
        max_answer_id = df_answers['id'].max()
    except FileNotFoundError:
        max_answer_id = 0

    with open(answersFilePath, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if max_answer_id == 0:
            writer.writerow(['id', 'id_question', 'answer', 'answer_letter'])

        for index, answer in enumerate(reponsesList, start=1):
            new_answer_id = max_answer_id + index
            answer_letter = chr(64 + index)  # 65 est le code ASCII pour 'A'
            writer.writerow([new_answer_id, new_question_id, answer, answer_letter])

    with open(solutionsFilePath, 'a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        try:
            with open(solutionsFilePath, 'r') as f:
                if f.readline().strip() == '':
                    writer.writerow(['id', 'id_question', 'solution'])
        except FileNotFoundError:
            writer.writerow(['id', 'id_question', 'solution'])

        # Écriture de la solution
        writer.writerow([new_question_id, new_question_id, solution])



def can_execute_command():
    global last_call_time
    current_time = time.time()
    if current_time - last_call_time < 60:
        # Pas assez de temps s'est écoulé
        return False
    else:
        # Assez de temps s'est écoulé, mettre à jour le temps du dernier appel
        last_call_time = current_time
        return True



def creation_question_answers_solutions(proba):

    if proba > random.random() :
            
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

        return question , reponsesList , solution , True
    
    else : 

        csvFilePath = 'bdd/questions.csv'
        answerCsvFilePath = 'bdd/answers.csv'
        solutionCsvFilePath = 'bdd/solution.csv'

        df = pd.read_csv(csvFilePath) 
        answers_df = pd.read_csv(answerCsvFilePath)
        dfSolution = pd.read_csv(solutionCsvFilePath)

        random_row = df.sample().iloc[0]

        # Selection la question et l'ID de la question
        idQuestion = random_row['id']
        question = random_row['question']

        # Sélectionner les réponses pour l'ID de question trouvé précédemment
        reponsesList = answers_df[answers_df['id_question'] == idQuestion]['answer'].tolist()

        # Sélectionner les réponses pour l'ID de question trouvé précédemment
        solution = dfSolution[dfSolution['id_question'] == idQuestion]['solution'].iloc[0]

        return question , reponsesList , solution , False


