from collections import Counter
import re

guesses = set(re.findall(r'"([^"]+)"', open("guesses.txt").read()))
solutions = set(re.findall(r'"([^"]+)"', open("solutions.txt").read()))

_first_guess_done = False

def compute_feedback(guess, secret):
    fb = ['0'] * 5
    for i in range(5):
        if guess[i] == secret[i]:
            fb[i] = '2'
    remaining = {}
    for i in range(5):
        if fb[i] != '2':
            remaining[secret[i]] = remaining.get(secret[i], 0) + 1
    for i in range(5):
        if fb[i] == '2':
            continue
        if remaining.get(guess[i], 0) > 0:
            fb[i] = '1'
            remaining[guess[i]] -= 1
    return ''.join(fb)

def guess():
    global _first_guess_done
    if not _first_guess_done:
        _first_guess_done = True
        return "crane"
    
    if len(solutions) == 1:
        return next(iter(solutions))
    
    best_word = None
    best_expected = float('inf')
    for g in guesses:
        pattern_counts = {}
        for sol in solutions:
            fb = compute_feedback(g, sol)
            pattern_counts[fb] = pattern_counts.get(fb, 0) + 1
        expected = sum(cnt * cnt for cnt in pattern_counts.values()) / len(solutions)
        if expected < best_expected:
            best_expected = expected
            best_word = g
    return best_word

def filter(feedback, guess_word):
    global solutions
    for solution in solutions.copy():
        frequencies = Counter(solution)
        valid = True
        for i in range(5):
            num = int(feedback[i])
            if num != 2:
                continue
            if guess_word[i] != solution[i]:
                valid = False
                solutions.remove(solution)
                break
            frequencies[guess_word[i]] -= 1
        if not valid:
            continue
        for i in range(5):
            num = int(feedback[i])
            if num == 1:
                if guess_word[i] == solution[i]:
                    valid = False
                    break
                if frequencies.get(guess_word[i], 0) <= 0:
                    valid = False
                    break
                frequencies[guess_word[i]] -= 1
            elif num == 0:
                if frequencies.get(guess_word[i], 0) > 0:
                    valid = False
                    break
        if not valid:
            solutions.remove(solution)

def reset_solutions():
    global solutions, _first_guess_done
    solutions = set(re.findall(r'"([^"]+)"', open("solutions.txt").read()))
    _first_guess_done = False