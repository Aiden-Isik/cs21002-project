import copy
import singleSimulation


class SearchAgent:
    """
    Lookahead search-based driver.

    Each frame:
      - Tries 3 actions: LEFT, STRAIGHT, RIGHT (always forward).
    """

    def __init__(self, lookahead_steps: int = 8, sensor_weight: float = 5.0, crash_penalty: float = 1e9):
        self.lookahead_steps = lookahead_steps
        self.sensor_weight = sensor_weight
        self.crash_penalty = crash_penalty

        # (turning, forward)
        # In SingleSimulation.tick:
        #   turning < -0.5 -> turn RIGHT (direction -= TurnAmount)
        #   turning > 0.5  -> turn LEFT  (direction += TurnAmount)
        self.actions = [
            (-1.0, 1.0),  
            (0.0, 1.0),   
            (1.0, 1.0),    
        ]

    def choose_action(self, sim: "singleSimulation.SingleSimulation"):
        best_action = (0.0, 1.0)
        best_score = -float("inf")

        for turning, forward in self.actions:
            # simulate on a copy
            test_sim = copy.deepcopy(sim)

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
       
        if sim.crashed:
            return -self.crash_penalty

       
        clear_count = 0.0
        for sensor in sim.car.dotSensorList:
            if sensor.detect == 0.0:
                clear_count += 1.0

        # combine forward progress + clear space
        return sim.fitness + clear_count * self.sensor_weight
