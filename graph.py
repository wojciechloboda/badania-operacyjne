from collections import deque
class RoomGraph:
    def __init__(self):
        self.graph = {}
        self.doors = set()
        self.tables = set()
        self.chairs = set()
        self.restricted = set()
        self.walls = set()
    def BFS(self,start):
        #Graph dict, key = (i,j), value = [(i1,j1),(i2,j2),...]
        #return dict, key = (i,j), value = distance
        queue = deque([start])
        distance = {}
        for key in self.graph.keys():
            distance[key] = float('inf')
        distance[start] = 0
        while queue:
            node = queue.popleft()
            for neighbor in self.graph[node]:
                if distance[neighbor] == float('inf'):
                    distance[neighbor] = distance[node] + 1
                    queue.append(neighbor)
        return distance