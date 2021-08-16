# This is a simple module to fetch data from MySQL db.
# python -m pip install mysql-connector //run this command if you face import error
# references: https://www.w3schools.com/python/python_mysql_getstarted.asp

import mysql.connector
import traceback

def getData(query:str):
        """
         @query: sql query that needs to be executed.
         returns the data being executed in "List" format
        """

        try:

            # Setup the connection.
            # Pass your database details here
            mydb = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="rasa_sante_bot"
                )

            # set up the cursor to execute the query
            cursor = mydb.cursor()
            cursor.execute(query)

            # fetch all rows from the last executed statement using `fetchall method`.
            results = cursor.fetchall()
            return results
        except:
            print("Error occured while connecting to database or fetching data from database. Error Trace: {}".format(traceback.format_exc()))
            return []


# test the file before integrating with the bot by uncommenting the below line.
#   cur = conn.cursor()
#         cur.execute(f'''SELECT * FROM eduresources
#                     WHERE {slot_name}="{slot_value}"''')

#         # return an array
#         rows = cur.fetchall()

#         return(rows)

# SELECT responses.id, responses.nom, responses.adresse, responses.telephone, responses.email, responses.disponibilite, responses.specialite from responses 
#     WHERE responses.adresse like '%hann mariste%' and responses.specialite IN 
#     (SELECT id from specialites WHERE specialites.nom LIKE "%d%")

# lieux d'une spec
# SELECT *
# FROM `lieuxes` WHERE lieuxes.id IN (
#     SELECT lieux_id
#     FROM `lieuxes_specialites__specialites_lieuxes`
#     WHERE specialite_id IN (
#     select specialites.id FROM specialites WHERE specialites.nom like "dentiste" )
#   )

#spec / lieu
# SELECT * FROM specialites WHERE specialites.id in (
#     SELECT specialite_id
#     FROM `lieuxes_specialites__specialites_lieuxes`
#     WHERE lieux_id IN (
#         SELECT lieuxes.id FROM lieuxes WHERE lieuxes.nom LIKE "dakar")
#     )

# not working 
# SELECT * FROM `responses` WHERE specialite IN (
#     SELECT specialites.id FROM specialites WHERE specialites.id IN (
#     	SELECT specialite_id FROM `lieuxes_specialites__specialites_lieuxes` WHERE lieux_id IN (
#         		SELECT lieuxes.id FROM lieuxes WHERE lieuxes.nom LIKE "touba") AND specialites.nom = "dentiste"))
