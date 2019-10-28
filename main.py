import copy
import math
import matplotlib.pyplot as plt
import numpy
import random

from graph import Graph
from graph_utilities import calculate_edges

# Given coordinates for the task
points_odd_index = {'a': (1, 2), 'b': (3, 1), 'c': (3, 6), 'd': (6, 7), 'e': (5, 2)}
# Calculate distances between the points (edges)
edges_odd_index = calculate_edges(points_odd_index)

# Initiate the point of the start
starting_point_odd_index = 'd'
# List the vertices of our graph.
vertices = list(points_odd_index.keys())

# --------------------OUTDATED----------------------------

# Solution using genetic algorithm provided by a library. --> REMOVE LATER
# gen_solve(points_odd_index)

# Initiate the main graph
graph = Graph()

# Set up graph with edges
for edge in edges_odd_index:
    graph.add_edge(*edge)

# ---------------------------------------------------------
# SIMULATED ANNEALING APPROACH

# Additional helper functions

# Initiate variables
number_of_cities = 10
# Generate random cities and a random tour
cities = [random.sample(range(100), 2) for x in range(number_of_cities)]
tour = random.sample(range(number_of_cities), number_of_cities)

# A reversed array of the temperature flow, which contains numbers evenly spaced on a log scale,
# to simulate the temperature drop better.
logarithmic_base_start = 0
logarithmic_base_end = 5
amount_of_temperature_numbers = 100000
temperature_flow = numpy.logspace(logarithmic_base_start, logarithmic_base_end, num=amount_of_temperature_numbers)[::-1]

# While temperature gets lower, perform simulated annealing (until it drops to zero)
for temperature in temperature_flow:
    # Take two random cities on our tour and then set them so that first city is first on the tour.
    cities_to_swap = sorted(random.sample(range(number_of_cities), 2))
    first_city = cities_to_swap[0]
    second_city = cities_to_swap[1]

    # TODO: Consider making the new_tour simpler
    # Create a new tour where the two generated cities are swapped in order on the tour.
    new_tour = tour[:first_city] + tour[second_city:second_city + 1] + tour[first_city + 1:second_city] + tour[first_city:first_city + 1] + tour[second_city + 1:]

    # Calculate the cost (length) of the path on our old tour and a new one.
    old_distances = sum([math.sqrt(sum(
        [(cities[tour[(k + 1) % number_of_cities]][d] - cities[tour[k % number_of_cities]][d]) ** 2 for d in [0, 1]]))
                         for k in [second_city, second_city - 1, first_city, first_city - 1]])
    new_distances = sum([math.sqrt(sum(
        [(cities[new_tour[(k + 1) % number_of_cities]][d] - cities[new_tour[k % number_of_cities]][d]) ** 2 for d in
         [0, 1]])) for k in [second_city, second_city - 1, first_city, first_city - 1]])

    # If our change of the path meets the conditions of our Briggs equation,
    # which is based on temperature, lengths of tours and probability, accept a new tour as our default one.
    if math.exp((old_distances - new_distances) / temperature) > random.random():
        tour = copy.copy(new_tour)

# After the temperature drops to zero and the algorithm stops, plot the map of the cities and the path on the diagram.
plt.plot([cities[tour[i % number_of_cities]][0] for i in range(number_of_cities + 1)],
         [cities[tour[i % number_of_cities]][1] for i in range(number_of_cities + 1)], 'go--')
plt.show()
