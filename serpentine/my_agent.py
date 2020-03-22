import numpy as np
from pommerman import characters
from pommerman.constants import Action, Item, BOARD_SIZE
from pommerman.agents import BaseAgent




class MyAgent(BaseAgent):
    """ Our version of the base agent. """

    def __init__(self, character=characters.Bomber):
        super().__init__(character)
        self.queue = []

    def act(self, obs, action_space):
        # Main event that is being called on every turn.
        if not self.queue:      # meaning, if the queue is empty
            my_location = obs['position']
            board = obs['board']

            if self.check_left(board, my_location):
                self.queue.append(Action.Left)

            if self.check_right(board, my_location):
                self.queue.append(Action.Right)

            if self.check_up(board, my_location):
                self.queue.append(Action.Up)

            if self.check_down(board, my_location):
                self.queue.append(Action.Down)

            # If we cannot move in any direction, send a pass
            if not self.queue:
                self.queue.append(Action.Stop)

        return self.queue.pop()

    def can_move_to(self, board: np.array, my_location: tuple, goal_location: tuple) -> bool:
        pass

    def check_left(self, board: np.array, my_location: tuple) -> bool:
        """ Checks if the tile to the left is passable. If it is, return True. """
        row, col = my_location
        if board[row, max(col-1, 0)] == Item.Passage.value:
            return True
        return False

    def check_right(self, board: np.array, my_location: tuple) -> bool:
        """ Checks if the tile to the right is passable. If it is, return True. """
        row, col = my_location
        if board[row, min(col+1, BOARD_SIZE-1)] == Item.Passage.value:
            return True
        return False

    def check_up(self, board: np.array, my_location: tuple) -> bool:
        """ Checks if the tile above it is passable. If it is, return True.  """
        row, col = my_location
        if board[max(row - 1, 0), col] == Item.Passage.value:
            return True
        return False

    def check_down(self, board: np.array, my_location: tuple) -> bool:
        """ Checks if the tile below it is passable, if it is, return True.  """
        row, col = my_location
        if board[min(row + 1, 10), col] == Item.Passage.value:
            return True
        return False




