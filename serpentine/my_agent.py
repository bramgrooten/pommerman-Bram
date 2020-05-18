import numpy as np
from dataclasses import dataclass
from pommerman import characters
from pommerman.constants import Action, Item, BOARD_SIZE
from pommerman.agents import BaseAgent


@dataclass
class Direction:
    name: str
    array: np.ndarray
    action: Action


@dataclass
class Directions:
    LEFT = Direction(name="left", array=np.array([0, -1]), action=Action.Left)
    RIGHT = Direction(name="right", array=np.array([0, 1]), action=Action.Right)
    UP = Direction(name="up", array=np.array([-1, 0]), action=Action.Up)
    DOWN = Direction(name="down", array=np.array([1, 0]), action=Action.Down)
    ALL = (LEFT, RIGHT, UP, DOWN)
    ZERO = Direction(name="zero", array=np.array([0, 0]), action=Action.Stop)

    @staticmethod
    def reverse(old_direction: Direction) -> Direction:
        """ Returns the reverse direction, left <--> right, up <--> down  """
        mapping = dict(left=Directions.RIGHT, right=Directions.LEFT, up=Directions.DOWN, down=Directions.UP)
        return mapping[old_direction.name]


class MyAgent(BaseAgent):
    """ Our version of the base agent. """

    def __init__(self, character=characters.Bomber):
        super().__init__(character)
        self.queue = []

    def act(self, obs, action_space):
        # Main event that is being called on every turn.
        if not self.queue:
            my_location = obs['position']
            board = obs['board']
            goal_location = (2, 2)

            if self.can_place_bomb(obs['bomb_life'], obs['ammo'], my_location):
                self.queue.append(Action.Bomb)

            direction = self.can_move_to(board, my_location, goal_location)
            self.queue.append(direction.action)

            # for direction in Directions.ALL:
            #     if self.check_direction_passable(board, my_location, direction):
            #         self.queue.append(direction.action)

            # If we cannot move in any direction, send a pass
            if not self.queue:
                self.queue.append(Action.Stop)

        return self.queue.pop(0)

    def check_direction_passable(self, board: np.array, location: tuple, direction: Direction) -> bool:
        """
            Checks for a given location and direction if the new position is a passage.

        :param board: The game board
        :param location: The location from which you start to move
        :param direction: The direction in which you are going to move (This is the Direction class)
        :return: True if the new location is a passage, False otherwise.
        """

        # Get new location
        new_location = np.array(location) + direction.array

        # Either the row or column value is not on the board.
        if min(new_location) < 0 or max(new_location) > 10:
            return False

        # Note that this is already a boolean (so no need for if statements)
        return board[tuple(new_location)] == Item.Passage.value

    def can_move_to(self, board: np.array, my_location: tuple, goal_location: tuple) -> Direction:
        """ BFS to a goal location.  Returns True if it can be reached.
        Works in the reverse way now (starting from goal_location)"""
        to_visit = [goal_location]
        visited = []

        # If we are already on the specified location!
        if my_location == goal_location:
            return Directions.ZERO

        while to_visit:
            point = to_visit.pop(0)

            for direction in Directions.ALL:
                # By making it a numpy array we can add the values
                new_point = tuple(np.array(point) + direction.array)

                # Check if we have found the location
                if new_point == my_location:
                    return Directions.reverse(direction)

                # We have already seen that point
                if new_point in visited:
                    continue

                # If we can reach this point add the point to the to visit list
                if self.check_direction_passable(board, point, direction):
                    to_visit.append(new_point)

            visited.append(point)
        return Directions.ZERO

    def can_place_bomb(self, bomb_life: np.ndarray, ammo: int, my_location: tuple) -> bool:
        """ Checks if you can place a bomb,
        if there is no bomb already placed and you have enough ammo, return True.  """

        # Check for bombs
        if not bomb_life[my_location] == 0:
            return False

        # Check for ammo
        if not ammo > 0:
            return False
        return True








