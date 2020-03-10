import numpy as np
from pommerman import characters
from pommerman.constants import Action, Item
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
            self.queue.append(Action.Right)
            self.queue.append(Action.Down)
            if self.check_left(board, my_location):
                self.queue.append(Action.Left)
            self.queue.append(Action.Up)
        return self.queue.pop()

    def check_left(self, board, my_location):
        row, col = my_location
        if board[row, max(col-1, 0)] == Item.Passage.value:
            return True
        return False
