import re

with open("solutions.txt", "r") as f:
    content = f.read()
all_solutions = re.findall(r'"([^"]+)"', content)

freq = [0] * 26
letters = [chr(i) for i in range(ord('a'), ord('z') + 1)]
for word in all_solutions:
    for ch in word:
        freq[ord(ch) - ord('a')] += 1

letterOrd = []
temp_freq = freq[:]
temp_letters = letters[:]
for _ in range(26):
    max_idx = temp_freq.index(max(temp_freq))
    letterOrd.append(temp_letters[max_idx])
    temp_freq.pop(max_idx)
    temp_letters.pop(max_idx)

current_solutions = all_solutions[:]

def reset_solutions():
    global current_solutions
    current_solutions = all_solutions[:]

def guess():
    # If no solutions remain, fallback to a fixed guess (should not happen in correct simulation)
    if not current_solutions:
        return "crane"
    best_score = -float('inf')
    best_word = current_solutions[0]  # default
    for word in current_solutions:
        score = 0
        seen = []
        for ch in word:
            score -= letterOrd.index(ch)
            if ch in seen:
                score -= 26
            seen.append(ch)
        if score > best_score:
            best_score = score
            best_word = word
    return best_word

def filter(feedback, guess_word):
    global current_solutions
    new_solutions = []
    for sol in current_solutions:
        valid = True
        for i in range(5):
            f = int(feedback[i])
            if f == 2:
                if guess_word[i] != sol[i]:
                    valid = False
                    break
            elif f == 1:
                if guess_word[i] not in sol or guess_word[i] == sol[i]:
                    valid = False
                    break
            else:  # f == 0
                # Naive: remove if the letter appears anywhere in the solution
                # (This is incorrect for duplicates, but matches the original friend's code)
                if guess_word[i] in sol:
                    valid = False
                    break
        if valid:
            new_solutions.append(sol)
    current_solutions = new_solutions
    # Safety: if filtering removed everything, revert to full list? No, better to keep empty.
    # The calling code will handle fallback in guess().