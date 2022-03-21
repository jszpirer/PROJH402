import numpy as np
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
from scipy.spatial import Voronoi, voronoi_plot_2d
from Artwork.Color_Palettes import Database_color

class ScipyVoronoi():
    most_frequent_word = None
    output_path = None
    color_database = None
    cmap = None
    palette = None

    def __init__(self, output_path, most_frequent_word, palette):
        self.most_frequent_word = most_frequent_word
        self.output_path = output_path
        self.color_database = Database_color("colors.db")
        self.palette = palette

    def number_of_points(self):
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

    def position_of_points(self,nb_points):
        # We choose randomly every position for now.
        list_of_points = np.random.weibull(a=3,size=[nb_points, 2])
        print(list_of_points)
        print([nb_points, 2])
        return list_of_points

    def make_diagram(self):
        # generate data/speed values
        nb_points = self.number_of_points()
        points = self.position_of_points(nb_points)
        speed = np.random.uniform(low=0.0, high=15.0, size=nb_points) #TODO: A améliorer pour que ça ne soit plus random

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
        mapper = cm.ScalarMappable(norm=norm, cmap=colormap) #We could change the colormap to make it unique

        # plot Voronoi diagram, and fill finite regions with color mapped from speed value
        voronoi_plot_2d(vor, show_points=False, show_vertices=False, s=1)
        for r in range(len(vor.point_region)):
            region = vor.regions[vor.point_region[r]]
            if not -1 in region:
                polygon = [vor.vertices[i] for i in region]
                plt.fill(*zip(*polygon), color=mapper.to_rgba(speed[r]))
        #plt.show()
        plt.axis("off")
        plt.savefig(self.output_path, bbox_inches='tight')
        return 0

    #Permet de tester les palettes créées facilement
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
        #This list needs to be changed because it's a list of strings.
        self.change_into_colors(list_of_colors_string)

    def change_into_colors(self, list_of_strings):
        """Transform information from database and fill in the cmap."""
        print("Liste de strings")
        print(list_of_strings)
        self.cmap = []
        for color in list_of_strings:
            new_color = eval(color)
            tuple_to_add = tuple(ti/255 for ti in new_color)
            self.cmap.append(tuple_to_add)
        print("Nouvelle liste.")
        print(self.cmap)





test = ScipyVoronoi("../Pictures/test.pdf", "Salux", 1)
test.make_diagram()
#cmap = ListedColormap(["darkorange", "gold", "lawngreen", "lightseagreen"])
#test.get_palette_in_database(1)
#cmap = LinearSegmentedColormap.from_list("mycmap", test.cmap)
#test.plot_examples([cmap])