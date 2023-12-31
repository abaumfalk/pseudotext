from functools import reduce
from pathlib import Path

from generator import SyllableGen, WordLenGen
from transcriptor import IPATranscriptor

VERSION = 1.1


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


def generate_pseudo_words(sy_gen, len_gen, num_words):
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
    syllable_gen = SyllableGen(Path(__file__).parent.parent / 'data' / 'silbenhaeufigkeit_de.txt')
    word_len_gen = WordLenGen(Path(__file__).parent.parent / 'data' / 'wortlaengen_de.txt')

    word_count = 128
    ipa_words = generate_pseudo_words(syllable_gen, word_len_gen, word_count)

    line_length = 58
    lines = words2lines(ipa_words, line_length=line_length)

    print("IPA:")
    for line in lines:
        print_words(line, syllable_join='-')
        print()

    print()

    print("Transkription:")
    tran = IPATranscriptor(Path(__file__).parent.parent / 'data' / 'lautschrift.txt')
    for line in lines:
        print_words(line, syllable_join='-', transcribe_fn=tran.transcribe)
        print()
