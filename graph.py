from collections import deque
class RoomGraph:
    def __init__(self):
        self.graph = {}
        self.doors = set()
        self.tables = set()
        self.chairs = set()
        self.restricted = set()
        self.walls = set()
