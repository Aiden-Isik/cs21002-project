import pyglet
import time
import singleSimulation

def simulation_view():
    """
    This is a fairly basic GUI attached to the underlying simulation so that a visualisation can be made of what's happening
    """

    # Define font used
    pyglet.font.add_file("ComicShannsMono-Regular.ttf")
    mainFont = "Comic Shanns Mono"
    mainFontSize = 24

    # Set up the default movement information
    moveLeft = 0.0
    moveRight = 0.0
    moveForwards = 0.0

    # Start up the simulator
    window = pyglet.window.Window(800, 800, "Test")
    sim = singleSimulation.SingleSimulation(10, 800, 500) # TODO: Completely decouple the simulation from this

    # Flip the Y coordinate so things render the right way round.
    # This isn't strictly necessary, and 0 being the bottom left is in my opinion superior,
    # however this renderer replaces a Pygame-based renderer which has Y in the top left instead,
    # and consistency is nice.
    def flip_y_coord(y):
        return window.get_size()[1] - y

    # On each frame, draw the scene
    @window.event
    def on_draw():
        sim.tick(moveRight - moveLeft, moveForwards)

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

    # Handle keypresses
    # TODO: Decouple input from the renderer
    @window.event
    def on_key_press(symbol, modifiers):
        # Instruct the interpreter to assign to the parent scope's variables instead of new ones
        nonlocal moveLeft
        nonlocal moveRight
        nonlocal moveForwards

        if(symbol == pyglet.window.key.A):
            moveLeft = 1.0

        elif(symbol == pyglet.window.key.D):
            moveRight = 1.0

        elif(symbol == pyglet.window.key.W):
            moveForwards = 1.0

    @window.event
    def on_key_release(symbol, modifiers):
        # Instruct the interpreter to assign to the parent scope's variables instead of new ones
        nonlocal moveLeft
        nonlocal moveRight
        nonlocal moveForwards

        if(symbol == pyglet.window.key.A):
            moveLeft = 0.0

        elif(symbol == pyglet.window.key.D):
            moveRight = 0.0

        elif(symbol == pyglet.window.key.W):
            moveForwards = 0.0


if __name__ == "__main__":
    simulation_view()
    pyglet.app.run()
