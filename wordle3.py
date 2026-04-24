import re
import random
import json
import os
import argparse
import importlib
from collections import Counter

# Load word lists (used by guess_input)
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

def run_simulation(solver_module):
    secret_answer = random.choice(list(solutions))
    print("secret answer is ", secret_answer)
    solver_module.reset_solutions()

    for round in range(6):
        guess = solver_module.guess()
        print("solver guesses: ", guess)

        feedback = guess_input(guess, secret_answer)
        print(feedback)

        if guess == secret_answer:
            print("solver solved in ", round+1, "attempts")
            return round+1

        solver_module.filter(feedback, guess)
    else:
        print("solver failed")
        return 7

def load_performance(filename):
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return json.load(f)
    return []

def save_performance(attempts_list, filename):
    with open(filename, "w") as f:
        json.dump(attempts_list, f)

def main():
    parser = argparse.ArgumentParser(description="Simulate Wordle solver performance")
    parser.add_argument("solver", nargs="?", default="wordle_solver_entropy",
                        help="Name of the solver module (e.g., wordle_solver_entropy, wordle_solver)")
    parser.add_argument("--simulations", "-n", type=int, default=10,
                        help="Number of simulations to run (default: 100)")
    args = parser.parse_args()

    # Import the requested solver module
    try:
        solver_module = importlib.import_module(args.solver)
    except ImportError:
        print(f"Error: Could not import module '{args.solver}'")
        return

    # Use a separate JSON file for each solver
    perf_filename = f"performance_{args.solver}.json"
    all_attempts = load_performance(perf_filename)
    new_attempts = []
    
    for _ in range(args.simulations):
        attempts = run_simulation(solver_module)
        new_attempts.append(attempts)
        all_attempts.append(attempts)
    
    save_performance(all_attempts, perf_filename)
    
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