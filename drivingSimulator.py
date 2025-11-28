import pyglet
import copy
import singleSimulation


class SearchAgent:
    """
    Lookahead search-based driver.

    Each frame:
      - Tries 3 actions: LEFT, STRAIGHT, RIGHT (always forward).
      - For each action, makes a COPY of the simulation.
      - Simulates that action for a few ticks into the future.
      - Scores the result:
          * Huge penalty if it crashed.
          * Reward for higher fitness (moving "forward").
          * Reward for sensors that are clear (no detection).
      - Picks the action with the best score.

    This is NOT a fixed path:
    - It reacts to where the obstacles currently are.
    - Obstacles respawn randomly (see Obstacle.respawn).
    """

    def __init__(self, lookahead_steps: int = 10, sensor_weight: float = 5.0, crash_penalty: float = 1e9):
        self.lookahead_steps = lookahead_steps
        self.sensor_weight = sensor_weight
        self.crash_penalty = crash_penalty

        # (turning, forward) – turning matches SingleSimulation.tick docs:
        #   turning < -0.5 -> turn RIGHT (direction -= TurnAmount)
        #   turning > 0.5  -> turn LEFT  (direction += TurnAmount)
        # uusing -1.0, 0.0, +1.0
        self.actions = [
            (-1.0, 1.0),   # turn right, forward
            (0.0, 1.0),    # straight, forward
            (1.0, 1.0),    # turn left, forward
        ]

    def choose_action(self, sim: "singleSimulation.SingleSimulation"):
        best_action = (0.0, 1.0)
        best_score = -float("inf")

        for turning, forward in self.actions:
            # copy the simulation so we don't affect the real one
            test_sim = copy.deepcopy(sim)

            # simulate a few steps into the future with this action
            for _ in range(self.lookahead_steps):
                test_sim.tick(turning, forward)
                if test_sim.crashed:
                    break

            score = self.score(test_sim)

            if score > best_score:
                best_score = score
                best_action = (turning, forward)

        return best_action

    def score(self, sim: "singleSimulation.SingleSimulation") -> float:
        # crash
        if sim.crashed:
            return -self.crash_penalty

        # reward open space from sensors
        sensor_clear = 0.0
        for sensor in sim.car.dotSensorList:
            if sensor.detect == 0.0:
                sensor_clear += 1.0
        return sim.fitness + sensor_clear * self.sensor_weight


def simulation_view():
    """
    GUI for the simulation:
      - Car drawn by its 4 coloured corners (like your original).
      - Obstacles drawn as coloured circles.
      - Raycasting lines from the car sensors.
      - Car controlled by SearchAgent (lookahead AI).
    """

    # Loading font
    pyglet.font.add_file("ComicShannsMono-Regular.ttf")
    mainFontName = "Comic Shanns Mono"
    mainFontSize = 24

    # Create window & simulation
    window = pyglet.window.Window(800, 800, "AI Driving - Search Agent")
    sim = singleSimulation.SingleSimulation(10, 800, 500)   # 10 obstacles to keep it smooth
    agent = SearchAgent(lookahead_steps=10, sensor_weight=5.0)

    def flip_y_coord(y):
        return window.height - y

    @window.event
    def on_draw():
        # AI CONTROL (this is the actual "intelligence") 
        turning, forward = agent.choose_action(sim)
        sim.tick(turning, forward)

        # batch for all drawing
        drawBatch = pyglet.graphics.Batch()
        objects = []

        # --- CAR CORNERS (original view) ---
        sim.car.makeScreenSpacePoints(window.width, window.height)

        objects.append(
            pyglet.shapes.Circle(
                sim.car.screenSpaceTopLeft[0],
                flip_y_coord(sim.car.screenSpaceTopLeft[1]),
                3,
                color=(255, 0, 255),
                batch=drawBatch,
            )
        )
        objects.append(
            pyglet.shapes.Circle(
                sim.car.screenSpaceTopRight[0],
                flip_y_coord(sim.car.screenSpaceTopRight[1]),
                3,
                color=(255, 255, 0),
                batch=drawBatch,
            )
        )
        objects.append(
            pyglet.shapes.Circle(
                sim.car.screenSpaceBottomLeft[0],
                flip_y_coord(sim.car.screenSpaceBottomLeft[1]),
                3,
                color=(0, 255, 255),
                batch=drawBatch,
            )
        )
        objects.append(
            pyglet.shapes.Circle(
                sim.car.screenSpaceBottomRight[0],
                flip_y_coord(sim.car.screenSpaceBottomRight[1]),
                3,
                color=(255, 255, 255),
                batch=drawBatch,
            )
        )

        #  SENSOR RAYS (raycasting visualisation) 
        # This mirrors your original pygame approach:
        # darker green when clear, bright green when detecting something.
        for sensor in sim.car.dotSensorList:
            start_x, start_y = sim.car.screenSpaceCentre
            end_x = sensor.farCorner[0] + start_x
            end_y = sensor.farCorner[1] + start_y

            g = 127 if sensor.detect == 0.0 else 255

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

        # --- DEBUG INFO ---
        objects.append(
            pyglet.text.Label(
                f"Dir: {sim.car.direction:.2f}",
                font_name=mainFontName,
                font_size=mainFontSize,
                color=(255, 255, 255, 255),
                x=10,
                y=flip_y_coord(10),
                anchor_x="left",
                anchor_y="top",
                batch=drawBatch,
            )
        )
        objects.append(
            pyglet.text.Label(
                f"Fitness: {sim.fitness:.2f}",
                font_name=mainFontName,
                font_size=mainFontSize,
                color=(255, 255, 255, 255),
                x=10,
                y=flip_y_coord(40),
                anchor_x="left",
                anchor_y="top",
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


if __name__ == "__main__":
    simulation_view()
    pyglet.app.run()
