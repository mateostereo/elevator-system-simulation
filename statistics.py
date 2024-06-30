import importlib
import numpy as np
from scipy import stats

# simulation assumptions:
# 50000 kroków symulacji, 8 pięter, maksymalnie 10 czekających na piętro
# szansa na pojawienie się pasażera: 1/25 na krok
# Pierwszy system: 1 winda o stałej prędkości piętro/10 kroków
# Drugi system: 2 windy o prędkościach z rozkładu płaskiego z zakresu piętro/7 kroków do piętra/13 kroków.


def two_el(n):
    import iteration2
    results = []
    for _ in range(n):
        result = iteration2.run_outside()
        results.append(result)
        importlib.reload(iteration2)
    return results


def one_el(n):
    import iteration1
    results = []
    for _ in range(n):
        result = iteration1.run_outside()
        results.append(result)
        importlib.reload(iteration1)
    return results


i = 5
results_one = one_el(i)
results_two = two_el(i)

# Perform t-test
t_stat, p_value = stats.ttest_ind(results_one, results_two)

# Print the results
print("t-statistic:", t_stat)
print("p-value:", p_value)

# Interpret the results
alpha = 0.05  # significance level
if p_value < alpha:
    print("Reject the null hypothesis: There is a significant difference in mean times.")
else:
    print("Fail to reject the null hypothesis: There is no significant difference in mean times.")
