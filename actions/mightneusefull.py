#from dbConnect import getData
# # write the sql query here.
# query = "select * from customer"
## pass the sql query to the getData method and store the results in `data` variable.
# data = getData(query)

#in hospitalisationn action ####

        # if intent is None:
        #     results = "Désolé une erreur s'est produite. Veuillez verifier vos informations"
        # else:
        #     results = _find_facilities_medecin(location.lower(),intent)

        # dispatcher.utter_message(text=results)
        # dispatcher.utter_message(text=results)

### medecin action searching ###
        # if slot_specialiste is None and slot_medecin == "generaliste":
        #     results = _find_facilities_medecin(location,"medecin")
        # else:
        #     results = _find_facilities_medecin(location.lower(),slot_specialiste)

        # dispatcher.utter_message(text=results)
         

# location validation ###########

        # if value.lower() in indiqueLieu(value.lower()):
        #     return {"location": value}
        # else:
        #     print("not loc")
        #     dispatcher.utter_message("Mauvaise localisation")
        #     # validation failed, set this slot to None, meaning the
        #     # user will be asked for the slot again
        #     return {"location": None}


### run function in ValidatePharmacieForm classs ####

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


 #This is for sending a maps in the chat 
                    # dispatcher.utter_message(
                    #     response="utter_give_location",
                    #     text="Voici sa localisation sur maps",
                    #     lat=str(result[7]),
                    #     long=str(result[8])
                    # )



#### ancienne fonction search pharmacie or medecin ####

# def _find_facilities_pharmacie(location: Text) -> Text:
#     """Returns object of pharma matching the search criteria."""

#     dataR= _search_bd("Pharmacies",location.lower())
#     if dataR == "null":
#         return "Désolé mais nous n'avons pas de pharmacie partenaire dans cette zone. Essayez en une autre 😊"
#     else:
#         message = (
#                         f"Je vous recommande : {dataR[1]} \n Adresse : {dataR[2]}\n"
#                         f"Telephone : {dataR[3]}.\n"
#                         f"Email: {'indisponible' if dataR[4] == 'null' else dataR[4]} \n"
#                     )
#         return message                


# def _find_facilities_medecin(location: Text, medecin: Text) -> Text:
#     """Returns object of doctor matching the search criteria."""

#     dataR= _search_bd(medecin,location.lower())
#     if dataR == "null":
#         return f"Désolé mais nous n'avons pas de {medecin} partenaire dans cette zone. Essayez en une autre 😊"
#     else:
#         message = (
#                         f"Je vous recommande : {dataR[1]} \n Adresse : {dataR[2]}\n"
#                         f"Telephone : {dataR[3]}.\n"
#                         f"Email: {'indisponible' if dataR[4] == 'null' else dataR[4]} \n"
#                     )
#         return message  


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


#### required slot function for medecin form ####

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


