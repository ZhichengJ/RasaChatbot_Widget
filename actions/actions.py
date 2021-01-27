# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
import os
import random
import json
import time
import requests
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import FollowupAction
from rasa_sdk.events import AllSlotsReset

################################################
# Devuelve un sonido para analizar
################################################


class action_dar_sonido(Action):
    def name(self):
        return 'action_dar_sonido'

    def run(self, dispatcher, tracker, domain):
        #Nos da el path absoluto de un sonido aleatorio del directorio sounds
        file = random.choice(os.listdir("sounds"))
        path = os.path.join(
            "/Users/marcosgamazo/PycharmProjects/chatbot-TFG/sounds", file)
        dispatcher.utter_message(path)
        return [SlotSet("eco", os.path.splitext(file)[0])]

class ActionContinuar(Action):
    def name(self):
        return 'action_continuar'

    def run(self, dispatcher, tracker, domain):
        buttons=[]
        buttons.append({"title": 'Si',
                        "payload": "/clasificar"})
        buttons.append({"title": 'No',
                        "payload": "/salir"})
        dispatcher.utter_message("¿Quieres continuar?", buttons=buttons)
        return[FollowupAction('')]


class action_pregunta_uno(Action):
    def name(self):
        return 'action_pregunta_uno'

    def run(self, dispatcher, tracker, domain):
        buttons = []
        buttons.append({"title": 'Menos de 1 segundo',
                        "payload": "/pregunta_dos{'respuesta1':'Menos de 1 segundo'}"})
        buttons.append({"title": 'Entre 1 y 5 segundos',
                        "payload": "/pregunta_dos{'respuesta1':'Entre 1 y 5 segundos'}"})
        buttons.append({"title": 'Mas de 9 segundos',
                        "payload": "/pregunta_dos{'respuesta1':'Mas de 9 segundos'}"})
        dispatcher.utter_message(
            text="¿Cuánto dura el sonido?", buttons=buttons)
        return[SlotSet('respuesta1', buttons)]


class action_pregunta_dos(Action):
    def name(self):
        return 'action_pregunta_dos'

    def run(self, dispatcher, tracker, domain):
        buttons = []
        buttons.append(
            {"title": 'Si', "payload": "/pregunta_tres{'respuesta2':'Si'}"})
        buttons.append(
            {"title": 'No', "payload": "/pregunta_tres{'respuesta2':'No'}"})
        dispatcher.utter_message(
            text='¿Se escucha al principio un sonido corto y luego un silencio o un sonido menos intenso?', buttons=buttons)
        return[SlotSet('respuesta2', buttons)]


class action_pregunta_tres(Action):
    def name(self):
        return 'action_pregunta_tres'

    def run(self, dispatcher, tracker, domain):
        buttons = []
        buttons.append(
            {"title": 'Si', "payload": "/post_api{'respuesta3':'Si'}"})
        buttons.append(
            {"title": 'No', "payload": "/post_api{'respuesta3':'No'}"})
        dispatcher.utter_message(
            text='¿Hay un sonido inicial con un tono distinto al resto?', buttons=buttons)
        return[SlotSet('respuesta3', buttons), FollowupAction('post_api')]


class action_reset(Action):
    def name(self):
        return 'action_reset'

    def run(self, dispatcher, tracker, domain):
        dispatcher.utter_message(tracker.get_slot('respuesta1'))
        dispatcher.utter_message(tracker.get_slot('respuesta2'))
        dispatcher.utter_message(tracker.get_slot('respuesta3'))
        dispatcher.utter_message(tracker.get_slot('eco'))
        dispatcher.utter_message(tracker.get_slot('nombre'))
        return[AllSlotsReset(), FollowupAction('action_restart')]

################################################
# Post a la API con las respuestas del usuario
################################################

class action_post_api(Action):
    def name(self):
        return 'action_post_api'

    def run(self, dispatcher, tracker, domain):
        url = 'http://138.100.100.143:3001/clasificaciones/'
        #url = 'http://127.0.0.1:3000/clasificaciones/'
        headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
        nombre = tracker.get_slot('nombre')
        respuesta1 = tracker.get_slot('respuesta1')[0]['title']
        respuesta2 = tracker.get_slot('respuesta2')[0]['title']
        respuesta3 = tracker.get_slot('respuesta3')[0]['title']
        eco = tracker.get_slot('eco')

        query = '{"_id":"' + str(eco) + '",'

        if nombre is not None:
            query += '"idUsuario":"' + str(nombre) + '",'

        query += '"Respuesta1":"' + str(respuesta1) + '",' + '"Respuesta2":"' + str(
            respuesta2) + '",' + '"Respuesta3":"' + str(respuesta3) + '"}'
        #print(query)
        r = requests.post(url, data=query, headers=headers)
        print(r.status_code)
        #Reseteamos los valores de los slots
        SlotSet("respuesta1","None")
        SlotSet("respuesta2","None")
        SlotSet("respuesta3","None")
        SlotSet("eco","None")
        return []