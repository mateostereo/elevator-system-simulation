from classes1 import Person
import copy


def generate_passengers(max_floor, max_people_floor, people_array):
    """
        Funkcja generuje pasażerów i dodaje ich do macierzy reprezentującej piętra
        :param max_floor: Pierwsza liczba całkowita.
        :param max_people_floor: Maksymalna ilość osób w piętrze
        :param people_array: Macierz numpy o wymiarach liczba piętra x maksymalna ilość osób w piętrze
        :return: Macierz numpy z wcześniejszymi i dodanymi pasażerami
        """
    amount = 1  # 1 pasażer
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


def visiting_floor(floor_int, elevator, people_array, passengers_at_dest, opening_door_delay):
    """
    Wykonaj akcje związane z odwiedzinami piętra
    :param floor_int: Aktualne piętro
    :param elevator: Obiekt z klasy Elevator
    :param people_array: Macierz numpy o wymiarach liczba piętra x maksymalna ilość osób w piętrze
    :param passengers_at_dest: Lista obiektów klasy Person, które skończyły udział w symulacji
    :param opening_door_delay: Liczba kroków, która zajmuje otworzenie drzwi windy.
    :return:
    """
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
    elevator.delay += opening_door_delay


def how_much_passengers_floor(floor_int, people_array):
    """
    Policz pasażerów na piętrze
    :param floor_int: Aktualne piętro
    :param people_array: Macierz numpy o wymiarach liczba piętra x maksymalna ilość osób w piętrze
    :return:
    """
    count_int = 0
    for passenger in people_array[floor_int]:
        if passenger is not None:
            count_int += 1
    return count_int


def sort_passengers(passengers_array):
    """
    Posortuj pasażerów od najdłużej do najkrócej czekających
    :param passengers_array: Macierz numpy o wymiarach liczba piętra x maksymalna ilość osób w piętrze
    :return:
    """
    # układ: pasażerowie czekający najdłużej od lewej strony wektora
    return sorted(filter(lambda x: x is not None, passengers_array), key=lambda person: person.wait_time, reverse=True)


def manage_requests(current_floor, elevator, people_array):
    """
    Odkliknij i kliknij przyciski na piętrach
    :param current_floor: Aktualne piętro
    :param elevator: Obiekt klasy Elevator
    :param people_array:
    :return: Macierz numpy o wymiarach liczba piętra x maksymalna ilość osób w piętrze
    """
    # jeżeli jest jakikolwiek pasażer na piętrze, to niech przycisk tego piętra będzie wciśnięty
    for passenger in people_array[current_floor]:
        if passenger is not None:
            elevator.add_floor_to_requested_queue(current_floor)
            return None
    elevator.remove_floor_from_requested(current_floor)


def floor_up(elevator):
    """
    Funkcja podwyższa obiekt klasy Elevator o piętro
    :param elevator: Obiekt klasy Elevator
    :return:
    """
    elevator.increase_floor()
    elevator.delay += elevator.speed


def floor_down(elevator):
    """
    Funkcja obniża obiekt klasy Elevator o piętro
    :param elevator: Obiekt klasy Elevator
    :return:
    """
    elevator.decrease_floor()
    elevator.delay += elevator.speed


def find_minimal(elevator):
    """
    Funkcja znajduje najniższe zażądane piętro
    :param elevator: Obiekt klasy Elevator
    :return: Najniższe zażądane piętro
    """
    chosen_floors = elevator.chosen_floors
    requested_floors = elevator.requested_floors

    if not chosen_floors and not requested_floors:
        return 0

    return min(chosen_floors + requested_floors, default=0)


def find_maximal(elevator):
    """
    Funkcja znajduje najwyższe zażądane piętro
        :param elevator: Obiekt klasy Elevator
        :return: Najwyższe zażądane piętro
        """
    chosen_floors = elevator.chosen_floors
    requested_floors = elevator.requested_floors

    if not chosen_floors and not requested_floors:
        return 99999

    return max(chosen_floors + requested_floors, default=99999)


def increase_personal_counter(elevator, people_array, step=1):
    """
    Funkcja zwiększa czas oczekiwania wszystkich pasażerów biorących udział w symulacji
    :param elevator: Obiekt klasy Elevator
    :param people_array:
    :param step: Liczba, o którą należy zwiększyć czas oczekiwania pasażerów
    :return:
    """
    for passenger_inside in elevator.people_inside_arr:
        passenger_inside.increase_waiting_time()
    for floor in people_array:
        for passenger_outside in floor:
            if passenger_outside is not None:
                passenger_outside.increase_waiting_time()
