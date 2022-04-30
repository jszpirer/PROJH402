import numpy as np
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from scipy.spatial import Voronoi, voronoi_plot_2d
from Artwork.Database import Database
import os
import glob
from PIL import Image


class ScipyVoronoi():
    most_frequent_word = None
    output_path = None
    color_database = None
    cmap = None
    palette = None

    def __init__(self, output_path, citations, list_of_coauthors, profile_name):
        #self.most_frequent_word = most_frequent_word
        self.citations = citations
        self.output_path = output_path
        self.color_database = Database("Artwork/ArtCreator.db")
        self.palette = self.color_database.color_from_coauthors(list_of_coauthors, profile_name)
        self.id = output_path

    def number_of_points_v1(self):
        nb_points = 0
        power_of_p = 1
        m = 10 ** (9) + 9  # probability of two random strings colliding is inversely proportional to m
        if self.most_frequent_word.isupper():
            p = 53
        else:
            p = 31
        for x in self.most_frequent_word:
            nb_points = (nb_points + (ord(x) - ord('a') + 1) * power_of_p) % m
            power_of_p = (power_of_p * p) % m
        nb_points = ((nb_points % m + m) % m) % 500
        return nb_points

    """def number_of_points(self, citations):
        #Calculate the number of points thanks to the number of citations.
        print("C'est le type")
        print(type(citations))
        nb_points = citations%900
        if citations >= 100000:
            nb_points += citations//1000
        elif citations >= 10000:
            nb_points += citations//500
        elif citations > 900:
            nb_points += citations//100
        else:
            nb_points//2
        return nb_points"""

    def number_of_points(self, citations):
        #nb_points = 20*int(np.log2(citations))
        nb_points = 10*int(np.sqrt(citations))
        if nb_points < 4:
            nb_points += 4
        return nb_points

    def position_of_points(self, nb_points, dict_years: dict):
        # The position of points depends on something.
        # list_of_points = np.random.weibull(a=3, size=[nb_points, 2])
        # On calcule d'abord le pourcentage d'articles par année
        total_articles = 0
        total_years = 0
        for key in dict_years.keys():
            total_articles += dict_years[key]
            total_years += 1
        # Il faut re-parcourir la liste pour avoir le pourcentage d'article par année
        if total_years == 0:
            return np.random.weibull(a=3, size=[nb_points, 2])
        dict_years = dict(sorted(dict_years.items()))
        list_percentage = []
        for key in dict_years.keys():
            dict_years[key] /= total_articles
            list_percentage.append(dict_years[key])
        list_of_points = np.ndarray((nb_points, 2), float) # Now we have to change the values into the right ones.
        # list_of_points = np.random.beta(a=2, b=8, size=[nb_points, 2])
        # On doit séparer l'espace en le nombre d'années du dictionnaire, trop d'espaces diff
        # On sépare d'abord en quatre parties.
        splitted_points = np.array_split(list_percentage, 4)
        p = 0
        r = 0
        for line in range(2):
            for column in range(2):
                percentages = 0
                for perc in splitted_points[p]:
                    percentages+=perc
                # On a le pourcentage du quartier
                p+=1
                points_of_quarter = int(nb_points*percentages)
                # Maintenant il faut trouver les coordonnées de chaque point.
                for point in range(points_of_quarter):
                    #x = np.random.uniform(low=column*0.5,high=(column+1)*0.5)
                    #y = np.random.uniform(low=line*0.5,high=(line+1)*0.5)
                    x = np.random.normal(0.25+column*0.5, 0.2, size=(1,1))
                    y = np.random.normal(0.25+line*0.5, 0.2, size=(1,1))
                    list_of_points[r][0] = x[0][0]
                    list_of_points[r][1] = y[0][0]
                    r += 1
        list_of_points = list_of_points[:r]
        return list_of_points

    def make_diagram(self, dict_years: dict, path_gif=None):
        # generate data/speed values
        # nb_points = self.number_of_points_v1()
        nb_points = self.number_of_points(self.citations)
        points = self.position_of_points(nb_points, dict_years)
        speed = np.random.uniform(low=0.0, high=15.0,
                                  size=nb_points)  # TODO: A améliorer pour que ça ne soit plus random

        # generate Voronoi tessellation
        vor = Voronoi(points)

        # find min/max values for normalization
        minima = min(speed)
        maxima = max(speed)

        # create colormap from list
        self.get_palette_in_database(self.palette)
        colormap = LinearSegmentedColormap.from_list("mycmap", self.cmap)

        # normalize chosen colormap
        norm = mpl.colors.Normalize(vmin=minima, vmax=maxima, clip=True)
        mapper = cm.ScalarMappable(norm=norm, cmap=colormap)  # We could change the colormap to make it unique

        # plot Voronoi diagram, and fill finite regions with color mapped from speed value
        voronoi_plot_2d(vor, show_points=False, show_vertices=False, s=1)
        for r in range(len(vor.point_region)):
            region = vor.regions[vor.point_region[r]]
            if not -1 in region:
                polygon = [vor.vertices[i] for i in region]
                plt.fill(*zip(*polygon), color=mapper.to_rgba(speed[r]))
        #plt.show()
        plt.axis("off")
        self.output_path = "Pictures/"+self.output_path+".pdf"
        if path_gif is None:
            plt.savefig(self.output_path, bbox_inches='tight')
        else:
            plt.savefig(path_gif, bbox_inches='tight')
        return 0

    # Permet de tester les palettes créées facilement
    def plot_examples(self, colormaps):
        """
        Helper function to plot data with associated colormap.
        """
        np.random.seed(19680801)
        data = np.random.randn(30, 30)
        n = len(colormaps)
        fig, axs = plt.subplots(1, n, figsize=(n * 2 + 2, 3),
                                constrained_layout=True, squeeze=False)
        for [ax, cmap] in zip(axs.flat, colormaps):
            psm = ax.pcolormesh(data, cmap=cmap, rasterized=True, vmin=-4, vmax=4)
            fig.colorbar(psm, ax=ax)
        plt.show()

    def get_palette_in_database(self, number):
        """Gets the right palette into the colors database."""
        list_of_colors_string = self.color_database.get_palette(number)
        # This list needs to be changed because it's a list of strings.
        self.change_into_colors(list_of_colors_string)

    def change_into_colors(self, list_of_strings):
        """Transform information from database and fill in the cmap."""
        self.cmap = []
        for color in list_of_strings:
            new_color = eval(color)
            tuple_to_add = tuple(ti / 255 for ti in new_color)
            self.cmap.append(tuple_to_add)

    def make_gif(self, dict_years : dict, nb_images):
        # Creates a gif from voronoi diagrams.
        nb_image = 0
        file_names=[]
        for i in range(nb_images):
            path_image = "Gif/" + str(nb_image) + ".png"
            self.make_diagram(dict_years, path_gif=path_image)
            file_names.append(path_image)
            if len(dict_years)!=0:
                self.citations -= dict_years[sorted(dict_years)[-1]]
                dict_years.popitem()
            nb_image+=1
        images = [Image.open(fn) for fn in file_names]
        self.output_path = "Gif/"+self.id+".gif"
        images[0].save(self.output_path,"GIF", save_all=True, append_images=images[1:], duration=300, loop=0)
        # End of the function
        self.clean_folders()
        return 0

    def get_outputpath(self):
        return self.output_path

    def clean_folders(self):
        print("Début de clean")
        files = glob.glob('Gif/*.png')
        for f in files:
            os.remove(f)
        print("On fait pareil pour Pictures")
        files = glob.glob('Pictures/*')
        for f in files:
            os.remove(f)
        return 0




#test = ScipyVoronoi("../Pictures/test.pdf", 4000, ["Swarm Intelligence"])
#test.make_diagram()
# cmap = ListedColormap(["darkorange", "gold", "lawngreen", "lightseagreen"])
# test.get_palette_in_database(1)
# cmap = LinearSegmentedColormap.from_list("mycmap", test.cmap)
# test.plot_examples([cmap])


#dict_test = {1998:5, 1999:78, 1997:65, 1996:43, 2000:9, 2010:7, 2011:34, 2014:23}
#test.make_gif(dict_test, 4)
