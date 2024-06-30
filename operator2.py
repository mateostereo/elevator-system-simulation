from classes1 import Elevator, Person, ElevatorSystem
from operator_func import generate_passengers, sort_passengers, increase_personal_counter, find_maximal, \
    find_minimal, floor_up, floor_down, visiting_floor, manage_requests
import random

"""
Plik operator2 zawiera funkcję obsługującą ruch wind w systemie dwóch wind.
"""


def operator(max_floor, spawn_chance, max_people_floor,
             people_array, winda, winda2, elevators, passengers_at_dest,
             opening_door_delay, elevator_system):
    def increase_personal_counter_elevator(elevator, step=1):
        for passenger_inside in elevator.people_inside_arr:
            passenger_inside.increase_waiting_time()

    def increase_personal_counter_floors(step=1):
        for floor in people_array:
            for passenger_outside in floor:
                if passenger_outside is not None:
                    passenger_outside.increase_waiting_time()

    current_floor = winda.current_floor
    current_state = winda.state
    requested_floors = elevator_system.requested_floors

    # ----- zewnętrzne operacje pasażerów -----
    new_floors_arr = []
    if random.randint(0, spawn_chance) == 1:  # 1 / spawn_chance szansy na jakichś pasażerów w turze
        new_floors_arr = generate_passengers(max_floor, max_people_floor, people_array)
    for new_floor in new_floors_arr:
        if new_floor not in requested_floors:
            elevator_system.add_floor_to_requested_queue(new_floor)  # wciskanie przycisków żądania windy
    winda.update_people_inside()
    winda2.update_people_inside()

    manage_requests(current_floor, elevator_system, people_array)

    # ----- podejmowanie decyzji o ruchu pierwszej windy
    if winda.delay == 0:  # sprawdzenie, czy opóźnienie dobiegło końca

        minimal = find_minimal(winda)
        maximal = find_maximal(winda)

        requested_floors_above = elevator_system.requested_chosen_floors_above(winda)
        requested_floors_below = elevator_system.requested_chosen_floors_below(winda)

        current_floor = winda.current_floor

        if not requested_floors_above and not requested_floors_below:
            winda.state = "STANDING"

        if winda.state == "STANDING":  # there's still a chance of a bug when elevator is standing
            if minimal > current_floor:
                if minimal in winda.chosen_floors or winda2.current_floor < current_floor:
                    winda.state = "UP"
                    floor_up(winda)
            elif maximal < current_floor:
                if maximal in winda.chosen_floors or winda2.current_floor > current_floor:
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

        # ----- podejmowanie decyzji o ruchu drugiej windy
        if winda2.delay == 0:  # sprawdzenie, czy opóźnienie dobiegło końca

            minimal = find_minimal(winda2)
            maximal = find_maximal(winda2)

            requested_floors_above = elevator_system.requested_chosen_floors_above(winda2)
            requested_floors_below = elevator_system.requested_chosen_floors_below(winda2)

            current_floor = winda2.current_floor

            if not requested_floors_above and not requested_floors_below:
                winda2.state = "STANDING"

            if winda2.state == "STANDING":
                if minimal > current_floor:
                    if minimal in winda2.chosen_floors or winda.current_floor > winda2.current_floor:
                        winda2.state = "UP"
                        floor_up(winda2)
                elif maximal < current_floor:
                    if maximal in winda2.chosen_floors or winda.current_floor > winda2.current_floor:
                        winda2.state = "DOWN"
                        floor_down(winda2)
                elif requested_floors_above or requested_floors_below:
                    winda2.state = "UP"

            elif winda2.state == "UP":
                if minimal > current_floor:
                    if minimal in winda2.chosen_floors or winda.current_floor < winda2.current_floor:
                        floor_up(winda2)
                elif not requested_floors_above:
                    if requested_floors_below:
                        winda2.state = "DOWN"
                        floor_down(winda2)
                else:
                    floor_up(winda2)

            elif winda2.state == "DOWN":
                if maximal < current_floor:
                    if maximal in winda2.chosen_floors or winda.current_floor > winda2.current_floor:
                        floor_down(winda2)
                elif not requested_floors_below:
                    if requested_floors_above:
                        winda2.state = "UP"
                        floor_up(winda2)
                else:
                    floor_down(winda2)

            if winda2.state == "STANDING" and winda.current_floor != 0 and winda2.current_floor > 0:
                winda2.state = "DOWN"
                floor_down(winda2)

        # ----- sprawdź czy otworzyć drzwi windy -----
        if winda.decide_if_stop(elevator_system):
            visiting_floor(winda.current_floor, winda, people_array, passengers_at_dest, opening_door_delay)

        if winda2.decide_if_stop(elevator_system):
            visiting_floor(winda2.current_floor, winda2, people_array, passengers_at_dest, opening_door_delay)

        manage_requests(current_floor, elevator_system, people_array)

    # ----- zwiększanie czasu oczekiwania wszystkich osób w systemie -----
    increase_personal_counter_elevator(winda)
    increase_personal_counter_elevator(winda2)
    increase_personal_counter_floors()

    if winda.delay > 0:
        winda.delay -= 1
    if winda2.delay > 0:
        winda2.delay -= 1

    return max_floor, spawn_chance, max_people_floor, people_array, winda, winda2, \
        elevators, passengers_at_dest, opening_door_delay
