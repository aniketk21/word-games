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

WORDLIST_FILENAME = "words_hangman.txt"

def loadWords():
	"""
        Returns: a list of valid words. Words are strings of lowercase letters.
	    
	Depending on the size of the word list, this function may
	take some time to finish.
	"""
	print "Loading word list from file..."
	# open file "words.txt'
	fp = open(WORDLIST_FILENAME, 'r', 0)
	# line: string
	line = fp.readline()
	# wordlist: list of strings
	wordlist = string.split(line)
	print "  ", len(wordlist), "words loaded."
	print
	return wordlist

def chooseWord(wordlist):
	"""
	wordlist (list): list of words (strings)

	Returns a word from wordlist at random
	"""
	return random.choice(wordlist)

# Load the list of words into the variable wordlist
wordlist = loadWords()

def isWordGuessed(secretWord, lettersGuessed):
	'''
	secretWord: string, the word the user is guessing
	lettersGuessed: list, what letters have been guessed so far
	returns: boolean, True if all the letters of secretWord are in lettersGuessed;
	False otherwise
	'''
	for letter in secretWord:
		if letter in lettersGuessed:
			continue
		else:
			return False
	return True

def getGuessedWord(secretWord, lettersGuessed):
	'''
	secretWord: string, the word the user is guessing
	lettersGuessed: list, what letters have been guessed so far
	returns: string, comprised of letters and underscores that represents
	what letters in secretWord have been guessed so far.
	'''
	word = ''
	length = len(secretWord)
	for letter in secretWord:
		if letter in lettersGuessed:
			word += ' ' + str(letter) + ' '
		else:
			word += ' _ '
	return word

def getAvailableLetters(lettersGuessed):
	'''
	lettersGuessed: list, what letters have been guessed so far
	returns: string, comprised of letters that represents what letters have not
	yet been guessed.
	'''
	atoz = string.ascii_lowercase # string of ASCII 'a' to 'z' in lowercase
	for letter in lettersGuessed:
		if letter in atoz:
			atoz = atoz.replace(letter, '')
	return atoz
    

def hangman(secretWord):
	'''
	secretWord: string, the secret word to guess.

	Starts up an interactive game of Hangman.

	* At the start of the game, displays how many 
	  letters the secretWord contains.

	* Asks the user to supply one guess (i.e. letter) per round.

	* The user receives feedback immediately after each guess 
	  about whether their guess appears in the computers' word.

	* After each round, also displays to the user the 
	  partially guessed word so far, as well as letters that the 
	  user has not yet guessed.
	'''
	lenSecretWord = len(secretWord)
	print 'Welcome to the game, Hangman!'
	print 'I am thinking of a word that is ' + str(lenSecretWord) + ' letters long.'
	print
	availStr = string.ascii_lowercase
	numGuesses = 8
	lettersGuessed1 = []
	lettersGuessed2 = []
	while numGuesses > 0:
		print '-------------'
		print
		print 'You have ' + str(numGuesses) + ' guesses left.'
		print 'Available letters: ' + availStr
		choice = raw_input('Please guess a letter: ')
		lettersGuessed1.append(choice)
		if choice in lettersGuessed2:
			print "Oops! You've already guessed that letter: ",
			print getGuessedWord(secretWord, lettersGuessed1)
		else:
			if choice in secretWord:
				print 'Good guess: ',
				print getGuessedWord(secretWord, lettersGuessed1)
				availStr = availStr.replace(choice, '')
			if not(choice in secretWord):
				print 'Oops! That letter is not in my word: ',
				print getGuessedWord(secretWord, lettersGuessed1)
				numGuesses -= 1
		availStr = getAvailableLetters(lettersGuessed1)
		if isWordGuessed(secretWord, lettersGuessed1):
			won = 1
			break
		else:
			won = 0
		lettersGuessed2.append(choice)
		print
	print '-------------'
	if won:
		print 'Congratulations, you won!'
	else:
		print 'Sorry, you ran out of guesses. The word was ' + secretWord + '.'				

secretWord = chooseWord(wordlist).lower()
hangman(secretWord)
