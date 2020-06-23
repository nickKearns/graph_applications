
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


class Vertex(object):
    def __init__(self, vertex_id):
        #have an ID for the vertex, these IDs will have to be generated when traversing the 2D array
        #I think vertex IDs could be a tuple of its x y point in the matrix
        self.id = vertex_id
        #initialize a dict to track the neighbors of the vertex
        self.neighbors_dict = {}

    def get_neighbors(self):
        return self.neighbors_dict.keys()

    def add_neighbor(self, vertex):
        self.neighbors_dict[vertex.id] = vertex

    def __str__(self):
        return str(self.id)
    def __repr__(self):
        return self.__str__()


def turn_matrix_into_graph(matrix: [[int]]):
    #the graph will just be a dictionary of vertices with the vertex id (the vertex's coords) as the keys and
    #the Vertex object as its value
    graph = {}
    for col in range(len(matrix[0])):
        for row in range(len(matrix)):
            print(row, col)
            # print(matrix[row][col])
            if matrix[row][col] == 1 and (row, col) not in graph:
               
                new_vertex = Vertex((row, col))
                graph[(row, col)] = new_vertex

                #check all the vertices in the 4 directions around the current one for 1's
                #so that we can add them as neighbors

               
                #check the neighbor beneath the vertex
                if 0 >= row+1 < len(matrix):
                    if matrix[row+1][col] == 1:
                        below_neighbor = Vertex((row+1, col))
                        graph[(row+1, col)] = below_neighbor
                        new_vertex.add_neighbor(below_neighbor)

                # check the neighbor above the vertex
                if 0 >= row-1 < len(matrix):
                    if matrix[row-1][col] == 1:
                        above_neighbor = Vertex((row-1, col))
                        graph[(row-1, col)] = above_neighbor
                        new_vertex.add_neighbor(above_neighbor)

                #check the neighbor to the left of the vertex
                if 0 >= col-1:
                    if matrix[row][col-1] == 1:
                        left_neighbor = Vertex((row, col-1))
                        graph[(row, col-1)] = left_neighbor
                        new_vertex.add_neighbor(left_neighbor)

                #check the neighbor to the right of the vertex
                if col+1 < len(matrix):
                    if matrix[row][col+1]:
                        right_neighbor = Vertex((row, col+1))
                        graph[(row, col+1)] = right_neighbor
                        new_vertex.add_neighbor(right_neighbor)

    return graph







if __name__ == "__main__":

    map1 = [
    [1, 1, 1, 1, 0],
    [1, 1, 0, 1, 0],
    [1, 1, 0, 0, 0],
    [0, 0, 0, 0, 0]
]

    print(turn_matrix_into_graph(map1))


                        


            
