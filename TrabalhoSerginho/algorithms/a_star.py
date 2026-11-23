import heapq
from itertools import count
from puzzle.base_search import BaseSearch
from puzzle.state import State, GOAL_STATE
from puzzle.result import SearchResult

_GOAL_POS = {tile: divmod(i, 3) for i, tile in enumerate(GOAL_STATE)}


class AStar(BaseSearch):
    """A* com f(n) = g(n) + h(n) e heurística de distância de Manhattan.

    Manhattan é admissível e consistente, logo o A* retorna solução ótima.
    """

    def heuristic(self, state: State) -> int:
        """Soma das distâncias de Manhattan de cada peça (exceto o vazio) até a posição final."""
        total = 0
        for i, tile in enumerate(state.tiles):
            if tile == 0:
                continue
            r, c = divmod(i, 3)
            gr, gc = _GOAL_POS[tile]
            total += abs(r - gr) + abs(c - gc)
        return total

    def search(self, initial: State) -> SearchResult:
        generated = 1
        expanded = 0
        tie = count()  

        frontier = [(self.heuristic(initial), next(tie), initial)]
        best_g = {initial.tiles: initial.cost}
        max_frontier = 1

        while frontier:
            _, _, node = heapq.heappop(frontier)

            
            if node.cost > best_g.get(node.tiles, node.cost):
                continue

            if node.is_goal:
                return SearchResult(node, expanded, generated, max_frontier, node.cost)

            expanded += 1
            for child in node.neighbors():
                g = best_g.get(child.tiles)
                if g is not None and g <= child.cost:
                    continue
                best_g[child.tiles] = child.cost
                generated += 1
                heapq.heappush(frontier, (child.cost + self.heuristic(child), next(tie), child))
            max_frontier = max(max_frontier, len(frontier))

        return SearchResult(None, expanded, generated, max_frontier, 0)
