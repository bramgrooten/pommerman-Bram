import unittest
import pommerman

from pommerman import agents
from serpentine.run import main


class MyTestCase(unittest.TestCase):

    def setUp(self) -> None:
        # Print all possible environments in the Pommerman registry
        self.env_names = pommerman.REGISTRY
        print(self.env_names)

    def test_games(self):
        """ Helper to parallelize game testing.  """
        for each in self.env_names:
            self.run_game(each)

    def run_game(self, env_name):
        # Create a set of agents (exactly four)
        agent_list = [
            agents.SimpleAgent(),
            agents.RandomAgent(),
            agents.SimpleAgent(),
            agents.RandomAgent(),
            # agents.DockerAgent("pommerman/simple-agent", port=12345),
        ]

        # Limit the agents for one vs one
        if 'oneVsOne' in env_name:
            agent_list = agent_list[:2]
        env = pommerman.make(env_name, agent_list)

        # Run the episodes just like OpenAI Gym
        for i_episode in range(1):
            state = env.reset()
            done = False
            while not done:
                # env.render()
                actions = env.act(state)
                state, reward, done, info = env.step(actions)
            print('Episode {} finished'.format(i_episode))
        env.close()

    def test_serpentine_main(self):
        main()


if __name__ == '__main__':
    unittest.main()
