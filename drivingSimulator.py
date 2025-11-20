def main():
    """
    this is a fairly basic GUI attached to the underlying simulation so that a visualisation can be made of whats happening
    """
    import pygame
    import time

    import singleSimulation

    pygame.init()
    pygame.font.init()

    mainFont = pygame.font.SysFont("SF Mono", 24)

    sim = singleSimulation.SingleSimulation(10, 800, 500)

    drawSurface = pygame.display.set_mode((800, 800))

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        # this is the beginning of the simulation things
        turning = 0.0

        if pygame.key.get_pressed()[pygame.K_a]:
            turning = -1.0
        elif pygame.key.get_pressed()[pygame.K_d]:
            turning = 1.0

        sim.tick(turning, 1.0 if pygame.key.get_pressed()[pygame.K_w] else 0.0)
        # this is the end of the simulation things, the rest is rendering

        # even then most of it is determining turning direction from user input, this would be similar for getting the output from artificiall intelligence

        sim.car.makeScreenSpacePoints(800, 800)

        drawSurface.fill((0, 0, 0))

        pygame.draw.circle(drawSurface, (255, 0, 255),   sim.car.screenSpaceTopLeft,     3)
        pygame.draw.circle(drawSurface, (255, 255, 0),   sim.car.screenSpaceTopRight,    3)
        pygame.draw.circle(drawSurface, (0, 255, 255), sim.car.screenSpaceBottomLeft,    3)
        pygame.draw.circle(drawSurface, (255, 255, 255), sim.car.screenSpaceBottomRight, 3)

        drawSurface.blit(mainFont.render(str(sim.car.direction),        True, (255, 255, 255)), (10, 10))
        drawSurface.blit(mainFont.render(str(sim.obstacleList[0].relX), True, (255, 255, 255)), (10, 40))
        drawSurface.blit(mainFont.render(str(sim.obstacleList[0].relY), True, (255, 255, 255)), (10, 70))
        drawSurface.blit(mainFont.render(str(sim.fitness),              True, (255, 255, 255)), (10, 100))

        for obstacle in sim.obstacleList:
            obstacle.makeScreenSpacePoints(800, 800)
            pygame.draw.circle(drawSurface, (255 if obstacle.collidingWithCar else 0, 0 if obstacle.collidingWithCar else 255, 0), (obstacle.screenSpaceX, obstacle.screenSpaceY), obstacle.radius())

        for sensor in sim.car.dotSensorList:
            pygame.draw.line(drawSurface, (0, 127 if sensor.detect == 0.0 else 255, 0), sim.car.screenSpaceCentre, ((sensor.farCorner[0] + sim.car.screenSpaceCentre[0]), (sensor.farCorner[1] + sim.car.screenSpaceCentre[1])))

        pygame.display.update()

        time.sleep(0.1)

if __name__ == "__main__":
    main()
