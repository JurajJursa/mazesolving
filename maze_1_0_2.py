# -*- coding: utf-8 -*-
"""
Created on Mon Dec 30 22:55:22 2019

@author: juraj
"""
from PIL import Image, ImageDraw
import time as t

class Maze:
    
    def __init__(self, file_name, ext):
        start = t.time()
        img = Image.open(file_name+"."+ext).convert('RGB')
        self.pic = img
        self.length = img.size[0]
        arr = list(img.getdata())
        
            
        #Changing the array into a 2D array "deflattening"
        #Representing black pixels as 1s and white pixels as 0s
        
        count = 0        
        proc_arr = [[] for i in range(self.length)]
        
        for i in arr:
            
            if sum(i) > 700:
                proc_arr[count].append(0)
            else:
                proc_arr[count].append(1)
            count+=1
            
            if count % self.length == 0:
                count = 0
            
        self.bit_maze = proc_arr

        #Finding the starting node and the ending node, which will also be added to the array of other nodes later
        for i in range(1, self.length):
            if self.bit_maze[i][0] == 0:
                self.start = Node(i, 0)
                break
        
        for i in range(1, self.length):
            if self.bit_maze[i][self.length-1] == 0:
                self.exit = Node(i, self.length-1)
                break    
                    
        #Determining the nodes and adding them to an array        
        self.node_arr = [self.start]
        for x in range(1, self.length-1):
            for y in range(1, self.length-1):
                if self.bit_maze[x][y] == 0:
                    opt = self.bit_maze[x][y-1] + self.bit_maze[x][y+1] + self.bit_maze[x-1][y] + self.bit_maze[x+1][y]
                    #This is a potential case when it is a straight path with no options, in that case opt == 2
                    #In case that we get a badly generated maze, there might be a single white point cut off opt == 4
                    if opt == 4 or (opt == 2 and (self.bit_maze[x][y-1] + self.bit_maze[x][y+1] == 0 or self.bit_maze[x-1][y] + self.bit_maze[x+1][y] == 0)): 
                        pass
                    else:
                        self.node_arr.append(Node(x,y))
                         
        
        self.node_arr = self.node_arr + [self.exit]


        #If I had done that inside the previous for loop, the conditions for a node would be much more complex, because I couldn't simply sum the adjacent pixels up
        for node in self.node_arr:
            y,x = node.location()
            self.bit_maze[y][x] = "X"
       
        #Print out the maze into the console
        '''
        for y in range(len(self.bit_maze)):
            for x in range(len(self.bit_maze)):
                print(self.bit_maze[x][y], end=" ")
            print()
        '''
        
        #Determining all the edges
        """
        1. Look down and right from the node
        2a. Count the number of walked pixels to get the weight of the edge
        2b. If encounters a black pixel on the way or another node, stop immediately
        3. If a node is encountered, register both nodes and the weight 
        """
        graph_time = t.time()
        print("The initialization took "+ format(graph_time-start, ".3f") +" seconds to complete")
        
        edge_map = {}
        
        for i in range(len(self.node_arr)):
            node = self.node_arr[i]
            node_x, node_y = node.location()
            
            #This looks for a possible node that connects to the right from the original node (increasing x direction)
            for x in range(node_x+1, self.length):
                
                #If it encounters a wall, the loop stops
                if self.bit_maze[x][node_y] == 1:
                    break
                elif self.bit_maze[x][node_y] == "X":
                    weight = x - node_x
                    
                    #Determining which node does the origin node connect to
                    for j in range(i+1, len(self.node_arr)+1):
                        connect = self.node_arr[j]
                        if connect.location() == (x, node_y):
                            break
                        
                    #Adding both to the dictionary
                    if node in edge_map:
                        edge_map[node].append((connect,weight))
                    else:
                        edge_map[node] = [(connect,weight)]
                    
                    if connect in edge_map:
                        edge_map[connect].append((node,weight))
                    else: 
                        edge_map[connect] = [(node,weight)]
                                        
                    break

            #Iterating through individual pixels going down from the node (increasing y direction)
            for y in range(node_y+1, self.length):
                
                #If it encounters a wall, the loop stops
                if self.bit_maze[node_x][y] == 1:
                    break
                elif self.bit_maze[node_x][y] == "X":
                    weight = y - node_y
                    
                    #Determining which node does the origin node connect to
                    for j in range(i+1, len(self.node_arr)+1):
                        connect = self.node_arr[j]
                        if connect.location() == (node_x, y):
                            break
                        
                    #Adding both to the dictionary
                    if node in edge_map:
                        edge_map[node].append((connect,weight))
                    else:
                        edge_map[node] = [(connect,weight)]
                    
                    if connect in edge_map:
                        edge_map[connect].append((node,weight))
                    else: 
                        edge_map[connect] = [(node,weight)]
                                        
                    break
                
        self.graph = edge_map
        print("The graph creation took "+ format(t.time()-graph_time, ".3f") +" seconds to complete")
        print("The number of nodes is "+str(len(self.node_arr)))        
    
    #This is the very first idea, very inefficient brute force
    def brute_force(self):
        start = t.time()
        self.paths = []
        
        def step(node, path, length, end):
            #Base case
            if node == end:
                self.paths.append([path.copy(), length])
            
            #Recursion for all connecting nodes
            for connect,weight in sorted(self.graph[node], key=lambda x : x[1]):
                if connect not in path:
                    step(connect, path+[connect], length+weight, end)
            
        #Calling the recursive function
        step(self.start, [self.start], 0, self.exit)

        #Drawing part        
        return_img = self.pic
        draw = ImageDraw.Draw(return_img)
        self.shortest_path = min(self.paths, key= lambda x : x[1])[0]
        
        for i in range(len(self.shortest_path)-1):
            first = self.shortest_path[i].location()    
            second = self.shortest_path[i+1].location()
            draw.line([first,second], fill=(255,0,0), width=1)
        
        return_img.show()
        print("This has taken "+ format(t.time()-start, ".3f") + " seconds to complete")

    def brute_force_single(self):
        start = t.time()
        self.paths = []
        
        def step(node, path, length, end):
            #Base case
            if len(self.graph[node]) == 1 and node != self.start:
                if node == end:
                    self.paths = path
                return
            
            #Recursion for all connecting nodes
            for connect,weight in sorted(self.graph[node], key=lambda x : x[1]):
                if connect not in path:
                    step(connect, path+[connect], length+weight, end)
                
            
        #Calling the recursive function
        step(self.start, [self.start], 0, self.exit)

        #Drawing part        
        return_img = self.pic
        draw = ImageDraw.Draw(return_img)
        
        for i in range(len(self.paths)-1):
            first = self.paths[i].location()    
            second = self.paths[i+1].location()
            draw.line([first,second], fill=(255,0,0), width=1)
        
        return_img.show()
        print("This has taken "+ format(t.time()-start, ".3f") + " seconds to complete")       
       
        
        
    
    def dijkstra(self):
        #Create an array with triples (node, weight from start, path via which node)
        #weight and paths get adjusted as we go from starting node
        #check all the nodes it connects to
        #move to the next node from which we check all it connects to
        #priority is always the node with the current lowest weight 
        
        def get_index_tuple(l, index, value):
            for pos,k in enumerate(l):
                if k[index] == value:
                    return pos
        
        start = t.time()

        #create the queue and set the weight for start to 0
        queue = [[i,self.length**2,None] for i in self.node_arr]
        queue[[i[0] for i in queue].index(self.start)][1] = 0
        
        track_checked = []
        track_checked_nodes = []
        
        node = None
        
        while node != self.exit:
            queue.sort(key = lambda x: x[1])
            node,current_weight,previous = queue[0]
            
            #look at what node connects to and add the connecting nodes to the queue
            for connect,weight in self.graph[node]:
                
                if connect != previous and connect not in track_checked_nodes:
                    ind = get_index_tuple(queue, 0, connect)
                    if queue[ind][1] > (current_weight + weight):
                        queue[ind][1] = current_weight + weight
                        queue[ind][2] = node    
              
            y = queue.pop(0)
            track_checked.append(y)
            track_checked_nodes.append(y[0])
        
        self.path = [self.exit]
        last = previous
        while last != self.start:
            self.path.append(last)
            ind = [i[0] for i in track_checked].index(last)
            last = track_checked[ind][2]
        
        #Drawing part        
        return_img = self.pic
        draw = ImageDraw.Draw(return_img)         
        for i in range(len(self.path)-1):
            first = self.path[i].location()    
            second = self.path[i+1].location()
            draw.line([first,second], fill=(255,0,0), width=1)
        
        return_img.show()
        print("Dijkstra has taken "+ format(t.time()-start, ".3f") + " seconds to complete")
        
    
    def astar(self, percentage):
        from math import sqrt
        start = t.time()
        
        def euclid(a, b):
            x1, y1 = a.location()
            x2, y2 = b.location()
            return sqrt((x1-x2)**2 + (y1-y2)**2)

        def get_index_tuple(l, index, value):
            for pos,k in enumerate(l):
                if k[index] == value:
                    return pos
        
        #create the queue and set the weight for start to 0
        queue = [[i,self.length**2,None, euclid(i, self.exit)] for i in self.node_arr]
        queue[[i[0] for i in queue].index(self.start)][1] = 0
        
        track_checked = []
        track_checked_nodes = []
        
        node = None
        
        while node != self.exit:
            queue.sort(key = lambda x: x[1]+(x[3]*percentage/100))
            node,current_weight,previous,dist = queue[0]
            
            #look at what node connects to and add the connecting nodes to the queue
            for connect,weight in self.graph[node]:
                
                #don't look at the node it came from
                if connect != previous and connect not in track_checked_nodes:
                    
                    ind = get_index_tuple(queue, 0, connect)
                    if queue[ind][1] > (current_weight + weight):
                        queue[ind][1] = current_weight + weight
                        queue[ind][2] = node
            
            y = queue.pop(0)
            track_checked.append(y)
            track_checked_nodes.append(y[0])
        
        self.path = [self.exit]
        last = previous
        while last != self.start:
            self.path.append(last)
            ind = [i[0] for i in track_checked].index(last)
            last = track_checked[ind][2]
        
        #Drawing part        
        return_img = self.pic
        draw = ImageDraw.Draw(return_img)         
        for i in range(len(self.path)-1):
            first = self.path[i].location()    
            second = self.path[i+1].location()
            draw.line([first,second], fill=(255,0,0), width=1)
        
        return_img.show()
        print("A* has taken "+ format(t.time()-start, ".3f") + " seconds to complete")
        
        
class Node:

    def __init__(self, x, y):
        self.loc_x = x
        self.loc_y = y
    
    def location(self):
        return (self.loc_x, self.loc_y)
    
    def __repr__(self):
        return "<"+str(self.loc_x)+","+str(self.loc_y)+">"





name=input("enter the name of the file: ")
ext=input("enter the file extension: ")
try:
    the_maze = Maze(name, ext)
    algo=input("enter the method you want to use (dijkstra/astar/brute): ")
    if algo=="dijkstra":
        the_maze.dijkstra()
    elif algo=="astar":
        weight=input("Enter the weight you want to assign to euclidian distance in %: ")
        the_maze.astar(int(weight))
    elif algo=="brute":
        the_maze.brute_force_single()
    else:
        print("Algorithm not found!")
except:
    print("File not found!")
        
   



