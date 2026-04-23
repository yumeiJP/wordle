guesses = set()
solutions = set()
round = 0

def guess():
    best_score, best_word = 0, ""
    for guess in guesses:
        score = 0
        for solution in solutions:
            green, yellow = 0,0
            for i in range(5):
                if guess[i]==solution[i]:
                    green += 1
                for j in range(5):
                    if i == j: continue
                    if guess[i] == solution[j]:
                        yellow += 1
            score += green + yellow/4
        if score > best_score:
            best_score = score
            best_word = guess
    return best_word

def filter(feedback, guess):
    for i in range(5):
        num = feedback[i]
        num = int(num)
        
        for solution in solutions:
            if num == 2:
                if guess[i] != solution[i]:
                    solutions.remove(solution)
            if num == 1:
                if guess[i] == solution[i]:
                    solutions.remove(solution)
                    break

                found = False

                for j in range(5):
                    if i == j: continue
                    if guess[i] == solution[j]:
                        found = True
                        break
                if not found:
                    solutions.remove(solution)
            if num == 0:
                for j in range(5):
                    if guess[i] == solution[j]:
                        solutions.remove(solution)
                        break

feedback = ""
while feedback != "22222" and round < 6:
    word = guess()
    print(word)
    feedback = input()
    filter(feedback,word)
    round += 1