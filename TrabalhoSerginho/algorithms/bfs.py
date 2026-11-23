from collections import deque
from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult


class BFS(BaseSearch):
    """Busca em Largura (graph search com teste de objetivo na geração).

    Completa e ótima (custo uniforme = 1 por movimento).
    """

    def search(self, initial: State) -> SearchResult:
        generated = 1
        expanded = 0
        max_frontier = 1

        if initial.is_goal:
            return SearchResult(initial, expanded, generated, max_frontier, initial.cost)

        frontier = deque([initial])
        visited = {initial.tiles}  

        while frontier:
            node = frontier.popleft()
            expanded += 1

            for child in node.neighbors():
                if child.tiles in visited:
                    continue
                generated += 1
                if child.is_goal:
                    return SearchResult(child, expanded, generated, max_frontier, child.cost)
                visited.add(child.tiles)
                frontier.append(child)
                max_frontier = max(max_frontier, len(frontier))

        return SearchResult(None, expanded, generated, max_frontier, 0)
