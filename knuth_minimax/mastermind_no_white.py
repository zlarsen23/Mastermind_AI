# Modified script frrom https://github.com/ilanschnell/mastermind

import sys
import itertools
from functools import cache
from random import choices

COLORS = 'BGKRWY'  # Blue, Green, blacK, Red, White, Yellow
SECRET = None
GLOBAL_COUNTER = 0  # counts number of guesses (not score calls)



@cache
def base_score(a, b):
    matches = sum(x == y for x, y in zip(a, b))
    whites = sum(min(a.count(c), b.count(c)) for c in COLORS) - matches
    return matches, whites

def score(a, b):
    """Return (black, white), but suppress white feedback for first 3 guesses."""
    matches, whites = base_score(a, b)
    if GLOBAL_COUNTER <= 3:
        whites = 0
    return matches, whites



allcodes = tuple(''.join(p) for p in itertools.product(COLORS, repeat=4))
responses = [(matches, ncolors) for matches in range(5)
             for ncolors in range(5 - matches)]
responses.remove((3, 1))  # +++- cannot be a valid response

@cache
def guess(S):
    if len(S) == len(allcodes):
        return 'BBGG'
    if len(S) == 1:
        return S[0]
    return min(allcodes, key=lambda t: max(sum(score(s, t) == resp for s in S)
                                           for resp in responses))

def solve(verbose=False):
    global GLOBAL_COUNTER
    S = allcodes

    for i in itertools.count(1):
        GLOBAL_COUNTER = i  # count actual guesses, not score calls
        g = guess(S)
        resp = score(SECRET, g)

        if verbose:
            whites_shown = " (no whites)" if i <= 3 else ""
            print(f"{i:2d} {len(S):4d} {g} {g in S}  {'+' * resp[0] + '-' * resp[1]}{whites_shown}")

        if resp == (4, 0) or not S:
            return i

        S = tuple(s for s in S if score(s, g) == resp)

def main():
    global SECRET
    SECRET = ''.join(choices(COLORS, k=4))
    
    
    if len(SECRET) != 4 or set(SECRET) - set(COLORS):
        sys.exit(f"ill-formed Mastermind code: {SECRET!r}")

    return solve()

if __name__ == '__main__':
    total = 0
    for i in range(1000):
        GLOBAL_COUNTER = 0
        guess_count = main()
        total += guess_count

    print(f"No white (first 3 rounds): {total / 1000}")
