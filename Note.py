from typing import List, Optional

class Note:
    _all_notes: List['Note'] = []

    def __init__(self, title: str, text: str = ""):
        self.title: str = title
        self.text: str = text
        self.parents: List['Note'] = []
        self.neighbors: List['Note'] = []
        self.children: List['Note'] = []
        Note._all_notes.append(self)

    def add_parent(self, parent: 'Note') -> None:
        if parent not in self.parents:
            self.parents.append(parent)
            parent.children.append(self)

    def add_neighbor(self, neighbor: 'Note') -> None:
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)
            neighbor.neighbors.append(self)

    def add_child(self, child: 'Note') -> None:
        if child not in self.children:
            self.children.append(child)
            child.parents.append(self)

    @classmethod
    def get_all_notes(cls) -> List['Note']:
        return cls._all_notes

    def __repr__(self) -> str:
        return f"Note(title='{self.title}')"
