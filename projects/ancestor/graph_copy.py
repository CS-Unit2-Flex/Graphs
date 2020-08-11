"""
Simple graph implementation
"""
# from util_copy import Stack, Queue  # These may come in handy
from collections import deque

class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to edges."""
    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        if vertex_id not in self.vertices:
            self.vertices[vertex_id] = set()
        # else:
        #     raise IndexError("this index already exists")

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2) # I am assuming that this is a directed graph for now
        else:
            raise IndexError("one of these vertices does not exist")

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        if vertex_id in self.vertices:
            return self.vertices[vertex_id]
        else:
            raise IndexError("vertex does not exist")

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        q = deque() # Used deque because popleft is O(1) instead of the Queue (which is O(n))
        visited = set()

        q.append(starting_vertex)

        while len(q) > 0:
            vertex = q.popleft()

            if vertex not in visited:
                visited.add(vertex)
                
                for neighbor in self.get_neighbors(vertex):
                    q.append(neighbor)
                print(vertex) # This is what the test is looking for (I was just using it to debug, so I had an extra string in there to find it easily)

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        s = deque()
        visited = set()

        s.append(starting_vertex)

        while len(s) > 0: 
            vertex = s.pop()

            if vertex not in visited: 
                visited.add(vertex)

                for neighbor in self.get_neighbors(vertex):
                    s.append(neighbor)
                print(vertex)

    def dft_recursive(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        visited = set()

        def inner_recursion(starting_vertex):
            if starting_vertex not in visited:
                visited.add(starting_vertex)
                neighbors = self.get_neighbors(starting_vertex)

                print(starting_vertex)        
                for neighbor in neighbors:
                    inner_recursion(neighbor)
        return inner_recursion(starting_vertex)

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        q = deque()
        q.append([starting_vertex])
        visited = set()

        while len(q) > 0:

            path = q.popleft()

            vertex = path[-1]

            if vertex not in visited:
                visited.add(vertex)

                if vertex == destination_vertex:

                    return path


                for neighbor in self.get_neighbors(vertex):
                    path_copy = list(path) 
                    path_copy.append(neighbor)
                    q.append(path_copy)
        return None

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        s = deque()
        s.append([starting_vertex])
        visited = set()

        while len(s) > 0:
            path = s.pop()

            vertex = path[-1]

            if vertex not in visited:
                visited.add(vertex)

                if vertex == destination_vertex:
                    return path

                for neighbor in self.get_neighbors(vertex):
                    path_copy = list(path)
                    path_copy.append(neighbor)
                    s.append(path_copy)
        return None


    # def dfs_recursive(self, starting_vertex, destination_vertex):
    #     visited = set()


    #     def recursion(s, d, path = None):
    #         if path is None:
    #             path = []

    #         if s not in visited:
    #             visited.add(s)
    #             path = path + [s]

    #             if s == d:
    #                 return path

    #             for neighbor in self.get_neighbors(s):
    #                 path_copy = recursion(neighbor, d, path)

    #                 if path_copy:
    #                     return path_copy
    #         return None
    #     return recursion(starting_vertex, destination_vertex)

    def dfs_recursive(self, starting_vertex, destination_vertex, visited = None, path = None):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        # if visited is None:
        #     visited = set()
        # if path is None:
        #     path = []

        if visited is None and path is None:
            visited = set()
            path = []

        visited.add(starting_vertex)
        path = path + [starting_vertex]

        if starting_vertex == destination_vertex:
            return path
        
        for neighbor in self.get_neighbors(starting_vertex):
            
            if neighbor not in visited:
                path_copy = self.dfs_recursive(neighbor, destination_vertex, visited, path)

                if path_copy is not None:
                    return path_copy
        return None

if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)
    # print(graph.get_neighbors(12)) Testing that the conditional works

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    graph.dft(1)
    graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print(graph.dfs(1, 6))
    print(graph.dfs_recursive(1, 6))
