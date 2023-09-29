import random
from functools import reduce
from pathlib import Path


class SyllableGen:
    def __init__(self, path):
        self.syllables = {}
        self.sum = 0
        with open(path) as f:
            for line in f.readlines():
                if line.startswith('#'):
                    continue

                _, syllable, count, _ = line.split(maxsplit=3)
                count = int(count)
                self.sum += count

                # combined syllable count might be denoted using the '/' separator
                # we distribute the count evenly
                syllables = syllable.split('/')
                syllable_count = len(syllables)
                add = count // syllable_count
                for syllable in syllables:
                    self.syllables[syllable] = add
                # correct for integer rounding
                self.syllables[syllable] += count - add * syllable_count

    def get(self):
        num = random.randrange(self.sum)
        for syllable, count in self.syllables.items():
            num -= count
            if num <= 0:
                return syllable

        # this should never happen
        raise RuntimeError("out of range")


class WordLenGen:
    def __init__(self, path):
        self.length_probability = {}
        self.sum = 0

        with open(path) as f:
            for line in f.readlines():
                if line.startswith('#'):
                    continue

                syllable_count, occurrence, _ = line.split(maxsplit=3)
                syllable_count = int(syllable_count)
                if syllable_count in self.length_probability:
                    raise RuntimeError(f"duplicate syllable count {syllable_count}")

                occurrence = int(occurrence)
                self.length_probability[syllable_count] = occurrence
                self.sum += occurrence

    def get(self):
        num = random.randrange(self.sum)
        for length, count in self.length_probability.items():
            num -= count
            if num <= 0:
                return length

        # this should never happen
        raise RuntimeError("out of range")


class IPATranscriptor:
    def __init__(self, path):
        self.trans = {}

        with open(path) as f:
            for line in f.readlines():
                if line.startswith('#'):
                    continue

                ipa, norm = line.split()
                self.trans[ipa] = norm

    def transcribe(self, ipa):
        return self.trans[ipa]


def print_words(words, word_join=' ', syllable_join='', transcribe_fn=None):
    for word in words:
        if transcribe_fn is not None:
            word = map(transcribe_fn, word)
        print(syllable_join.join(word), end='')
        print(word_join, end='')


def words2lines(words, line_length=80):
    lines = []
    line = []
    length = 0
    for word in words:
        word_length = reduce(lambda x, y: x + len(y), word, 0)
        if word_length + length > line_length:
            lines.append(line)
            line = []
            length = 0
        line.append(word)
        length += word_length

    if line:
        lines.append(line)

    return lines


def generate_pseudo_words(num_words):
    words = []
    for _ in range(num_words):
        word_len = word_len_gen.get()
        word = []
        for _ in range(word_len):
            ipa = syllable_gen.get()
            word.append(ipa)
        words.append(word)

    return words


if __name__ == '__main__':
    syllable_gen = SyllableGen(Path(__file__).parent / 'silbenhaeufigkeit_de.txt')
    word_len_gen = WordLenGen(Path(__file__).parent / 'wortlaengen_de.txt')

    word_count = 128
    ipa_words = generate_pseudo_words(word_count)

    line_length = 58
    lines = words2lines(ipa_words, line_length=line_length)

    print("IPA:")
    for line in lines:
        print_words(line, syllable_join='-')
        print()

    print()

    print("Transkription:")
    tran = IPATranscriptor(Path(__file__).parent / 'lautschrift.txt')
    for line in lines:
        print_words(line, syllable_join='-', transcribe_fn=tran.transcribe)
        print()
