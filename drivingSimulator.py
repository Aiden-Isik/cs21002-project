import pyglet
import singleSimulation
from ai_search_agent import SearchAgent


def simulation_view():
    """
    GUI for the simulation:
      - Renders the car (4 coloured corners)
      - Renders obstacles
      - Renders ray sensors
      - Calls SearchAgent to decide actions
    """

    # Load font
    pyglet.font.add_file("ComicShannsMono-Regular.ttf")
    mainFontName = "Comic Shanns Mono"
    mainFontSize = 24

    # Create window & simulation
    window = pyglet.window.Window(800, 800, "AI Driving - Search Agent")

    # Simulation (10 obstacles)
    sim = singleSimulation.SingleSimulation(10, 800, 500)

    # Import AI controller
    agent = SearchAgent(lookahead_steps=10, sensor_weight=5.0)

    # Flip Y coordinate for Pyglet rendering
    def flip_y_coord(y):
        return window.height - y

    # -------------------------
    #        DRAW LOOP
    # -------------------------
    @window.event
    def on_draw():

        # ---- AI CONTROL (brain) ----
        turning, forward = agent.choose_action(sim)
        sim.tick(turning, forward)

        # ---- DRAWING ----
        drawBatch = pyglet.graphics.Batch()
        objects = []

        # --- CAR CORNERS ---
        sim.car.makeScreenSpacePoints(window.width, window.height)

        objects.append(
            pyglet.shapes.Circle(
                sim.car.screenSpaceTopLeft[0],
                flip_y_coord(sim.car.screenSpaceTopLeft[1]),
                3, color=(255, 0, 255), batch=drawBatch,
            )
        )
        objects.append(
            pyglet.shapes.Circle(
                sim.car.screenSpaceTopRight[0],
                flip_y_coord(sim.car.screenSpaceTopRight[1]),
                3, color=(255, 255, 0), batch=drawBatch,
            )
        )
        objects.append(
            pyglet.shapes.Circle(
                sim.car.screenSpaceBottomLeft[0],
                flip_y_coord(sim.car.screenSpaceBottomLeft[1]),
                3, color=(0, 255, 255), batch=drawBatch,
            )
        )
        objects.append(
            pyglet.shapes.Circle(
                sim.car.screenSpaceBottomRight[0],
                flip_y_coord(sim.car.screenSpaceBottomRight[1]),
                3, color=(255, 255, 255), batch=drawBatch,
            )
        )

        # --- SENSOR RAYS ---
        for sensor in sim.car.dotSensorList:
            start_x, start_y = sim.car.screenSpaceCentre
            end_x = sensor.farCorner[0] + start_x
            end_y = sensor.farCorner[1] + start_y

            g = 127 if sensor.detect == 0.0 else 255  # darker = clear, bright = hit

            objects.append(
                pyglet.shapes.Line(
                    start_x,
                    flip_y_coord(start_y),
                    end_x,
                    flip_y_coord(end_y),
                    color=(0, g, 0),
                    batch=drawBatch,
                )
            )

        # --- DEBUG TEXT ---
        objects.append(
            pyglet.text.Label(
                f"Dir: {sim.car.direction:.2f}",
                font_name=mainFontName, font_size=mainFontSize,
                color=(255, 255, 255, 255),
                x=10, y=flip_y_coord(10),
                anchor_x="left", anchor_y="top",
                batch=drawBatch,
            )
        )
        objects.append(
            pyglet.text.Label(
                f"Fitness: {sim.fitness:.2f}",
                font_name=mainFontName, font_size=mainFontSize,
                color=(255, 255, 255, 255),
                x=10, y=flip_y_coord(40),
                anchor_x="left", anchor_y="top",
                batch=drawBatch,
            )
        )

        # --- OBSTACLES ---
        for obstacle in sim.obstacleList:
            obstacle.makeScreenSpacePoints(window.width, window.height)
            objects.append(
                pyglet.shapes.Circle(
                    obstacle.screenSpaceX,
                    flip_y_coord(obstacle.screenSpaceY),
                    obstacle.radius(),
                    color=(
                        255 if obstacle.collidingWithCar else 0,
                        0 if obstacle.collidingWithCar else 255,
                        0,
                    ),
                    batch=drawBatch,
                )
            )

        window.clear()
        drawBatch.draw()


# Run window
if __name__ == "__main__":
    simulation_view()
    pyglet.app.run()
