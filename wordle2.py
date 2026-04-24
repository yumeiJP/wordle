import re
import random
import json
import os
import wordle_solver_entropy as solver
from collections import Counter

guesses = set(re.findall(r'"([^"]+)"', open("guesses.txt").read()))
solutions = set(re.findall(r'"([^"]+)"', open("solutions.txt").read()))

def guess_input(guess, secret_answer):
    feedback = ['0']*5
    secret_answer_frequencies = Counter(secret_answer)

    for i in range(5):
        if guess[i] == secret_answer[i]:
            feedback[i] = "2"
            secret_answer_frequencies[guess[i]] -= 1
    
    for i in range(5):
        if feedback[i] == "2":
            continue
        if secret_answer_frequencies.get(guess[i], 0) > 0:
            feedback[i] = "1"
            secret_answer_frequencies[guess[i]] -= 1
    
    return "".join(feedback)

def run_simulation():
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
            return round+1

        solver.filter(feedback, guess)
    else:
        print("solver failed")
        return 7

def load_performance(filename="performance.json"):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return []

def save_performance(attempts_list, filename="performance.json"):
    with open(filename, "w") as f:
        json.dump(attempts_list, f)

def main():
    all_attempts = load_performance()
    simulation_count = 5
    new_attempts = []
    
    for _ in range(simulation_count):
        attempts = run_simulation()
        new_attempts.append(attempts)
        all_attempts.append(attempts)
    
    save_performance(all_attempts)
    
    total = len(all_attempts)
    results = [0]*7
    expected_value = 0
    for att in all_attempts:
        results[att-1] += 1
    
    for i in range(7):
        fraction = results[i]/total if total > 0 else 0
        expected_value += fraction*(i+1)
        print("Attempt count", i+1, ": ", fraction*100, "%")
    print("Expected Attempts: ", expected_value)
    print("Total simulations run: ", total)
    print("Results from this batch: ", new_attempts)

if __name__ == "__main__":
    main()