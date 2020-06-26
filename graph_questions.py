
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
def numIslands(graph):

    #this set will contain vertex objects
    visited = set()

    connected_comps = []

    def get_cc_recursive(current_vertex: Vertex, visited_vertices, connected_vertices):
        visited_vertices.add(current_vertex)
        connected_vertices.append(current_vertex.id)
        # print(current_vertex)

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

def timeToRot(matrix: [[int]]):
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



#THIS IS QUESTION 3:
#Class Scheduling
#There are a number of courses starting at 0 going to n-1
#course can have prerequisites that need to be taken before that course can be taken
#these relationships between courses are expressed as pairs 
#Example: (1,0) to take course 1 you must have had to have taken course 0 before
#this problem can be solved using a topological sort algorithm such as Kahns algorithm

def courseOrder(numCourses, prerequisites):

    #keep a dictionary to track the in-degree of each course vertex
    in_degrees_dict = {}



    for course, prereq in prerequisites:
        

        if course in in_degrees_dict:
            #if that course is already in the in-degree dictionary then add one more to its in-degree
            in_degrees_dict[course] += 1
        #if it isnt in the in-degree dict then add it and give it a value of 1
        #because it is in the prereq list it has 1 in-degree currently
        else:
            in_degrees_dict[course] = 1

        if prereq not in in_degrees_dict:
            in_degrees_dict[prereq] = 0

            '''the prereqs are one of the only courses that could possibly have an in-degree of 0 
                so set it to zero here and if it happens to be a course that has prereqs later in the 
                prereqs list then it will be assigned the correct in-degree in the above if statement
                the only courses with an in-degree of 0 at the end will either only appear as a prereq in the 
                prereq list or it will not appear at all in the prereq list but could be included through the numCourses
                example of that would be a course that isnt a prereq to anything else but it is a course regardless
                that would be a single vertex with no edges in a graph
                so that has to be checked for later in this function'''


    top_sort = []



    while len(in_degrees_dict) > 0:


        current_course_in_degree_zero = None

        # print(in_degrees_dict)
        for course in in_degrees_dict:
            #find any courses with 0 in-degree
            if in_degrees_dict[course] == 0:
                current_course_in_degree_zero = course
        #append the current course to our top sort answer
        top_sort.append(current_course_in_degree_zero)


        in_degrees_dict.__delitem__(current_course_in_degree_zero)

        
        for course, prereq in prerequisites:
            if current_course_in_degree_zero == prereq:
                #find the course(s) that has our current course as a prereq and decrement its in-degree by 1
                in_degrees_dict[course] -= 1
            
        #delete the current course with in degree zero from the in-degrees dictionary so it does not 
        #keep becoming the current course 
    return top_sort


 













if __name__ == "__main__":



    #THIS IS QUESTION 1:
    #HOW MANY ISLANDS ARE THERE

    map1 = [
    [1, 1, 1, 1, 0],
    [1, 1, 0, 1, 0],
    [1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0]
    ]
    graph = turn_matrix_into_graph(map1)
    print(len(numIslands(graph)))

    map2 = [
    [1, 1, 0, 0, 0],
    [1, 1, 0, 0, 0],
    [0, 0, 1, 0, 0],
    [0, 0, 0, 1, 1]
    ]
    graph2 = turn_matrix_into_graph(map2)
    print(len(numIslands(graph2)))



    

    oranges1 = [
        [2,1,1],
        [1,1,0],
        [0,1,1]
    ]
    print(timeToRot(oranges1))

    oranges2 = [
    [2,1,1],
    [0,1,1],
    [1,0,1]
    ]
    print(timeToRot(oranges2))

    oranges3 = [
    [0,2]
    ]

    print(timeToRot(oranges3))


    courses1 = [ [1,0] ]
    print(courseOrder(2, courses1))

    courses2 = [ [1,0], [2,0], [3,1], [3,2] ]

    print(courseOrder(4, courses2))

    


            
                        


