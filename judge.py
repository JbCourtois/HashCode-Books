import bisect
from collections import defaultdict
import json
from glob import glob


def read_int(stream):
    return int(stream.readline())


def read_int_array(stream):
    return [int(x) for x in stream.readline().split()]


class InvalidSubmissionError(ValueError):
    pass


class Server:
    @classmethod
    def from_input(cls, stream):
        self = cls()
        self.size, self.capacity = read_int_array(stream)
        return self


class Row:
    def __init__(self):
        self.blocks = {}  # slot -> reason of block
        self.capacities = defaultdict(int)  # pool -> sum of capacities


class Case:
    def __init__(self, debug=False):
        self.is_debug = debug
        self.score = 0

    def debug(self, *args, **kwargs):
        if self.is_debug:
            print(*args, **kwargs)

    def run(self, filename):
        FILL_WIDTH = 50
        self.debug(f' Case: {filename} '.center(50, '-'))
        try:
            with open(f'Inputs/{filename}') as stream:
                self.parse_in(stream)
            with open(f'Outputs/{filename}') as stream:
                self.parse_out(stream)
        except Exception:
            if self.is_debug:
                raise
        self.debug('-' * FILL_WIDTH)

    def parse_in(self, stream):
        nb_rows, self.nb_slots, nb_x, self.nb_pools, self.nb_servers = read_int_array(stream)
        self.rows = [Row() for _ in range(nb_rows)]

        # Forbidden slots
        for _ in range(nb_x):
            block_row, block_slot = read_int_array(stream)
            self.rows[block_row].blocks[block_slot] = -1

        # Servers
        self.servers = [Server.from_input(stream) for _ in range(self.nb_servers)]

    def parse_out(self, stream):
        for server_id in range(self.nb_servers):
            raw = stream.readline().rstrip()
            if raw == 'x':
                continue

            server = self.servers[server_id]
            row_id, slot_id, pool_id = [int(x) for x in raw.split()]

            try:
                try:
                    row = self.rows[row_id]
                except IndexError:
                    raise InvalidSubmissionError(f'Row {row_id} is out of bounds')

                if slot_id < 0 or slot_id + server.size > self.nb_slots:
                    raise InvalidSubmissionError('Out of bounds')

                for _ in range(server.size):
                    if (reason := row.blocks.get(slot_id)) is not None:
                        if reason == -1:
                            raise InvalidSubmissionError('Forbidden slot')
                        else:
                            raise InvalidSubmissionError(
                                f'Slot already oppupied by server {reason}')

                    row.blocks[slot_id] = server_id
                    slot_id += 1
            except Exception as exc:
                raise InvalidSubmissionError(
                    f'Cannot place server {server_id} at position ({row_id}, {slot_id}): {exc}'
                ) from exc

            row.capacities[pool_id] += server.capacity

        # Score
        self.score = min(self.get_score(pool_id) for pool_id in range(self.nb_pools))

    def get_score(self, pool_id):
        capacities = [row.capacities[pool_id] for row in self.rows]
        return sum(capacities) - max(capacities)


def get_files(foldername):
    return set(filename.rpartition('/')[-1] for filename in glob(f'{foldername}/*.txt'))


if __name__ == '__main__':
    score = 0
    filenames = get_files('Inputs').intersection(get_files('Outputs'))
    for filename in filenames:
        case = Case(debug=True)
        case.run(filename)
        score += case.score

    print('Submission score:', score)

    with open('rankings.json') as file:
        rankings = json.load(file)

    ranks, scores = zip(*rankings)
    index = bisect.bisect_left(scores, score)
    print("Rank:", ranks[index - 1])
