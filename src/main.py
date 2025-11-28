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

    # Define the font to use
    pyglet.font.add_file("assets/ComicShannsMono-Regular.ttf")
    mainFont = "Comic Shanns Mono" # lol
    h1Size = 24
    h2Size = 22
    textSize = 18
    foregroundColour = (255, 255, 255)

    # Spawn the window
    window = pyglet.window.Window(800, 800, "PLACEHOLDER-NAME - Control Panel")

    # Spawn an instance of the simulation (TEMP)
    sim = simulation.SingleSimulation(10, 800, 500)

    # On each frame, draw the scene
    @window.event
    def on_draw():
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
                                     y=common.flip_y_coord(window,
                                                           title.x + title.content_height + 10),
                                     anchor_x="left", anchor_y="top",
                                     batch=drawBatch)

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
