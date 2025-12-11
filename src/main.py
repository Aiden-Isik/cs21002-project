import os
import common
import pyglet
import gymnasium
from gymnasium.utils.env_checker import check_env
import threading
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

    ml_env = gymnasium.make("gymnasium_env/SimulationGymnasiumAdapter-v0")

    # Test the machine learning environment
    try:
        gymnasium.utils.env_checker.check_env(ml_env.unwrapped)
        print("ML checks passed!")
    except Exception as err:
        print(f"ML checks failed: {err}!")


if __name__ == "__main__":
    main()
