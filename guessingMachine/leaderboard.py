


class GamerInfo:
    def __init__(self, name, rounds, time, total_sec):
        self.name = name
        self.rounds = rounds
        self.time = time
        self.total_sec = total_sec

    def __repr__(self):
        return repr((self.name, self.rounds, self.time, self.total_sec))

    def get_record(self):
        return self.name + "\t" + str(self.rounds) + "\t" + self.time + "\n"

    def get_rounds(self):
        return self.rounds

    def get_total_sec(self):
        return self.total_sec
