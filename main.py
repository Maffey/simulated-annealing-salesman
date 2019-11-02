import copy
import math
import matplotlib.pyplot as plt
import numpy
import random

# SIMULATED ANNEALING APPROACH

# Our cities from A to E respectively, for student's index XXX7
cities = [[1, 2], [3, 1], [3, 6], [6, 7], [5, 2]]
number_of_cities = len(cities)

xmin = min(pair[0] for pair in cities)
xmax = max(pair[0] for pair in cities)

ymin = min(pair[1] for pair in cities)
ymax = max(pair[1] for pair in cities)


def transform(pair):
    x = pair[0]
    y = pair[1]
    return [(x - xmin) * 100 / (xmax - xmin), (y - ymin) * 100 / (ymax - ymin)]


rescaled_cities = [transform(b) for b in cities]

cities = rescaled_cities

# If we need to test on random amount of cities, use the line below
# cities = [random.sample(range(15), 2) for x in range(number_of_cities)]

# Generate a random tour between those cities
# Note that we DO NOT start from the point "D", which was given as the starting point for the task,
# since it doesn't change the behavior of our algorithm in any way, just makes the code more confusing.
tour = random.sample(range(number_of_cities), number_of_cities)

# A reversed array of the temperature flow, which contains numbers evenly spaced on a logarithmic scale,
# to simulate the temperature drop in a natural way.
logarithmic_base_start = 0
logarithmic_base_end = 5
amount_of_temperature_numbers = 100000
temperature_flow = numpy.logspace(logarithmic_base_start, logarithmic_base_end, num=amount_of_temperature_numbers)[::-1]

# While temperature gets lower, perform simulated annealing (until it drops to zero)
for temperature in temperature_flow:
    # Take two random cities on our tour and then set them so that first city is first on the tour.
    first_city, second_city = sorted(random.sample(range(number_of_cities), 2))

    # Create a new tour where the two generated cities are swapped in order on the tour.
    new_tour = copy.copy(tour)
    new_tour[first_city], new_tour[second_city] = new_tour[second_city], new_tour[first_city]

    # Calculate the cost (length) of the path on our old tour and a new one.
    old_distances_trace = [math.sqrt(sum(
        [(cities[tour[(k + 1) % number_of_cities]][d] - cities[tour[k % number_of_cities]][d]) ** 2 for d in range(2)]))
        for k in [second_city, second_city - 1, first_city, first_city - 1]]
    new_distances_trace = [math.sqrt(sum(
        [(cities[new_tour[(k + 1) % number_of_cities]][d] - cities[new_tour[k % number_of_cities]][d]) ** 2 for d in
         range(2)])) for k in [second_city, second_city - 1, first_city, first_city - 1]]
    old_distances = sum(old_distances_trace)
    new_distances = sum(new_distances_trace)

    # If our change of the path meets the conditions of our Briggs equation,
    # which is based on temperature, lengths of tours and probability, accept a new tour as our default one.
    if math.exp((old_distances - new_distances) / temperature) > random.random():
        tour = copy.copy(new_tour)

# After the temperature drops to zero and the algorithm stops, plot the map of the cities and the path on the diagram.
plt.plot([cities[tour[i % number_of_cities]][0] for i in range(number_of_cities + 1)],
         [cities[tour[i % number_of_cities]][1] for i in range(number_of_cities + 1)], 'go--')
plt.show()
