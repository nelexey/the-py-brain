from collections import Counter
from typing import Dict, List, Any
from models.Note import Note


class NoteStats:
    @staticmethod
    def get_note_stats(notes: List[Note]) -> Dict[str, Any]:
        stats = {
            'total_notes': len(notes),
            'total_connections': sum(len(n.parents) + len(n.children) + len(n.neighbors) for n in notes),
            'avg_connections_per_note': 0,
            'most_connected_notes': [],
            'isolated_notes': [],
            'tag_distribution': Counter(),
            'depth_distribution': Counter()
        }

        if stats['total_notes'] > 0:
            stats['avg_connections_per_note'] = stats['total_connections'] / stats['total_notes']

        connection_counts = [(n, len(n.parents) + len(n.children) + len(n.neighbors)) for n in notes]
        connection_counts.sort(key=lambda x: x[1], reverse=True)

        stats['most_connected_notes'] = connection_counts[:5]
        stats['isolated_notes'] = [n for n, count in connection_counts if count == 0]

        for note in notes:
            for tag in note.tags:
                stats['tag_distribution'][tag] += 1

        return stats