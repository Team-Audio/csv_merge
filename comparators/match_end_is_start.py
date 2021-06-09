from comparators import ComparatorBase
from common.note_repr import Note


class MatchEndIsStart(ComparatorBase):
    def compare(self, previous: Note, current: Note) -> bool:
        return previous.time_start_delta + previous.duration == current.time_start_delta
