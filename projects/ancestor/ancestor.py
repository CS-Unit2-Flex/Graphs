from collections import deque
from graph_copy import Graph
def earliest_ancestor(ancestors, starting_node):
    print(ancestors)
    g = Graph()

    for ancestor in ancestors: # Had to get rid of IndexError conditional in graph_copy
        g.add_vertex(ancestor[0])
        g.add_vertex(ancestor[1])
        g.add_edge(ancestor[1], ancestor[0]) 

    # print(g.get_neighbors(5))
    visited = set()

    q = deque()
    q.append([starting_node])

    path_to_furthest_ancestor = []

    if len(g.get_neighbors(starting_node)) < 1:
        return -1

    while len(q) > 0:
        current_path = q.popleft()
        current_ancestor = current_path[-1]

        for neighbor in g.get_neighbors(current_ancestor):
            path_copy = list(current_path)
            path_copy.append(neighbor)
            q.append(path_copy)
            print(path_copy, path_copy[-1])
            if len(path_copy) > len(current_path):
                path_to_furthest_ancestor.append(path_copy[-1])

    # print(path_to_furthest_ancestor[0])
    return path_to_furthest_ancestor[-1]


if __name__ == '__main__':
    test_ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7), (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]
    print(earliest_ancestor(test_ancestors, 1))