from __future__ import print_function
from decimal import Decimal
import matplotlib.pyplot as plt


class AStarGraph(object):
    # Define a class board like grid with two barriers

    def __init__(self, walls):
        self.barriers = []
        for wall in walls:
            self.barriers.append(wall)

    def heuristic(self, start, goal):
        # Use Chebyshev distance heuristic if we can move one square either
        # adjacent or diagonal
        D = 1
        dx = abs(start[0] - goal[0])
        dy = abs(start[1] - goal[1])
        return D * (dx + dy)

    def get_vertex_neighbours(self, pos):
        n = []
        # Moves allow link a chess king
        # for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, 1), (1, -1), (-1, -1)]:
        for dx, dy in [(100, 0), (-100, 0), (0, 100), (0, -100)]:
            x2 = pos[0] + dx
            y2 = pos[1] + dy
            n.append((x2, y2))
        return n

    def move_cost(self, a, b):
        for barrier in self.barriers:
            if b in barrier:
                return 10000  # Extremely high cost to enter barrier squares
        return 1  # Normal movement cost


def AStarSearch(start, end, graph, display=False):
    G = {}  # Actual movement cost to each position from the start position
    F = {}  # Estimated movement cost of start to end going via this position

    # Initialize starting values
    G[start] = 0
    F[start] = graph.heuristic(start, end)

    closedVertices = set()
    openVertices = set([start])
    cameFrom = {}

    while len(openVertices) > 0:
        # Get the vertex in the open list with the lowest F score
        current = None
        currentFscore = None
        for pos in openVertices:
            if current is None or F[pos] < currentFscore:
                currentFscore = F[pos]
                current = pos

        # Check if we have reached the goal
        if current == end:
            # Retrace our route backward
            path = [current]
            while current in cameFrom:
                current = cameFrom[current]
                path.append(current)
            path.reverse()
            prevTarget = path[0]
            iterResult = iter(path)
            next(iterResult)
            state = 0
            combinedResults = list()

            delta = 0
            for target in iterResult:
                if Decimal(target[0]) - Decimal(prevTarget[0]) == 0 and state is 0:
                    state = 0
                    delta += target[1] - prevTarget[1]
                elif Decimal(target[0]) - Decimal(prevTarget[0]) == 0 and state is 1:
                    state = 0
                    combinedResults.append((delta, 0))
                    delta = 0
                    delta += target[1] - prevTarget[1]
                elif Decimal(target[1]) - Decimal(prevTarget[1]) == 0 and state is 1:
                    state = 1
                    delta += target[0] - prevTarget[0]
                elif Decimal(target[1]) - Decimal(prevTarget[1]) == 0 and state is 0:
                    state = 1
                    combinedResults.append((0, delta))
                    delta = 0
                    delta += target[0] - prevTarget[0]
                prevTarget = target

            if state is 0:
                combinedResults.append((0, delta))
            elif state is 1:
                combinedResults.append((delta, 0))

            if display:
                plt.plot([v[0] for v in path], [v[1] for v in path])
                for barrier in graph.barriers:
                    plt.plot([v[0] for v in barrier], [v[1] for v in barrier])
                plt.xlim(-100, 800)
                plt.ylim(-100, 800)
                plt.savefig("chart.png", bbox_inches='tight')
                plt.show()

            return combinedResults, F[end], path  # Done!

        # Mark the current vertex as closed
        openVertices.remove(current)
        closedVertices.add(current)

        # Update scores for vertices near the current position
        for neighbour in graph.get_vertex_neighbours(current):
            if neighbour in closedVertices:
                continue  # We have already processed this node exhaustively
            candidateG = G[current] + graph.move_cost(current, neighbour)

            if neighbour not in openVertices:
                openVertices.add(neighbour)  # Discovered a new vertex
            elif candidateG >= G[neighbour]:
                continue  # This G score is worse than previously found

            # Adopt this G score
            cameFrom[neighbour] = current
            G[neighbour] = candidateG
            H = graph.heuristic(neighbour, end)
            F[neighbour] = G[neighbour] + H

    raise RuntimeError("A* failed to find a solution")


if __name__ == "__main__":
    barriers = list()
    barrierA = list()
    barrierB = list()
    barrierC = list()
    for i in range(300):
        barrierA.append((0 * 100 + i, 500))
    for i in range(300):
        barrierB.append((400, 3 * 100 + i))
    for i in range(700):
        barrierC.append((2 * 100 + i, 600))

    barriers.append(barrierA)
    barriers.append(barrierB)
    barriers.append(barrierC)
    graph = AStarGraph(barriers)

    start = (350,500)
    end = (700,700)
    distances, cost, result = AStarSearch(start, end, graph, True)

    print("route", distances)
    print("cost", cost)
