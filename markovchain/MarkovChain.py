import codecs
from random import choice

def _is_end_of_sentence(word):
        seems_so = word[-1] in ['.', '!', '?', ':']
        is_a_digit = word[:-1].isdigit()
        return seems_so and not is_a_digit

class MarkovChain(object):
    def __init__(self, order=2):
        self.database = {}
        self.possible_starts = set()
        self.order = order

    def feedFromFile(self, path):
        with codecs.open(path, 'r', encoding='utf-8') as f:
            data = f.read()
        words = [word.replace('"', '') for word in data.split()]

        for i in range(len(words[:-1 * self.order])):
            items_for_key = words[i : i + self.order]
            next_one = words[i + self.order]
            if any(_is_end_of_sentence(w) for w in items_for_key):
                continue

            key = tuple(items_for_key)

            if i == 0 or _is_end_of_sentence(words[i-1]):
                self.possible_starts.add(key)

            if key not in self.database:
                self.database[key] = [next_one]
            else:
                self.database[key].append(next_one)

    def generateSentence(self):
        key = choice(list(self.possible_starts))
        sentence = [word for word in key]
        while True:
            next_word = choice(self.database[key])
            sentence.append(next_word)
            if _is_end_of_sentence(next_word):
                break;
            key = tuple(list(key[1:]) + [next_word])
        return u' '.join(sentence)