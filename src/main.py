import os
import common
import pyglet
import threading
import simulation
import renderer

def control_panel():
    """
    Runs the control panel, which is responsible for running simulations,
    visualising the data, etc.
    """

    # Set the load path for assets
    pyglet.resource.path = [os.path.dirname(__file__) + "/.."]
    pyglet.resource.reindex()
    print(pyglet.resource.path[0])

    # Spawn an instance of the simulation
    sim = simulation.SingleSimulation(10, 800, 500)
    renderer.render(sim)
    pyglet.app.run()


if __name__ == "__main__":
    control_panel()
