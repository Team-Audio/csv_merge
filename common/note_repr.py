class Note:
    def __init__(self, note_index, duration, velocity, time_start_delta):
        self.duration = duration
        self.velocity = velocity
        self.time_start_delta = time_start_delta
        self.note_index = note_index
