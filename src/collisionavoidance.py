import simulation

# manual searching
# makes three copies of the vehicle, one for left, one for right, and another for forwards
# then moves the copy forwards by lookaheadLength steps, whilst also going the direction specified, and checks to see if it has crashed
# each copy is scored based off of whether or not it has crashed, and how many obstacles it can detect
# this is added to the forwards progress to get the total fitness of the copy
# the copy with the highest fitness is then chosen as the one to go forwards with

class SearchAgent:
    """
    looks ahead nSteps steps to check for the best method forwards
    """

    def __init__(self, nSteps = 8, sensorWeight = 5.0, crashPenalty = -1e9):
        self.nSteps = nSteps
        self.sensorWeight = sensorWeight
        self.crashPenalty = crashPenalty

        # posasible directions to turn
        self.potentialActions = [
            -1.0, # turning left
            0.0,  # no turning
            1.0   # turning right
        ]

    # choose which direction to turn: left, right, or no turning
    def chooseDirection(self, simInstance: simulation.SingleSimulation):
        bestChoice      = self.potentialActions[1] # best choice we have found to turn so far
        highScore       = float("-Infinity")       # the score of that choice

        # check every direction
        for i in self.potentialActions:
            currentScore = 0.0

            # make a new instance
            checkingInstance = simInstance.copy()

            # step forwards
            for j in range(self.nSteps):
                checkingInstance.tick(i, 1.0)

            # update the current score
            currentScore = checkingInstance.fitness
            if checkingInstance.crashed:
                currentScore += self.crashPenalty

            if currentScore > highScore:
                bestChoice = i
                highScore = currentScore

        return bestChoice