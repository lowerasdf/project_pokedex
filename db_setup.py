import mysql.connector
import csv
import os
from mysql.connector import errorcode

def generate_db():
    try:
      cnx = mysql.connector.connect(user='test1', password='test1', database='pokedex')
    except mysql.connector.Error as err:
      if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
      elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
      else:
        print(err)


    path = os.path.join(".", "csv")
    pokemon_path = os.path.join(path, "pokemon.csv")
    pokemon_type_path = os.path.join(path, "pokemon_types.csv")
    types_path = os.path.join(path, "types.csv")
    all_pokemon = {}
    pokemon_list = []
    pokemon_type_list = []
    types_list = []
    types_mapping = {}
    end_of_kalos = 722

    with open(pokemon_path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        pokemon_list = list(spamreader)[1:]
    with open(pokemon_type_path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        pokemon_type_list = list(spamreader)[1:]
    with open(types_path, newline='') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=' ', quotechar='|')
        types_list = list(spamreader)[1:]
    for row in pokemon_list:
        splitted = row[0].split(",")
        entry = [int(splitted[0]), splitted[1]]
        if int(splitted[0]) == end_of_kalos:
            break
        all_pokemon[int(splitted[0])] = entry
    for row in types_list:
        splitted = row[0].split(",")
        types_mapping[int(splitted[0])] = splitted[1]
    for row in pokemon_type_list:
        splitted = row[0].split(",")
        if int(splitted[0]) == end_of_kalos:
            break
        all_pokemon[int(splitted[0])].append(types_mapping[int(splitted[1])])

    cursor = cnx.cursor()
    cursor.execute("DROP TABLE IF EXISTS pokemon;")
    cursor.execute('CREATE TABLE `pokemon` (`ID` int(11) NOT NULL AUTO_INCREMENT,`Name` varchar(100) DEFAULT NULL,`Type_1` varchar(100) DEFAULT NULL,`Type_2` varchar(100) DEFAULT NULL,PRIMARY KEY (`ID`)) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;')
    insert_query = ("INSERT INTO pokemon " "(Name, Type_1, Type_2)" "VALUES (%s, %s, %s)")
    for _, val in all_pokemon.items():
        if len(val) == 3:
            data = (val[1], val[2], None)
        elif len(val) == 4:
            data = (val[1], val[2], val[3])
        cursor.execute(insert_query, data)
    cnx.commit()

    cursor.close()
    cnx.close()
    print("Database has been successfully created!")

if __name__=="__main__":
    generate_db()

