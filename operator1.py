from classes1 import Elevator, Person
from operator_func import generate_passengers, sort_passengers, increase_personal_counter, find_maximal, \
    find_minimal, floor_up, floor_down, visiting_floor, manage_requests
import random
import copy
import numpy as np

"""
Plik operator1 zawiera funkcję obsługującą ruch windy w systemie jednej windy.
"""


def operator(max_floor, spawn_chance, max_people_floor, people_array, winda, elevators, passengers_at_dest,
             opening_door_delay):
    current_floor = winda.current_floor
    current_state = winda.state
    requested_floors = winda.requested_floors

    # ----- zewnętrzne operacje pasażerów -----
    new_floors_arr = []
    if random.randint(0, spawn_chance) == 1:  # 1 / spawn_chance szansy na jakichś pasażerów w turze
        new_floors_arr = generate_passengers(max_floor, max_people_floor, people_array)
    for new_floor in new_floors_arr:
        if new_floor not in requested_floors:
            winda.add_floor_to_requested_queue(new_floor)  # wciskanie przycisków żądania windy
    winda.update_people_inside()

    manage_requests(current_floor, winda, people_array)
    # ----- podejmowanie decyzji o ruchu windy
    if winda.delay == 0:  # sprawdzenie, czy opóźnienie dobiegło końca

        minimal = find_minimal(winda)
        maximal = find_maximal(winda)

        requested_floors_above = winda.requested_chosen_floors_above()
        requested_floors_below = winda.requested_chosen_floors_below()

        current_floor = winda.current_floor

        if not requested_floors_above and not requested_floors_below:
            winda.state = "STANDING"

        if winda.state == "STANDING":
            if minimal > current_floor:
                winda.state = "UP"
                floor_up(winda)
            elif maximal < current_floor:
                winda.state = "DOWN"
                floor_down(winda)
            elif requested_floors_above or requested_floors_below:
                winda.state = "UP"  # Start moving up even in a standing state

        elif winda.state == "UP":
            if minimal > current_floor:
                floor_up(winda)
            elif not requested_floors_above:
                if requested_floors_below:
                    winda.state = "DOWN"
                    floor_down(winda)
            else:
                floor_up(winda)

        elif winda.state == "DOWN":
            if maximal < current_floor:
                floor_down(winda)
            elif not requested_floors_below:
                if requested_floors_above:
                    winda.state = "UP"
                    floor_up(winda)
            else:
                floor_down(winda)

        # ----- sprawdź czy otworzyć drzwi windy -----
        if winda.decide_if_stop():
            visiting_floor(winda.current_floor, winda, people_array, passengers_at_dest, opening_door_delay)

        manage_requests(current_floor, winda, people_array)

    # ----- zwiększanie czasu oczekiwania wszystkich osób w systemie -----
    increase_personal_counter(winda, people_array)

    if winda.delay > 0:
        winda.delay -= 1

    return max_floor, spawn_chance, max_people_floor, people_array, winda, elevators, passengers_at_dest, \
        opening_door_delay
