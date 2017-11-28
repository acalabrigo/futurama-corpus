#!/usr/bin/env python

# Adam Calabrigo 2017
# Import this class to parse the Futurama Corpus!

import nltk, re

class Futurama:
    ''' This class is used to parse the corpus and extract all the dialogue by
        character. It creates a dictinary of dialogue, with character being
        the key '''
    def __init__(self):
        self.filename = './data/futurama_scripts.txt'
        self.characters = {}
        # go through corpus, extract lines by character
        apos = ["n't", "'s", "'ll", "'d", "'m", "'re", "ta", "na", "'", "'t", "'ve"]
        quotes = ["''", "``"]
        lines = [line.rstrip('\n') for line in open(self.filename)]
        for line in lines:
            match = re.match(r'([a-zA-z]+:\s*)(.*)', line)
            if match:
                name = match.group(1)[:-2]
                if name not in self.characters:
                    self.characters[name] = []
                tokens = nltk.word_tokenize(match.group(2))

                if len(tokens) > 0:
                    fixed_tokens = []
                    for i in range(1, len(tokens)):
                        if tokens[i] in apos:
                            fixed_tokens.append(tokens[i-1] + tokens[i])
                        elif tokens[i-1] in apos or tokens[i-1] in quotes:
                            pass
                        else:
                            fixed_tokens.append(tokens[i-1])

                    fixed_tokens.append(tokens[len(tokens)-1])
                    self.characters[name].extend(fixed_tokens)
