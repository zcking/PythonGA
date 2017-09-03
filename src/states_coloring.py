import datetime
import csv


def load_data(file_name):
    '''Expectes AA,BB;CC;DD;... where AA is state and BB, CC, DD, ... are the adjacent states to AA'''
    with open(file_name, mode='r') as fin:
        reader = csv.reader(fin)
        lookup = {row[0]: row[1].split(';') for row in reader if row}
    return lookup


class Rule(object):
    node = None
    adjacent = None

    def __init__(self, node, adjacent):
        if node < adjacent:
            node, adjacent = adjacent, node
        self.node = node
        self.adjacent = adjacent

    def __eq__(self, other):
        return self.node == other.node and self.adjacent == other.adjacent

    def __hash__(self):
        return hash(self.node) * 397 ^ hash(self.adjacent)

    def __str__(self):
        return '{node} -> {adj}'.format(
            node=self.node,
            adj=self.adjacent
        )

    def IsValid(self, genes, node_index_lookup):
        index = node_index_lookup[self.node]
        adjacent_state_index = node_index_lookup[self.adjacent]
        return genes[index] != genes[adjacent_state_index]


def build_rules(items):
    rules_added = {}

    for state, adjacent in items.items():
        for adjacent_state in adjacent:
            if adjacent_state == '':
                continue
            rule = Rule(node=state, adjacent=adjacent_state)
            if rule in rules_added:
                rules_added[rule] += 1
            else:
                rules_added[rule] = 1

    # Sanity check - if A is next to B then B should show it is next to A
    for k, v in rules_added.items():
        assert v == 2, 'rule {0} is not bidirectional'.format(k)

    return rules_added.keys()


def display(candidate, start_time):
    time_diff = datetime.datetime.now() - start_time
    print('{genes}\t{fitness}\t{timing}'.format(
        genes=''.join(map(str, candidate.genes)),
        fitness=candidate.fitness,
        timing=str(time_diff)
    ))


def get_fitness(genes, rules, state_index_lookup):
    rules_that_pass = sum(1 for rule in rules if rule.IsValid(genes, state_index_lookup))
    return rules_that_pass