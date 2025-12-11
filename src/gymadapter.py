import enum
import gymnasium
import simulator

class SimulationGymnasiumAdapter(gymnasium.Env):
    class Actions(enum.Enum):
        FORWARDS = 0
        LEFT = 1
        RIGHT = 2

    metadata = {"render_modes": ["pylget_renderer"]}

    def __init__(self, render_mode=None, sandbox_size=800, min_spawn_dist=500, obstacle_count=10):
        # Create the simulator object
        self.sim = simulation.SingleSingulation(obstacle_count, sandbox_size, min_spawn_dist)

        self.action_space = gymnasium.spaces.Discrete(3) # 3 actions: forwards, left, right

    def reset(self, seed=None, options=None):
        self.sim = simulation.SingleSingulation(obstacle_count, sandbox_size, min_spawn_dist)

    def step(self, action):
        if action == Actions.FORWARDS:
            self.sim.tick(0.0, 1.0)

        elif action == Actions.LEFT:
            self.sim.tick(-1.0, 1.0)

        elif action == Actions.RIGHT:
            self.sim.tick(1.0, 1.0)

    def render():
        # If the renderer isn't already running, start it
        if(self.renderer_running != True):
            self.window = pyglet.window.Window(800, 800, "Car Navigation - Renderer")
            renderer.render(self.sim, self.window)
            self.renderer_running = True

        # Render a frame
        pyglet.clock.tick()
        self.window.switch_to()
        self.window.dispatch_events()
        self.window.dispatch_event("on_draw")
        self.window.flip()

    def close():
        self.window.close()
