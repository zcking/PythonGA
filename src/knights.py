import random
import datetime


class Position(object):
    x = None
    y = None

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '{x},{y}'.format(x=self.x, y=self.y)

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def __hash__(self):
        return self.x * 1000 + self.y


class Board(object):
    def __init__(self, positions, width, height):
        board = [['.'] * width for _ in range(height)]

        for index in range(len(positions)):
            knight_position = positions[index]
            board[knight_position.y][knight_position.x] = 'N'
        self._board = board
        self._width = width
        self._height = height

    def print(self):
        # 0, 0 in bottom left
        for i in reversed(range(self._height)):
            print(i, '\t', ' '.join(self._board[i]))
        print(' \t', ' '.join(map(str, range(self._width))))


def get_attacks(location, board_width, board_height):
    return [i for i in set(
        Position(x + location.x, y + location.y)
        for x in [-2, -1, 1, 2] if 0 <= x + location.x < board_width
        for y in [-2, -1, 1, 2] if 0 <= y + location.y < board_height
        and abs(y) != abs(x)
    )]


def create(fn_get_random_position, expected_knights):
    genes = [fn_get_random_position() for _ in range(expected_knights)]
    return genes


def mutate(genes, board_width, board_height, all_positions, non_edge_positions):
    count = 2 if random.randint(0, 10) == 0 else 1
    while count > 0:
        count -= 1
        position_to_knight_indices = dict((p, []) for p in all_positions)
        for i, knight in enumerate(genes):
            for position in get_attacks(knight, board_width, board_height):
                position_to_knight_indices[position].append(i)

        knight_indices = set(i for i in range(len(genes)))
        unattacked = []
        for pos, indices in position_to_knight_indices.items():
            if len(indices) > 1:
                continue
            if len(indices) == 0:
                unattacked.append(pos)
                continue
            for p in indices:
                if p in knight_indices:
                    knight_indices.remove(p)

        potential_knight_positions = \
            [p for positions in
             map(lambda x: get_attacks(x, board_width, board_height), unattacked)
             for p in positions if p in non_edge_positions] if len(unattacked) > 0 else non_edge_positions
        gene_index = random.randrange(0, len(genes)) \
            if len(knight_indices) == 0 \
            else random.choice([i for i in knight_indices])
        position = random.choice(potential_knight_positions)
        genes[gene_index] = position


def display(candidate, start_time, board_width, board_height):
    time_diff = datetime.datetime.now() - start_time
    board = Board(candidate.genes, board_width, board_height)
    board.print()

    print('{genes}\n\t{fitness}\t{timing}'.format(
        genes=' '.join(map(str, candidate.genes)),
        fitness=candidate.fitness,
        timing=str(time_diff)
    ))


def get_fitness(genes, board_width, board_height):
    attacked = set(pos for kn in genes for pos in get_attacks(
        location=kn, board_width=board_width, board_height=board_height
    ))
    return len(attacked)
