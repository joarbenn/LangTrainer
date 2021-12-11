class Vocable:
    def __init__(self, eng_words=None, pol_words=None):
        self.words = []
        if pol_words is None:
            pol_words = list()
        if eng_words is None:
            eng_words = list()

        self.words.append(eng_words)
        self.words.append(pol_words)