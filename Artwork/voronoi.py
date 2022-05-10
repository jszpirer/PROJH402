# Class used before finding out that scipy was doing it pretty well

from PIL import Image, ImageDraw
from Artwork import DataType
import math
import random

events = DataType.PriorityQueue()
points = DataType.PriorityQueue()
output = []  # List of the segments we need to print
root = None
X0 = 800
Y0 = 800
X1 = 0
Y1 = 0


class voronoi():

    def __init__(self, output_path, most_frequent_word):
        image = Image.new("RGB", (800, 800), "#000000")
        # Il faut choisir des points au hasard et puis les faire avancer pour créer des courbes.
        self.draw = ImageDraw.Draw(image)
        self.number_of_points(most_frequent_word)
        list = self.position_of_points()
        self.FortuneAlgorithm(list, self.draw)
        image.show()
        image.save(output_path)

    def number_of_points(self, most_frequent_word):
        self.nb_points = 0
        power_of_p = 1
        m = 10 ** (9) + 9  # probability of two random strings colliding is inversely proportional to m
        if most_frequent_word.isupper():
            p = 53
        else:
            p = 31
        for x in most_frequent_word:
            self.nb_points = (self.nb_points + (ord(x) - ord('a') + 1) * power_of_p) % m
            power_of_p = (power_of_p * p) % m
        self.nb_points = ((self.nb_points % m + m) % m ) % 100
        return self.nb_points

    def position_of_points(self):
        # We choose randomly every position for now.
        list_of_points = []
        for i in range(self.nb_points):
            # For every point we need to integer values between X1 and X0.
            x = random.randint(X1, X0)
            y = random.randint(Y1, Y0)
            p = DataType.Point(x, y)
            list_of_points.append(p)
            self.draw.point((x, y))
        return list_of_points


    # Find the rightmost point on the circle through a,b,c.
    def circle(self, a, b, c):
        # Check that bc is a "right turn" from ab.
        if a is None or b is None or c is None:
            return False, None, None
        if (b.x - a.x) * (c.y - a.y) - (c.x - a.x) * (b.y - a.y) > 0:
            return False, None, None

        # Algorithm from O 'Rourke 2ed p. 189.
        A = b.x - a.x
        B = b.y - a.y
        C = c.x - a.x
        D = c.y - a.y
        E = A * (a.x + b.x) + B * (a.y + b.y)
        F = C * (a.x + c.x) + D * (a.y + c.y)
        G = 2 * (A * (c.y - b.y) - B * (c.x - b.x))

        if G == 0:
            # Points are co-linear.
            return False, None, None

        # Point o is the center of the circle.
        o = DataType.Point(1.0 * (D * E - B * F) / G, 1.0 * (A * F - C * E) / G)

        # o.x plus radius  equals max x coordinate.
        px = o.x + math.sqrt(pow(a.x - o.x, 2) + pow(a.y - o.y, 2))
        return True, px, o

    # Where do two parabolas intersect?
    def intersection(self, p0, p1, l):
        p = p0
        if (p0.x == p1.x):
            py = (p0.y + p1.y) / 2
        elif (p1.x == l):
            py = p1.y
        elif (p0.x == l):
            py = p0.y
            p = p1
        else:
            # Use the quadratic formula.
            z0 = 2.0 * (p0.x - l)
            z1 = 2.0 * (p1.x - l)

            a = 1.0 / z0 - 1.0 / z1
            b = -2.0 * (p0.y / z0 - p1.y / z1)
            c = 1.0 * (p0.y ** 2 + p0.x ** 2 - l ** 2) / z0 - 1.0 * (p1.y ** 2 + p1.x ** 2 - l ** 2) / z1

            py = 1.0 * (-b - math.sqrt(b * b - 4 * a * c)) / (2 * a)
        # Plug back into one of the parabola equations.
        px = 1.0 * (p.x ** 2 + (p.y - py) ** 2 - l ** 2) / (2 * p.x - 2 * l)
        res = DataType.Point(px, py)
        return res

    # Look for a new circle event for arc
    def check_circle_event(self, arc):
        # Invalidate any old event.
        if arc.event is not None and arc.event.x != X0:
            arc.event.valid = False
        arc.event = None

        if arc.previous is None or arc.next is None:
            return

        check, px, o = self.circle(arc.previous.point, arc.point, arc.next.point)
        if check and px > X0:
            # Create new event.
            arc.event = DataType.Event(px, o, arc)
            events.push(arc.event)

    # Will a new parabola at point p intersect with arc i?
    def intersect(self, point, arc):
        if arc is None:
            return False, None
        if arc.point is None:
            return False, None
        if arc.point.x == point.x:
            return False, None

        a = 0.0
        b = 0.0

        if arc.previous is not None:  # Get the intersection of i->prev, i.
            a = (self.intersection(arc.previous.point, arc.point, point.x)).y
        if arc.next is not None:  # Get the intersection of i->next, i.
            b = (self.intersection(arc.point, arc.next.point, point.x)).y

        if (arc.previous is None or a <= point.y) and (arc.next is None or point.y <= b):
            res = DataType.Point(
                1.0 * (arc.point.x ** 2 + (arc.point.y - point.y) ** 2 - point.x ** 2) / (
                            2 * arc.point.x - 2 * point.x), point.y)

            return True, res
        return False, None

    def front_insert(self, point):
        global root
        if root is None:
            root = DataType.Arc(point)
        else:
            # find current arcs at point.y
            i = root
            while i is not None:
                flag, z = self.intersect(point, i)
                if flag:
                    # new parabola intersects arc i
                    if i.next is not None:
                        flag, zz = self.intersect(point, i.next)
                        if not flag:
                            i.next.previous = DataType.Arc(i.point, i, i.next)
                            i.next = i.next.previous
                    else:
                        i.next = DataType.Arc(i.point, i)
                    i.next.seg1 = i.seg1

                    # add point between i and i.next
                    i.next.previous = DataType.Arc(point, i, i.next)
                    i.next = i.next.previous

                    i = i.next  # now i points to the new arc

                    # add new half-edges connected to i's endpoints
                    seg = DataType.Segment(z)
                    output.append(seg)
                    i.previous.seg1 = i.seg0 = seg

                    seg = DataType.Segment(z)
                    output.append(seg)
                    i.next.seg0 = i.seg1 = seg

                    # check for new circle events around the new arc
                    self.check_circle_event(i)
                    self.check_circle_event(i.previous)
                    self.check_circle_event(i.next)

                    return

                i = i.next

            # if point never intersects an arc, append it to the list
            i = root
            while i.next is not None:
                i = i.next
            i.next = DataType.Arc(point, i)

            # insert new segment between point and i
            pointx = X0
            if i.next.point is not None and i.point is not None:
                y = (i.next.point.y + i.point.y) / 2.0
                start = DataType.Point(pointx, y)

                seg = DataType.Segment(start)
                i.seg1 = i.next.seg0 = seg
                output.append(seg)
        return

    def process_point(self):
        # Get the next point from the queue.
        e = points.pop()

        # Add a new arc to the parabolic front.
        self.front_insert(e)

    def process_event(self):
        e = events.pop()

        if e.valid:
            # We need to create a new segment and add it to the output
            seg = DataType.Segment(e.p)
            output.append(seg)

            # We take the associated arc
            a = e.a

            # If the arc has previous and/or next arc, we change their attributes
            if a.previous is not None:
                a.previous.next = a.next
                a.previous.seg1 = seg
            if a.next is not None:
                a.next.previous = a.previous
                a.next.seg0 = seg

            # We finish the segments of a
            if a.seg0 is not None:
                a.seg0.finish(e.p)
            if a.seg1 is not None:
                a.seg1.finish(e.p)

            # We need to check for other circle events on either side of p
            if a.previous is not None:
                self.check_circle_event(a.previous)
            if a.next is not None:
                self.check_circle_event(a.next)

    def finish_edges(self):
        # Advance the sweep line so no parabolas can cross the bounding box.
        l = X1 + (X1 - X0) + (Y1 - Y0)
        i = root
        # Extend each remaining segment to the new parabola intersections.
        while i.next is not None:
            if i.seg1 is not None:
                p = self.intersection(i.point, i.next.point, l * 2.0)
                i.seg1.finish(p)
            i = i.next

    def print_output(self, draw):
        # For each segment, we print a line with Pillow
        for segment in output:
            seg = [(segment.start.x, segment.start.y), (segment.end.x, segment.end.y)]
            draw.line(seg, width=1, fill="green", joint="curve")

    def FortuneAlgorithm(self, listPoints, draw):
        global X0, Y0, X1, Y1
        # We need to have a list with all the points that will construct the Voronoi Diagram
        # We'll add every point in the PriorityQueue points
        for point in listPoints:
            points.push(point)
            if point.x < X0:
                X0 = point.x
            elif point.x > X1:
                X1 = point.x
            if point.y > Y1:
                Y1 = point.y
            elif point.y < Y0:
                Y0 = point.y
        # We can add margins to the bounding box
        dx = (X1 - X0 + 1) / 5
        dy = (Y1 - Y0 + 1) / 5
        X0 = 0
        X1 = 400
        Y0 = 0
        Y1 = 400

        # Process all points
        while not points.isEmpty():
            if not events.isEmpty() and events.top().x <= points.top().x:
                self.process_event()
            else:
                self.process_point()  # handle site event
        # After all points are processed, do the remaining circle events.
        while not events.isEmpty():
            self.process_event()

        self.finish_edges()  # Clean up dangling edges.
        self.print_output(draw)  # Output the voronoi diagram.
