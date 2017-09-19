import nltk, re, random

''' This class is used to parse the corpus and extract all the dialogue by
    character. '''
class Futurama:
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

n=5
numSentences = 5
punctuation = ",;.!?:"
end_punct = "!?."
ngram_DB = [[], [], [], []]

f = Futurama()
words = f.characters['Fry']

#produce and store all the ngrams in a list
for x in range(2, n+1):
    for index in range(len(words)-x):
        ngram_DB[x-2].append(words[index:index+x])

tags = [t for w,t in nltk.pos_tag(words)]
tag_grams = nltk.bigrams(tags)
pos_dist = nltk.ConditionalFreqDist(tag_grams)

''' Generator output filter. Makes sure responses are of a
    certain length (so we're not just getting small actual
    sentences from dialogue). Also uses POS bigrams to make sure
    sentences are properly formed. '''
def text_filter(text, dist):
    # basic length filter to prevent short exclamations
    if len(text) <= 6:
        return False

    # POS bigram filter
    word_tags = nltk.pos_tag(text)
    tags = [t for w,t in word_tags]
    for i in range(0, len(tags) - 1):
        if tags[i + 1] not in [t for t,n in dist[tags[i]].most_common()]:
            return False

    return True

# GENERATOR
kbInput = ""
while (kbInput is not "q"):
    for sentenceIndex in range(numSentences):
        while(True):
            text = []

            firstWordCandidates = [ngram_DB[0][0][0]]
            firstWordCandidates.extend([ngram[1] for ngram in ngram_DB[n-2]
                if ngram[0] in end_punct and ngram[1] not in end_punct])
            text.append(random.choice(firstWordCandidates))

            while(text[-1] not in end_punct):
                if (len(text) < n - 1):
                    x = len(text) + 1
                else:
                    x = n
                candidates = []
                while len(candidates) == 0:
                    candidates = [ngram[x-1] for ngram in ngram_DB[x-2] if False not in
                        [(ngram[x-i] == text[-(x-(x-i)-1)]) for i in range(x, 1, -1)]]
                    if len(candidates) == 0:
                        x -= 1
                text.append(random.choice(candidates))
            val = text_filter(text, pos_dist)
            #print(val)
            if val is True:
                break

        #this is a way to clean up the text so there's no extra space before punctuation marks.
        cleanText = []
        for index in range(1,len(text)):
            if text[index] in punctuation:
                cleanText.append(text[index-1]+text[index])
            elif text[index-1] in punctuation:
                pass
            else:
                cleanText.append(text[index-1])

        print(' '.join(cleanText))
    kbInput = input("[q to quit or ENTER for next] ")
