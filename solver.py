from judge import Case, get_files


class Solver(Case):
    def run(self, filename):
        with open(f'Inputs/{filename}') as stream:
            self.parse_in(stream)
        with open(f'Outputs/{filename}', 'w') as stream:
            self.solve(stream)

    def solve(self, stream):
        def output(*args):
            print(*args, file=stream)

        def score_library(lib):
            reward = sum(self.book_scores[book] for book in lib.books)
            return reward / lib.signup

        for lib_id, lib in enumerate(self.libraries):
            lib.id = lib_id

        self.libraries.sort(key=score_library, reverse=True)

        output(len(self.libraries))
        for lib in self.libraries:
            output(lib.id, len(lib.books))
            books = sorted(lib.books, key=self.book_scores.__getitem__, reverse=True)
            output(*books)


if __name__ == '__main__':
    for filename in get_files('Inputs'):
        case = Solver(debug=True)
        case.run(filename)
