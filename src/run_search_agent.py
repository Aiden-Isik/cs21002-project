import os
import common
import pyglet
import threading
import simulation
import time

from collisionavoidance import SearchAgent

def render(sim, window):
    """
    Render the given simulation 'sim' into window 'window'
    """

    # Define font used
    pyglet.resource.add_font("assets/ComicShannsMono-Regular.ttf")
    mainFont = "Comic Shanns Mono"
    mainFontSize = 24

    # Flip the Y coordinate so things render the right way round.
    # This isn't strictly necessary, and 0 being the bottom left is in my opinion superior,
    # however this renderer replaces a Pygame-based renderer which has Y in the top left instead,
    # and consistency is nice.
    def flip_y_coord(y):
        return window.get_size()[1] - y

    # On each frame, draw the scene
    @window.event
    def on_draw():
        # Even though this array is not read, all objects to be drawn must be added or they won't render.
        # Presumably, that is the garbage collector's doing.
        objects = []

        # Batch all of the draws together so Pyglet can optimise the OpenGL
        drawBatch = pyglet.graphics.Batch()

        # Car corners
        sim.car.makeScreenSpacePoints(800, 800)

        objects.append(pyglet.shapes.Circle(sim.car.screenSpaceTopLeft[0], flip_y_coord(sim.car.screenSpaceTopLeft[1]), 3, color=(255, 0, 255), batch=drawBatch))
        objects.append(pyglet.shapes.Circle(sim.car.screenSpaceTopRight[0], flip_y_coord(sim.car.screenSpaceTopRight[1]), 3, color=(255, 255, 0), batch=drawBatch))
        objects.append(pyglet.shapes.Circle(sim.car.screenSpaceBottomLeft[0], flip_y_coord(sim.car.screenSpaceBottomLeft[1]), 3, color=(0, 255, 255), batch=drawBatch))
        objects.append(pyglet.shapes.Circle(sim.car.screenSpaceBottomRight[0], flip_y_coord(sim.car.screenSpaceBottomRight[1]), 3, color=(255, 255, 255), batch=drawBatch))

        # Debug info
        objects.append(pyglet.text.Label(str(sim.car.direction), font_name=mainFont, font_size=mainFontSize, color=(255, 255, 255), x=10, y=flip_y_coord(10), anchor_x="left", anchor_y="top", batch=drawBatch))
        objects.append(pyglet.text.Label(str(sim.obstacleList[0].relX), font_name=mainFont, font_size=mainFontSize, color=(255, 255, 255), x=10, y=flip_y_coord(40), anchor_x="left", anchor_y="top", batch=drawBatch))
        objects.append(pyglet.text.Label(str(sim.obstacleList[0].relY), font_name=mainFont, font_size=mainFontSize, color=(255, 255, 255), x=10, y=flip_y_coord(70), anchor_x="left", anchor_y="top", batch=drawBatch))
        objects.append(pyglet.text.Label(str(sim.instanceNo), font_name=mainFont, font_size=mainFontSize, color=(255, 255, 255), x=10, y=flip_y_coord(100), anchor_x="left", anchor_y="top", batch=drawBatch))

        # Obstacles
        for obstacle in sim.obstacleList:
            obstacle.makeScreenSpacePoints(800, 800)
            objects.append(pyglet.shapes.Circle(obstacle.screenSpaceX,
                                                flip_y_coord(obstacle.screenSpaceY),
                                                obstacle.radius(),
                                                color=(255 if obstacle.collidingWithCar else 0,
                                                       0 if obstacle.collidingWithCar else 255,
                                                       0),
                                                batch=drawBatch))

        # Draw the scene
        window.clear()
        drawBatch.draw()

        sim.tick(SearchAgent().chooseDirection(sim), 1.0)

        if sim.crashed:
            pyglet.app.exit()

    @window.event
    def on_close():
        window.close()

def main():
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
    sim.tick(0.0, 0.0)
    render(sim, pyglet.window.Window(800, 800, "Car Navigation - Renderer"))
    pyglet.app.run()
    print("Fitness for search agent: " + str(sim.fitness))

if __name__ == "__main__":
    main()
