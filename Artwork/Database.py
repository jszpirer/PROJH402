#This class is used to choose between different color palettes for the Voronoi Diagram
import sqlite3
from sqlite3 import Error
import random


class Database:
    location = None
    connection = None
    cursor = None

    def __init__(self, location):
        self.location = location
        self.__create_table_colors()
        self.__create_table_coauthors()


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

    def __create_table_colors(self):
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

    def __create_table_coauthors(self):
        """Creates the table containing username1, username2 and common key associated."""
        self.__open_connection()
        sql_request = """CREATE TABLE IF NOT EXISTS coauthors(
                                author text PRIMARY KEY,
                                palette integer NOT NULL);"""
        try:
            self.cursor.execute(sql_request)
        except Error as e:
            print(e)
        self.connection.commit()
        self.__close_connection()

    def remove_all_rows(self):
        """Deletes all rows from the palette table."""
        self.__open_connection()
        sql_request = """DROP TABLE color_palettes;"""
        try:
            self.cursor.execute(sql_request)
        except Error as e:
            print(e)
        self.connection.commit()
        self.__close_connection()

    def remove_all_rows_subjects(self):
        """Deletes all rows from the palette table."""
        self.__open_connection()
        sql_request = """DROP TABLE subjects"""
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
                     VALUES(1, '(255,255,255)', '(218,242,218)', '(184,230,184)', '(152,217,152)', '(106,77,50)', '(0,0,0)', '(30,63,31)', '(107,50,17)', '(70,105,0)', '(124,67,37)'), 
                     (2, '(220,172,164)', '(188,132,124)', '(164,76,20)', '(84,60,60)', '(28,36,36)', '(228,228,228)', '(195,115,115)', '(199,142,142)', '(199,162,142)', '(125, 48, 6)'),
                     (3, '(218,189,166)', '(91,51,37)', '(159,123,79)', '(40,30,27)', '(143,96,59)', '(170,157,141)', '(167,146,140)', '(133,99,92)', '(180,108,60)', '(214,178,113)'),
                     (4, '(235,214,188)', '(44,25,24)', '(192,99,59)', '(135,52,37)', '(178,151,144)', '(130,117,108)', '(244,168,51)', '(84,73,67)', '(91,87,84)', '(84,60,60)');"""
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
        result = data[0]
        self.__close_connection()
        return result

    def get_palette_from_author(self, author):
        self.__open_connection()
        sql_select = """SELECT palette
                        FROM coauthors
                        WHERE author = '""" +author+ """';"""
        self.cursor.execute(sql_select)
        data = self.cursor.fetchall()
        if len(data) == 0:
            return None
        result = data[0][0]
        self.__close_connection()
        return result

    def add_author(self, author, palette):
        self.__open_connection()
        sql_add = """INSERT INTO coauthors
                        VALUES ('"""+author+"""', """+str(palette)+""");"""
        try:
            self.cursor.execute(sql_add)
        except Error as e:
            print(e)
        self.connection.commit()
        self.__close_connection()

    def color_from_coauthors(self, list_of_coauthors, profile_name):
        colors = []
        color_in_db = self.get_palette_from_author(profile_name)
        if color_in_db is not None:
            new_color = color_in_db
        else:
            if len(list_of_coauthors)==0:
                new_color = random.randint(1, 4)
            else:
                for author in list_of_coauthors:
                    print(author)
                    color = self.get_palette_from_author(author)
                    if color is not None:
                        print(color)
                        colors.append(color)
                if len(colors)==0:
                    new_color = random.randint(1, 4)
                else:
                    new_color = self.most_frequent(colors)
            self.add_author(profile_name, new_color)
        return new_color

    def most_frequent(self, colors):
        counter = 0
        num = colors[0]

        for i in colors:
            curr_frequency = colors.count(i)
            if (curr_frequency > counter):
                counter = curr_frequency
                num = i

        return num