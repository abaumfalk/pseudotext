import random


class RandomGenerator:
    def __init__(self):
        self.item_count = {}
        self.sum = 0

    def get(self):
        num = random.randrange(self.sum)
        for item, count in self.item_count.items():
            num -= count
            if num <= 0:
                return item

        # this should never happen
        raise RuntimeError("out of range")


class SyllableGen(RandomGenerator):
    def __init__(self, path):
        super().__init__()

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
                    self.item_count[syllable] = add
                # correct for integer rounding
                self.item_count[syllable] += count - add * syllable_count


class WordLenGen(RandomGenerator):
    def __init__(self, path):
        super().__init__()

        with open(path) as f:
            for line in f.readlines():
                if line.startswith('#'):
                    continue

                syllable_count, occurrence, _ = line.split(maxsplit=3)
                syllable_count = int(syllable_count)
                if syllable_count in self.item_count.keys():
                    raise RuntimeError(f"duplicate syllable count {syllable_count}")

                occurrence = int(occurrence)
                self.item_count[syllable_count] = occurrence
                self.sum += occurrence
