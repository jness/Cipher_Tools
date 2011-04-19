#!/usr/bin/env python
import argparse
from re import compile
import pickle
from string import ascii_lowercase
from operator import itemgetter

def simple_search(user_input):
    matched = 0
    processed = 0
    matches = []
    found = []
    for word in sorted(dictionary.items(), key=itemgetter(1)):
        processed += 1
        match = compile('^' + user_input + '$').findall(word[0])

        if match:
            matches.append(word[1])
            matched += 1
            found.append(match[0])
    return found, matched, processed, matches


# Build my Parser with help for user input
parser = argparse.ArgumentParser()
parser.add_argument('word', 
    help='? in places of unknowns, @@ in place of unknown duplicate bigram')
args = parser.parse_args()

# Load the Dictionary File
f = open('dictionary.db', 'rb')
dictionary = pickle.load(f)

if '?' in args.word and '@@' not in args.word:
    user_input = args.word
    user_input = user_input.replace('?', '.')
    search = simple_search(user_input)

elif '@@' in args.word:
    user_input = args.word
    new_input = user_input.replace('?', '.')
    new_input = new_input.replace('@@', '([a-z])\\1')
    search = simple_search(new_input)

if search:
    # flip our dictionary
    dictionary = dict((v,k) for k, v in dictionary.items())

    # Get our id matches
    found = []
    for id in search[3]:
        found.append(dictionary[id])
    for word in sorted(found):
        print word


    print '-'*35
    print '%s words searched %s matches' % (search[2], search[1])
