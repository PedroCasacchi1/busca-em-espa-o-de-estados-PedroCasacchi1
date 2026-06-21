import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import GOAL_STATE, State
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        goal_positions = {
            tile: divmod(index, 3)
            for index, tile in enumerate(GOAL_STATE)
        }

        distance = 0
        for index, tile in enumerate(state.tiles):
            if tile == 0:
                continue

            row, col = divmod(index, 3)
            goal_row, goal_col = goal_positions[tile]
            distance += abs(row - goal_row) + abs(col - goal_col)

        return distance

    def search(self, initial: State) -> SearchResult:
        frontier = []
        counter = 0
        heapq.heappush(
            frontier,
            (initial.cost + self.heuristic(initial), counter, initial),
        )

        best_cost = {initial.tiles: initial.cost}
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while frontier:
            _, _, current = heapq.heappop(frontier)

            if current.cost > best_cost[current.tiles]:
                continue

            if current.is_goal:
                return SearchResult(
                    solution=current,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=len(current.path()) - 1,
                )

            nodes_expanded += 1
            for neighbor in current.neighbors():
                previous_cost = best_cost.get(neighbor.tiles)
                if previous_cost is not None and previous_cost <= neighbor.cost:
                    continue

                best_cost[neighbor.tiles] = neighbor.cost
                counter += 1
                priority = neighbor.cost + self.heuristic(neighbor)
                heapq.heappush(frontier, (priority, counter, neighbor))
                nodes_generated += 1

            max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
        )
