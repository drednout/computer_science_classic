from __future__ import annotations
from typing import Generic, List, TypeVar, Optional

T = TypeVar('T')


class Stack(Generic[T]):
    def __init__(self) -> None:
        self._container: List[T] = []

    def push(self, elem: T) -> None:
        return self._container.append(elem)

    def pop(self) -> T:
        return self._container.pop()

    @property
    def empty(self) -> bool:
        return not self._container

    def __repr__(self) -> str:
        return "Stack(" + repr(self._container) + ")"



class Node(Generic[T]):
    def __init__(self, state: T, parent: Optional[Node], 
                 cost: float = 0.0, heuristic: float = 0.0):
        self.state: T = state
        self.parent: Optional[Node] = parent
        self.cost: float = cost
        self.heuristic: float = heuristic


def dfs(initial: T, is_goal_achieved: Callable[[T], bool], get_neighbours: Callable[[T], 
        List[T]]) -> Optional[Node[T]]:
    frontier: Stack[Node[T]] = Stack()
    
    frontier.push(Node(initial, None))
    explored: Set[T] = {initial}
    
    while not frontier.empty:
        current_node: Node[T] = frontier.pop()
        current_state: T = current_node.state
        if is_goal_achieved(current_state):
            return current_node

        for child in get_neighbours(current_state):
            if child in explored:
                continue
            explored.add(child)
            frontier.push(Node(child, current_node))

    return None # all cells are visited


def node_to_path(node: Node[T]) -> List[T]:
    path: List[T] = [node.state]
    while node.parent is not None:
        path.append(node.state)
        node = node.parent

    return path

