from operator2 import operator
import operator2
from classes1 import Elevator, ElevatorSystem
from numpy import mean, arange
import importlib
import numpy as np
import random

"""
Plik iteration2 obsługuje procedowanie symulacji dla pliku operator2
"""

simulation_time = 50000

time_array = arange(simulation_time)
arr_count_people_outside = []
arr_count_people_inside = []

max_floor = 8
spawn_chance = 25
max_people_floor = 10
people_array = np.full((max_floor + 1, max_people_floor), None, dtype=object)  # macierzowa reprezentacja pięter
winda = Elevator(5, max_floor, starting_floor=3, speed=random.randint(7, 13))
winda2 = Elevator(5, max_floor, speed=random.randint(7, 13))
elevators = [winda, winda2]
passengers_at_dest = []
opening_door_delay = 5
elevator_system = ElevatorSystem(max_floor)
parameters = (max_floor, spawn_chance, max_people_floor, people_array, winda, winda2, elevators,
              passengers_at_dest, opening_door_delay, elevator_system)


def count_people_outside(floors):
    output = 0
    for floor in floors:
        for person in floor:
            if person is not None:
                output += 1
    return output


def count_people_elevators(array_elevators):
    output = 0
    for elevator in array_elevators:
        output += elevator.people_inside_int
    return output


def iteration(parameters):
    for step in range(simulation_time):
        parameters = operator(max_floor, spawn_chance, max_people_floor,
                              people_array, winda, winda2, elevators, passengers_at_dest,
                              opening_door_delay, elevator_system)
        arr_count_people_outside.append(count_people_outside(people_array))
        arr_count_people_inside.append(count_people_elevators(elevators))
    importlib.reload(operator2)


def run_outside(parameters):
    iteration(parameters)
    waiting_times = []
    for waiting_time in passengers_at_dest:
        waiting_times.append(waiting_time.wait_time)

    result = mean(waiting_times)
    return result


if __name__ == "__main__":

    iteration(parameters)
    waiting_times = []
    for waiting_time in passengers_at_dest:
        waiting_times.append(waiting_time.wait_time)

    result = mean(waiting_times)
    print(result)
