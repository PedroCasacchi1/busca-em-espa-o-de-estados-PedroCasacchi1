from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        frontier = [initial]
        best_depth = {initial.tiles: initial.cost}
        nodes_expanded = 0
        nodes_generated = 1
        max_frontier_size = 1

        while frontier:
            current = frontier.pop()

            if current.cost > best_depth[current.tiles]:
                continue

            if current.is_goal:
                return SearchResult(
                    solution=current,
                    nodes_expanded=nodes_expanded,
                    nodes_generated=nodes_generated,
                    max_frontier_size=max_frontier_size,
                    depth=len(current.path()) - 1,
                )

            if current.cost >= self.depth_limit:
                continue

            nodes_expanded += 1
            for neighbor in current.neighbors():
                previous_depth = best_depth.get(neighbor.tiles)
                if previous_depth is not None and previous_depth <= neighbor.cost:
                    continue

                best_depth[neighbor.tiles] = neighbor.cost
                frontier.append(neighbor)
                nodes_generated += 1

            max_frontier_size = max(max_frontier_size, len(frontier))

        return SearchResult(
            solution=None,
            nodes_expanded=nodes_expanded,
            nodes_generated=nodes_generated,
            max_frontier_size=max_frontier_size,
        )
