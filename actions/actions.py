# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/core/actions/#custom-actions/

# pylint: disable=import-error


# This is a simple example for a custom action which utters "Hello World!"

from typing import Any, Text, Dict, List, Optional
import nltk 
nltk.download('punkt')
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
from rasa_sdk.events import SlotSet, AllSlotsReset, EventType
from rasa_sdk.forms import FormValidationAction
from actions.dbConnect import getData,call_get_distance #pylint: disable=import-error

import json,re
import os
import random


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


def hyperlink_payload(tracker, message, title, url):
    return {
        "attachment": {
            "type": "template",
            "payload": {
                "template_type": "button",
                "text": message,
                "buttons": [
                    {
                        "type": "web_url",
                        "url": url,
                        "title": title,
                        "webview_height_ratio": "full",
                    }
                ],
            },
        }
    }


def _search_location_specialites(loctext: Text,pattern:bool):
    """
            Given location or specialites , we search in the bd of the id 
            :param loctext: the data the text location or the specialites
            :param pattern: the process to do 1 for loc 0 for specialite 
            :return: list of elements or null
    """
    if pattern:
        query = f'''SELECT id, nom, location, latitude, longitude from lieuxes where nom LIKE "%{loctext}%" '''
    else :
        query = f'''SELECT id, nom from specialites where nom LIKE "%{loctext}%" '''
        
    # ## pass the sql query to the getData method and store the results in `data` variable.
    data = getData(query)
    if len(data) == 0:
        return "null"
    else:  
        return data[0] 

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
        

def _format_responses(data: any,type: bool):
    """
            Given data and a type we extract (if the type is 1) the lat and lng from the slot
            or we extract it from the databases responses (is the type is 0)
            :param location: the data passed to process
            :param kind: the process to use 1 for extraction 0 for formatting response 
            :return: Dict of two slots
            """
    returndata = []
    if type:
        b = re.split('[":{},]',data)
        returndata.extend([b[4],b[8]])
    # else: 
        # to continue include the dispatcher etc
        # 0 : id
        # 1 : nom
        # 2 : adresse
        # 3 : telephon
        # 4 : emai
        # 5 : disponibilite
        # 6 : specialite 
        # 7 : latitude
        # 8 : longitude
        # 9 : localisation

        # for result in data:
        #     print(result[0])
        #     print(result[1])
        #     print(result[2])
        #     print(result[3])
    
    return returndata


def get_latest_event(events):
    latest_actions = []
    for e in events:
        if e['event'] == 'action':
            latest_actions.append(e)

    return latest_actions[-4:][0]['name']

class AskForLocationAction(Action):
    def name(self) -> Text:
        return "action_ask_location"

    def run(
        self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict
    ) -> List[EventType]:

        reply_Markup = {"keyboard":[ [{ "text":"Appuyez pour envoyer votre localisation", "request_location":True }] ] , "one_time_keyboard":True }
        jsonaa = {
                "chat_id":tracker.current_state()['sender_id'],
                "text":"Pouvez vous partagez avec nous votre localisation svp ? \n Vous pouvez soit écrire du texte ou appuyer sur le boutton ",
                "reply_markup": json.dumps(reply_Markup)
                }        
        dispatcher.utter_message(json_message=jsonaa)
        return []

class ActionStoreIntentMessage(Action):
    """Stores the bot use case in a slot"""

    def name(self):
        return "action_store_intent_message"

    def run(self, dispatcher, tracker, domain):

        # we grab the whole user utterance here as there are no real entities
        # in the use case
        message = tracker.latest_message['intent'].get('name')

        return [SlotSet('intent_message', message)]

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

        # if value.lower() in indiqueLieu(value.lower()):

        if re.search(r"((\{\"lng\":)(\-?|\+?)?\d+(\.\d+)?),\s*((\{?\"lat\":)(\-?|\+?)?\d+(\.\d+)?)\}", value.lower()) :
            return {"location": value}
        elif value.lower() in _search_location_specialites(value.lower(),True):
            return {"location": value}
        else:
            dispatcher.utter_message("Mauvaise localisation")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"location": None}


#Class for form pharmacie actions

class ActionPharmacieSearching(Action):

    def name(self) -> Text:
        return "action_pharmacie_searching"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text,Any]
    ) -> List[Dict[Text,Any]]:
        
        dispatcher.utter_message(text="Merci pour le partage, veuillez patienter un instant svp...")
        location = tracker.get_slot('location')
        if re.search(r"((\{\"lng\":)(\-?|\+?)?\d+(\.\d+)?),\s*((\{?\"lat\":)(\-?|\+?)?\d+(\.\d+)?)\}", location.lower()) :
            datatopass = _format_responses(location,True)
            #We extract and pass the lat datatopass[1] and the long datatopass[0] to the function
            a = call_get_distance(datatopass[1],datatopass[0],5,1)
            if a:
                dispatcher.utter_message(text="Je vous recommande les adresses suivantes selon votre localisation")
                for result in a:
                    message = (
                                f"Nom : {result[1]} \n Adresse : {result[2]}\n"
                                f"Telephone : {result[3]}.\n"
                                f"Email: {'indisponible' if result[4] == 'null' else result[4]} \n"
                            )
                    # dispatcher.utter_message(text=message)
                    reply_Markup = {"inline_keyboard":[ [{ "text":"Localisation sur google maps", "url":result[9] }] ] }
                    jsonaa = {
                            "chat_id":tracker.current_state()['sender_id'],
                            "text":message,
                            "reply_markup": json.dumps(reply_Markup)
                            }        
                    dispatcher.utter_message(json_message=jsonaa)                                       

            else:
                dispatcher.utter_message(text="Désolé mais nous n'avons pas de pharmacie partenaire dans cette zone. Essayez en une autre 😊")
        else:
            ech = _search_location_specialites(location.lower(),True)
            if ech: 
                a = call_get_distance(ech[3],ech[4],5,1)
                if a :
                    dispatcher.utter_message(text="Je vous recommande les adresses suivantes selon votre localisation")
                    for result in a:
                        message = (
                                    f"Nom : {result[1]} \n Adresse : {result[2]}\n"
                                    f"Telephone : {result[3]}.\n"
                                    f"Email: {'indisponible' if result[4] == 'null' else result[4]} \n"
                                )
                        reply_Markup = {"inline_keyboard":[ [{ "text":"Localisation sur google maps", "url":result[9] }] ] }
                        jsonaa = {
                                "chat_id":tracker.current_state()['sender_id'],
                                "text":message,
                                "reply_markup": json.dumps(reply_Markup)
                                }        
                        dispatcher.utter_message(json_message=jsonaa)
                else :
                    dispatcher.utter_message(text="Désolé mais nous n'avons pas de pharmacie partenaire dans cette zone. Essayez en une autre 😊")                    
            else:
                dispatcher.utter_message(text="Désolé mais nous n'avons pas de pharmacie partenaire dans cette zone. Essayez en une autre 😊")

        ### This is how we were searching before ! (we keep it we never know)  ###
        # results = _find_facilities_pharmacie(location.lower())
        # dispatcher.utter_message(text=results)
        return [SlotSet("location", None)]



#Class for form hospitalisation validation

class ValidateHospitalisationForm(FormValidationAction):
    """Example of a form validation action."""

    def name(self) -> Text:
        return "validate_hospitalisation_form"

    def validate_location(
        self,
        value: Any,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> Dict[Text, Any]:
        """Validate location value."""

        if re.search(r"((\{\"lng\":)(\-?|\+?)?\d+(\.\d+)?),\s*((\{?\"lat\":)(\-?|\+?)?\d+(\.\d+)?)\}", value.lower()) :
            return {"location": value}
        elif value.lower() in _search_location_specialites(value.lower(),True):
            return {"location": value}
        else:
            dispatcher.utter_message("Mauvaise localisation")
            # validation failed, set this slot to None, meaning the
            # user will be asked for the slot again
            return {"location": None}
        


#Class for form hospitalisation actions

class ActionHospitalisationSearching(Action):

    def name(self) -> Text:
        return "action_hospitalisation_searching"

    async def run(
        self, dispatcher, tracker: Tracker, domain: Dict[Text,Any]
    ) -> List[Dict[Text,Any]]:
                
        results = ""
        intent = tracker.get_slot('intent_message')
        specialite_id = _search_location_specialites(intent.lower(),False)
        location = tracker.get_slot('location')

        if re.search(r"((\{\"lng\":)(\-?|\+?)?\d+(\.\d+)?),\s*((\{?\"lat\":)(\-?|\+?)?\d+(\.\d+)?)\}", location.lower()) :
            datatopass = _format_responses(location,True)
            #We extract and pass the lat datatopass[1] and the long datatopass[0] to the function
            a = call_get_distance(datatopass[1],datatopass[0],5,specialite_id[0])
            if a:
                dispatcher.utter_message(text="Je vous recommande les adresses suivantes selon votre localisation")                
                for result in a:
                    message = (
                                f"Nom : {result[1]} \n Adresse : {result[2]}\n"
                                f"Telephone : {result[3]}.\n"
                                f"Email: {'indisponible' if result[4] == 'null' else result[4]} \n"
                            )
                    # dispatcher.utter_message(text=message)
                    reply_Markup = {"inline_keyboard":[ [{ "text":"Localisation sur google maps", "url":result[9] }] ] }
                    jsonaa = {
                            "chat_id":tracker.current_state()['sender_id'],
                            "text":message,
                            "reply_markup": json.dumps(reply_Markup)
                            }        
                    dispatcher.utter_message(json_message=jsonaa)            
            else:
                dispatcher.utter_message(text="Désolé mais nous n'avons pas de partenaires dans cette zone. Essayez en une autre 😊"    )            
        else:
            ech = _search_location_specialites(location.lower(),True)
            a = call_get_distance(ech[3],ech[4],5,specialite_id[0])
            if a: 
                dispatcher.utter_message(text="Je vous recommande les adresses suivantes selon votre localisation")
                for result in a:
                    message = (
                                f"Nom : {result[1]} \n Adresse : {result[2]}\n"
                                f"Telephone : {result[3]}.\n"
                                f"Email: {'indisponible' if result[4] == 'null' else result[4]} \n"
                            )
                    reply_Markup = {"inline_keyboard":[ [{ "text":"Localisation sur google maps", "url":result[9] }] ] }
                    jsonaa = {
                            "chat_id":tracker.current_state()['sender_id'],
                            "text":message,
                            "reply_markup": json.dumps(reply_Markup)
                            }        
                    dispatcher.utter_message(json_message=jsonaa)
            else:
                dispatcher.utter_message(text="Désolé mais nous n'avons pas de partenaires dans cette zone. Essayez en une autre 😊")

        return [SlotSet("intent_message", None),SlotSet("location", None)]
  
  
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

        if re.search(r"((\{\"lng\":)(\-?|\+?)?\d+(\.\d+)?),\s*((\{?\"lat\":)(\-?|\+?)?\d+(\.\d+)?)\}", value.lower()) :
            return {"location": value}
        elif value.lower() in _search_location_specialites(value.lower(),True):
            return {"location": value}
        else:
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

        # if value.lower() in self.specialiste_db():
        if value.lower() in _search_location_specialites(value.lower(),False):
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
        a = None

        if (slot_medecin is not None) and (slot_medecin.lower() in ["generaliste","généraliste","géneraliste","genéraliste"]):
            slot_medecin = "generaliste"
        elif (slot_medecin is not None) and (slot_medecin.lower() in ["specialiste","spécialiste"]):
            slot_medecin = "specialiste"
        elif slot_specialiste is None and slot_medecin is None:
            results = "Désolé une erreur s'est produite. Veuillez verifier vos informations et recommencez svp"
            dispatcher.utter_message(text=results)
            return [SlotSet("medecin_slot", None),SlotSet("specialiste_slot", None),SlotSet("location", None)]

        if re.search(r"((\{\"lng\":)(\-?|\+?)?\d+(\.\d+)?),\s*((\{?\"lat\":)(\-?|\+?)?\d+(\.\d+)?)\}", location.lower()) :
            datatopass = _format_responses(location,True)
            #We extract and pass the lat datatopass[1] and the long datatopass[0] to the function
            if slot_specialiste is None and slot_medecin == "generaliste":
                # results = _find_facilities_medecin(location,"medecin")
                a = call_get_distance(datatopass[1],datatopass[0],5,4)
            else:
                specialite_id = _search_location_specialites(slot_specialiste.lower(),False)
                # results = _find_facilities_medecin(location.lower(),slot_specialiste)
                a = call_get_distance(datatopass[1],datatopass[0],5,specialite_id[0])
            if a:
                dispatcher.utter_message(text="Je vous recommande les adresses suivantes selon votre localisation")
                for result in a:
                    message = (
                                f"Nom : {result[1]} \n Adresse : {result[2]}\n"
                                f"Telephone : {result[3]}.\n"
                                f"Email: {'indisponible' if result[4] == 'null' else result[4]} \n"
                            )
                    # dispatcher.utter_message(text=message)
                    reply_Markup = {"inline_keyboard":[ [{ "text":"Localisation sur google maps", "url":result[9] }] ] }
                    jsonaa = {
                            "chat_id":tracker.current_state()['sender_id'],
                            "text":message,
                            "reply_markup": json.dumps(reply_Markup)
                            }        
                    dispatcher.utter_message(json_message=jsonaa)            
            else:
                dispatcher.utter_message(text="Désolé mais nous n'avons pas de partenaires dans cette zone. Essayez en une autre 😊")    
        else:
            ech = _search_location_specialites(location.lower(),True)
            if slot_specialiste is None and slot_medecin == "generaliste":
                # results = _find_facilities_medecin(location,"medecin")
                a = call_get_distance(ech[3],ech[4],5,4)
            else:
                # results = _find_facilities_medecin(location.lower(),slot_specialiste)
                specialite_id = _search_location_specialites(slot_specialiste.lower(),False)
                a = call_get_distance(ech[3],ech[4],5,specialite_id[0])
                
            if a: 
                dispatcher.utter_message(text="Je vous recommande les adresses suivantes selon votre localisation")
                for result in a:
                    message = (
                                f"Nom : {result[1]} \n Adresse : {result[2]}\n"
                                f"Telephone : {result[3]}.\n"
                                f"Email: {'indisponible' if result[4] == 'null' else result[4]} \n"
                            )
                    reply_Markup = {"inline_keyboard":[ [{ "text":"Localisation sur google maps", "url":result[9] }] ] }
                    jsonaa = {
                            "chat_id":tracker.current_state()['sender_id'],
                            "text":message,
                            "reply_markup": json.dumps(reply_Markup)
                            }        
                    dispatcher.utter_message(json_message=jsonaa)
            else:
                dispatcher.utter_message(text="Désolé mais nous n'avons pas de partenaires dans cette zone. Essayez en une autre 😊"    )
                
        return [SlotSet("medecin_slot", None),SlotSet("specialiste_slot", None),SlotSet("location", None)]
