# -*- coding: utf-8 -*-

import json
from readline import insert_text 
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
            card_details.append(None)

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
        #saga cards have two sides - kinda janky
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
                new_values.append(None)
            else: 
                new_values.append(', '.join(value))
        else: 
            new_values.append(None)
                
    clean[column] = new_values     

#clean["manaValue"] = clean["manaValue"].astype('int')
#clean["manaValue"] = clean["manaValue"].apply(lambda x: int(x))

clean["index"] = range(clean.shape[0])
clean = clean.set_index("index")

df_as_tuples = [tuple(clean.loc[i, :]) for i in range(clean.shape[0])]

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

# mycursor.execute("DESCRIBE neo")

# for x in mycursor.fetchall(): 
#     print(x)

## populating the table 
# I know there is an alternative using sqlalchemy 

# for row in range(clean.shape[0]): 
#     n, c, cI, mC, mV, oT, t, subt, supert, OT, kw, p, t, r, sC, img_ref = tuple([x for x in clean.loc[row, :]])

#     print(n)

#     mycursor.execute("""INSERT INTO neo VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (n, c, cI, mC, int(mV), oT, t, subt, supert, OT, kw, p, t, r, sC, img_ref))

# db.commit()

# mycursor.execute("SELECT * FROM neo")

# for x in mycursor: 
#     print(x)

## some of the names are too long for the VARCHAR(50) constraint 
# alter_query = "ALTER TABLE neo MODIFY COLUMN name VARCHAR(54)"
# mycursor.execute(alter_query)

# ### using .executemany()

# stmt = "INSERT INTO neo (name, colors, colorIdentity, manaCost, manaValue, originalType, types, subtypes, supertypes, originalText, keywords, power, toughness, rarity, setCode, image_ref) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

# mycursor.executemany(stmt, df_as_tuples)

# db.commit()

mycursor.execute("SELECT * FROM neo")

for x in mycursor: 
     # print([str(y).encode("utf-8") for y in x]) # :(
    print(x)


#codec cant  can't encode character '\u2212' = - (minus sign)