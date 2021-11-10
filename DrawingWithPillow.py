import random
from PIL import Image, ImageDraw
import DataType


def line(output_path):
    image = Image.new("RGB", (400, 400), "#000000")
    # Il faut choisir des points au hasard et puis les faire avancer pour créer des courbes.
    # points = [(100, 100), (150, 200), (200, 50), (400, 400)]
    # Pour le moment, on en prend un seul
    draw = ImageDraw.Draw(image)
    FortuneAlgorithm(200, 40, image, draw)
    # draw.line(points, width=15, fill="green", joint="curve")
    image.show()
    # image.save(output_path)


def FortuneAlgorithm(listPoints, image, draw):
    events = DataType.PriorityQueue()
    points = DataType.PriorityQueue()

    #We need to keep the minimal X and the minimal Y
    X0 = 400
    Y0 = 400

    #Same for maximal values
    X1 = 0
    Y1 = 0

    #These are the limits of the bounding box

    #We need to have a list with all the points that will construct the Voronoi Diagram
    #We'll add every point in the PriorityQueue points
    for point in listPoints:
        points.push(point)
        if point.x<X0:
            X0 = point.x
        elif point.y<Y0:
            Y0 = point.y
        elif point.x>X1:
            X1 = point.x
        elif point.y>Y1:
            Y1 = point.y
    #We can add margins to the bounding box
    dx = (X1-X0+1)/5
    dy = (Y1-Y0+1)/5
    X0 -= dx
    X1 += dx
    Y0 -= dy
    Y1 += dy

    #Process all points
    while not points.isEmpty():
        if not events.isEmpty() :
