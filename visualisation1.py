import pygame
import sys
from operator2 import operator, people_array, max_floor, winda, winda2, floor_down, floor_up, passengers_at_dest, \
    elevator_system
from numpy import mean

# Pygame setup
pygame.init()

# Constants
NUM_ELEVATORS = 2
WIDTH, HEIGHT = 800, 600
FLOOR_HEIGHT = HEIGHT // (max_floor + 1)
CIRCLE_RADIUS = 15
ELEVATOR_WIDTH = 40
ELEVATOR_HEIGHT = FLOOR_HEIGHT - 10
ELEVATOR_SPACING = 20  # Spacing between elevators
FPS = 2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Initialize Pygame screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Elevator Simulation")

clock = pygame.time.Clock()


def draw_floor(floor_number):
    pygame.draw.line(screen, WHITE, (0, FLOOR_HEIGHT * (max_floor - floor_number)),
                     (WIDTH, FLOOR_HEIGHT * (max_floor - floor_number)))

    # Draw floor number text
    font = pygame.font.Font(None, 30)
    text = font.render(str(floor_number), True, WHITE)
    screen.blit(text, (WIDTH - 50, FLOOR_HEIGHT * (max_floor - floor_number) + FLOOR_HEIGHT // 2 - 15))


def draw_passengers():
    for floor in range(max_floor + 1):
        for i, passenger in enumerate(people_array[floor]):
            if passenger is not None:
                # Draw passenger circle
                pygame.draw.circle(screen, WHITE, (20 + i * 40, HEIGHT - FLOOR_HEIGHT * floor - FLOOR_HEIGHT // 2),
                                   CIRCLE_RADIUS)
                # Draw desired floor text on the circle
                font = pygame.font.Font(None, 20)
                text = font.render(str(passenger.desired_floor), True, BLACK)
                screen.blit(text, (15 + i * 40, HEIGHT - FLOOR_HEIGHT * floor - FLOOR_HEIGHT // 2 - 10))


def draw_elevators(elevators):
    for i, elevator in enumerate(elevators):
        x_position = WIDTH - (ELEVATOR_WIDTH + ELEVATOR_SPACING) * (i + 1)
        pygame.draw.rect(screen, RED,
                         (x_position, HEIGHT - FLOOR_HEIGHT * elevator.current_floor - ELEVATOR_HEIGHT - 5,
                          ELEVATOR_WIDTH, ELEVATOR_HEIGHT))

        # Draw current number of passengers inside the elevator
        font = pygame.font.Font(None, 30)
        text = font.render(f"{elevator.people_inside_int}", True, WHITE)
        screen.blit(text, (x_position - 100, HEIGHT - FLOOR_HEIGHT * elevator.current_floor - FLOOR_HEIGHT // 2 - 10))


def draw_chosen_floors(chosen_floors):
    chosen_floors = []
    requested_floors = elevator_system.requested_floors
    for person in winda.people_inside_arr:
        chosen_floors.append(person.desired_floor)
    chosen_floors2 = []
    for person in winda2.people_inside_arr:
        chosen_floors2.append(person.desired_floor)
    # Draw chosen floors text at the bottom
    font = pygame.font.Font(None, 25)
    text = font.render("Chosen Floors: " + ", ".join(map(str, chosen_floors)) + "   Chosen Floors2: " + ", ".join(
        map(str, chosen_floors2)) +
                       "            Requested Floors: " +
                       ", ".join(map(str, requested_floors)), True, WHITE)
    screen.blit(text, (10, HEIGHT - 30))


def main():
    simulation_time = 5000

    for step in range(simulation_time):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP]:
            floor_up(winda2)

        if keys[pygame.K_DOWN]:
            floor_down(winda2)

        operator()

        screen.fill(BLACK)

        for floor in range(max_floor + 1):
            draw_floor(floor)

        draw_passengers()

        draw_elevators([winda, winda2])  # Pass a list of current floors for each elevator

        draw_chosen_floors(winda.chosen_floors)

        pygame.display.flip()
        clock.tick(FPS)

    waiting_times = []
    for waiting_time in passengers_at_dest:
        waiting_times.append(waiting_time.wait_time)
    print(mean(waiting_times))


if __name__ == "__main__":
    main()
