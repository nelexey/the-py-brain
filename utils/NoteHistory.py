from datetime import datetime
from typing import List, Dict, Any


class NoteHistory:
    def __init__(self):
        self.history: List[Dict[str, Any]] = []

    def add_change(self, note_title: str, change_type: str, details: str) -> None:
        self.history.append({
            'timestamp': datetime.now().isoformat(),
            'note_title': note_title,
            'change_type': change_type,
            'details': details
        })

    def get_note_history(self, note_title: str) -> List[Dict[str, Any]]:
        return [h for h in self.history if h['note_title'] == note_title]