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

    # Define the font to use
    pyglet.resource.add_font("assets/ComicShannsMono-Regular.ttf")
    mainFont = "Comic Shanns Mono" # lol
    h1Size = 24
    h2Size = 22
    textSize = 18
    foregroundColour = (255, 255, 255)

    # Spawn the window
    window = pyglet.window.Window(800, 800, "PLACEHOLDER-NAME - Control Panel")

    # Spawn an instance of the simulation (TEMP)
    sim = simulation.SingleSimulation(10, 800, 500)

    # Start the simulation (TEMP)
    simThread = threading.Thread(target = sim.run)
    simThread.start()

    # Start the simulations
    #def start_simulations():
    #    print("test")

    # Batch draws together for some extra efficiency
    drawBatch = pyglet.graphics.Batch()

    # Header
    title = pyglet.text.Label("PLACEHOLDER-NAME",
                              font_name=mainFont,
                              font_size=h1Size,
                              color=foregroundColour,
                              x=10, y=common.flip_y_coord(window, 10),
                              anchor_x="left", anchor_y="top",
                              batch=drawBatch)
    
    subtitle = pyglet.text.Label("Control Panel",
                                 font_name=mainFont,
                                 font_size=h2Size,
                                 color=foregroundColour,
                                 x=10,
                                 y=title.y - title.content_height - 10,
                                 anchor_x="left", anchor_y="top",
                                 batch=drawBatch)

    # Simulation controls
    #startSimButton = pyglet.gui.PushButton(pressed=pyglet.resource.image("assets/button.png"),
    #                                       depressed=pyglet.resource.image("assets/button.png"),
    #                                       x=10,
    #                                       y=subtitle.y - subtitle.content_height - 40,
    #                                       batch=drawBatch)

    #startSimButton.set_handler('on_press', start_simulations)

    #window.push_handlers(startSimButton)

    # On each frame, draw the scene
    @window.event
    def on_draw():
        # Draw the scene
        window.clear()
        drawBatch.draw()

    # If the control panel is closed, close everything
    @window.event
    def on_close():
        pyglet.app.exit()

    renderer.render(sim)
    pyglet.app.run()


if __name__ == "__main__":
    control_panel()
