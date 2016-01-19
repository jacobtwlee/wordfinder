class WordFinder:
    dictionary_path = "wordlists/unix.txt"
    letter_scores = {}
    min_length = 2
    
    def read_words(self, filename):
        # dictionary can be arbitrarily large, so use a generator expression instead of a list comprehension for better performance
        return (word.strip() for word in open(filename))

    def solve(self, letters):
        words = self.read_words(self.dictionary_path)
        return ((word, self.score_word(word), len(word)) for word in words if self.is_spellable(word, letters) and len(word) >= self.min_length)
    
    def score_word(self, word):
        return sum([self.letter_scores[char] for char in word if char in self.letter_scores])
    
    def is_spellable(self, word, letters):
        if len(word) > len(letters):
            return False
            
        letters = letters.lower()
            
        for char in word.lower():
            if char in letters:
                letters = letters.replace(char, "", 1)
            else:
                return False
        return True


class ScrabbleWordFinder(WordFinder):
    dictionary_path = "wordlists/scrabble.txt"
    letter_scores = {
        "a": 1, "c": 3, "b": 3, "e": 1, "d": 2, "g": 2, "f": 4, "i": 1, "h": 4,
        "k": 5, "j": 8, "m": 3, "l": 1, "o": 1, "n": 1, "q": 10, "p": 3, "s": 1,
        "r": 1, "u": 1, "t": 1, "w": 4, "v": 4, "y": 4, "x": 8, "z": 10
    }

class WordsWithFriendsWordFinder(WordFinder):
    dictionary_path = "wordlists/words-with-friends.txt"
    letter_scores = {
        "a": 1, "c": 4, "b": 4, "e": 1, "d": 2, "g": 3, "f": 4, "i": 1, "h": 3,
        "k": 5, "j": 10, "m": 4, "l": 2, "o": 1, "n": 2, "q": 10, "p": 4, "s": 1,
        "r": 1, "u": 2, "t": 1, "w": 4, "v": 5, "y": 3, "x": 10, "z": 10
    }
    

import sys

if __name__ == "__main__":
    if len(sys.argv) == 2:
        letters = sys.argv[1].strip()
    else:
        letters = input("Enter your letters: ").strip()
        
    wordlists = {"1": "None (words only)", "2": "Scrabble", "3": "Words With Friends"}
    selected = None
    while not selected:
        for key in sorted(wordlists.keys()):
            print("(" + key + ") " + wordlists[key])
        selected = input("Select a game (0 to exit): ")
        if selected not in wordlists.keys():
            if selected == "0":
                exit()
            selected = None

    if selected == "1":
        solutions = WordFinder().solve(letters)
    if selected == "2":
        solutions = ScrabbleWordFinder().solve(letters)
    elif selected == "3":
        solutions = WordsWithFriendsWordFinder().solve(letters)
    
    print("Showing words for: " + letters)
    
    cur_len = 0
    for solution in sorted(solutions, key=lambda x: (x[2], x[1]), reverse=True):
        if (cur_len != solution[2]):
            cur_len = solution[2]
            print("\n---------------\n" + str(cur_len) + " Letter Words:\n---------------")
        score = ""
        if solution[1] > 0:
            score = "(Score: " + str(solution[1]) + ")"
        print(solution[0], score)