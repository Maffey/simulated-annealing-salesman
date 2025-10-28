import copy
import math
import random
import sys

import matplotlib.pyplot as plt
import numpy


def seg_len(first_point, second_point):
    return math.sqrt((first_point[0] - second_point[0]) ** 2 + (first_point[1] - second_point[1]) ** 2)


def main():
    # SIMULATED ANNEALING APPROACH
    if len(sys.argv) >= 2:
        work_mode = sys.argv[1]
    else:
        work_mode = input("Do you want to insert custom, random or default values? [c/r/D]: ")

    if work_mode == "c":
        print("Creating custom map...")
        cities = []
        number_of_cities = int(input("Provide number of cities: "))
        for custom_city in range(number_of_cities):
            print(f"==City: {custom_city}. ==")
            cord_x = int(input(f"Please provide X for the {custom_city}. city: "))
            cord_y = int(input(f"Please provide Y for the {custom_city}. city: "))
            cities.append([cord_x, cord_y])
    elif work_mode == "r":
        print("Creating random map...")
        number_of_cities = int(input("Provide number of cities: "))
        cities = [random.sample(range(100), 2) for x in range(number_of_cities)]
    else:
        print("Default values initialized.")
        # Our cities from A to E respectively, for student's index XXX7
        cities = [[1, 2], [3, 1], [3, 6], [6, 7], [5, 2]]
        number_of_cities = len(cities)

    print(f"Cities: {cities}")

    # Rescale cities so the algorithm works more efficiently. Otherwise might sometimes be ineffective.

    xmin = min(pair[0] for pair in cities)
    xmax = max(pair[0] for pair in cities)

    ymin = min(pair[1] for pair in cities)
    ymax = max(pair[1] for pair in cities)


    def transform(pair):
        x = pair[0]
        y = pair[1]
        return [(x - xmin) * 100 / (xmax - xmin), (y - ymin) * 100 / (ymax - ymin)]


    rescaled_cities = [transform(b) for b in cities]

    # rescaled_cities = cities  # NO NORMALIZATION APPROACH

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

        """
        Calculate the cost (length) of the path on our old tour and a new one.
        The modulo part considers the part where there might be a path where one city_index is out of bound.
        If it is, then it connects to the last city (if it's out of bound on the left side of the array)
        or first city (if it's out of bound on the right side of the array)
        """
        old_distances_paths = []
        for city_index in [second_city, second_city - 1, first_city, first_city - 1]:
            distance = seg_len(rescaled_cities[tour[(city_index + 1) % number_of_cities]],
                               rescaled_cities[tour[city_index % number_of_cities]])
            old_distances_paths.append(distance)
        old_distance = sum(old_distances_paths)

        new_distances_paths = []
        for city_index in [second_city, second_city - 1, first_city, first_city - 1]:
            distance = seg_len(rescaled_cities[new_tour[(city_index + 1) % number_of_cities]],
                               rescaled_cities[new_tour[city_index % number_of_cities]])
            new_distances_paths.append(distance)
        new_distance = sum(new_distances_paths)

        # If our change of the path meets the conditions of our Briggs equation,
        # which is based on temperature, lengths of tours and probability, accept a new tour as our default one.
        if math.exp((old_distance - new_distance) / temperature) > random.random():
            tour = copy.copy(new_tour)

    # After the temperature drops to zero and the algorithm stops, print out our path and its final cost.
    print("Tour: ", tour)

    final_path = []
    for city_index in tour:
        distance = seg_len(rescaled_cities[tour[(city_index + 1) % number_of_cities]],
                           rescaled_cities[tour[city_index % number_of_cities]])
        final_path.append(distance)
    final_path_cost = sum(final_path)
    print("Total cost of the path (normalized): ", final_path_cost)

    # Plot the map of the cities and the path on the diagram for further convenience.
    # The modulo part considers the part where the index might be the last city, then it connects to the first city.
    plt.plot([rescaled_cities[tour[i % number_of_cities]][0] for i in range(number_of_cities + 1)],
             [rescaled_cities[tour[i % number_of_cities]][1] for i in range(number_of_cities + 1)], 'go--')
    plt.show()

    return 0


if __name__ == "__main__":
    sys.exit(main())