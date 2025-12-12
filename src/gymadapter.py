import enum
import gymnasium
import numpy
import pyglet
import renderer
import simulation

class SimulationGymnasiumAdapter(gymnasium.Env):
    class Actions(enum.Enum):
        FORWARDS = 0
        LEFT = 1
        RIGHT = 2

    metadata = {"render_modes": ["pylget_renderer"], "render_fps": 60}


    def __init__(self, render_mode=None, sandbox_size=800, min_spawn_dist=500, obstacle_count=10):
        # Create the simulator object
        self.obstacle_count = obstacle_count
        self.min_spawn_dist = min_spawn_dist
        self.sandbox_size = sandbox_size
        self.sim = simulation.SingleSimulation(obstacle_count, sandbox_size, min_spawn_dist)

        # Create the action space
        self.action_space = gymnasium.spaces.Discrete(3) # 3 actions: forwards, left, right

        # Create the observation space
        observation_list = []

        for sensor in self.sim.car.dotSensorList:
            observation_list.append(int(sensor.length) + 1)

        self.observation_space = gymnasium.spaces.MultiDiscrete(observation_list)

        # Set render mode
        assert render_mode is None or render_mode in self.metadata["render_modes"]
        self.render_mode = render_mode
        self.window = None # Initialised in render() if rendering


    def reset(self, seed=None, options=None):
        # Seed the random number generator
        super().reset(seed=seed)

        # Create a new simulation
        self.sim = simulation.SingleSimulation(self.obstacle_count, self.sandbox_size, self.min_spawn_dist)
        self.sim.tick(0.0, 0.0)

        # Observe the detection of each sensor
        observation_list = []

        for sensor in self.sim.car.dotSensorList:
            observation_list.append(int(sensor.detect))

        return (numpy.array(observation_list), {})


    # Run one tick of the simulation
    def step(self, action):
        # Tick over the simulation based on the action chosen
        if action == self.Actions.FORWARDS:
            self.sim.tick(0.0, 1.0)

        elif action == self.Actions.LEFT:
            self.sim.tick(-1.0, 1.0)

        elif action == self.Actions.RIGHT:
            self.sim.tick(1.0, 1.0)

        # Return the results of the tick

        # If we've crashed this simulation is terminated
        terminated = self.sim.crashed

        # Higher fitness == better
        reward = self.sim.fitness

        # Observe the detection of each sensor
        observation_list = []

        for sensor in self.sim.car.dotSensorList:
            observation_list.append(int(sensor.detect))

        # Render a frame if required
        if self.render_mode == "pyglet_renderer":
            self._render_frame()

        # No truncation ever
        # (the simulation will always eventually finish as obstacle density keeps rising)
        # Also no auxiliary info
        return (numpy.array(observation_list), reward, terminated, False, {})


    # Render one frame of the simulation
    def render(self):
        # If the renderer isn't already running, start it
        if(self.window == None):
            self.window = pyglet.window.Window(800, 800, "Car Navigation - Renderer")
            renderer.render(self.sim, self.window)

        # Render a frame
        pyglet.clock.tick()
        self.window.switch_to()
        self.window.dispatch_events()
        self.window.dispatch_event("on_draw")
        self.window.flip()


    # End the simulation
    def close(self):
        if(self.window != None):
            self.window.close()
