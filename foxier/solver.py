"""
    -Some work to find games to enter and play (Can I play multiple games?)
        - Probably shouldnt to avoid obv botting
    - Some work to make optimal play in a current game
        - Exhaust all possible plays then if nothing available
          Swap all constants, or some Vowels if all vowels

    TODO: Consider using heap for storing subset of words
        I just want the words worth the most points
"""
import logging
import json
from itertools import cycle
from enum import Enum


class WordOrientation(Enum):  # GameState Enum
    HORIZONTAL = 1
    VERTICAL = 2

dictionary = json.load('dictionary\\DictPrimeRep.txt')


def findWordPlays(board, rack):
    """
    Returns list of MoveSubmission objects with point value
    (moveSub, word, totalPoints)
    """
    rackhand = [tile.Letter.value for tile in rack]
    boardij = list(organizeBoard(board, 15))
    logging.info('Board organized %s:', boardij)
    playList = list()
    isBoardEmpty = True  # Used to choose an initial or SWAP play

    for i, row in enumerate(boardij):
        for j, slot in enumerate(row):
            if slot.tile:  # None if no piece there
                isBoardEmpty = False
                wordSeeker(boardij, rackhand, {(i, j): slot.tile.letter.value})

    if isBoardEmpty:  # (better ways of checking empty board via API)
        options = [word for word in wordPossibilityFinder(rackhand) if (len(word) < 7)]
        scoredOptions = scoreWords(options)
        #wordToPlay = max(scoredOptions.items(), key=(lambda key: scoredOptions[key]))[0]
        for word, score in scoredOptions.items():  # TODO list comprehension
            move = constructMove(7, 7,  WordOrientation.HORIZONTAL, rackhand, boardij, word)
            playList.append((move, word, score))
    return playList

    logging.info('Tiles: %s', rack)
    logging.info('Board: %s', board)
    raise Exception('Finish implementing')
    return playList


def wordSeeker(boardM, letters, lettersPositionDict):
    """
    Dictionary containing letter(key) and position requirements for a word

    returns list of possible words matches
    """
    lettersPositionDict = {(1, 2): 'a'}  # ease in making class, del

def constructMove(i, j, orientation, playerRack, boardM, word):
    """
    i,j = start coordinates for play
    orientation = the tiles will be played.  Uses Enum WordOrientation
    playerRack = players current hand
    boardM = current board state as a matrix
    Returns MoveSubmission object
    """
    pass

def chooseSwap(letters):
    pass


def wordPossibilityFinder(letters):
    """
    Generator return string of viable word with letters
    Based on dictionary specified
    """
    for k, v in dictionary.items():
        if letters % v == 0:
            yield k


def organizeBoard(boardAsList, rowsize):
    """
    A generator for a board of row size
    Take the inital board as a 1 dimensional list<>
    """
    elemIndx = 0
    while elemIndx < len(boardAsList):
        rowContent = boardAsList[elemIndx:elemIndx + rowsize]
        yield rowContent
        elemIndx += rowsize

def scoreWords(wordlist):
    """
    Takes a list of words
    Create dictionary of word=key and score=val
    """
    return dict()
