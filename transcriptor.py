
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
