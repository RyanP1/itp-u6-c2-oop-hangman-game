from .exceptions import *
import random

class GuessAttempt(object):
    def __init__(self, letter, hit = False, miss = False):
        self.letter = letter
        self.hit = hit
        self.miss = miss
        
        if self.hit == self.miss:
            raise InvalidGuessAttempt ("Can't be a miss and a hit")
        
    def is_hit(self):
        return self.hit 

    def is_miss(self):
        return self.miss


class GuessWord(object):
    def __init__(self, answer):
        if not answer or answer == '':
            raise InvalidWordException("No word entered")
        
        self.answer = answer.lower()
        self.masked = len(answer) * '*'
    
    def perform_attempt(self, letter_guess):
        letter_guess = letter_guess.lower()
        
        if len(letter_guess) > 1 or letter_guess is None:
            raise InvalidGuessedLetterException()
        
        if letter_guess not in self.answer:
            attempt = GuessAttempt(letter_guess, miss=True)
        else:
            attempt = GuessAttempt(letter_guess, hit=True)
            masked_word = ''
            for index, letter in enumerate(self.answer):
                if letter_guess.lower() == letter:
                    masked_word += letter
                else:
                    masked_word += self.masked[index]
            self.masked = masked_word
        
        return attempt


class HangmanGame(object):
    

    def __init__(self, guess_list = None, number_of_guesses = 5):
        self.number_of_guesses = number_of_guesses
        self.remaining_misses = number_of_guesses
        self.previous_guesses = []
        self.WORD_LIST = ['rmotr', 'python', 'awesome']
        
        if not guess_list:
            guess_word = self.select_random_word(self.WORD_LIST)
        else:
            guess_word = guess_list[0]
        
        self.word = GuessWord(guess_word)
        
    def select_random_word(list_of_words = None):
        if not list_of_words:
            raise InvalidListOfWordsException("No word to select")
        else:
            return random.choice(list_of_words)
        
    def guess(self, letter_guess):
        if self.is_finished():
            raise GameFinishedException ("No remaining guesses!")
        
        letter_guess = letter_guess.lower()
        attempt = self.word.perform_attempt(letter_guess)
        self.previous_guesses.append(letter_guess)
                
        if attempt.is_hit():
            if self.is_won():
                raise GameWonException
        else:
            self.remaining_misses -= 1            
            if self.is_lost():
                raise GameLostException ("You lost!")
        
        return attempt
        
    def is_finished(self):
        return self.is_won() or self.is_lost()
    
    def is_lost(self):
        return self.remaining_misses <= 0
    
    def is_won(self):
        return self.word.answer == self.word.masked
        
        
        
        
    
    
