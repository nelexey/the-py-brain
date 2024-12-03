import json
from datetime import datetime
from typing import List, Dict, Any
from .Note import Note


class NoteState:
    def __init__(self):
        self.filename = "notes.json"

    def save_notes(self, notes: List[Note]) -> None:
        note_data = []
        for note in notes:
            note_dict = {
                'title': note.title,
                'text': note.text,
                'parents': [p.title for p in note.parents],
                'children': [c.title for c in note.children],
                'neighbors': [n.title for n in note.neighbors],
                'tags': note.tags,
                'created_at': note.created_at,
                'modified_at': note.modified_at
            }
            note_data.append(note_dict)

        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(note_data, f, ensure_ascii=False, indent=2)

    def load_notes(self) -> List[Note]:
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                note_data = json.load(f)

            title_to_note = {}
            for data in note_data:
                note = Note(data['title'], data['text'])
                note.tags = data.get('tags', [])
                note.created_at = data.get('created_at')
                note.modified_at = data.get('modified_at')
                title_to_note[data['title']] = note

            for data in note_data:
                note = title_to_note[data['title']]
                for parent_title in data['parents']:
                    if parent_title in title_to_note:
                        note.add_parent(title_to_note[parent_title])
                for child_title in data['children']:
                    if child_title in title_to_note:
                        note.add_child(title_to_note[child_title])
                for neighbor_title in data['neighbors']:
                    if neighbor_title in title_to_note:
                        note.add_neighbor(title_to_note[neighbor_title])

            return list(title_to_note.values())
        except FileNotFoundError:
            return []