''' An example to show how to set up an pommerman game programmatically.  '''

import os
import sys

## Adding pommerman directory, for terminal use
directory = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(directory)

import pommerman
from pommerman import agents
from serpentine.my_agent import MyAgent


def main():
    '''Simple function to bootstrap a game.  '''

    # Print all possible environments in the Pommerman registry
    print(pommerman.REGISTRY)

    # Create a set of agents (exactly four)
    agent_list = [
        MyAgent(),
        agents.RandomAgent(),
        agents.SimpleAgent(),
        agents.RandomAgent(),
    ]

    # Make the "Free-For-All" environment using the agent list
    env = pommerman.make('PommeFFACompetition-v0', agent_list)

    # Run the episodes just like OpenAI Gym
    for i_episode in range(1):
        state = env.reset()
        done = False
        while not done:
            # This renders the game
            env.render()

            # This is where we give an action to the environment
            actions = env.act(state)

            # This performs the step and gives back the new information
            state, reward, done, info = env.step(actions)

        print('Episode: {:2d} finished'.format(i_episode))
    env.close()


if __name__ == '__main__':
    main()
