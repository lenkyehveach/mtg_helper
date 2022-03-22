import json 
import pandas as pd 
import numpy as np 

# sql 
import mysql.connector
import configparser

f = open("Standard.json", encoding="utf8")
neo_full = json.load(f)

columns = ["name", "colors", "colorIdentity", "manaCost", "manaValue", "originalType", "types", "subtypes", "supertypes", "originalText", "keywords", "power", "toughness", "rarity", "setCode", "image_ref"]

neo_set = []
for card in neo_full["data"]["NEO"]["cards"]: 
    card_details = []

    check = [x in card.keys() for x in columns]
    for att, present in zip(columns, check[:-1]): 
        
        if present: 
            card_details.append(card[att])
        else: 
            card_details.append(np.nan)

    #add the first available link to image         
    card_details.append(card["purchaseUrls"][list(card["purchaseUrls"].keys())[0]])

    neo_set.append(card_details)


######clean the data up a lil bit

#1 set contains multiple different artworks of the same card; unnecessary 

neo_df = pd.DataFrame(neo_set, columns=columns)

first_copy = []
pos = [False for x in range(len(neo_df["name"].values))]

for i in range(len(neo_df["name"].values)): 
           
    if neo_df["name"][i] in first_copy: 
        if ("//" in neo_df["name"][i]) & (first_copy.count(neo_df['name'][i]) < 2):
            first_copy.append(neo_df["name"][i])
            pos[i] = True
            
    if not neo_df["name"][i] in first_copy:
        first_copy.append(neo_df["name"][i])
        pos[i] = True      

clean = neo_df.loc[pos]

list_cols = ["colors" , "colorIdentity", "types", "subtypes", "supertypes", "keywords"] 

#2 converting the columns which contain lists to str
for column in list_cols: 
    new_values = []
    for i in range(clean.shape[0]):
        value = clean[column].values[i]
        #print(value, i)
        if type(value) == list: 
            if len(value) == 0:
                new_values.append(np.nan)
            else: 
                new_values.append(', '.join(value))
        else: 
            new_values.append(np.nan)
                
    clean[column] = new_values     

clean["manaValue"] = clean["manaValue"].astype('int32')


### put this into a SQL database 
config = configparser.ConfigParser()
config.read('mtg_helper/db.ini')

db = mysql.connector.connect(
  host = config["mysql"]["host"], 
  user = config["mysql"]["user"],
  passwd = config["mysql"]["passwd"],
  database = config["mysql"]["database"] # uncomment once created

)

mycursor = db.cursor()

## Create db: 
#mycursor.execute("CREATE DATABASE mtg_standard")

## creating table for NEO cards - different tables for different sets? 

# mycursor.execute("""CREATE TABLE neo (
#   name VARCHAR(50), 
#   colors VARCHAR(50), 
#   colorIdentity VARCHAR(50), 
#   manaCost VARCHAR(50), 
#   manaValue tinyint UNSIGNED, 
#   originalType VARCHAR(50), 
#   types VARCHAR(50), 
#   subtypes VARCHAR(50), 
#   supertypes VARCHAR(50), 
#   originalText TEXT, 
#   keywords VARCHAR(50), 
#   power tinyint UNSIGNED, 
#   toughness tinyint UNSIGNED, 
#   rarity VARCHAR(10), 
#   setCode VARCHAR(3), 
#   image_ref VARCHAR(50),
#   cardID int PRIMARY KEY AUTO_INCREMENT)
#   """)

mycursor.execute("DESCRIBE neo")
result = mycursor.fetchall()
for row in result: 
    print(row)