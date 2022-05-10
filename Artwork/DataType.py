# Used before finding out that scipy was doing the job pretty well.

import heapq
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

    def push(self, point):
        # On veut simplement ajouter une tâche mais pas la marquée comme étant achevée sir elle existe déjà
        if point in self.entry_finder:
            return
        count = next(self.counter)
        entry = [point.x, count, point]
        self.entry_finder[point] = entry
        heapq.heappush(self.pq, entry)

    # for checking if the queue is empty
    def isEmpty(self):
        return len(self.pq) == 0

    # for popping an element based on Priority
    def delete(self):
        try:
            max = 0
            for i in range(len(self.pq)):
                if self.pq[i] > self.pq[max]:
                    max = i
            item = self.pq[max]
            del self.pq[max]
            return item
        except IndexError:
            print()
            exit()

    def top(self):
        while self.pq:
            priority, count, item = heapq.heappop(self.pq)
            if item is not self.REMOVED:
                del self.entry_finder[item]
                self.push(item)
                return item
        raise KeyError('top from an empty priority queue')

    def pop(self):
        'Remove and return the lowest priority task. Raise KeyError if empty.'
        while self.pq:
            priority, count, task = heapq.heappop(self.pq)
            if task is not self.REMOVED:
                del self.entry_finder[task]
                return task
        raise KeyError('pop from an empty priority queue')


class Event:
    x = 0.0
    p = None
    a = None  # Arc associated to the event
    valid = True

    def __init__(self, x, p, a):
        self.x = x
        self.p = p
        self.a = a
        self.valid = True


class Segment:
    start = None
    end = None
    done = False

    def __init__(self, p):
        self.start = p
        self.end = None
        self.done = False

    def finish(self, pend):
        if self.done:
            return
        self.end = pend
        self.done = True


class Arc:
    point = None
    previous = None
    next = None
    event = None
    seg0 = None
    seg1 = None

    def __init__(self, p, arc1=None, arc2=None):
        self.point = p
        self.previous = arc1
        self.next = arc2
        self.event = None
        self.seg0 = None
        self.seg1 = None

    def copy(self, toCopy):
        self.point = toCopy.point
        self.previous = toCopy.previous
        self.next = toCopy.next
        self.event = toCopy.event
        self.seg0 = toCopy.seg0
        self.seg1 = toCopy.seg1
