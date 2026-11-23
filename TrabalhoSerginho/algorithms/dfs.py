from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):
    """Busca em Profundidade com limite de profundidade (iterativa, com pilha).

    Sem limite, a DFS pode descer indefinidamente; por isso `depth_limit`.
    Um estado só é reexpandido se for alcançado por um caminho mais raso do
    que o melhor já visto (evita ciclos sem perder soluções dentro do limite).
    Não garante solução ótima.
    """

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        generated = 1
        expanded = 0
        max_frontier = 1

        stack = [initial]
        best_depth = {initial.tiles: 0}

        while stack:
            node = stack.pop()

            if best_depth.get(node.tiles, node.cost) < node.cost:
                continue

            if node.is_goal:
                return SearchResult(node, expanded, generated, max_frontier, node.cost)

            if node.cost >= self.depth_limit:
                continue

            expanded += 1
            
            for child in reversed(node.neighbors()):
                seen = best_depth.get(child.tiles)
                if seen is not None and seen <= child.cost:
                    continue
                best_depth[child.tiles] = child.cost
                generated += 1
                stack.append(child)
            max_frontier = max(max_frontier, len(stack))

        return SearchResult(None, expanded, generated, max_frontier, 0)
