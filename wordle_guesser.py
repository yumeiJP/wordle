from collections import Counter
import re

guesses = set(re.findall(r'"([^"]+)"', open("guesses.txt").read()))
solutions = set(re.findall(r'"([^"]+)"', open("solutions.txt").read()))
round = 0

def guess():
    best_score, best_word = 0, ""
    for guess in solutions:
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
            if guess in solutions:
                score += 10000
        if score > best_score:
            best_score = score
            best_word = guess
    return best_word

def filter(feedback, guess):
    for solution in solutions.copy():
        frequencies = Counter(solution)
        valid = True
        #green
        for i in range(5):
            num = feedback[i]
            num = int(num)

            if num != 2: continue

            if guess[i] != solution[i]:
                valid = False
                solutions.remove(solution)
                break
            frequencies[guess[i]] -= 1
        
        if not valid: continue

        #yellow and gray
        for i in range(5):
            num = feedback[i]
            num = int(num)

            if num == 1:
                if guess[i] == solution[i]:
                    valid = False
                    break
                    
                if frequencies.get(guess[i], 0) <= 0:
                    valid = False
                    break

                frequencies[guess[i]] -= 1
            
            if num == 0:
                if frequencies.get(guess[i],0) > 0:
                    valid  = False
                    break
        
        if not valid:
            solutions.remove(solution)

feedback = ""
while feedback != "22222" and round < 6:
    if round == 0:
        word = "saree"
    else:
        word = guess()
    print(word)
    guesses.remove(word)
    feedback = input("feedback?")
    user_word_input = input("word used? empty for provided guess")
    if user_word_input:
        word = user_word_input
    filter(feedback,word)
    print(solutions)
    round += 1