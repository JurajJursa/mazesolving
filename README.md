# Mazesolving
Project inspired by https://youtu.be/rop0W4QDOUI

My take on path-finding algorithms and turning a picture into a graph
I attempted to do basic optimization, but I am sure that skilled developers would find a lot of space for improvement. This was mostly an exercise in algorithmic thinking. 

# Input
The mazes that this script accepts consists of black and white pixels, with a white pixel in the top row being the start, and a white pixel in the very bottom row being the exit. Other than that, it is expected that the maze is surrounded by black pixel wall.
Image that is to be processed needs to be in the same folder as the script.

# Processing
The image is turned into a graph, which I represent as a dict with a structure of {node_x:((node_y, weight_to_y), (node_z, weight_to_z))} and then has a pathfinding algorithm applied to it. The ones included are depth-first, dijkstra and astar.
Dijkstra seems to outperform A*, I presume it's because of the fact, that euclidian distance is not a good heuristic for a maze.    

# Output
The script outputs an image with the path painted red.



