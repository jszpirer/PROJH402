#This class is used to choose between different color palettes for the Voronoi Diagram
import sqlite3
from sqlite3 import Error


class Database_color:
    location = None
    connection = None
    cursor = None

    def __init__(self, location):
        self.location = location
        #A retirer pour l'utilisateur car la database sera d'office créée.
        self.__create_table()

    def __open_connection(self):
        """Creates the connection with the database if the database does not already exist."""
        try:
            self.connection = sqlite3.connect(self.location)
            self.cursor = self.connection.cursor()
        except Error as e:
            print(e)

    def __close_connection(self):
        """Closes all the connections."""
        self.cursor.close()
        self.connection.close()

    def __create_table(self):
        """Creates the table containing username1, username2 and common key associated."""
        self.__open_connection()
        sql_request = """CREATE TABLE IF NOT EXISTS color_palettes(
                                name integer PRIMARY KEY,
                                color1 text NOT NULL,
                                color2 text NOT NULL,
                                color3 text NOT NULL,
                                color4 text NOT NULL,
                                color5 text NOT NULL,
                                color6 text NOT NULL,
                                color7 text NOT NULL,
                                color8 text NOT NULL,
                                color9 text NOT NULL,
                                color10 text NOT NULL);"""
        try:
            self.cursor.execute(sql_request)
        except Error as e:
            print(e)
        self.connection.commit()
        self.__close_connection()

    def remove_all_rows(self):
        """Deletes all rows from the palette table."""
        self.__open_connection()
        sql_request = """DELETE FROM color_palettes"""
        try:
            self.cursor.execute(sql_request)
        except Error as e:
            print(e)
        self.connection.commit()
        self.__close_connection()

    def add_palettes(self):
        """Function that needs to be used once to add all palettes in the database."""
        self.__open_connection()
        sql_insert_client = """INSERT INTO color_palettes
                     VALUES(1, '(0,18,25)', '(0,95,115)', '(10,147,150)', '(148,210,189)', '(233,216,166)', '(238,155,0)', '(202,103,2)', '(187,62,3)', '(174,32,18)', '(155,34,38)'), 
                     (2, '(5,60,94)', '(29,57,88)', '(53,54,82)', '(76,51,77)', '(100,48,71)', '(124,46,65)', '(148,43,59)', '(171,40,54)', '(195,37,48)', '(219, 34, 42)'),
                     (3, '(217,237,146)', '(181,228,140)', '(153,217,140)', '(118,200,147)', '(82,182,154)', '(52,160,164)', '(22,138,173)', '(26,117,159)', '(30,96,145)', '(24,78,119)');"""
        self.cursor.execute(sql_insert_client)
        self.connection.commit()
        self.__close_connection()

    def get_palette(self, numberOfPalette):
        self.__open_connection()
        sql_select = """
                    SELECT color1, color2, color3, color4, color5, color6, color7, color8, color9, color10
                    FROM color_palettes
                    WHERE name = '""" + str(numberOfPalette) + """';"""
        self.cursor.execute(sql_select)
        data = self.cursor.fetchall()
        print(data)
        result =  data[0]
        self.__close_connection()
        return result

test = Database_color("colors.db")
test.remove_all_rows()
test.add_palettes()
test.get_palette(1)