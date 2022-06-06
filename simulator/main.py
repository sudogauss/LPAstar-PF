import pygame
import sys
import yaml


if __name__ == "__main__":
    data = None
    with open("config/simulator_config.yaml") as config:
        try:
            data = yaml.safe_load(config)
        except yaml.YAMLError as err:
            print(err)

    width, height = data["width"], data["height"]
    size = (data["width"], data["height"])

    background = (80, 80, 80)
    clear_color = (255, 255, 255)
    obstacle_color = (0, 0, 0)
    robot_color = (255, 0, 0)

    pygame.init()
    screen = pygame.display.set_mode(size)

    case_size = data["case_size"]

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)

        screen.fill(background)
        for i in range(0, height, case_size):
            for j in range(0, width, case_size):
                pygame.draw.rect(screen, clear_color, pygame.Rect((j+1, i+1), (case_size-2, case_size-2)))
        pygame.display.flip()
