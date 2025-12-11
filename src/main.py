import os
import common
import pyglet
import threading
import simulation
import renderer
import time

def main():
    """
    Runs the simulations and AI agents
    """

    # Set the load path for assets
    pyglet.resource.path = [os.path.dirname(__file__) + "/.."]
    pyglet.resource.reindex()
    print(pyglet.resource.path[0])

    # Spawn an instance of the simulation
    sim = simulation.SingleSimulation(10, 800, 500)
    renderer_running = False
    window = pyglet.window.Window(800, 800, "Car Navigation - Renderer")

    # If the renderer isn't already running, start it
    while(not window.has_exit):
        if(renderer_running != True):
            renderer.render(sim, window)
            renderer_running = True

        # Render a frame
        sim.tick(0.0, 1.0)
        pyglet.clock.tick()
        window.switch_to()
        window.dispatch_events()
        window.dispatch_event("on_draw")
        window.flip()


if __name__ == "__main__":
    main()
