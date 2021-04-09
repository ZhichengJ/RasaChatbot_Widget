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
import logging
from datetime import datetime
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
from rasa_sdk.events import FollowupAction
from rasa_sdk.events import AllSlotsReset

################################################
# Devuelve un sonido para analizar
################################################


# class action_dar_sonido(Action):
#     def name(self):
#         return 'action_dar_sonido'

#     def run(self, dispatcher, tracker, domain):
#         #Nos da el path absoluto de un sonido aleatorio del directorio sounds
#         file = random.choice(os.listdir("sounds"))
#         path = os.path.join(
#             "/Users/marcosgamazo/PycharmProjects/chatbot-TFG/sounds", file)
#         dispatcher.utter_message(path)
#         return [SlotSet("eco", os.path.splitext(file)[0])]

logger = logging.getLogger(__name__)
headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}#, 'Access-Control-Allow-Origin':'*'}

class action_dar_sonido(Action):
    def name(self):
        return 'action_dar_sonido'

    def run(self, dispatcher, tracker, domain):
        #Nos da el path absoluto de un sonido aleatorio del directorio sounds
        #url = 'http://host.docker.internal:3000/sonidos?policy=random'  
        #url = 'http://localhost:3000/sonidos?policy=random' #Esta linea se utiliza en caso de que no se realice un despliegue en docker
        url = 'http://138.100.100.143:3001/sonidos?policy=random'
        r = requests.get(url, headers=headers)
        decoded = json.loads(r.text)
        dispatcher.utter_message(decoded["Ruta"])
        dispatcher.utter_message(decoded["_id"])
        return [SlotSet("eco", decoded["_id"])]

class action_dar_imagenes(Action):
    def name(self):
        return 'action_dar_imagenes'

    def run(self, dispatcher, tracker, domain):
        url = 'http://138.100.100.143:3001/curvasdeluz'
        r = requests.get(url, headers=headers)
        decoded = json.loads(r.text)
        n = random.randrange(1,len(decoded))
        decoded = decoded[n]
        dispatcher.utter_message(decoded["Imagen"])
        dispatcher.utter_message(decoded["_id"])
        url = 'http://138.100.100.143:3001/espectrogramas'
        r = requests.get(url, headers=headers)
        decoded_lc = json.loads(r.text)
        decoded = decoded_lc[n]
        dispatcher.utter_message(decoded["Imagen"])
        dispatcher.utter_message(decoded["_id"])
        slots = []
        slots.append(SlotSet("curvasdeluz", decoded["_id"]))
        slots.append(SlotSet("espectrogramas", decoded["_id"]))
        return slots


# class ActionContinuar(Action):
#     def name(self):
#         return 'action_continuar'

#     def run(self, dispatcher, tracker, domain):
#         buttons=[]
#         buttons.append({"title": 'Si',
#                         "payload": "/clasificar"})
#         buttons.append({"title": 'No',
#                         "payload": "/salir"})
#         dispatcher.utter_message("¿Quieres continuar?", buttons=buttons)
#         return[FollowupAction('')]


# class action_pregunta_uno(Action):
#     def name(self):
#         return 'action_pregunta_uno'

#     def run(self, dispatcher, tracker, domain):
#         buttons = []
#         buttons.append({"title": 'Menos de 1 segundo',
#                         "payload": "/pregunta_dos{{'respuesta1':'Menos de 1 segundo'}}"})
#         buttons.append({"title": 'Entre 1 y 5 segundos',
#                         "payload": "/pregunta_dos{{'respuesta1':'Entre 1 y 5 segundos'}}"})
#         buttons.append({"title": 'Mas de 9 segundos',
#                         "payload": "/pregunta_dos{{'respuesta1':'Mas de 9 segundos'}}"})
#         dispatcher.utter_message(
#             text="¿Cuánto dura el sonido?", buttons=buttons)
#         #return[SlotSet('respuesta1', buttons)]
#         return[]

# class action_pregunta_dos(Action):
#     def name(self):
#         return 'action_pregunta_dos'

#     def run(self, dispatcher, tracker, domain):
#         buttons = []
#         buttons.append(
#             {"title": 'Si', "payload": "/pregunta_tres{{'respuesta2':'Si'}}"})
#         buttons.append(
#             {"title": 'No', "payload": "/pregunta_tres{{'respuesta2':'No'}}"})
#         dispatcher.utter_message(
#             text='¿Se escucha al principio un sonido corto y luego un silencio o un sonido menos intenso?', buttons=buttons)
#         #return[SlotSet('respuesta2', buttons)]
#         return[]

# class action_pregunta_tres(Action):
#     def name(self):
#         return 'action_pregunta_tres'

#     def run(self, dispatcher, tracker, domain):
#         buttons=[]
#         buttons.append(
#             {"title": 'Si', "payload": "/post_api{{'respuesta3':'Si'}}"})
#         buttons.append(
#             {"title": 'No', "payload": "/post_api{{'respuesta3':'No'}}"})
#         dispatcher.utter_message(
#             text='¿Hay un sonido inicial con un tono distinto al resto?', buttons=buttons)
#         return[]
# class action_reset(Action):
#     def name(self):
#         return 'action_reset'

#     def run(self, dispatcher, tracker, domain):
#         dispatcher.utter_message(tracker.get_slot('respuesta1'))
#         dispatcher.utter_message(tracker.get_slot('respuesta2'))
#         dispatcher.utter_message(tracker.get_slot('respuesta3'))
#         dispatcher.utter_message(tracker.get_slot('eco'))
#         dispatcher.utter_message(tracker.get_slot('nombre'))
#         return[AllSlotsReset(), FollowupAction('action_restart')]

################################################
# Post a la API con las respuestas del usuario
################################################

# def getClasificaciones(eco):
#     url = 'http://138.100.100.143:3001/ecos/' + eco
#     #url = 'http://127.0.0.1:3000/ecos/' + eco
#     #url = 'http://host.docker.internal:3000/ecos/' + eco  #Esta linea se utiliza en caso de que no se realice un despliegue en docker
#     r = requests.get(url,headers=headers)
#     decode = json.loads(r.text)
#     #logger.debug(str(r.text))
#     clasificaciones = decode["nClasificaciones"]
#     return clasificaciones


class action_post_api(Action):
    def name(self):
        return 'action_post_api'

    def run(self, dispatcher, tracker, domain):
        url = 'http://138.100.100.143:3001/clasificaciones/'
        #url = 'http://127.0.0.1:3000/clasificaciones/'  #Esta linea se utiliza en caso de que no se realice un despliegue en docker
        #url = 'http://host.docker.internal:3000/clasificaciones/'

        query_Dict ={}
        eco = tracker.get_slot('eco')
        #nClasificaciones = getClasificaciones(eco) + 1

        #dispatcher.utter_message(nClasificaciones)
        
        nombre = tracker.get_slot('nombre')
        message = tracker.latest_message['text']

        #logger.debug(tracker.get_slot('respuesta1'))
        #logger.debug(tracker.get_slot('respuesta2'))
        #logger.debug(tracker.get_slot('respuesta3'))

        respuesta1 = tracker.get_slot('respuesta1')
        respuesta2 = tracker.get_slot('respuesta2')
        respuesta3 = tracker.get_slot('respuesta3')
        
        #dispatcher.utter_message("RESPUESTA1: "+tracker.get_slot('respuesta1'))
        #dispatcher.utter_message("RESPUESTA2: "+ tracker.get_slot('respuesta2'))
        #dispatcher.utter_message("RESPUESTA3: " + tracker.get_slot('respuesta3'))
        #dispatcher.utter_message("ECO: " +  eco)
        
        query_Dict['_id'] = datetime.now().strftime("%Y-%m-%d_%H:%M:%S")     
        query_Dict['idEco'] = eco
        query_Dict['Nombre'] = nombre
        query_Dict['Respuesta1'] = respuesta1
        query_Dict['Respuesta2'] = respuesta2
        query_Dict['Respuesta3'] = respuesta3
        
        #logger.debug("Clasificaciones: " + str(nClasificaciones))
        
        r = requests.post(url, data=json.dumps(query_Dict), headers=headers)
        #actualizamos la clasificacion
        #actualizarClasificacion(eco, nClasificaciones)
        
        #Reseteamos los valores de los slots
        return [SlotSet("respuesta1",None),SlotSet("respuesta2",None),SlotSet("respuesta3",None),SlotSet("eco",None)]

# def actualizarClasificacion(eco, clasificaciones):
#     url = 'http://138.100.100.143:3001/ecos/' + eco
#     #url = 'http://127.0.0.1:3000/ecos/'+ eco  #Esta linea se utiliza en caso de que no se realice un despliegue en docker
#     #url = 'http://host.docker.internal:3000/ecos/'+ eco

#     #headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
#     query={}
#     query['nClasificaciones']=clasificaciones
#     #logger.debug("Respuesta")
#     r = requests.patch(url, data =json.dumps(query),headers=headers)
#     return