import os
import sys

import pyglet
import gymnasium
from gymnasium.utils.env_checker import check_env

# Add stable-baselines3 from lib subdir
sys.path.append(os.path.dirname(__file__) + "/../lib/stable_baselines3")
import stable_baselines3

import common
import simulation
import renderer
import gymadapter

inputFilename = ""

def main():
    if len(sys.argv) < 2:
        print("please have the filename as the last argument")
        print("usage: python.exe " + sys.argv[0] + " <input filename>")

        return

    inputFilename = sys.argv[-1]

    """
    Runs the simulations and AI agents
    """

    # Set the load path for assets
    pyglet.resource.path = [os.path.dirname(__file__) + "/.."]
    pyglet.resource.reindex()
    print(pyglet.resource.path[0])

    # Set up the machine learning environment
    gymnasium.register(id="gymnasium_env/SimulationGymnasiumAdapter-v0",
                       entry_point=gymadapter.SimulationGymnasiumAdapter)

    ml_vec_env = stable_baselines3.common.env_util.make_vec_env(gymadapter.SimulationGymnasiumAdapter)

    # Load the agent
    ml_model = stable_baselines3.A2C.load(inputFilename, env=ml_vec_env)

    # Test the agent
    obs = ml_vec_env.reset()

    for _ in range(10):
        action, states = ml_model.predict(obs)
        obs, rewards, _, info = ml_vec_env.step(action)
        ml_vec_env.render()

if __name__ == "__main__":
    main()
