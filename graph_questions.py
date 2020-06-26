
#Question 1:
#Write a function, numIslands, which takes in a 2D grid map of 1s (land) and 0s (water). 
# Your function should return the number of distinct islands in the grid. 
# An island is surrounded by water and is formed by connecting adjacent lands horizontally or vertically. 
# You may assume all four edges of the grid are all surrounded by water.


#Input 1:
#11110
#11010
#11000
#00000
#Output: 1

#Input 2:
#1000
#11000
#00100
#00011

#Output: 3

#This seems to be a question about finding the connected components of a graph 
#The tough part is translating the matrix into a graph structure
#I would like to try and turn the 2D array into a graph using adjacency lists for each vertex
#1's are vertices and then 0s will just not be added into the graph
#hopefully I can do it in a way so that I can iterate over each vertex and then finding the connected
#components will be much simpler after that is done

from collections import deque

class Vertex(object):
    def __init__(self, vertex_id):
        #have an ID for the vertex, these IDs will have to be generated when traversing the 2D array
        #I think vertex IDs could be a tuple of its x y point in the matrix
        self.id = vertex_id
        #initialize a dict to track the neighbors of the vertex
        self.neighbors_dict = {}

    def get_neighbors(self):
        return self.neighbors_dict.values()

    def add_neighbor(self, vertex):
        self.neighbors_dict[vertex.id] = vertex

    def add_edge(self, vertex):
        self.add_neighbor(vertex)
        vertex.add_neighbor(self)

    def __str__(self):
        neighbor_ids = list(self.neighbors_dict.keys())
        return f'{self.id} adjacent to {neighbor_ids}'
    def __repr__(self):
        return self.__str__()


def turn_matrix_into_graph(matrix: [[int]]):
    #the graph will just be a dictionary of vertices with the vertex id (the vertex's coords) as the keys and
    #the Vertex object as its value
    graph = {}
    for col in range(len(matrix[0])):
        for row in range(len(matrix)):
            # print(row, col)
            # print(matrix[row][col])
            if matrix[row][col] == 1:
               

                if (row, col) not in graph:
                    current_vertex = Vertex((row, col))

                    #check all the vertices in the 4 directions around the current one for 1's
                    #so that we can add them as neighbors


                    #check the neighbor beneath the vertex
                    if row+1 < len(matrix):
                        # print("checking beneath")
                        if matrix[row+1][col] == 1:
                            if (row+1, col) in graph:
                                current_vertex.add_edge(graph[(row+1, col)])
                            else:
                                below_neighbor = Vertex((row+1, col))
                                graph[(row+1, col)] = below_neighbor
                                # current_vertex.add_neighbor(below_neighbor)
                                current_vertex.add_edge(below_neighbor)
                    # check the neighbor above the vertex
                    # print(row-1)
                    if 0 <= row-1:
                        # print("checking above")
                        if matrix[row-1][col] == 1:

                            if (row-1, col) in graph:
                                current_vertex.add_edge(graph[(row-1, col)])

                            else:
                                above_neighbor = Vertex((row-1, col))
                                graph[(row-1, col)] = above_neighbor
                                # current_vertex.add_neighbor(above_neighbor)
                                current_vertex.add_edge(above_neighbor)

                    #check the neighbor to the left of the vertex
                    if 0 <= col-1:
                        # print("checking to the left")
                        if matrix[row][col-1] == 1:
                        
                            if (row, col-1) in graph:
                                current_vertex.add_edge(graph[(row,col-1)])

                            else:
                                left_neighbor = Vertex((row, col-1))
                                graph[(row, col-1)] = left_neighbor
                                # current_vertex.add_neighbor(left_neighbor)
                                current_vertex.add_edge(left_neighbor)

                    #check the neighbor to the right of the vertex
                    if col+1 < len(matrix[0]):
                        # print("checking to the right")
                        if matrix[row][col+1] == 1:

                            if (row, col+1) in graph:
                                current_vertex.add_edge(graph[(row, col+1)])

                            else:

                                right_neighbor = Vertex((row, col+1))
                                graph[(row, col+1)] = right_neighbor
                                # current_vertex.add_neighbor(right_neighbor)
                                current_vertex.add_edge(right_neighbor)
                    if current_vertex not in graph:
                        graph[(row, col)] = current_vertex

    return graph

#This function is used and combined with the above function to find the number of
#islands in a 2d array of integers (matrix)
def get_connected_components(graph):

    #this set will contain vertex objects
    visited = set()

    connected_comps = []

    def get_cc_recursive(current_vertex: Vertex, visited_vertices, connected_vertices):
        visited_vertices.add(current_vertex)
        connected_vertices.append(current_vertex.id)
        print(current_vertex)

        for neighbor in current_vertex.get_neighbors():
            # print(neighbor.__str__() + " is a neighbor to " + current_vertex.__str__())
            if neighbor not in visited_vertices:
                get_cc_recursive(neighbor, visited_vertices, connected_vertices)
        return connected_vertices

    for vertex in graph.values():
        if vertex not in visited:

            current_connected_vertices = []
            get_cc_recursive(vertex, visited, current_connected_vertices)

            connected_comps.append(current_connected_vertices)
    return connected_comps


#QUESTION 2:
#rotten oranges
#given a matrix of integers where 2 is a rotten orange, 1 is a fresh orange and 0 denotes no orange
#the rotten orange turns all oranges it is adjacent to into rotten oranges
#each minute the rotten orange(s) will turn its neighbors rotten
#return how many steps(minutes) it would take to turn all oranges rotten
#it is possible that not all oranges can be turned rotten because there could be orange(s) not connected
#to other rotten oranges

def rotten_oranges(matrix: [[int]]):
    minutes = -1
    visited = set()

    queue = deque()

    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if matrix[row][col] == 2:
                queue.append((row, col))
    if len(queue) == 0:
        return -1

    
    while queue:

        

        current_rotten_oranges = []

        for (row, col) in queue.copy():


            matrix[row][col] = 2
            current_rotten_oranges.append((row,col))
            visited.add((row,col))

            #here is where we check all the neighbors around the current spot in the matrix
            if row+1 < len(matrix):
                if matrix[row+1][col] == 1:
                    if (row+1, col) not in visited:
                        queue.append((row+1, col))
            if row-1 >= 0:
                if matrix[row-1][col] == 1:
                    if (row-1, col) not in visited:
                        queue.append((row-1, col))
            if col+1 < len(matrix[0]):
                if matrix[row][col+1] == 1:
                    if (row, col+1) not in visited:
                        queue.append((row, col+1))
            if col-1 >= 0:
                if matrix[row][col-1] == 1:
                    if (row, col-1) not in visited:
                        queue.append((row, col-1))

            queue.remove((row, col))
        minutes += 1

    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if matrix[row][col] == 1:
                return -1

    return minutes






# def bfs_traversal(graph):

#     seen = set()
#     start_vertex = graph[(0,0)]
#     seen.add(start_vertex)

#     distance_away = 0

#     queue = deque()

#     queue.append(start_vertex)


#     while queue:
#         current_vertex = queue.popleft()



#         for neighbor in current_vertex.get_neighbors():
#             if neighbor not in seen:
#                 seen.add(neighbor)
#                 queue.append(neighbor)
#     return distance_away












if __name__ == "__main__":



    #THIS IS QUESTION 1:
    #HOW MANY ISLANDS ARE THERE

    # map1 = [
    # [1, 1, 1, 1, 0],
    # [1, 1, 0, 1, 0],
    # [1, 1, 0, 0, 0],
    # [0, 0, 0, 0, 0]
    # ]
    # graph = turn_matrix_into_graph(map1)
    # print(len(get_connected_components(graph)))

    # map2 = [
    # [1, 1, 0, 0, 0],
    # [1, 1, 0, 0, 0],
    # [0, 0, 1, 0, 0],
    # [0, 0, 0, 1, 1]
    # ]
    # graph2 = turn_matrix_into_graph(map2)
    # print(len(get_connected_components(graph2)))


    oranges_graph = [
        [2,1,1],
        [1,1,0],
        [0,1,1]
    ]

    oranges2 = [
    [2,1,1],
    [0,1,1],
    [1,0,1]
    ]

    oranges3 = [
    [0,2]
    ]

    print(rotten_oranges(oranges3))

    


                        


            
