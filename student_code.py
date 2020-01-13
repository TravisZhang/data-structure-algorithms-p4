from collections import deque
import operator
import math

class Node():
    def __init__(self, idx, cost_f, cost_g):
        self.idx = idx
        self.cost_f = cost_f
        self.cost_g = cost_g
        
class PriorityQueue():
    def __init__(self):
        self.d = dict()
        
    def enq(self, node):
        self.d[node.idx] = [node.cost_f, node.cost_g]
        
    def deq(self):
        if len(self.d) > 0:
            # sort by cost_f
            list_sorted = sorted(self.d.items(), key=lambda item: item[1][0]) 
            temp = list(list_sorted[0])
            node = Node(temp[0], temp[1][0], temp[1][1])
            # remove the node with lowest cost_f
            self.remove(node)
            # return this node
            return node
        else:
            return None
    
    def exist(self, node):
        if node.idx not in self.d:
            return False
        return True

    def find(self, node):
        if self.exist(node) == False:
            return None
        temp = self.d[node.idx]
        return Node(node.idx, temp[0], temp[1])
    
    def remove(self, node):
        if self.exist(node) == True:
            self.d.pop(node.idx)
    
    def update_g(self, node):
        if len(self.d) > 0 and node.idx in self.d:
            self.d[node.idx][1] = node.cost_g
    
    def update_f(self, node):
        if len(self.d) > 0 and node.idx in self.d:
            self.d[node.idx][0] = node.cost_f
    
    def __len__(self):
        return len(self.d)
        
        
def cal_cost_g(pos0, pos1):
    return math.sqrt(pow((pos0[0] - pos1[0]), 2) + pow((pos0[1] - pos1[1]), 2))
        
def cal_cost_h(pos0, pos1):
#     return abs(pos1[0] - pos0[0]) + abs(pos1[1] - pos0[1])
    return math.sqrt(pow((pos0[0] - pos1[0]), 2) + pow((pos0[1] - pos1[1]), 2))
#     return 0

def get_neighbors(current_node, roads, inters, goal):
    neighbor_idxs = roads[current_node.idx]
    neighbors = []
    for idx in neighbor_idxs:
        cost_g = current_node.cost_g + cal_cost_g(inters[idx], inters[current_node.idx])
        cost_h = cal_cost_h(inters[idx], inters[goal])
        cost_f = cost_g + cost_h
        neighbors.append(Node(idx, cost_f, cost_g))
    return neighbors

def reconstruct_path(parent_map, start, goal):
    current_idx = goal
    path = [current_idx]
    while current_idx != start:
        current_idx = parent_map[current_idx]
        path.insert(0, current_idx)
#     print("final_path: ", path)
    return path

def shortest_path(M,start,goal):
    print("shortest path called")
    inters = M.intersections # dict with node [idx:[x,y]]
    roads = M.roads # list with node [connections] for each idx
    open_list = PriorityQueue() # dict with node [idx:Node]
    closed_list = PriorityQueue() # dict with node [idx:Node]
    parent_map = dict() # dict with node [idx:parent_idx]
    open_list.enq(Node(start, 0, 0))
    while 1:
        current_node = open_list.deq()
        if current_node == None:
            print("Path not found !!!")
            return None
#         print("current_node: ", current_node)
        if current_node.idx == goal:
            print("Path found.")
            break
        else:
            closed_list.enq(current_node)
            neighbors = get_neighbors(current_node, roads, inters, goal)
#             print("neighbors: ", [n[0] for n in neighbors])
            for neighbor in neighbors:
                neighbor_c = closed_list.find(neighbor)
                neighbor_o = open_list.find(neighbor)
                if neighbor_c != None and neighbor.cost_g < neighbor_c.cost_g:
                    closed_list.update_g(neighbor)
                    parent_map[neighbor.idx] = current_node.idx
                elif neighbor_o != None and neighbor.cost_g < neighbor_o.cost_g:
                    open_list.update_g(neighbor)
                    parent_map[neighbor.idx] = current_node.idx
                elif neighbor_c == None and neighbor_o == None:
                    open_list.enq(neighbor)
                    parent_map[neighbor.idx] = current_node.idx
#             print("open_list: ", open_list)
#     print("parent_map: ", parent_map)
    final_path = reconstruct_path(parent_map, start, goal)
    return final_path