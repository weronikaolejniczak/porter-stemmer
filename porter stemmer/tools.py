import re


class PorterStemmer:

    def __init__(self):
        self.word = ""  # holds a word to be stemmed
        self.buffer = []
        self.steps = []
        self.part_of_speech = []
        self.first = 0
        self.last = 0
        self.j = 0  # offset into the string

    def clear(self):
        self.buffer = []
        self.steps = []
        self.part_of_speech = []
        self.first = 0
        self.last = 0
        self.j = 0  # offset into the string

    # split word into letters
    def split_word(self):
        self.buffer = list(self.word)

    # check if letter[i] is a consonant
    def consonant(self, i):
        if self.buffer[i] == "a" or self.buffer[i] == "e" or self.buffer[i] == "i" or self.buffer[i] == "o" \
                or self.buffer[i] == "u":
            return 0
        if self.buffer[i] == "y":
            if i == self.last:
                return 1
            else:
                return not self.consonant(i - 1)

        return 1

    # the number of consonant clusters between self.first and self.j
    def measure_clusters(self):
        """
            <c><v> gives 0
            <c>vc<v> gives 1
            <c>vcvc<v> gives 2
            <c>vcvcvc<v> gives 3
            ...
        """

        n = 0
        i = self.first

        # look for letters(i) that is a consonant
        while 1:
            if i > self.j:
                return n
            if not self.consonant(i):
                break
            i = i + 1
        i = i + 1

        while 1:
            while 1:
                if i > self.j:
                    return n
                if self.consonant(i):
                    break
                i = i + 1
            i = i + 1
            n = n + 1

            while 1:
                if i > self.j:
                    return n
                if not self.consonant(i):
                    break
                i = i + 1
            i = i + 1

    # check if stem contains a vowel
    def vowel(self):
        for i in range(self.first, self.j + 1):
            if not self.consonant(i):
                return 1
        return 0

    # check if stem contains a double consonant
    def double_consonant(self, j):
        if j < (self.first + 1):
            return 0
        if self.buffer[j] != self.buffer[j - 1]:
            return 0

        return self.consonant(j)

    # consonant-vowel-consonant, unless the second consonant is w, x or y
    def cvc(self, i):
        """
        :param i:
        :return: TRUE if 1 - 2, i - 1, i are a consonant-vowel-consonant structure
        and if the second consonant is NOT w, x or y
        """

        if i < (self.first + 2) or not self.consonant(i) or self.consonant(i - 1) or not self.consonant(i - 2):
            return 0

        character = self.buffer[i]

        if character == "w" or character == "x" or character == "y":
            return 0

        return 1

    def ends_with(self, string):
        """
        :param string: word endings, e.g. "-ing"
        :return: TRUE if buffer ends with the string "string"
        """

        length = len(string)
        split_string = list(string)
        if string[length - 1] != self.buffer[self.last]:
            return 0
        if length > (self.last - self.first + 1):
            return 0
        if self.buffer[(self.last - length + 1):(self.last + 1)] != split_string:
            return 0

        self.j = self.last - length
        step = "Remove ending -" + string + "."

        self.steps.append(step)

        return 1

    def set_to(self, string):
        """
        sets (self.j + 1), ..., self.last to the chars in string "string"
        :param string: ending
        """

        length = len(string)

        self.buffer = self.buffer[:self.j + 1] + list(string) + self.buffer[self.j + length + 1:]
        self.last = self.j + length

        if len(string) > 0:
            step = "Set ending to -" + string + "."
            self.steps.append(step)

    def r(self, string):
        if self.measure_clusters() > 0:
            self.set_to(string)

    def set_pos(self, word):
        """
        Adjective
        suffixes: -ible, -ed, -ent, -al, -ical, -ing, -ant

        Noun
        suffixes: -ment, -tion, -ence, -ation, -is, -ity, -ant, -ance, -ity

        Verb
        suffixes: -ist, -ate, -ize

        Adverbs: -ly

        Preposition: about, above, across, after, against, ahead, along, amidst, among,
        around, as, at, barring, without, before, because, behind, below, beneath, beside,
        besides, between, beyond, by, concerning, despite, down, during, in, plus, within,
        next, inside, into, except, excluding, for, following, from, like, minus, near,
        outside, over, past, per, round, since, off, on, onto, opposite, out, than,
        through, throughout, till, times, to, toward, towards, under, underneath, unlike,
        until, unto, up, upon, via, with

        Pronoun:
            1st person: I, me, my, mine, myself
            2nd person: you, your, yours, yourself
            3rd person: he, him, his, himself
                        she, her, hers, herself
                        it, its, itself
            1st person: we, our, ours, ourselves
            2nd person: you, your, yours, yourselves
            3rd person: they, them, their, theirs, themselves

        Conjunction:
            coordinating: for, and, nor, but, or, yet, so
            subordinating: after, although, as, because, before, when, where, wherever,
            if, since, than, though, unless, until, whenever, whereas, while
            correlative: either, neither, both, whether, just, the, rather
        """

        adj_pattern = \
            "\w*ible$|\w*able$|\w*ed$|\w*ent$|\w*al$|\w*ical$|\w*ing$|\w*ant$"
        noun_pattern = \
            "\w*ment$|\w*tion$|\w*ence$|\w*ation$|\w*is$|\w*ity$|\w*ant$|\w*ance$|\w*s$"
        verb_pattern = \
            "\w*ing$|\w*ed$|\w*ate$|\w*ize$|\w*ise$|\w*s$|^am$"
        adverb_pattern = "\w*ly$"
        prep_pattern = \
            "^about$|^above$|^across$|^after$|^against$|^ahead$|^along$|^amidst$|^among$" \
            "|^around$|^as$|^at$|^barring$|^without$|^before$|^because$|^behind$|^below$" \
            "|^beneath$|^beside$|^besides$|^between$|^beyond$|^by$|^concerning$|^despite$" \
            "|^down$|^during$|^in$|^plus$|^within$|^next$|^inside$|^into$|^except$|^excluding$" \
            "|^for$|^following$|^from$|^like$|^minus$|^near$|^outside$|^over$|^past$|^per$" \
            "|^round$|^since$|^off$|^on$|^onto$|^opposite$|^out$|^than$|^through$|^throughout$" \
            "|^till$|^times$|^to$|^toward$|^towards$|^under$|^underneath$|^unlike$|^unto$" \
            "|^until$|^unto$|^up$|^upon$|^via$|^with$"
        pronoun_pattern = \
            "^i$|^me$|^my$|^mine$|^myself$|" \
            "^you$|^your$|^yours$|^yourself$|^yourselves$|" \
            "^she$|^her$|^hers$|^herself$|" \
            "^he$|^him$|^his$|^himself$|" \
            "^it$|^its$|^itself$|" \
            "^we$|^our$|^ours$|^ourselves$|" \
            "^they$|^them$|^their$|^theirs$|^themselves$"
        conj_pattern = "^for|^and$|^nor$|^but$|^or$|^yet$|^so$" \
                       "|^after$|^although$|^as$|^because$|^before$|^when$|^where$" \
                       "|^wherever$|^if$|^since$|^than$|^though$|^unless$|^until$" \
                       "|^whenever$|^whereas$|^while$|^either$|^neither$|^both$" \
                       "|^whether$|^just$|^the$|^rather$"

        if re.match(adj_pattern, word):
            self.part_of_speech.append("adj")
        if re.match(noun_pattern, word):
            self.part_of_speech.append("noun")
        if re.match(verb_pattern, word):
            self.part_of_speech.append("verb")
        if re.match(adverb_pattern, word):
            self.part_of_speech.append("adverb")
        if re.match(prep_pattern, word):
            self.part_of_speech.append("prepos")
        if re.match(pronoun_pattern, word):
            self.part_of_speech.append("pronoun")
        if re.match(conj_pattern, word):
            self.part_of_speech.append("conj+")

        return self.part_of_speech

    # PORTER ALGORITHM STEPS

    # get rid of plurals and -ed or -ing
    def step1(self):
        if self.buffer[self.last] == "s":
            if self.ends_with("sses"):
                self.last = self.last - 2
            elif self.ends_with("ies"):
                self.set_to("i")
            elif self.buffer[self.last - 1] != "s":
                self.last = self.last - 1
                step = "Remove -s."
                self.steps.append(step)
        elif self.ends_with("eed"):
            if self.measure_clusters() > 0:
                self.last = self.last - 1
        elif (self.ends_with("ed") or self.ends_with("ing")) and self.vowel():
            self.last = self.j
            if self.ends_with("at"):
                self.set_to("ate")
            elif self.ends_with("bl"):
                self.set_to("ble")
            elif self.ends_with("iz"):
                self.set_to("ize")
            elif self.double_consonant(self.last):
                self.last = self.last - 1
                character = self.buffer[self.last]
                if character == "l" or character == "s" or character == "z":
                    self.last = self.last + 1
                else:
                    step = "Remove the doubled consonant: " + character + "."
                    self.steps.append(step)
            elif self.measure_clusters() == 1 and self.cvc(self.last):
                self.set_to("e")

    # change -y to -i if word contains a vowel
    def step2(self):
        if self.ends_with("y") and self.vowel():
            self.buffer = self.buffer[:self.last] + list("i") + self.buffer[self.last + 1:]
            step = "Change -y to -i."
            self.steps.append(step)

    # map double suffices to single ones
    def step3(self):
        if self.buffer[self.last - 1] == "a":
            if self.ends_with("ational"):
                self.r("ate")
            elif self.ends_with("tional"):
                self.r("tion")
        elif self.buffer[self.last - 1] == "c":
            if self.ends_with("enci"):
                self.r("ence")
            elif self.ends_with("anci"):
                self.r("ance")
        elif self.buffer[self.last - 1] == "e":
            if self.ends_with("izer"):
                self.r("ize")
        elif self.buffer[self.last - 1] == "l":
            if self.ends_with("bli"):
                self.r("ble")
            elif self.ends_with("alli"):
                self.r("al")
            elif self.ends_with("entli"):
                self.r("ent")
            elif self.ends_with("eli"):
                self.r("e")
            elif self.ends_with("ousli"):
                self.r("ous")
        elif self.buffer[self.last - 1] == "o":
            if self.ends_with("ization"):
                self.r("ize")
            elif self.ends_with("ation"):
                self.r("ate")
            elif self.ends_with("ator"):
                self.r("ate")
        elif self.buffer[self.last - 1] == "s":
            if self.ends_with("alism"):
                self.r("al")
            elif self.ends_with("iveness"):
                self.r("ive")
            elif self.ends_with("fulness"):
                self.r("ful")
            elif self.ends_with("ousness"):
                self.r("ous")
        elif self.buffer[self.last - 1] == "t":
            if self.ends_with("aliti"):
                self.r("al")
            elif self.ends_with("iviti"):
                self.r("ive")
            elif self.ends_with("biliti"):
                self.r("ble")
        elif self.buffer[self.last - 1] == "g":
            if self.ends_with("logi"):
                self.r("log")

    # stems with -ness, -full
    def step4(self):
        if self.buffer[self.last] == "e":
            if self.ends_with("icate"):
                self.r("ic")
            elif self.ends_with("ative"):
                self.r("")
            elif self.ends_with("alize"):
                self.r("al")
        elif self.buffer[self.last] == "i":
            if self.ends_with("iciti"):
                self.r("ic")
        elif self.buffer[self.last] == "l":
            if self.ends_with("ical"):
                self.r("ic")
            elif self.ends_with("ful"):
                self.r("")
        elif self.buffer[self.last] == "s":
            if self.ends_with("ness"):
                self.r("")

    # leave -ant, -ence when <c>vcvc<v>
    def step5(self):
        if self.buffer[self.last - 1] == "a":
            if self.ends_with("al"):
                pass

            else:
                return
        elif self.buffer[self.last - 1] == "c":
            if self.ends_with("ance"):
                pass
                step = "Leave -ance ending."
                self.steps.append(step)
            elif self.ends_with("ence"):
                pass
                step = "Leave -ence ending."
                self.steps.append(step)
            else:
                return
        elif self.buffer[self.last - 1] == "e":
            if self.ends_with("er"):
                pass
                step = "Leave -er ending."
                self.steps.append(step)
            else:
                return
        elif self.buffer[self.last - 1] == "i":
            if self.ends_with("ic"):
                pass
                step = "Leave -ic ending."
                self.steps.append(step)
            else:
                return
        elif self.buffer[self.last - 1] == "l":
            if self.ends_with("able"):
                pass
                step = "Leave -able ending."
                self.steps.append(step)
            elif self.ends_with("ible"):
                pass
                step = "Leave -ible ending."
                self.steps.append(step)
            else:
                return
        elif self.buffer[self.last - 1] == "n":
            if self.ends_with("ant"):
                pass
                step = "Leave -ant ending."
                self.steps.append(step)
            elif self.ends_with("ement"):
                pass
                step = "Leave -ement ending."
                self.steps.append(step)
            elif self.ends_with("ment"):
                pass
                step = "Leave -ment ending."
                self.steps.append(step)
            elif self.ends_with("ent"):
                pass
                step = "Leave -ent ending."
                self.steps.append(step)
            else:
                return
        elif self.buffer[self.last - 1] == "o":
            if self.ends_with("ion") and (self.buffer[self.j] == "s" or self.buffer[self.j] == "t"):
                pass
                step = "Leave -ion ending."
                self.steps.append(step)
            elif self.ends_with("ou"):
                pass
                step = "Leave -ou ending."
                self.steps.append(step)
            else:
                return
        elif self.buffer[self.last - 1] == "s":
            if self.ends_with("ism"):
                pass
                step = "Leave -ism ending."
                self.steps.append(step)
            else:
                return
        elif self.buffer[self.last - 1] == "t":
            if self.ends_with("ate"):
                pass
                step = "Leave -ate ending."
                self.steps.append(step)
            elif self.ends_with("iti"):
                pass
                step = "Leave -iti ending."
                self.steps.append(step)
            else:
                return
        elif self.buffer[self.last - 1] == "u":
            if self.ends_with("ous"):
                pass
                step = "Leave -ous ending."
                self.steps.append(step)
            else:
                return
        elif self.buffer[self.last - 1] == "v":
            if self.ends_with("ive"):
                pass
                step = "Leave -ive ending."
                self.steps.append(step)
            else:
                return
        elif self.buffer[self.last - 1] == "z":
            if self.ends_with("ize"):
                pass
                step = "Leave -ize ending."
                self.steps.append(step)
            else:
                return
        else:
            return
        if self.measure_clusters() > 1:
            self.last = self.j

    # remove an ending -e if measure_clusters() > 1;
    # change ending -ll to -l if measure_clusters() > 1
    def step6(self):
        self.j = self.last
        if self.buffer[self.last] == "e":
            x = self.measure_clusters()
            if x > 1 or (x == 1 and not self.cvc(self.last - 1)):
                self.last = self.last - 1
                step = "Remove -e."
                self.steps.append(step)
        if self.buffer[self.last] == "l" and self.double_consonant(self.last) and self.measure_clusters() > 1:
            self.last = self.last - 1
            step = "Change -ll to -l."
            self.steps.append(step)

    # Stem the word given
    def stem(self):
        self.split_word()

        # copy the parameters into statics
        self.last = (len(self.word)) - 1
        if self.last <= self.first + 1:
            return self.word

        print("> Steps of stemming \"" + self.word + "\":\n")
        self.step1()
        self.step2()
        self.step3()
        self.step4()
        self.step5()
        self.step6()

        self.steps.append("Result: " + "".join(self.buffer[self.first:(self.last + 1)]))

        self.set_pos(self.word)

        if len(self.steps) > 0:
            for step in self.steps:
                print(str(self.steps.index(step) + 1) + ". " + step)
        else:
            print("No steps.")
        print("\n")

        return self.buffer[self.first:(self.last + 1)]
