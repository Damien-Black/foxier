"""
Take adictionary of words in format:

1 word per line

Generate a new dictionary file k,v = 'word','product of primes representation'
Then pickle the generated dictionary

Lazy Sieve implementation from:
    The Genuine Sieve of Eratosthenes
        Melissa E. O’Neill
    Harvey Mudd College, Claremont, CA, U.S.A. (e-mail: oneill@acm.org)
Using the variant that skips 2 and 3 by adding 2 and 4 alternatively
"""
import os  # Allow command line file input
import json
import logging
from itertools import count, cycle


def lazySieveEras():
    yield 2
    yield 3
    candidates = count(5, 2)  # Skip even numbers, starting at 5
    composites = {9:{3}}  # map composites to their prime factors

    for candidate in candidates:
        try:
            factors = composites.pop(candidate)
        except KeyError:  # if it's not in the dict, it's prime
            yield candidate
            composites[candidate**2] = {candidate}  # Euler's optimization: start from prime**2
        else:
            for prime in factors:  # Increment factors by primes
                try:
                    composites[candidate+prime*2].add(prime)  # Ignore evens
                except KeyError:
                    composites[candidate+prime*2] = {prime}


def lazySieveErasWithWheel():  # know what multiple youre on when prime*X
    yield 2
    yield 3
    yield 5
    yield 7
    wheel = [2, 4, 2, 4, 6, 2, 6, 4, 2, 4, 6, 6, 2, 6, 4, 2, 6, 4, 6, 8, 4, 2,
            4, 2, 4, 8, 6, 4, 6, 2, 4, 6, 2, 6, 6, 4, 2, 4, 6, 2, 6, 4, 2, 4,
            2, 10, 2, 10]
    candidates = wheelCount(11, wheel)  # Skip even numbers, starting at 5
    composites = {143: {11, 13}}  # map composites to their prime factors

    for candidate in candidates:
        try:
            factors = composites.pop(candidate)
        except KeyError:  # if it's not in the dict, it's prime
            yield candidate
            composites[candidate**2] = {candidate}  # Euler's optimization: start from prime**2
        else:
            for prime in factors:  # go through the prime factors and increment their keys
                try:
                    composites[candidate+prime*10].add(prime)
                except KeyError:
                    composites[candidate+prime*10] = {prime}
                finally:
                    # Space optimization delete the candidate ke in dict
                    # since it will no longer be used
                    del composites[candidate]

def wheelCount(start, wheel):
    n = start
    wheelCycle = cycle(wheel)
    while True:
        yield n
        n += wheelCycle.__next__()

def createLetterKeys():
    """
    Create dictionary where keys = letter and value = prime representation
    """
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i',
                'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r',
                's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    primes = lazySieveEras()
    letterPrimes = dict()
    for letter in letters:
        letterPrimes[letter] = primes.__next__()
    return letterPrimes

def readDictionaryWords(filepath):
    with open(filepath) as f:
        dictionary = [line.strip() for line in f]
    return dictionary

def createPrimeValueDict(dictList, letterDict):
    newdict = dict()
    for word in dictList:
        product = 1
        for letter in letterDict:
            product *= letterDict[letter]
        newdict[word] = product
    return newdict

if __name__ == '__main__': #  Alter to take command line arguments
    logging.basicConfig(
        format='%(levelname)s:%(message)s',
        filename='dictionaryMaker.log', filemode='w', level=logging.INFO)
    lettersDict = createLetterKeys()
    externalDict = readDictionaryWords('wwf_dict.txt')
    dictRepr = createPrimeValueDict(externalDict, lettersDict)
    with open('DictPrimeRep.txt', 'w') as outfile:
        json.dump(dictRepr, outfile)
