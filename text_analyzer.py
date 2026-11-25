"""
Text Analyzer (Pandas + NumPy version)
Concepts: Python basics (strings, loops) + pandas Series (word frequency)
          + numpy (word-length statistics).
"""

import numpy as np
import pandas as pd


def clean_words(text):
    # keep only letters and spaces, then split into words
    cleaned = ""
    for ch in text.lower():
        if ch.isalpha() or ch == " ":
            cleaned += ch
    return cleaned.split()


def count_vowels(text):
    total = 0
    for ch in text.lower():
        if ch in "aeiou":
            total += 1
    return total


def count_sentences(text):
    total = 0
    for ch in text:
        if ch in ".!?":
            total += 1
    return total


def analyze_text():
    text = input("\nEnter your text: ").strip()
    if text == "":
        print("You did not enter any text.")
        return

    words = clean_words(text)
    if len(words) == 0:
        print("No words found.")
        return

    word_series = pd.Series(words)                     # pandas Series of all words
    frequency = word_series.value_counts()             # how many times each word appears
    lengths = np.array([len(word) for word in words])  # numpy array of word lengths

    longest = words[int(np.argmax(lengths))]           # position of the longest word

    print("\n----- Analysis -----")
    print(f"Characters (with spaces): {len(text)}")
    print(f"Words                   : {len(words)}")
    print(f"Unique words            : {word_series.nunique()}")
    print(f"Sentences               : {count_sentences(text)}")
    print(f"Vowels                  : {count_vowels(text)}")
    print(f"Longest word            : {longest}")
    print(f"Average word length     : {np.mean(lengths):.2f}")
    print(f"Median word length      : {np.median(lengths):.1f}")

    print("\nTop 3 words:")
    for word, number in frequency.head(3).items():
        print(f"   {word} -> {number} time(s)")

    print("\nWord length distribution:")
    unique_lengths, counts = np.unique(lengths, return_counts=True)
    for length, number in zip(unique_lengths, counts):
        print(f"   {length} letters: {number} word(s)")


def check_palindrome():
    text = input("\nEnter a word or phrase: ").strip().lower()
    letters = ""
    for ch in text:
        if ch.isalnum():
            letters += ch

    if letters == "":
        print("Nothing to check.")
        return

    is_palindrome = True
    for i in range(len(letters) // 2):
        if letters[i] != letters[-1 - i]:
            is_palindrome = False
            break

    if is_palindrome:
        print("Yes, it is a palindrome!")
    else:
        print("No, it is not a palindrome.")


def main():
    print("=== Text Analyzer ===")
    while True:
        print("\n1) Analyze text")
        print("2) Palindrome checker")
        print("3) Exit")
        choice = input("Choose an option (1-3): ").strip()

        if choice == "1":
            analyze_text()
        elif choice == "2":
            check_palindrome()
        elif choice == "3":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Enter 1, 2 or 3.")


if __name__ == "__main__":
    main()
