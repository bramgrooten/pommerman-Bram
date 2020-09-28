from .directions import Direction, Directions
import numpy as np


class PathFinder:
    def __init__(self):
        self.to_visit = deque()
        self.visited = list()
        self.trail: Dict[tuple, Direction] = dict()

    def reset(self):
        self.to_visit = deque()
        self.visited = list()
        self.trail = dict()

    def is_on_grid(self, point: tuple) -> bool:
        if min(point) < 0 or max(point) > 7:
            return False
        return True

    def bfs_generator(self, start_location: tuple) -> tuple:
        """
            A generator that returns only valid unseen points from a grid, in a
            BFS manner starting from a specific location.
        """
        self.reset()
        self.to_visit.append(start_location)
        self.trail[start_location] = None
        while self.to_visit:
            point = self.to_visit.popleft()
            if point in self.visited: continue
            for direction in Directions.ALL:
                new_point = tuple(np.array(point) + direction.array)
                if self.is_on_grid(new_point) and new_point not in self.visited:
                    self.trail[new_point] = direction
                    yield new_point
            self.visited.append(point)






