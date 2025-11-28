# searchAgent.py
import copy

class SearchAgent:
    """
    Simple AI that tests LEFT, STRAIGHT, RIGHT and picks the safest.
    """

    def __init__(self, lookahead_steps=5):
        self.lookahead_steps = lookahead_steps
        self.actions = [(-1.0, 1.0), (0.0, 1.0), (1.0, 1.0)]  # left, straight, right

    def choose_action(self, sim):
        best_action = (0.0, 1.0)
        best_score = -1e18

        for action in self.actions:
            turning, forward = action
            
            # Copy the simulation so we don't touch the real one
            test_sim = copy.deepcopy(sim)

            # Simulate ahead
            for _ in range(self.lookahead_steps):
                test_sim.tick(turning, forward)
                if test_sim.crashed:
                    break

            # Score this future
            score = self.score(test_sim)

            if score > best_score:
                best_score = score
                best_action = action

        return best_action

    def score(self, sim):
        if sim.crashed:
            return -1e9  # big negative for crashing

        # Sum all sensor distances (bigger = safer)
        sensor_total = sum(sensor.detect for sensor in sim.car.dotSensorList)

        # Fitness already tracks forward movement
        return sim.fitness + sensor_total * 5
