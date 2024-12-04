from datetime import datetime
from typing import List, Optional


class Note:
    _all_notes: List['Note'] = []

    def __init__(self, title: str, text: str = ""):
        self.title: str = title
        self.text: str = text
        self.parents: List['Note'] = []
        self.neighbors: List['Note'] = []
        self.children: List['Note'] = []
        self.tags: List[str] = []
        self.created_at: str = datetime.now().isoformat()
        self.modified_at: str = self.created_at
        Note._all_notes.append(self)

    def add_parent(self, parent: 'Note') -> None:
        if parent not in self.parents:
            self.parents.append(parent)
            parent.children.append(self)
            self.modified_at = datetime.now().isoformat()

    def add_neighbor(self, neighbor: 'Note') -> None:
        if neighbor not in self.neighbors:
            self.neighbors.append(neighbor)
            neighbor.neighbors.append(self)
            self.modified_at = datetime.now().isoformat()

    def add_child(self, child: 'Note') -> None:
        if child not in self.children:
            self.children.append(child)
            child.parents.append(self)
            self.modified_at = datetime.now().isoformat()

    def add_tag(self, tag: str) -> None:
        if tag not in self.tags:
            self.tags.append(tag)
            self.modified_at = datetime.now().isoformat()

    def remove_tag(self, tag: str) -> None:
        if tag in self.tags:
            self.tags.remove(tag)
            self.modified_at = datetime.now().isoformat()

    @classmethod
    def get_all_notes(cls) -> List['Note']:
        return cls._all_notes

    def __repr__(self) -> str:
        return f"Note(title='{self.title}', tags={self.tags})"
