from classes1 import Elevator, Person
import random
import copy
import numpy as np
import time

max_floor = 5
max_people_floor = 10
people_array = np.full((max_floor + 1, max_people_floor), None, dtype=object)  # macierzowa reprezentacja pięter
winda = Elevator(5, max_floor)
passengers_at_dest = []


def generate_passengers():
    amount = random.randint(0, 1)  # od 0 do 3 pasażerów
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
    # usuwanie osób z piętra które wsiadły do windy
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


def manage_requests(current_floor, elevator):
    # jeżeli jest jakikolwiek pasażer na piętrze, to niech przycisk tego piętra będzie wciśnięty
    for passenger in people_array[current_floor]:
        if passenger is not None:
            elevator.add_floor_to_requested_queue(current_floor)
            return None
    elevator.remove_floor_from_requested(current_floor)


def floor_up(elevator):
    elevator.increase_floor()


def floor_down(elevator):
    elevator.decrease_floor()


def find_minimal(elevator):
    chosen_floors = elevator.chosen_floors
    requested_floors = elevator.requested_floors

    print("Chosen Floors:", chosen_floors)
    print("Requested Floors:", requested_floors)

    if not chosen_floors and not requested_floors:
        return 0

    return min(chosen_floors + requested_floors, default=0)


def find_maximal(elevator):
    chosen_floors = elevator.chosen_floors
    requested_floors = elevator.requested_floors

    print("Chosen Floors:", chosen_floors)
    print("Requested Floors:", requested_floors)

    if not chosen_floors and not requested_floors:
        return 99999

    return max(chosen_floors + requested_floors, default=99999)


def increase_personal_counter(elevator, step=1):
    for passenger_inside in elevator.people_inside_arr:
        passenger_inside.increase_waiting_time()
    for floor in people_array:
        for passenger_outside in floor:
            if passenger_outside is not None:
                passenger_outside.increase_waiting_time()


def operator():
    if winda.delay > 0:
        # zmniejszanie delay tu!!!!!
        return 0
    current_floor = winda.current_floor
    current_state = winda.state
    requested_floors = winda.requested_floors

    # ----- zewnętrzne operacje pasażerów -----
    new_floors_arr = []
    if random.randint(0, 4) == 3:  # 1 / 4 szansy na jakichś pasażerów w turze
        new_floors_arr = generate_passengers()
    for new_floor in new_floors_arr:
        if new_floor not in requested_floors:
            winda.add_floor_to_requested_queue(new_floor)  # wciskanie przycisków żądania windy
    winda.update_people_inside()

    manage_requests(current_floor, winda)

    # ----- podejmowanie decyzji o ruchu windy
    minimal = find_minimal(winda)
    maximal = find_maximal(winda)

    print("min: ", minimal)
    print("max: ", maximal)

    requested_floors_above = winda.requested_chosen_floors_above()
    requested_floors_below = winda.requested_chosen_floors_below()

    current_floor = winda.current_floor

    if winda.state == "STANDING":
        if minimal > current_floor:
            winda.state = "UP"
        elif maximal < current_floor:
            winda.state = "DOWN"
        elif requested_floors_above or requested_floors_below:
            winda.state = "UP"  # Start moving up even in a standing state

    elif winda.state == "UP":
        if minimal > current_floor:
            floor_up(winda)
        elif not requested_floors_above:
            winda.change_direction()
            if requested_floors_below:
                winda.state = "DOWN"

    elif winda.state == "DOWN":
        if maximal < current_floor:
            floor_down(winda)
        elif not requested_floors_below:
            winda.change_direction()
            if requested_floors_above:
                winda.state = "UP"

    print("state: ", winda.state)

    # ----- sprawdź czy otworzyć drzwi windy -----
    if winda.decide_if_stop():
        visiting_floor(winda.current_floor, winda)

    manage_requests(current_floor, winda)

    # ----- zwiększanie czasu oczekiwania wszystkich osób w systemie -----
    increase_personal_counter(winda)

    time.sleep(0.1)
