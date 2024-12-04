from typing import List
from models.Note import Note


class NoteSearch:
    @staticmethod
    def search_notes(notes: List[Note], query: str) -> List[Note]:
        query = query.lower()
        results = []

        for note in notes:
            if (query in note.title.lower() or
                    query in note.text.lower() or
                    any(query in tag.lower() for tag in note.tags)):
                results.append(note)

        return results

    @staticmethod
    def filter_by_tag(notes: List[Note], tag: str) -> List[Note]:
        return [note for note in notes if tag in note.tags]