# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

# pylint: disable=import-error
#from dbConnect import getData
# # write the sql query here.
# query = "select * from customer"
## pass the sql query to the getData method and store the results in `data` variable.
# data = getData(query)

# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Optional
import nltk 
nltk.download('punkt')
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset, EventType
from rasa_sdk.forms import FormValidationAction
from actions.dbConnect import getData #pylint: disable=import-error
# # write the sql query here.
# query = "select * from specialites"
# ## pass the sql query to the getData method and store the results in `data` variable.
# data = getData(query)
# print("the dataa######################")
# print(data)

import json
import os
import random

with open('intents.json', mode="rt") as json_data:
    data = json.load(json_data)


#return a place from a sentence
def indiqueLieu(requete):
    liste = ["2","3","5","6","almadies","parcelles","assainies","bourguiba","camberene","castor","cipres","cite ","keur ","gorgui","massar","sacre","coeur",\
"colobane","corniche","patte","d'oie","dakar","dalifort","diamniadio","diourbel","djambars","djaraf","fann","fass","fatick","front","terre",\
"gentina","golf","grand","yoff","guediawaye","gueule ","tapee","hann ","maristes","hlm","kaffrine","kaolack","kedouguou ","kolda","liberte",\
"louga","malika","mamelles","matam","mbour","medina","mermoz","ndioum","ngor","nord","ouakam","ouest ","foire","ourossogui","pasteur","pikine",\
"point ","e","richard ","toll","rufisque","sahm","saint ","louis","saly","scat ","urbam","sedhiou","sicap ","mbao","sipress","soprim",\
"soumbedioune","tambacounda","technopole","thiaroye","thies","tivaoune","touba","vdn","yeumbeul","ziguinchor"]

    my_requete = nltk.word_tokenize(requete)
    my_requete = map(lambda x:x.lower(), my_requete)
    lieu = filter(lambda x:x in liste, my_requete)
    lieu = [w for w in lieu]
    if len(lieu) != 0:
        return [' '.join(lieu)]
    else:
        return ["null"] 


# def _ancienne_function_search_intent_in_file(location: Text) -> Text:
#     """Returns object of pharma matching the search criteria."""
#     for theint in data["intentions"]:
#         if theint['tags'] == "Pharmacies":
#             reponse = [choix['pharmacies']+" adr : "+choix['adresse']+" Tel : "+choix['telephone']+". " for choix in theint['responses'] if location.lower() in indiqueLieu(choix['adresse'].lower())]
#             if len(reponse) != 0:
#                 return "Je vous recommande " + reponse[random.choice(range(len(reponse)))]
#             else:
#                 return "Désolé mais nous n'avons pas de pharmacie partenaire dans cette zone. Essayez en une autre 😊"

#     #return "Une erreur s'est produite, un de nos services ne réponds pas. Veuillez réessayer plus tard "

#     """Returns object of doctor matching the search criteria."""
#     if medecin is not None:
#         medecin= medecin.lower()
#     for theint in data["intentions"]:
#         if theint['tags'] == medecin:
#             reponse = [choix['docteur']+" adr : "+choix['adresse']+" Tel : "+choix['telephone']+". " for choix in theint['responses'] if location.lower() in indiqueLieu(choix['adresse'].lower())]
#             if len(reponse) != 0:
#                 return "Je vous recommande " + reponse[random.choice(range(len(reponse)))]
#             else:
#                 return "Désolé mais nous n'avons pas de "+ theint['tags'] +" partenaire dans cette zone. Essayez en une autre 😊"

#     return "Une erreur s'est produite, un de nos services ne réponds pas. Veuillez réessayer plus tard"

def _search_bd(typeResponse: Text, localisation: Text)-> Text:
    # create the query for the database
    query = f'''SELECT responses.id, responses.nom, responses.adresse, responses.telephone, responses.email, responses.disponibilite, responses.specialite from responses 
    WHERE responses.disponibilite=1 and responses.adresse like "%{localisation}%" and 
    responses.specialite IN 
    (SELECT id from specialites WHERE specialites.nom LIKE "%{typeResponse}%")'''

    # ## pass the sql query to the getData method and store the results in `data` variable.
    data = getData(query)
    if len(data) == 0:
        return "null"
    else:        
        return data[random.choice(range(len(data)))]
    
    
def _find_facilities_pharmacie(location: Text) -> Text:
    """Returns object of pharma matching the search criteria."""

    dataR= _search_bd("Pharmacies",location.lower())
    if dataR == "null":
        return "Désolé mais nous n'avons pas de pharmacie partenaire dans cette zone. Essayez en une autre 😊"
    else:
        message = (
                        f"Je vous recommande : {dataR[1]} \n Adresse : {dataR[2]}\n"
                        f"Telephone : {dataR[3]}.\n"
                        f"Email: {'indisponible' if dataR[4] == 'null' else dataR[4]} \n"
                    )
        return message                


def _find_facilities_medecin(location: Text, medecin: Text) -> Text:
    """Returns object of doctor matching the search criteria."""

    dataR= _search_bd(medecin,location.lower())
    if dataR == "null":
        return f"Désolé mais nous n'avons pas de {medecin} partenaire dans cette zone. Essayez en une autre 😊"
    else:
        message = (
                        f"Je vous recommande : {dataR[1]} \n Adresse : {dataR[2]}\n"
                        f"Telephone : {dataR[3]}.\n"
                        f"Email: {'indisponible' if dataR[4] == 'null' else dataR[4]} \n"
                    )
        return message  

class ActionSearching(Action):

    def name(self) -> Text:
        return "action_searching"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        location = tracker.get_slot("location")
        address = "Dakar pours l'instant"
        
        dispatcher.utter_message("Vous cherchez {}".format(location))

        return []

#Class for form pharmacie validation

class ValidatePharmacieForm(FormValidationAction):
    """Example of a form validation action."""

    def name(self) -> Text:
        return "validate_pharmacie_form"

    def validate_location(
        self,
        value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate location value."""

        if value.lower() in indiqueLieu(value.lower()):
            return {"location": value}
        else:
            print("not loc")
            dispatcher.utter_message("Mauvaise localisation")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"location": None}

    # async def run(
    #     self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    # ) -> List[EventType]:
    #     """ define which slot should be requested """

    #     required_slots = ["location"]

    #     for slot_name in required_slots:
    #         if tracker.slots.get(slot_name) is None:
    #             #not filled yet ask to fill this slot next
    #             return[SlotSet("requested_slot",slot_name)]
        
    #     #All slot filled
    #     return [SlotSet("requested_slot")]

#Class for form pharmacie actions

class ActionPharmacieSearching(Action):

    def name(self) -> Text:
        return "action_pharmacie_searching"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text,Any]
    ) -> List[Dict[Text,Any]]:
        
        location = tracker.get_slot('location')
        results = _find_facilities_pharmacie(location.lower())
        dispatcher.utter_message(text=results)
        # dispatcher.utter_message(text=results)

        return [SlotSet("location", None)]
  
  
#Class for medecin form validation

class ValidateMedecinForm(FormValidationAction):
    """Example of a form validation action."""

    def name(self) -> Text:
        return "validate_medecin_form"

    @staticmethod
    def specialiste_db() -> List[Text]:
        """Database of supported specialiste."""

        return [
            "dentiste",
            "ophtalmologue",
            "gynecologue",
            "clinique",
            "laboratoire",
            "cardiologue",
            "kinesitherapeute",
            "imagerie medicale",
            "ORL",
            "neurologue",
            "hopital",
            "chirurgien orthopedique",
            "urologue",
            "gastro-enterologue",
            "dermatologue",
            "rhumatologue",
            "endocrinologue",
            "orthoptiste",
            "audioprothesiste",
            "pediatre",
            "stomatologue"
        ]

    def validate_location(
        self,
        value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate location value."""

        if value.lower() in indiqueLieu(value.lower()):
            print(value)
            return {"location": value}
        else:
            print("not loc")
            dispatcher.utter_message("Mauvaise localisation")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"location": None}

    def validate_medecin_slot(
        self,
        value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate medecin value."""

        if value.lower() in ["generaliste","généraliste","géneraliste","genéraliste"]:
            print(value)
            return {"medecin_slot": "generaliste"}
        elif value.lower() in ["specialiste","spécialiste"]:
            return {"medecin_slot": "specialiste"}
        else:
            dispatcher.utter_message(template="utter_wrong_medecin")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"medecin_slot": None}

    def validate_specialiste_slot(
        self,
        value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate specialiste value."""

        if value.lower() in self.specialiste_db():
            # validation succeeded, set the value of the "specialiste" slot to value
            return {"specialiste_slot": value}
        else:
            dispatcher.utter_message(template="utter_wrong_specialiste")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"specialiste_slot": None}

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:
        """ define which slot should be requested """

        required_slots = ["location","medecin_slot"]
        
        if (tracker.get_slot("specialiste_slot") in self.specialiste_db()) and (tracker.get_slot("medecin_slot") is None):
            required_slots.remove("medecin_slot")

        if (tracker.get_slot("medecin_slot") is not None):
            if (tracker.get_slot("medecin_slot").lower() in ["specialiste","spécialiste"]) and (tracker.get_slot("specialiste_slot") is None):
                required_slots.append("specialiste_slot")

        for slot_name in required_slots:
            if tracker.slots.get(slot_name) is None:
                #not filled yet ask to fill this slot next
                return[SlotSet("requested_slot",slot_name)]        
        
        #All slot filled
        return [SlotSet("requested_slot",None)]
    
    # async def required_slots(
    #     self,
    #     slots_mapped_in_domain: List[Text],
    #     dispatcher: "CollectingDispatcher",
    #     tracker: "Tracker",
    #     domain: "DomainDict",
    # ) -> Optional[List[Text]]:
    #     additional_slots = []
    #     print(tracker.slots.get("medecin_slot"))
    #     if tracker.slots.get("medecin_slot") == "specialiste":
    #         # If the user wants to sit outside, ask
    #         # if they want to sit in the shade or in the sun.
    #         additional_slots.append("specialiste_slot")

    #     return additional_slots + slots_mapped_in_domain


#class for form medecin actions

class ActionMedecinSearching(Action):

    def name(self) -> Text:
        return "action_medecin_searching"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text,Any]
    ) -> List[Dict[Text,Any]]:
        
        location = tracker.get_slot('location')
        slot_medecin = tracker.get_slot('medecin_slot')
        slot_specialiste = tracker.get_slot('specialiste_slot')

        if (slot_medecin is not None) and (slot_medecin.lower() in ["generaliste","généraliste","géneraliste","genéraliste"]):
            slot_medecin = "generaliste"
        elif (slot_medecin is not None) and (slot_medecin.lower() in ["specialiste","spécialiste"]):
            slot_medecin = "specialiste"

        if slot_specialiste is None and slot_medecin is None:
            results = "Désolé une erreur s'est produite. Veuillez verifier vos informations"
        elif slot_specialiste is None and slot_medecin == "generaliste":
            results = _find_facilities_medecin(location,"medecin")
        else:
            results = _find_facilities_medecin(location.lower(),slot_specialiste)

        dispatcher.utter_message(text=results)
        return [SlotSet("medecin_slot", None),SlotSet("specialiste_slot", None),SlotSet("location", None)]
