#!/usr/bin/env python
from re import compile
import pickle
from string import ascii_lowercase
from operator import itemgetter

def simple_search(user_input, dictionary):
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

def expression(argword, dictionary):
    if '?' in argword and '@@' not in argword:
        user_input = argword
        user_input = user_input.replace('?', '.')
        search = simple_search(user_input, dictionary)

    elif '@@' in argword:
        user_input = argword
        new_input = user_input.replace('?', '.')
        new_input = new_input.replace('@@', '([a-z])\\1')
        search = simple_search(new_input, dictionary)

    else:
        user_input = argword
        search = simple_search(user_input, dictionary)

    if search:
        # flip our dictionary
        dictionary = dict((v,k) for k, v in dictionary.items())

        # Get our id matches
        found = []
        for id in search[3]:
            found.append(dictionary[id])

        # Only 10 results
        count = 1
        words = []
        for word in sorted(found):
            if count <= 10:
                count += 1
                words.append(word)
        return words
