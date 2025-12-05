import sys
import itertools
from functools import cache
from random import choices


COLORS = 'BGKRWYTQ'  # Blue, Green, blacK, Red, White, Yellow, Teal, Q
SECRET = None

@cache
def score(a, b):
    matches = sum(x == y for x, y in zip(a, b))
    return matches, sum(min(a.count(c), b.count(c)) for c in COLORS) - matches

allcodes = tuple(''.join(p) for p in itertools.product(COLORS, repeat=6))
responses = [(matches, ncolors) for matches in range(7)
             for ncolors in range(7 - matches)]
responses.remove((5, 1))  # +++- cannot be a valid response

@cache
def guess(S):
    if len(S) == len(allcodes):  # first
        return 'BBGGKK'
    if len(S) == 1:
        return S[0]
    # Pick a guess which minimizes the maximum number of remaining S over
    # all 14 responses.
    # The guess will result in the minimum elements S remaining in the
    # next step, regardless of what the next response actually is.
    return min(allcodes, key=lambda t: max(sum(score(s, t) == resp for s in S)
                                           for resp in responses))

def solve(verbose=False):
    S = allcodes
    for i in itertools.count(1):
        g = guess(S)
        resp = score(SECRET, g)
        if verbose:
            print("%2d %4d %s %5s %s" %
                  (i, len(S), g, g in S, '+' * resp[0] + '-' * resp[1]))
        if resp == (6, 0) or not S:
            return i
        # only keep the codes which would give the same response
        S = tuple(s for s in S if score(s, g) == resp)

def main():
    
    global SECRET    
    SECRET = ''.join(choices(COLORS, k=6))
    
    if len(SECRET) != 6 or set(SECRET) - set(COLORS):
        sys.exit("ill-formed Mastermind code: %r" % SECRET)

    guesses = solve()
    return guesses

if __name__ == '__main__':
    total = 0
    for i in range(1):
        num_guess = main()
        total += num_guess

    print(f"All feedback: {total / 1}")