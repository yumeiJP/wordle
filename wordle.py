import re
import random
import wordle_solver as solver
from collections import Counter

guesses = set(re.findall(r'"([^"]+)"', open("guesses.txt").read()))
solutions = set(re.findall(r'"([^"]+)"', open("solutions.txt").read()))

def guess_input(guess, secret_answer):
    feedback = ['0']*5
    secret_answer_frequencies = Counter(secret_answer)

    #green
    for i in range(5):
        if guess[i] == secret_answer[i]:
            feedback[i] = "2"
            secret_answer_frequencies[guess[i]] -= 1
    
    for i in range(5):
        if feedback[i] == "2":
            continue
        if secret_answer_frequencies.get(guess[i],0) > 0:
            feedback[i] = "1"
            secret_answer_frequencies[guess[i]] -= 1
    
    return "".join(feedback)

def main():
    secret_answer = random.choice(list(solutions))
    print("secret answer is ", secret_answer)
    solver.reset_solutions()

    for round in range(6):
        guess = solver.guess()
        print("solver guesses: ", guess)

        feedback = guess_input(guess, secret_answer)
        print(feedback)

        if guess == secret_answer:
            print("solver solved in ", round+1, "attempts")
            break

        solver.filter(feedback, guess)
    else:
        print("solver failed")

main()


