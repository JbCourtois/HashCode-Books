import bisect
import json
from glob import glob


def read_int(stream):
    return int(stream.readline())


def read_int_array(stream):
    return [int(x) for x in stream.readline().split()]


class Library:
    @classmethod
    def from_input(cls, stream):
        self = cls()
        _, self.signup, self.flow = read_int_array(stream)
        self.books = set(read_int_array(stream))

        return self


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
        _, nb_libraries, self.limit = read_int_array(stream)
        self.book_scores = read_int_array(stream)
        self.libraries = [Library.from_input(stream) for _ in range(nb_libraries)]

    def parse_out(self, stream):
        books_delivered = set()
        nb_libraries = read_int(stream)

        day = 0

        for _ in range(nb_libraries):
            lib_id, _ = read_int_array(stream)
            library = self.libraries[lib_id]
            day += library.signup
            if day >= self.limit:
                break

            can_scan = (self.limit - day) * library.flow
            books = library.books.intersection(read_int_array(stream)[:can_scan])

            self.debug(f'Scanned books {books} from library {lib_id}.')
            books_delivered.update(books)

        total_score = sum(self.book_scores[book_id] for book_id in books_delivered)
        self.debug('Overall scanned books:', books_delivered)
        self.debug('Total score:', total_score)

        self.score = total_score


def get_files(foldername):
    return set(filename.rpartition('/')[-1] for filename in glob(f'{foldername}/*.txt'))


if __name__ == '__main__':
    score = 0
    filenames = get_files('Inputs').intersection(get_files('Outputs'))
    for filename in filenames:
        case = Case()
        case.run(filename)
        score += case.score

    print('Submission score:', score)

    with open('rankings.json') as file:
        rankings = json.load(file)

    ranks, scores = zip(*rankings)
    index = bisect.bisect_left(scores, score)
    print("Rank:", ranks[index - 1])
