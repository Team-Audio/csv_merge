from comparators import ComparatorBase
from common.note_repr import Note


class MatchVelocity(ComparatorBase):
    def compare(self, previous: Note, current: Note) -> bool:
        return previous.velocity == current.velocity
