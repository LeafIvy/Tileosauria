from src.utils import *
from .creature import Creature

import heapq


class Tileosaur(Creature):
    """Base class for fauna"""
    def __init__(self, surf, pos, target, collision_sprites):
        super().__init__(surf, pos)

        self.collision_sprites = collision_sprites

        # movement
        self.speed          = 6
        self.initial_delay  = 1000/self.speed
        self.move_delay     = Timer(self.initial_delay, func=self.move, autostart=True, repeat=True)
        self.player         = target
        self.direction      = pg.Vector2()

        #pathfinding
        self.OFFSETS = [(TILE_SIZE, TILE_SIZE), (TILE_SIZE, -TILE_SIZE),                         # List of offsets to
                        (-TILE_SIZE, TILE_SIZE), (-TILE_SIZE, -TILE_SIZE), (-TILE_SIZE, 0),      # get position of each
                        (0, TILE_SIZE), (0, -TILE_SIZE), (TILE_SIZE, 0)]                         # neighbouring node
        self.DIAGONAL_OFFSETS = self.OFFSETS[:4]
        self.range = 8
        self.nodes = {}
        self.create_nodes()

    def create_nodes(self):
        """Create TileNodes used for pathfinding around the sprite"""
        centerx = [x for x in range(int(self.rect.centerx - self.range * TILE_SIZE),
                                    int(self.rect.centerx + self.range * TILE_SIZE + 1), TILE_SIZE)]
        centery = [y for y in range(int(self.rect.centery - self.range * TILE_SIZE),
                                    int(self.rect.centery + self.range * TILE_SIZE + 1), TILE_SIZE)]
        centers = [(x, y) for x in centerx for y in centery]
        for pos in centers: self.nodes[pos] = TileNode(pos, self.collision_sprites)

    def astar(self, target):
        """
        Uses A* and returns list of nodes to target

        target = Rect at goal
        """
        if target.center not in self.nodes: return [self.rect]  # don't move if target is outside of range

        self._initialize_nodes(target)

        current_node        = self.nodes[self.rect.center]     # node at sprite position
        current_node.cost   = 0
        open_set            = []                               # list of contacted nodes
        closed_set          = set()                            # list of fully explored nodes
        path                = []                               # list of nodes tracing from target to self

        heapq.heappush(open_set, (current_node.total_cost(), current_node))

        while open_set:
            _, current_node = heapq.heappop(open_set)       # choose node with lowest cost
            closed_set.add(current_node.center)             # mark it as explored


            # Get the list of nodes from goal to self and exit the loop
            if current_node.center == target.center:
                path = self._get_path(current_node)
                if path: break

            self._explore_neighbours(current_node, open_set, closed_set)

        path.reverse()      # to trace it from self to target
        return path

    def _initialize_nodes(self, target):
        """Reset node costs and assign them their distance cost"""
        for node in self.nodes.copy().values():
            node.reset()

            # Calculate Chebyshev distance
            node.distance_cost = max(abs(node.centerx - target.centerx), abs(node.centery-target.centery)) // TILE_SIZE

    def _get_path(self, current_node):
        """Returns list of nodes leading from target to self"""
        path = []

        # If target is adjacent to self then don't move
        for dx, dy in self.OFFSETS:
            pos = (current_node.centerx + dx, current_node.centery + dy)
            if pos in self.nodes:
                neighbour = self.nodes[pos]
                if neighbour.colliderect(self.rect):
                    path.append(self.rect)
                    return path

        # If target coincides with self then don't move
        if current_node.center == self.rect.center:
            path.append(current_node)
            return path

        # Else, get all the nodes leading from target back to self
        while current_node.center != self.rect.center:
            path.append(current_node)
            current_node = current_node.parent
        return path

    def _explore_neighbours(self, current_node, open_set, closed_set):
        """Explore the neighbouring nodes and assign them a cost and mark add them into open set"""
        for dx, dy in self.OFFSETS:
            pos = (current_node.centerx + dx, current_node.centery + dy)
            if pos in self.nodes: neighbour = self.nodes[pos]
            else: continue

            path_cost = TILE_SIZE
            if (dx, dy) in self.DIAGONAL_OFFSETS: path_cost *= 1.414       # Diagonal paths cost more

            if neighbour.center in closed_set: continue

            self._update_node_cost(neighbour, current_node, path_cost, open_set)

    def _update_node_cost(self, neighbour, current_node, path_cost, open_set):
        """
        If node's cost can be updated to lower its cost through new path, then do that
        Here, current_node.cost + path_cost is g(n)
        """
        if (neighbour.total_cost()) > ((current_node.cost + path_cost) + neighbour.distance_cost):
            neighbour.cost = current_node.cost + path_cost
            neighbour.parent = current_node
            heapq.heappush(open_set, (neighbour.total_cost(), neighbour))  # enable it to be explored later

    def get_direction(self, target):
        direction_node = self.astar(target)[0]

        # move in the direction of the next node or stand still
        self.direction = (pg.Vector2(direction_node.center) - pg.Vector2(self.rect.center)) // TILE_SIZE

        # normalizing diagonal movement speed
        if self.direction.magnitude() > 1:
            self.move_delay.duration = 1.414 * self.initial_delay
        else:
            self.move_delay.duration = self.initial_delay

    def move(self):
        """Moves sprite in the direction it's pointing"""
        self.rect.x += TILE_SIZE * self.direction.x
        self.rect.y += TILE_SIZE * self.direction.y

        # clear and create new nodes every time sprite moves for dynamic pathfinding
        if self.direction.magnitude() >= 1:
            self.nodes.clear()
            self.create_nodes()

    def update(self, _):
        """Updates sprite values"""
        self.get_direction(self.player.rect)
        self.move_delay.update()

class TileNode(pg.FRect):
    """Nodes used for pathfinding through A*"""
    def __init__(self, pos, collision_sprites):
        super().__init__(pos, (5, 5))
        self.center         = pos
        self.parent         = None
        self.cost           = math.inf    # cost from initial point, i.e, g(n)
        self.distance_cost  = math.inf    # cost to target, i.e, h(n)

        self.sprite = None
        for sprite in collision_sprites:
            if self.colliderect(sprite.rect):
                self.sprite = sprite
                break

    def reset(self):
        self.parent = None
        self.cost = math.inf
        self.distance_cost = math.inf

    def total_cost(self):
        """Returns total cost of node, i.e, f(n)"""
        return self.cost + self.distance_cost
