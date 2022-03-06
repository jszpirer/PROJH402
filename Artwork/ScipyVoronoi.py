import numpy as np
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from scipy.spatial import Voronoi, voronoi_plot_2d

class ScipyVoronoi():
    most_frequent_word = None
    output_path = None

    def __init__(self, output_path, most_frequent_word):
        self.most_frequent_word = most_frequent_word
        self.output_path = output_path

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
        nb_points = ((nb_points % m + m) % m) % 100
        return nb_points

    def position_of_points(self,nb_points):
        # We choose randomly every position for now.
        list_of_points = np.random.uniform(size=[nb_points, 2])
        return list_of_points

    def make_diagram(self):
        # generate data/speed values
        nb_points = self.number_of_points()
        points = self.position_of_points(nb_points)
        speed = np.random.uniform(low=0.0, high=5.0, size=nb_points) #TODO: A améliorer pour que ça ne soit plus random

        # generate Voronoi tessellation
        vor = Voronoi(points)

        # find min/max values for normalization
        minima = min(speed)
        maxima = max(speed)

        # normalize chosen colormap
        norm = mpl.colors.Normalize(vmin=minima, vmax=maxima, clip=True)
        mapper = cm.ScalarMappable(norm=norm, cmap=cm.Blues_r) #We could change the colormap to make it unique

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