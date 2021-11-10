import heapq #utlisé pour faire la queue
import itertools


class Point:
    x = 0.0
    y = 0.0

    def __init__(self, x, y):
        self.x = x
        self.y = y


class PriorityQueue(object):
    def __init__(self):
        self.pq = []  # list of entries arranged in a heap
        self.entry_finder = {}  # mapping of tasks to entries
        self.REMOVED = '<removed-task>'  # placeholder for a removed task
        self.counter = itertools.count()  # unique sequence count

    def push(self,point):
        # On veut simplement ajouter une tâche mais pas la marquée comme étant achevée sir elle existe déjà
        if point in self.entry_finder :
            return
        count = next(self.counter)
        entry = [point.x, count, point]
        self.entry_finder[point] = entry
        heapq.heappush(self.pq, entry)

    # for checking if the queue is empty
    def isEmpty(self):
        return len(self.queue) == 0

    # for inserting an element in the queue
    def insert(self, data):
        self.queue.append(data)

    # for popping an element based on Priority
    def delete(self):
        try:
            max = 0
            for i in range(len(self.queue)):
                if self.queue[i] > self.queue[max]:
                    max = i
            item = self.queue[max]
            del self.queue[max]
            return item
        except IndexError:
            print()
            exit()