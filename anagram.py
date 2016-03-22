"""
   Word Games: Hangman and Anagram implemented in Python.
   Copyright (C) 2016  Aniket Kulkarni  <kaniket21@gmail.com>

   This program is free software: you can redistribute it and/or modify
   it under the terms of the GNU General Public License as published by
   the Free Software Foundation, either version 3 of the License, or
   (at your option) any later version.

   This program is distributed in the hope that it will be useful,
   but WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
   GNU General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

import random
import string

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 10

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

WORDLIST_FILENAME = "words_anagram.txt"

def loadWords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    # fp: file
    fp = open(WORDLIST_FILENAME, 'r', 0)
    # wordList: list of strings
    wordList = []
    for line in fp:
        wordList.append(line.strip().lower())
    print "  ", len(wordList), "words loaded."
    return wordList

def getFrequencyDict(sequence):
    """
    Returns a dictionary where the keys are elements of the sequence
    and the values are integer counts, for the number of times that
    an element is repeated in the sequence.

    sequence: string or list
    return: dictionary
    """
    # freqs: dictionary (element_type -> int)
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq

def getWordScore(word, n):
    """
    Returns the score for a word. Assumes the word is a valid word.

    The score for a word is the sum of the points for letters in the
    word, multiplied by the length of the word, PLUS 50 points if all n
    letters are used on the first turn.

    Letters are scored as in Scrabble; A is worth 1, B is worth 3, C is
    worth 3, D is worth 2, E is worth 1, and so on (see SCRABBLE_LETTER_VALUES)

    word: string (lowercase letters)
    n: integer (HAND_SIZE; i.e., hand size required for additional points)
    returns: int >= 0
    """
    l = len(word)
    if l == 0:
        return l
    total = 0
    if l == n:
        for ch in word:
            total += SCRABBLE_LETTER_VALUES[str(ch)]
        total = total * l + 50
    else:
        for ch in word:
            total += SCRABBLE_LETTER_VALUES[str(ch)]
        total = total * l
    return total    

def displayHand(hand):
    """
    Displays the letters currently in the hand.

    For example:
    >>> displayHand({'a':1, 'm':2, 'c':3, 'e':1})
    Should print out something like:
       a m m c c c e
    The order of the letters is unimportant.

    hand: dictionary (string -> int)
    """
    for letter in hand.keys():
        for j in range(hand[letter]):
             print letter,              # print all on the same line
    print                               # print an empty line

def dealHand(n):
    """
    Returns a random hand containing n lowercase letters.
    At least n/3 the letters in the hand should be VOWELS.

    Hands are represented as dictionaries. The keys are
    letters and the values are the number of times the
    particular letter is repeated in that hand.

    n: int >= 0
    returns: dictionary (string -> int)
    """
    hand={}
    numVowels = n / 3
    
    for i in range(numVowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(numVowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
        
    return hand

def updateHand(hand, word):
    """
    Assumes that 'hand' has all the letters in word.
    In other words, this assumes that however many times
    a letter appears in 'word', 'hand' has at least as
    many of that letter in it. 

    Updates the hand: uses up the letters in the given word
    and returns the new hand, without those letters in it.

    Has no side effects: does not modify hand.

    word: string
    hand: dictionary (string -> int)    
    returns: dictionary (string -> int)
    """
    new = hand.copy()
    for ch in word:
        new[str(ch)] -= 1
    return new    

def isValidWord(word, hand, wordList):
    """
    Returns True if word is in the wordList and is entirely
    composed of letters in the hand. Otherwise, returns False.

    Does not mutate hand or wordList.
   
    word: string
    hand: dictionary (string -> int)
    wordList: list of lowercase strings
    """
    new = hand.copy()
    if word in wordList:
        for ch in word:
            if new.get(str(ch), 0) <= 0:
                return False
            else:
                new[str(ch)] -= 1    
        return True        
    else:
        return False

def calculateHandlen(hand):
    """ 
    Returns the length (number of letters) in the current hand.
    
    hand: dictionary (string-> int)
    returns: integer
    """
    total = 0
    for i in hand.keys():
        total += hand[i]
    return total

def playHand(hand, wordList, n):
    """
    Allows the user to play the given hand, as follows:

    * The hand is displayed.
    * The user may input a word or a single period (the string ".") 
      to indicate they're done playing
    * Invalid words are rejected, and a message is displayed asking
      the user to choose another word until they enter a valid word or "."
    * When a valid word is entered, it uses up letters from the hand.
    * After every valid word: the score for that word is displayed,
      the remaining letters in the hand are displayed, and the user
      is asked to input another word.
    * The sum of the word scores is displayed when the hand finishes.
    * The hand finishes when there are no more unused letters or the user
      inputs a "."

      hand: dictionary (string -> int)
      wordList: list of lowercase strings
      n: integer (HAND_SIZE; i.e., hand size required for additional points)
      
    """
    
    # score: total score
    score = 0
    tokens = calculateHandlen(hand)
    
    # tokens: letters left in the hand:
    while tokens > 0:
        # Display the hand
        print 'Current Hand: ',
        displayHand(hand)
        # Ask user for input
        inp = raw_input('Enter word, or a "." to indicate that you are finished: ')
        # single period: end the game
        if inp == '.':
            break
        else:
            # If the word is not valid:
            if not(isValidWord(inp, hand, wordList)):
                # Reject invalid word (print a message followed by a blank line)
                print 'Invalid word, please try again.'
                print
            # Otherwise (the word is valid):
            else:
                # Tell the user how many points the word earned, and the updated total score
                cur_points = getWordScore(inp, n)
                score += cur_points
                print inp + ' earned ' + str(cur_points) + ' points. Total: ' + str(score) + ' points'
                print
                # Update the hand 
                hand = updateHand(hand, inp)
        tokens = calculateHandlen(hand)                

    # Game is over (user entered a '.' or ran out of letters), so tell user the total score
    if inp == '.':
        print 'Goodbye! Total score: ' + str(score)
        print
    else:
        print 'Run out of letters. Total score: ' + str(score) + ' points.'    
        print

def playGame(wordList):
    """
    Allow the user to play an arbitrary number of hands.

    1) Asks the user to input 'n' or 'r' or 'e'.
      * If the user inputs 'n', let the user play a new (random) hand.
      * If the user inputs 'r', let the user play the last hand again.
      * If the user inputs 'e', exit the game.
      * If the user inputs anything else, tell them their input was invalid.
 
    2) When done playing the hand, repeat from step 1    
    """
    reset = 0
    while True:
        choice = raw_input('Enter n to deal a new hand, r to replay the last hand, or e to end game: ')
        if choice == 'n':
            hand = dealHand(HAND_SIZE)
            previous = hand.copy()
            playHand(hand, wordList, HAND_SIZE)
            reset = 1
        elif choice == 'r':
            if reset:
                hand = previous.copy()
                playHand(hand, wordList, HAND_SIZE)
            else:
                print 'You have not played a hand yet. Please play a new hand first!'
                print
        elif choice == 'e':
            break
        else:
            print 'Invalid command.'                  

if __name__ == '__main__':
    wordList = loadWords()
    playGame(wordList)
