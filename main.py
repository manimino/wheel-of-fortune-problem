from typing import *

from collections import Counter

from annoy import AnnoyIndex  # pip install annoy


"""
Find the Wheel of Fortune answer containing the closest letter counts to your query, 
using approximate nearest neighbors.
"""

N_LETTERS = 26


def get_letter_counts(answer: str) -> Tuple[int]:
    counter = Counter([c for c in answer if c.isalnum()])  # convert to letter frequencies {a: 2, b:1, d:4 ...}
    letter_counts = tuple(counter.get(c, 0) for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ')  # just the numbers, (2, 1, 0, 4...)
    return letter_counts


def read_input() -> Dict[tuple, List[str]]:
    """
    Reads in the file containing all Wheel of Fortune answers. Returns as a dict keyed on letter counts.

    Example return value: {
        (1, 0, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 1, 0, 2, 3, 0, 0, 0, 0, 0, 1, 0): ['A SCARY SPIDER'],
        (0, 0, 0, 0, 3, 0, 0, 0, 2, 0, 1, 1, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0): ['KEY LIME PIE'],
        (0, 0, 1, 1, 2, 0, 0, 0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0): ['DELI CORNER', 'CORNER DELI']
    }
    """
    letter_counts_to_answers = {}
    with open('wheel_of_fortune.txt') as fh:
        for line in fh.readlines():
            answer = line.strip().upper()
            letter_counts = get_letter_counts(answer)
            if letter_counts in letter_counts_to_answers:
                letter_counts_to_answers[letter_counts].append(answer)
            else:
                letter_counts_to_answers[letter_counts] = [answer]

    return letter_counts_to_answers


def build_index(letter_counts_to_answers: Dict[tuple, List[str]]) -> AnnoyIndex:
    idx = AnnoyIndex(N_LETTERS, 'manhattan')
    for i, letter_count_vector in enumerate(letter_counts_to_answers.keys()):
        idx.add_item(i, letter_count_vector)

    idx.build(10) # 10 trees
    return idx


def vec_dist(query_vec: Tuple[int], result_vec: Tuple[int]):
    return sum(abs(query_vec[i] - result_vec[i]) for i in range(N_LETTERS))


def main():
    letter_counts_to_answers = read_input()
    idx = build_index(letter_counts_to_answers)

    query = 'SNAKES ON A PLANE'
    query_vec = get_letter_counts(query)
    print('Query\n=====')
    print(query)
    print(query_vec)

    print('\nResults\n=======')
    neighbor_ids = idx.get_nns_by_vector(query_vec, 10)
    for n in neighbor_ids:
        vec = idx.get_item_vector(n)  # list of floats, can't use as dict key
        r_vec = tuple(int(i) for i in vec)
        print(letter_counts_to_answers[r_vec])
        print(r_vec, 'distance:', vec_dist(query_vec, r_vec), '\n')


if __name__ == '__main__':
    main()