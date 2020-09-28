from dataclasses import dataclass

import numpy as np

from pommerman.constants import Action


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