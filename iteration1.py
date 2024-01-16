from operator1 import operator, people_array, passengers_at_dest
from numpy import mean

simulation_time = 50000


def iteration():
    for step in range(simulation_time):
        operator()


iteration()

waiting_times = []
for waiting_time in passengers_at_dest:
    waiting_times.append(waiting_time.wait_time)
print(mean(waiting_times))

if __name__ == "__main__":
    iteration()
