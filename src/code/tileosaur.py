import heapq

from src.utils import *
from .creature import Creature


class Tileosaur(Creature):
    """Base class for fauna"""
    def __init__(self, surf, pos, groups, target):
        super().__init__(surf, pos, groups)
        # movement
        self.speed          = 3
        self.initial_delay  = 1000/self.speed
        self.move_delay     = Timer(self.initial_delay, func=self.move, autostart=True, repeat=True)
        self.player         = target
        self.direction      = pg.Vector2()

        #pathfinding
        self.range = 5
        self.nodes = {}
        self.create_nodes()

    def create_nodes(self):
        """Create TileNodes used for pathfinding around the sprite"""
        centerx = [x for x in range(int(self.rect.centerx - self.range * TILE_SIZE),
                                    int(self.rect.centerx + self.range * TILE_SIZE + 1), TILE_SIZE)]
        centery = [y for y in range(int(self.rect.centery - self.range * TILE_SIZE),
                                    int(self.rect.centery + self.range * TILE_SIZE + 1), TILE_SIZE)]
        centers = [(x, y) for x in centerx for y in centery]
        for pos in centers: self.nodes[pos] = TileNode(pos)

    def astar(self, target):
        """
        Uses A* and returns list of nodes to target

        target = Rect at goal
        """
        if target.center not in self.nodes: return [self.rect]  # don't move if target is outside of range

        for node in self.nodes.values(): node.distance_cost = ((node.centerx - target.centerx) ** 2
                                                               + (node.centery - target.centery) ** 2)

        current_node        = self.nodes[self.rect.center]     # node at sprite position
        current_node.cost   = 0
        start               = current_node    # for referencing first node later
        open_set            = []       # list of contacted nodes
        closed_set          = set()  # list of fully explored nodes
        path                = []   # list of nodes tracing from target to self
        heapq.heappush(open_set, (current_node.total_cost(), current_node))

        offsets = [(TILE_SIZE, TILE_SIZE), (TILE_SIZE, -TILE_SIZE),                         # List of offsets to
                   (-TILE_SIZE, TILE_SIZE), (-TILE_SIZE, -TILE_SIZE), (-TILE_SIZE, 0),      # get position of each
                   (0, TILE_SIZE), (0, -TILE_SIZE), (TILE_SIZE, 0)]                         # neighbouring node

        while open_set:
            _, current_node = heapq.heappop(open_set)       # choose node with lowest cost
            closed_set.add(current_node.center)             # mark it as explored

            if current_node.center == target.center:
                if current_node == start:       # incase target ends up at same location as sprite
                    path.append(current_node)
                    break
                while current_node.center != self.rect.center:      # when target is not at sprite's location
                    path.append(current_node)                       # trace back to start node
                    current_node = current_node.parent
                break

            for dx, dy in offsets:
                path_cost = TILE_SIZE       # movement cost, needs work
                if (dx, dy) in offsets[:4]:         # diagonal offsets
                    path_cost = TILE_SIZE * 1.414   # cost more to move to
                neighbour = self.nodes[(current_node.centerx + dx, current_node.centery + dy)]
                if neighbour.center in closed_set:
                    continue
                # if node's cost can be updated to lower it through new path then do that
                # here, current_node.cost + path_cost is g(n)
                if (neighbour.total_cost()) > (current_node.cost + path_cost + neighbour.distance_cost):
                    neighbour.cost   = current_node.cost + path_cost
                    neighbour.parent = current_node
                heapq.heappush(open_set, (neighbour.total_cost(), neighbour))   # enable it to be explored later

        path.reverse()      # to trace it from self to target
        return path

    def get_direction(self, target):
        direction_node = self.astar(target)[0]      # get next node to move to

        # move in the direction of the next node or stand still
        if direction_node.centerx < self.rect.centerx: self.direction.x = -1
        elif direction_node.centerx > self.rect.centerx: self.direction.x = 1
        else: self.direction.x = 0

        if direction_node.centery < self.rect.centery: self.direction.y = -1
        elif direction_node.centery > self.rect.centery: self.direction.y = 1
        else: self.direction.y = 0

        # normalizing diagonal movement speed
        if self.direction.magnitude() > 1:
            if self.move_delay.duration  == self.initial_delay:
                self.move_delay.duration *= 1.414
        else:
            self.move_delay.duration = 1000/self.speed

    def move(self):
        """Moves sprite in the direction it's pointing"""
        self.rect.x += TILE_SIZE * self.direction.x
        self.rect.y += TILE_SIZE * self.direction.y

    def update(self, _):
        """Updates sprite values"""
        self.nodes.clear()      # clear and create new nodes every frame for dynamic pathfinding
        self.create_nodes()
        self.get_direction(self.player.rect)
        self.move_delay.update()

class TileNode(pg.FRect):
    """Nodes used for pathfinding through A*"""
    def __init__(self, pos):
        super().__init__(pos, (5, 5))
        self.center         = pos
        self.parent         = None
        self.cost           = math.inf   # cost from initial point, i.e, g(n)
        self.distance_cost  = math.inf    # cost to target, i.e, h(n)

    def total_cost(self):
        """Returns total cost of node, i.e, f(n)"""
        return self.cost + self.distance_cost
