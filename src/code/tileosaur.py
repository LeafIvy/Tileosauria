from src.utils import *
from .creature import Creature


class Tileosaur(Creature):
    """Base class for fauna"""
    def __init__(self, surf, pos, groups):
        super().__init__(surf, pos, groups)
        self.set_move_delay_timer(3)

        self.direction = pg.Vector2()
        self.range = 5
        self.nodes = []

    def set_move_delay_timer(self, speed):
        """
        Creates the move_delay Timer by calculating delay based on tiles per second as given

        speed = tiles per second
        """
        self.move_delay = Timer(1000/speed)

    def create_nodes(self):
        """Create TileNodes used for pathfinding around the sprite"""
        centerx = [x for x in range(int(self.rect.centerx - self.range * TILE_SIZE),
                                    int(self.rect.centerx + self.range * TILE_SIZE + 1), TILE_SIZE)]
        centery = [y for y in range(int(self.rect.centery - self.range * TILE_SIZE),
                                    int(self.rect.centery + self.range * TILE_SIZE + 1), TILE_SIZE)]
        centers = [(x, y) for x in centerx for y in centery]
        for pos in centers: self.nodes.append(TileNode(pos))

    def astar(self, target):
        """
        Uses A* to pathfind to target and return next node to move to

        target = Rect at goal
        """
        if target.collidelist(self.nodes) == -1: return self.rect   # don't move if target is outside of range

        current_node = [node for node in self.nodes if node.center == self.rect.center][0]  # initial node at sprite's position
        current_node.parent = current_node
        current_node.distance_cost = math.sqrt((target.centerx - current_node.centerx) ** 2 + (target.centery - current_node.centery) ** 2)
        # Initializing node distance_costs
        for node in self.nodes:
            node.distance_cost = math.sqrt((target.centerx - node.centerx) ** 2 + (target.centery - node.centery) ** 2)
            if node.colliderect(current_node):
                node.parent = current_node
                node.cost = TILE_SIZE

        leaf_nodes = [current_node]
        while leaf_nodes:
            leaf_nodes.remove(current_node)

            if current_node.center == target.center:
                while not current_node.colliderect(self.rect):
                    current_node = current_node.parent
                return current_node

            for node in self.nodes:
                if node.colliderect(current_node) and not node in leaf_nodes:
                    if node.parent:
                        if (node.cost + node.distance_cost) > (current_node.cost + TILE_SIZE + node.distance_cost):
                            node.parent = current_node
                            node.cost = current_node.cost + TILE_SIZE
                    else:
                        node.cost = current_node.cost + TILE_SIZE
                    leaf_nodes.append(node)

            current_node = min(leaf_nodes, key=lambda x: x.cost + x.distance_cost)

class TileNode(pg.FRect):
    def __init__(self, pos):
        super().__init__(pos, (TILE_SIZE + 5,) * 2)
        self.parent = None
        self.cost = 0   # cost from initial point, i.e, g(n)
        self.distance_cost = math.inf    # cost to target, i.e, h(n)
