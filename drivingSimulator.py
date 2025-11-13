def main():
    """
    this is a fairly basic GUI attached to the underlying simulation so that a visualisation can be made of whats happening
    """
    import pygame
    import time

    import Entity.vehicle
    import Entity.obstacle

    pygame.init()

    car = Entity.vehicle.Vehicle()
    obstacle = Entity.obstacle.Obstacle(-200, -200)
    drawSurface = pygame.display.set_mode((800, 800))

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit()

        if pygame.key.get_pressed()[pygame.K_a]:
            car.direction -= 0.1

        if pygame.key.get_pressed()[pygame.K_d]:
            car.direction += 0.1

        if pygame.key.get_pressed()[pygame.K_w]:
            obstacle.move(10, car.direction)

        car.rotatePoints()
        car.makeScreenSpacePoints(800, 800)
        obstacle.makeScreenSpacePoints(800, 800)

        drawSurface.fill((0, 0, 0))

        pygame.draw.circle(drawSurface, (255, 0, 255), car.screenSpaceTopLeft,     3)
        pygame.draw.circle(drawSurface, (255, 255, 0), car.screenSpaceTopRight,    3)
        pygame.draw.circle(drawSurface, (255, 255, 255), car.screenSpaceBottomLeft,  3)
        pygame.draw.circle(drawSurface, (255, 255, 255), car.screenSpaceBottomRight, 3)

        colliding = car.collidedWith(obstacle)

        pygame.draw.circle(drawSurface, (255 if colliding else 0, 0 if colliding else 255, 0), (obstacle.screenSpaceX, obstacle.screenSpaceY), Entity.obstacle.Obstacle.radius())

        pygame.display.update()

        time.sleep(0.1)

if __name__ == "__main__":
    main()
