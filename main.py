from typing import List

import argh

# deserialize csv into array
# layout [note-> array of notes, note1 -> array of notes etc...]
import comparators
from common.note_repr import Note


def deserialize(contents: List[str]) -> List[List[Note]]:
    note_array = [[] for _ in range(88)]
    for row in contents:
        if row.startswith("sep=,"):
            continue
        [duration, velocity, note, time_start_delta] = [int(x) for x in row.split(',')]
        note_array[note] += [Note(note, duration, velocity, time_start_delta)]
    return note_array


# iterate over each individual note
# iterate over each set in the note
# check if previous set end where current set begins
# if yes merge the sets
def merge(note_array: List[List[Note]], comps: List[comparators.ComparatorBase]) -> List[List[Note]]:
    ret = [[] for note in note_array]
    for i,note in enumerate(note_array):
        if len(note) > 0:
            ret[i] = [note[0]]

    indices = [0 for _ in note_array]

    for note in note_array:
        if len(note) > 0:
            for index in range(1, len(note)):
                current_note = note[0].note_index
                return_index = indices[current_note]

                do_merge = all([comp.compare(note[index - 1], note[index]) for comp in comps])

                if do_merge:
                    ret[current_note][return_index].duration += note[index].duration
                else:
                    ret[current_note] += [note[index]]
                    indices[current_note] = return_index + 1

    return ret


# save output array
def serialize(note_array: List[List[Note]]) -> str:
    ret = "sep=,\n"
    indices = [0 for _ in note_array]
    min_element = 0

    while min_element is not None:
        min_element = None
        for idx, note in enumerate(note_array):
            if indices[idx] >= len(note):
                continue

            candidate = note[indices[idx]]
            if min_element is not None:
                if candidate.time_start_delta < min_element.time_start_delta:
                    min_element = candidate
            else:
                min_element = candidate

        if min_element is not None:
            indices[min_element.note_index] += 1
            ret += f"{min_element.duration},{min_element.velocity},{min_element.note_index},{min_element.time_start_delta}\n"

    return ret


def run(filename: str, comps: str):
    # prepare array
    with open(filename) as input_file:
        note_array = deserialize(input_file.readlines())

    # create comparators
    comp_instances = [T() for k, T in comparators.comparators.items() if k in comps.split(',')]

    # merge
    output = merge(note_array, comp_instances)
    # serialize

    with open(filename + ".merged.csv", "w") as output_file:
        output_file.write(serialize(output))


def list_comparators():
    print(comparators.comparators.keys())


if __name__ == "__main__":
    argh.dispatch_commands([run, list_comparators])
