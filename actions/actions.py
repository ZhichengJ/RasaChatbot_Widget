# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
import os, random
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet
#
#
# class ActionHelloWorld(Action):

#     def name(self) -> Text:
#         return "action_hello_world"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         dispatcher.utter_message(text="Hello World!")

#         return []

class Action_post(Action):
def name(self):
    return 'action_test'

def run(self, dispatcher, tracker, domain):
    intent = tracker.latest_message['intent'].get('name')
    # do whatever it takes
return []


################################################
# Devuelve un sonido para analizar
################################################

class action_dar_sonido(Action):
    def name(self):
        return 'action_dar_sonido'
    
    def run (self, dispatcher, tracker, domain):
        #Nos da el path absoluto de un sonido aleatorio del directorio sounds
        path = os.path.abspath(random.choice(os.listdir("../sounds")))
        dispatcher.utter_message(json_message={"soundUri:"path})
        return [SlotSet("eco","path")]


################################################
# Post a la API con las respuestas del usuario
################################################

class ActionPostRespuestas(Action):
    def name(self):
        return 'action_post_respuestas'
    
    def run(self, dispatcher, tracker, domain):
        resp1 = tracker.get_slot.