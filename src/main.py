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

def main():
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

    ml_env = gymnasium.make("gymnasium_env/SimulationGymnasiumAdapter-v0", render_mode="pyglet_renderer")

    # Set up the agent
    ml_model = stable_baselines3.A2C("MlpPolicy", ml_env, verbose=1)

    # Train the agent
    ml_model.learn(progress_bar=True, total_timesteps=100000)

    # Save the agent
    ml_model.save("a2c_collision_avoidance")


if __name__ == "__main__":
    main()
