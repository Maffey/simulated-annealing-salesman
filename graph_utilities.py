import math


# Calculates the distance between the nodes from the given coordinates of the nodes.
def vector_length(from_node, to_node):
    x1, y1 = from_node
    x2, y2 = to_node
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


def calculate_edges(points):
    edges = []
    for key_from in points:
        coords_from = points[key_from]
        for key_to in points:
            if key_to == key_from:
                continue
            coords_to = points[key_to]

            distance = vector_length(coords_from, coords_to)
            # Round up to an integer. Possibly optional
            distance = int(distance + 0.5)
            edges.append((key_from, key_to, distance))
    return edges


def dynamic_alpha(starting_point, vertices, edges):
    """
    This is a prototype function which was intended to use dynamic programming approach and be as straight-forward
    and easy as possible. Unfortunately that hasn't worked out and although it kind of calculates some path,
    it's far from solving the Travelling Salesman Problem.
    :param starting_point: Point at which we start our Hamilton's Cycle.
    :param vertices: Points which we can travel to.
    :param edges: Distances between points.
    :return: Cost of the path.
    """
    vertices.pop(vertices.index(starting_point))
    possible_paths = []
    for edge in edges:
        if edge[0] == starting_point and edge[1] in vertices:
            possible_paths.append(edge)
    for path in possible_paths:
        if len(vertices) == 1:
            return path[2] + dist_to_origin(starting_point, edges)  # append to a list instead of return?
        else:
            return path[2] + dynamic_alpha(path[1], vertices, edges)


def dist_to_origin(starting_point, edges, ending_point='d'):
    for edge in edges:
        if edge[0] == starting_point and edge[1] == ending_point:
            return edge[2]
