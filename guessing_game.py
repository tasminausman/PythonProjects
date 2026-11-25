"""
Number Guessing Game (Pandas + NumPy version)
Concepts: Python basics + numpy (random number, distance hints, sorting)
          + pandas (game history table and win statistics).
"""

import numpy as np
import pandas as pd

MAX_ATTEMPTS = 7

# History table: one row per game
history = pd.DataFrame(columns=["game", "result", "attempts"])


def play_round():
    secret = int(np.random.randint(1, 101))      # numpy random number 1 to 100
    attempts = 0
    guesses = []
    print("\nI have picked a number between 1 and 100.")
    print(f"You have {MAX_ATTEMPTS} attempts. Good luck!")

    while attempts < MAX_ATTEMPTS:
        guess = input(f"Attempt {attempts + 1}/{MAX_ATTEMPTS} - your guess: ").strip()

        if not guess.isdigit():
            print("Please enter a whole number.")
            continue                      # does not use up an attempt

        guess = int(guess)
        if guess < 1 or guess > 100:
            print("Number must be between 1 and 100.")
            continue

        attempts += 1
        guesses.append(guess)

        if guess == secret:
            print(f"Correct! You guessed it in {attempts} attempts.")
            print("Your guesses (sorted):", np.sort(guesses).tolist())
            return True, attempts

        distance = np.abs(guess - secret)    # how far is the guess?
        if guess < secret:
            hint = "Too low."
        else:
            hint = "Too high."

        if distance <= 5:
            hint += " Very hot!"
        elif distance <= 15:
            hint += " Warm."
        else:
            hint += " Cold."
        print(hint)

    print(f"Game over! The number was {secret}.")
    print("Your guesses (sorted):", np.sort(guesses).tolist())
    return False, attempts


def show_history():
    if len(history) == 0:
        return
    print("\n===== Game History =====")
    print(history.to_string(index=False))

    wins = history[history["result"] == "Win"]          # filter rows
    win_rate = len(wins) / len(history) * 100
    print(f"\nGames played : {len(history)}")
    print(f"Win rate     : {win_rate:.0f}%")
    if len(wins) > 0:
        attempts = wins["attempts"].to_numpy(dtype=float)
        print(f"Average attempts in wins: {np.mean(attempts):.1f}")
        print(f"Best game (fewest attempts): {int(np.min(attempts))}")


def main():
    print("=== Number Guessing Game ===")
    game_number = 1

    while True:
        won, attempts = play_round()
        result = "Win" if won else "Loss"
        history.loc[len(history)] = [game_number, result, attempts]
        game_number += 1

        again = input("\nPlay again? (y/n): ").strip().lower()
        if again != "y":
            break

    show_history()
    print("\nThanks for playing!")


if __name__ == "__main__":
    main()
