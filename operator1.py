from classes1 import Elevator, Person
import random
import copy
import numpy as np
import time

max_floor = 5
max_people_floor = 10
people_array = np.full((max_floor + 1, max_people_floor), None, dtype=object)  # macierzowa reprezentacja pięter
winda = Elevator(5, max_floor)


def generate_passengers():
    amount = random.randint(0, 3)  # od 0 do 3 pasażerów
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


def floor_up(elevator):
    elevator.increase_floor()
    time.sleep(1)


def floor_down(elevator):
    elevator.decrease_floor()
    time.sleep(1)


def operator():
    if winda.delay > 0:
        # zmniejszanie delay tu!!!!!
        return 0
    current_floor = winda.current_floor
    current_state = winda.state
    requested_floors = winda.requested_floors

    # ----- zewnętrzne operacje pasażerów -----
    new_floors_arr = []
    if random.randint(0, 5) == 3:  # 0,5 szansy na jakichś pasażerów w turze
        new_floors_arr = generate_passengers()
    for new_floor in new_floors_arr:
        if new_floor not in requested_floors:
            winda.add_floor_to_requested_queue(new_floor)  # wciskanie przycisków żądania windy
    winda.update_people_inside()

    # ----- podejmowanie decyzji o ruchu windy -----

    # ----- sprawdź czy otworzyć drzwi windy -----
    if winda.decide_if_stop():
        visiting_floor(winda.current_floor, winda)
    time.sleep(0.1)


# --------test---------

def operator_test():
    mati = Person(10, desired_floor=0, starting_floor=4)
    mati.wait_time = 10
    ala = Person(10, desired_floor=0, starting_floor=4)
    ala.wait_time = 7
    ola = Person(10, desired_floor=0, starting_floor=4)
    ola.wait_time = 15
    people_array[4] = [mati, ala, ola, None, None, None, None]
    winda.add_floor_to_requested_queue(4)

    floor_up(winda)
    print("Aktualne piętro:", winda.current_floor, "\tLiczba pasażerów:", winda.people_inside_int)

    floor_up(winda)
    print("Aktualne piętro:", winda.current_floor, "\tLiczba pasażerów:", winda.people_inside_int)

    floor_up(winda)
    print("Aktualne piętro:", winda.current_floor, "\tLiczba pasażerów:", winda.people_inside_int)

    floor_up(winda)
    print("Aktualne piętro:", winda.current_floor, "\tLiczba pasażerów:", winda.people_inside_int)
    winda.add_floor_to_chosen_queue(0)

    floor_up(winda)
    print("Aktualne piętro:", winda.current_floor, "\tLiczba pasażerów:", winda.people_inside_int)

    floor_down(winda)
    print("Aktualne piętro:", winda.current_floor, "\tLiczba pasażerów:", winda.people_inside_int)

    floor_down(winda)
    print("Aktualne piętro:", winda.current_floor, "\tLiczba pasażerów:", winda.people_inside_int)
    aleks = Person(10, desired_floor=3, starting_floor=0)
    winda.add_floor_to_requested_queue(0)
    people_array[0] = [None, aleks, None, None, None, None, None]

    floor_down(winda)
    print("Aktualne piętro:", winda.current_floor, "\tLiczba pasażerów:", winda.people_inside_int)

    floor_down(winda)
    print("Aktualne piętro:", winda.current_floor, "\tLiczba pasażerów:", winda.people_inside_int)

    floor_down(winda)
    print("Aktualne piętro:", winda.current_floor, "\tLiczba pasażerów:", winda.people_inside_int)
    winda.add_floor_to_chosen_queue(3)

    floor_up(winda)
    print("Aktualne piętro:", winda.current_floor, "\tLiczba pasażerów:", winda.people_inside_int)

    floor_up(winda)
    print("Aktualne piętro:", winda.current_floor, "\tLiczba pasażerów:", winda.people_inside_int)

    floor_up(winda)
    print("Aktualne piętro:", winda.current_floor, "\tLiczba pasażerów:", winda.people_inside_int)
