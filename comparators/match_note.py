from comparators import ComparatorBase
from common.note_repr import Note


class MatchNote(ComparatorBase):
    def compare(self, previous: Note, current: Note) -> bool:
        return previous.note_index == current.note_index
