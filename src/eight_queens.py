import datetime


class Board(object):
    def __init__(self, genes, size):
        board = [['.'] * size for _ in range(size)]
        for index in range(0, len(genes), 2):
            row = genes[index]
            column = genes[index + 1]
            board[column][row] = 'Q'
        self._board = board

    def print(self):
        for i in reversed(range(len(self._board))):
            print(' '.join(self._board[i]))

    def get(self, row, column):
        return self._board[column][row]


def get_fitness(genes, size):
    board = Board(genes=genes, size=size)
    rows_with_queens = set()
    cols_with_queens = set()
    northeast_diagonal_with_queens = set()
    southeast_diagonal_with_queens = set()

    for row in range(size):
        for col in range(size):
            if board.get(row, col) == 'Q':
                rows_with_queens.add(row)
                cols_with_queens.add(col)
                northeast_diagonal_with_queens.add(row + col)
                southeast_diagonal_with_queens.add(size - 1 - row + col)

    total = size - len(rows_with_queens) \
        + size - len(cols_with_queens) \
        + size - len(northeast_diagonal_with_queens) \
        + size - len(southeast_diagonal_with_queens)

    return Fitness(total=total)


def display(candidate, start_time, size):
    time_diff = datetime.datetime.now() - start_time
    board = Board(genes=candidate.genes, size=size)
    board.print()
    print('{genes}\t- {fitness}\t{timing}'.format(
        genes=' '.join(map(str, candidate.genes)),
        fitness=candidate.fitness,
        timing=str(time_diff)
    ))


class Fitness(object):
    total = None

    def __init__(self, total):
        self.total = total

    def __gt__(self, other):
        return self.total < other.total

    def __str__(self):
        return '{tot}'.format(tot=self.total)