import random
import pytest
from puzzle.state import State, GOAL_STATE
from algorithms.bfs import BFS
from algorithms.dfs import DFS
from algorithms.a_star import AStar

APPLY = {"UP": -3, "DOWN": 3, "LEFT": -1, "RIGHT": 1}


def scramble(n, seed):
    rng = random.Random(seed)
    s = State(GOAL_STATE)
    for _ in range(n):
        s = rng.choice(s.neighbors())
    return State(s.tiles)  


def replay(initial, actions):
    t = list(initial.tiles)
    for a in actions:
        b = t.index(0)
        n = b + APPLY[a]
        t[b], t[n] = t[n], t[b]
    return tuple(t)


def test_neighbors_counts():
    assert len(State((0, 1, 2, 3, 4, 5, 6, 7, 8)).neighbors()) == 2
    assert len(State((1, 0, 2, 3, 4, 5, 6, 7, 8)).neighbors()) == 3
    assert len(State((1, 2, 3, 4, 0, 5, 6, 7, 8)).neighbors()) == 4


def test_path_and_actions():
    init = State((1, 2, 3, 4, 5, 6, 7, 0, 8))
    r = AStar().search(init)
    assert r.actions == ["RIGHT"]
    assert [s.tiles for s in r.solution.path()] == [init.tiles, GOAL_STATE]


def test_goal_is_initial():
    for alg in (BFS(), DFS(), AStar()):
        r = alg.search(State(GOAL_STATE))
        assert r.found and r.path_cost == 0 and r.actions == []


@pytest.mark.parametrize("seed", range(10))
def test_optimal_and_valid(seed):
    init = scramble(18, seed)
    b, a = BFS().search(init), AStar().search(init)
    assert b.found and a.found
    assert b.path_cost == a.path_cost == b.depth == a.depth
    assert replay(init, b.actions) == GOAL_STATE
    assert replay(init, a.actions) == GOAL_STATE
    assert a.nodes_expanded <= b.nodes_expanded


@pytest.mark.parametrize("seed", range(5))
def test_dfs_finds_valid(seed):
    init = scramble(12, seed)
    r = DFS().search(init)
    assert r.found and r.path_cost <= 50
    assert replay(init, r.actions) == GOAL_STATE


def test_unsolvable():
    init = State((8, 1, 2, 3, 4, 5, 6, 7, 0)) 
    for alg in (BFS(), AStar()):
        assert not alg.search(init).found
