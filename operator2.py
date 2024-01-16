from classes1 import Elevator, Person, ElevatorSystem
import random
import copy
import numpy as np
import time

max_floor = 10
max_people_floor = 10
people_array = np.full((max_floor + 1, max_people_floor), None, dtype=object)  # macierzowa reprezentacja pięter
winda = Elevator(5, max_floor)
winda2 = Elevator(5, max_floor)
passengers_at_dest = []
delay_tick = 4
opening_door_delay = None
elevator_system = ElevatorSystem(max_floor)
moves = 0


def generate_passengers():
    amount = 1  # od 0 do 3 pasażerów
    new_floors_arr = []
    for person in range(amount):
        person = Person(max_floor)
        if person.starting_floor not in new_floors_arr:
            new_floors_arr.append(person.starting_floor)
        for i in range(max_people_floor):
            if people_array[person.starting_floor, i] is None:
                people_array[person.starting_floor, i] = copy.deepcopy(person)
                break
    return new_floors_arr


def visiting_floor(floor_int, elevator):
    # wysiadanie pasażerów:
    passengers_inside_arr = elevator.people_inside_arr
    passengers_leaving_arr = []
    for passenger_inside in passengers_inside_arr:
        if passenger_inside.desired_floor == floor_int:
            passengers_leaving_arr.append(passenger_inside)
    elevator.leave(passengers_leaving_arr)
    for passenger_left in passengers_leaving_arr:
        passengers_at_dest.append(passenger_left)
    # wsiadanie pasażerów
    floor = people_array[floor_int]
    sorted_floor = sort_passengers(floor)
    space_left = elevator.how_much_space_left()
    passengers_entering_arr = []
    for i in range(min(space_left, len(sorted_floor))):
        if sorted_floor[i] is not None:
            passengers_entering_arr.append(sorted_floor[i])

    elevator.enter(passengers_entering_arr)
    # usuwanie osób z piętra, które wsiadły do windy
    for passenger in people_array[floor_int]:
        if passenger in passengers_entering_arr:
            people_array[people_array == passenger] = None


def how_much_passengers_floor(floor_int):
    count_int = 0
    for passenger in people_array[floor_int]:
        if passenger is not None:
            count_int += 1
    return count_int


def sort_passengers(passengers_array):
    # układ: pasażerowie czekający najdłużej od lewej strony wektora
    return sorted(filter(lambda x: x is not None, passengers_array), key=lambda person: person.wait_time, reverse=True)


def manage_requests(current_floor):
    # jeżeli jest jakikolwiek pasażer na piętrze, to niech przycisk tego piętra będzie wciśnięty
    for passenger in people_array[current_floor]:
        if passenger is not None:
            elevator_system.add_floor_to_requested_queue(current_floor)
            return None
    elevator_system.remove_floor_from_requested(current_floor)


def floor_up(elevator):
    elevator.increase_floor()
    elevator.delay += delay_tick


def floor_down(elevator):
    elevator.decrease_floor()
    elevator.delay += delay_tick


def find_minimal(elevator):
    chosen_floors = elevator.chosen_floors
    requested_floors = elevator.requested_floors

    if not chosen_floors and not requested_floors:
        return 0

    return min(chosen_floors + requested_floors, default=0)


def find_maximal(elevator):
    chosen_floors = elevator.chosen_floors
    requested_floors = elevator.requested_floors

    if not chosen_floors and not requested_floors:
        return 99999

    return max(chosen_floors + requested_floors, default=99999)


def increase_personal_counter_elevator(elevator, step=1):
    for passenger_inside in elevator.people_inside_arr:
        passenger_inside.increase_waiting_time()


def increase_personal_counter_floors(step=1):
    for floor in people_array:
        for passenger_outside in floor:
            if passenger_outside is not None:
                passenger_outside.increase_waiting_time()


def operator():
    current_floor = winda.current_floor
    current_state = winda.state
    requested_floors = elevator_system.requested_floors

    # ----- zewnętrzne operacje pasażerów -----
    new_floors_arr = []
    if random.randint(0, 11) == 3:  # 1 / 4 szansy na jakichś pasażerów w turze
        new_floors_arr = generate_passengers()
    for new_floor in new_floors_arr:
        if new_floor not in requested_floors:
            elevator_system.add_floor_to_requested_queue(new_floor)  # wciskanie przycisków żądania windy
    winda.update_people_inside()
    winda2.update_people_inside()

    manage_requests(current_floor)

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

        # ----- podejmowanie decyzji o ruchu drugiej windy
        if winda2.delay == 0:  # sprawdzenie, czy opóźnienie dobiegło końca

            minimal = find_minimal(winda2)
            maximal = find_maximal(winda2)

            requested_floors_above = elevator_system.requested_chosen_floors_above(winda2)
            requested_floors_below = elevator_system.requested_chosen_floors_below(winda2)

            current_floor = winda2.current_floor

            if not requested_floors_above and not requested_floors_below:
                winda2.state = "STANDING"

            if winda2.state == "STANDING":  # theres still a chance of a bug when elevator is standing
                if minimal > current_floor:
                    winda2.state = "UP"
                    floor_up(winda2)
                elif maximal < current_floor:
                    winda2.state = "DOWN"
                    floor_down(winda2)
                elif requested_floors_above or requested_floors_below:
                    winda2.state = "UP"  # Start moving up even in a standing state

            elif winda2.state == "UP":
                if minimal > current_floor:
                    floor_up(winda2)
                elif not requested_floors_above:
                    if requested_floors_below:
                        winda2.state = "DOWN"
                        floor_down(winda2)
                else:
                    floor_up(winda2)

            elif winda2.state == "DOWN":
                if maximal < current_floor:
                    floor_down(winda2)
                elif not requested_floors_below:
                    if requested_floors_above:
                        winda2.state = "UP"
                        floor_up(winda2)
                else:
                    floor_down(winda2)

        # ----- sprawdź czy otworzyć drzwi windy -----
        if winda.decide_if_stop(elevator_system):
            visiting_floor(winda.current_floor, winda)

        if winda2.decide_if_stop(elevator_system):
            visiting_floor(winda2.current_floor, winda2)

        manage_requests(current_floor)

    # ----- zwiększanie czasu oczekiwania wszystkich osób w systemie -----
    increase_personal_counter_elevator(winda)
    increase_personal_counter_floors()

    if winda.delay > 0:
        winda.delay -= 1
    if winda2.delay > 0:
        winda2.delay -= 1
