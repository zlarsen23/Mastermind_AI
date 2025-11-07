import sys
import unittest
from collections import Counter
from random import choices

import knuth_minimax.mastermind_original as mastermind_original


class TestMastermind(unittest.TestCase):

    def test_allcodes(self):
        a = mastermind_original.allcodes
        self.assertEqual(len(a), 6 ** 4)
        self.assertEqual(len(set(a)), 6 ** 4)

    def test_responses(self):
        self.assertEqual(len(mastermind_original.responses), 14)

    def test_score(self):
        for a, b, r in [
                ('BGGG', 'KRKR', (0, 0)),
                ('BGKR', 'YWGY', (0, 1)),
                ('YWGR', 'WYKK', (0, 2)),
                ('BGKR', 'GKRY', (0, 3)),
                ('GGBB', 'BBGG', (0, 4)),
                ('YBRK', 'BBGW', (1, 0)),
                ('BBKK', 'BKGG', (1, 1)),
                ('GBYW', 'KWYB', (1, 2)),
                ('BGKB', 'KBGB', (1, 3)),
                ('BBKB', 'BGKR', (2, 0)),
                ('BBKB', 'BBGG', (2, 0)),
                ('BBKY', 'BKGY', (2, 1)),
                ('GBKR', 'BGKR', (2, 2)),
                ('WWKR', 'WYKR', (3, 0)),
                ('BGKR', 'BGKR', (4, 0)),
        ]:
            self.assertEqual(mastermind_original.score(a, b), r)
            self.assertEqual(mastermind_original.score(b, a), r)
            self.assertTrue(r in mastermind_original.responses)

    def test_solve(self):
        mastermind_original.SECRET = ''.join(choices(mastermind_original.COLORS, k=4))
        i = mastermind_original.solve(verbose=False)
        self.assertTrue(i <= 5)


def test_all():
    stat = Counter()
    for secret in mastermind_original.allcodes:
        mastermind_original.SECRET = secret
        i = mastermind_original.solve(verbose=False)
        stat[i] += 1
        sys.stdout.write('.')
        sys.stdout.flush()
    print(stat)
    n = sum(i * n for i, n in stat.items())
    print('n:', n)
    print('average: %.2f' % (n / len(mastermind_original.allcodes)))
    print('worst: %d' % max(stat.keys()))
    assert stat == {
        1:    1,
        2:    6,
        3:   25,
        4:  239,
        5: 1025,
    }

if __name__ == '__main__':
    if len(sys.argv) > 1:
        test_all()
        sys.exit()
    unittest.main()
