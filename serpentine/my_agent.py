from pommerman import characters
from pommerman.constants import Action
from pommerman.agents import BaseAgent


class MyAgent(BaseAgent):
    """ Our version of the base agent. """

    def __init__(self, character=characters.Bomber):
        super().__init__(character)

    def act(self, obs, action_space):
        # Main event that is being called on every turn.
        return Action.Stop
