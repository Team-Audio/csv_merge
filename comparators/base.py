import abc
from common.note_repr import Note


class ComparatorBase(metaclass=abc.ABCMeta):

    @abc.abstractmethod
    def compare(self, previous: Note, current: Note) -> bool:
        raise NotImplementedError("Abstract Method not implemented")
