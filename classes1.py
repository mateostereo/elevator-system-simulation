import random


class ElevatorSystem:
    def __init__(self, max_possible_floor):
        self.max_possible_floor = max_possible_floor
        self.requested_floors = []

    def add_floor_to_requested_queue(self, new_floor):
        """
        Metoda dodająca nowe piętro do listy z żądaniami
        :param new_floor: indeks nowego piętra
        :return:
        """
        if new_floor not in self.requested_floors:
            self.requested_floors.append(new_floor)

    def remove_floor_from_requested(self, floor):
        """
        Metoda usuwająca konkretne piętro z listy z żądaniami
        :param floor: indeks usuwanego piętra
        :return:
        """
        if floor in self.requested_floors:
            self.requested_floors.remove(floor)

    def requested_chosen_floors_above(self, elevator):
        """
        Metoda zwracająca żądane piętra, które są ponad aktualnym piętrem
        :param elevator: Obiekt klasy Elevator
        :return: Listę zawierającą indeksy żądanych pięter nad windą
        """
        current_floor = elevator.current_floor
        above = []
        for requested_floor in self.requested_floors:
            if requested_floor > current_floor:
                above.append(requested_floor)
        for chosen_floor in elevator.chosen_floors:
            if chosen_floor > current_floor:
                above.append(chosen_floor)
        return above

    def requested_chosen_floors_below(self, elevator):
        """
        Method zwracająca żądane piętra, które są poniżej aktualnego piętra
        :param elevator: Obiekt klasy Elevator
        :return: Lista zawierająca indeksy żądanych pięter nad windą
        """
        current_floor = elevator.current_floor
        below = []
        for requested_floor in self.requested_floors:
            if requested_floor < current_floor:
                below.append(requested_floor)
        for chosen_floor in elevator.chosen_floors:
            if chosen_floor < current_floor:
                below.append(chosen_floor)
        return below


class Elevator:
    def __init__(self, max_people_inside, max_possible_floor, starting_floor=0, speed=1):
        self.current_floor = starting_floor
        self.people_inside_int = 0
        self.max_people_inside = max_people_inside
        self.max_possible_floor = max_possible_floor

        self.requested_floors = []
        self.chosen_floors = []
        self.queue = None  # fully managed by operator
        self.state = "STANDING"
        self.people_inside_arr = []
        self.delay = 0
        self.speed = speed

    def enter(self, people_entering_arr):
        """
        Metoda obsługująca osoby wchodzące do windy
        :param people_entering_arr: lista z obiektami klasy Person
        :return:
        """
        for person in people_entering_arr:
            self.people_inside_arr.append(person)
        self.update_people_inside()

    def leave(self, people_leaving_arr):
        """
        Metoda obsługująca osoby wysiadające z windy
        :param people_leaving_arr: lista z obiektami klasy Person
        :return:
        """
        for person in people_leaving_arr:
            self.people_inside_arr.remove(person)
        self.update_people_inside()

    def update_people_inside(self):
        """
        Metoda aktualizująca osoby w środku windy
        :return:
        """
        self.people_inside_int = len(self.people_inside_arr)
        arr = []
        for person in self.people_inside_arr:
            arr.append(person.desired_floor)
            if person.desired_floor not in self.chosen_floors:
                self.add_floor_to_chosen_queue(person.desired_floor)
        for chosen_floor in self.chosen_floors:
            if chosen_floor not in arr:
                self.remove_floor_from_chosen(chosen_floor)

    def state_up(self):
        """
        Zmień obecny stan windy na jadącą w gorę
        :return:
        """
        self.state = "UP"

    def state_down(self):
        """
        Zmień obecny stan windy na jadącą w dół
        :return:
        """
        self.state = "DOWN"

    def state_none(self):
        """
        Zmień obecny stan windy na stojącą
        :return:
        """
        self.state = "STANDING"

    def add_floor_to_requested_queue(self, new_floor):
        """
        Metoda dodająca piętro do listy z żądaniami
        :param new_floor: indeks piętra
        :return:
        """
        if new_floor not in self.requested_floors:
            self.requested_floors.append(new_floor)

    def remove_floor_from_requested(self, floor):
        """
        Metoda usuwająca wybrane piętro z listy z żądaniami
        :param floor: indeks piętra
        :return:
        """
        if floor in self.requested_floors:
            self.requested_floors.remove(floor)

    def add_floor_to_chosen_queue(self, new_floor):
        """
        Metoda dodająca piętro do listy z wybranymi piętrami (z zewnątrz)
        :param new_floor: indeks piętra
        :return:
        """
        self.chosen_floors.append(new_floor)

    def remove_floor_from_chosen(self, floor):
        """
        Metoda usuwająca piętro z listy z wybranymi piętrami (z zewnątrz)
        :param floor: indeks piętra
        :return:
        """
        if floor in self.chosen_floors:
            self.chosen_floors.remove(floor)

    def decide_if_stop(self, elevator_system=None):
        """
        Metoda decydująca, czy winda powinna zatrzymać się na danym piętrze
        :param elevator_system: Obiekt klasy ElevatorSystem
        :return: True or False
        """
        if elevator_system is None:
            if self.current_floor in self.requested_floors:
                return True
        else:
            if self.current_floor in elevator_system.requested_floors:
                return True
        if self.current_floor in self.chosen_floors:
            return True
        return False

    def pop_visited_floor(self):
        """
        Metoda usuwająca z listy z żądaniami odwiedzone piętro.
        :return:
        """
        self.requested_floors.remove(self.current_floor)

    def increase_floor(self):
        """
        Metoda zwiększająca piętro windy o 1
        :return:
        """
        if self.current_floor + 1 > self.max_possible_floor:
            print("Nie można pojechać wyżej, osiągnięto najwyższe piętro.")
        else:
            self.current_floor += 1

    def decrease_floor(self):
        """
        Metoda zmniejszająca piętro windy o 1
        :return:
        """
        if self.current_floor - 1 < 0:
            print("Nie można pojechać niżej, osiągnięto najniższe piętro.")
        else:
            self.current_floor -= 1

    def how_much_space_left(self):
        """
        :return: Ile osób może się jeszcze zmieścić do windy
        """
        return self.max_people_inside - self.people_inside_int

    def requested_chosen_floors_above(self):
        """
        Metoda zwracająca żądane piętra, które są ponad aktualnym piętrem
        :return: Listę zawierającą indeksy żądanych pięter nad windą
        """
        above = []
        for requested_floor in self.requested_floors:
            if requested_floor > self.current_floor:
                above.append(requested_floor)
        for chosen_floor in self.chosen_floors:
            if chosen_floor > self.current_floor:
                above.append(chosen_floor)
        return above

    def requested_chosen_floors_below(self):
        """
            Method zwracająca żądane piętra, które są poniżej aktualnego piętra
            :return: Lista zawierająca indeksy żądanych pięter nad windą
                """
        below = []
        for requested_floor in self.requested_floors:
            if requested_floor < self.current_floor:
                below.append(requested_floor)
        for chosen_floor in self.chosen_floors:
            if chosen_floor < self.current_floor:
                below.append(chosen_floor)
        return below


class Person:
    def __init__(self, max_floor, desired_floor=None, starting_floor=None):
        if starting_floor is None:
            choice = random.randint(0, 1)
            if choice == 0:
                self.starting_floor = 0
            else:
                self.starting_floor = random.randint(1, max_floor)
        else:
            self.starting_floor = starting_floor

        self.current_floor = starting_floor
        self.wait_time = 0

        if desired_floor is None:
            if self.starting_floor == 0:
                self.desired_floor = random.randint(1, max_floor)
            else:
                self.desired_floor = 0
        else:
            self.desired_floor = desired_floor

    def increase_waiting_time(self, step=1):
        """
        Zwiększ czas czekania osoby
        :param step: Ile czasu
        :return:
        """
        self.wait_time += step
