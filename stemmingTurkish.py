import string


class StemmingTurkish:
    def __init__(self, text) -> None:
        self.text = text.lower()
        self.word_list = self.text.split(' ')
        self.roots_words = []
        self.root = None
        self.punc = set(string.punctuation)
        self.number = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        with open("sw.txt", encoding='utf-8') as f:
            stop_words = f.read().split()
        self.stop_words = stop_words
        with open("ComparaisonSuffix.txt", encoding='utf-8') as f:
            ComparaisonSuffix = f.read().split()
        self.ComparaisonSuffix = ComparaisonSuffix
        with open("NewSuffixTimePerso.txt", encoding='utf-8') as f:
            TimeSuffix = f.read().split()
        self.TimeSuffix = TimeSuffix
        with open("KipSuffix.txt", encoding='utf-8') as f:
            KipSuffix = f.read().split()
        self.KipSuffix = KipSuffix
        with open("Adjectıve-Noun.txt", encoding='utf-8') as f:
            AdjNoun = f.read().split()
        self.AdjNoun = AdjNoun
        with open("yapımeki.txt", encoding='utf-8') as f:
            ProductSuffix = f.read().split()
        self.ProductSuffix = ProductSuffix
        with open("mekmakilebitenkelimeler.txt", encoding='utf-8') as f:
            EndMakSuffix = f.read().split()

        self.EndMakSuffix = EndMakSuffix

        with open("ZarfFiil.txt", encoding='utf-8') as f:
            ZarfFiil = f.read().split()

        self.ZarfFiil = ZarfFiil


        with open("stopwods.txt", encoding='utf-8') as f:
            StopWords = f.read().split()

        self.sw = StopWords

        with open("ifsuffix.txt", encoding='utf-8') as f:
            ifSuffix = f.read().split()

        self.ifSuffix = ifSuffix

        with open("questionsuffix.txt", encoding='utf-8') as f:
            questSuffix = f.read().split()

        self.questSuffix = questSuffix

        with open("negationTimeSuffix.txt", encoding='utf-8') as f:
            NegationTimeSuffix = f.read().split()

        self.NegationTimeSuffix = NegationTimeSuffix

        self.theStatusCaseSuffix = ['i', 'ı', 'u', 'ü', 'nı', 'ni', 'nu', 'nü', 'mı', 'mi', 'mu', 'mü', 'si', 'su', 'sü', 'si']
        self.EndLetter = 'bgdc'
        self.Vowels = 'aeiouüö'
        self.deepVowels = 'eiöü'
        self.lowVowels = 'aıou'
        self.end_change = {'b': 'p', 'g': 'k', 'd': 't', 'c': 'ç'}
        self.end_change_2 = {'p': 'b', 'k': 'ğ', 't': 'd'}
        self.ABC = 'abcçdefgğhıijklmnoöprsştuüvyzwxqABCÇDEFGĞHIİJKLMNOÖPRSŞTUÜVYZXWQ'
        self.result = ""
        self.syllables = []
        self.result_syllables = []
        self.negative_words = []

    @staticmethod
    def isConsonant(letter):
        if letter not in "aeiıoöuüAEIUOÜÖİ":
            return True
        return False

    def convert_to_binary(self, words):
        s = []
        for i in range(len(words)):

            if len(s) == 0:
                if self.isConsonant(words[i]):
                    s.append(1)
                else:
                    try:
                        if self.isConsonant(words[i + 2]) is not True:
                            s.append(0)
                            self.syllables.append(s)
                            s = []
                        else:
                            s.append(0)
                    except IndexError:
                        s.append(0)

            else:
                if s[-1] == 1 and self.isConsonant(words[i]):
                    self.syllables.append(s)
                    s = [1]


                elif s[-1] == 1 and self.isConsonant(words[i]) is not True:
                    if 0 in s:
                        self.syllables.append(s)
                        s = [0]
                    else:
                        s.append(0)

                elif s[-1] == 0 and self.isConsonant(words[i]) is not True:
                    self.syllables.append(s)
                    s = [0]


                else:
                    try:
                        if self.isConsonant(words[i + 1]):
                            s.append(1)
                        else:
                            self.syllables.append(s)

                            s = [1]
                    except IndexError:
                        s.append(1)
                        self.syllables.append(s)
                        s = []
        if len(s) != 0:
            self.syllables.append(s)

        del_index = []
        for j in range(1, len(self.syllables)):
            if len(self.syllables[j]) == 1:
                del_index.append(j)
                self.syllables[j - 1].insert(len(self.syllables[j - 1]), self.syllables[j][0])
                self.syllables[j].clear()

        if del_index:
            for i in del_index:
                self.syllables.pop(i)

    def convert_to_words(self, words):
        min_index = 0
        max_index = 0
        for i in range(len(self.syllables)):
            length = len(self.syllables[i])
            max_index += length
            syllable = words[min_index: max_index]
            self.result_syllables.append(syllable)
            min_index += length

    def get_result(self, words):
        self.convert_to_binary(words)
        self.convert_to_words(words)

        return self.result_syllables

    def word_by_word_with_tokenization(self):

        result = []

        for word in self.word_list:
            w = ''
            for letter in word:
                if letter in self.ABC:
                    w += letter.lower()

            if len(w) > 3 and w not in self.stop_words:
                result.append(w)

        return result

    def first_control_verb(self, x):
        if 'mek' in x[1:]:
            new_word = self.control_end(x.split('mek')[0])
            return new_word
        elif 'mak' in x[1:]:
            new_word = self.control_end(x.split('mak')[0])
            return new_word
        else:
            for word in self.EndMakSuffix:
                if word in x:
                    if word[-1] == 'ğ':
                        new_word = word[:-1] + 'k'
                        return new_word
                    else:
                        return word
                else:
                    continue
            return False

    def first_control_adj_noun(self, x):
        result = []

        for word in self.AdjNoun:
            t = len(word)
            if len(x) >= t:
                if word == x[:t]:
                    result.append(word)

                else:
                    if x[t-1] in self.EndLetter:
                        if x[t-1:] not in self.TimeSuffix:
                            new = x[:t-1] + str(self.end_change[x[t-1]])
                            if word in new:
                                result.append(word)


        if result:
            result = sorted(result, key=len)
            return result[-1]
        else:
            return False

    def existe_comparaison(self, x):
        result = []

        for suffix in self.ComparaisonSuffix:
            t = len(suffix)
            if len(x) > t:
                if suffix == x[-t:]:
                    result.append(x[:len(x)-t])
        if result:
            result = sorted(result, key=len)
            new = self.control_end(result[0])
            return new
        else:
            return x

    def existe_adj_noun(self, x):

        result_first = []
        for n in self.AdjNoun:
            t = len(n)
            if n in x[:t]:
                result_first.append([n, t])
        if result_first:
            k = [j[1] for j in result_first]
            m = max(k)
            r = result_first[k.index(m)][0]
            return r, True, False
        else:
            result = []
            for suffix in self.ProductSuffix:
                t = len(suffix)
                if len(x) > t:
                    if suffix == x[-t:]:
                        result.append(x[:len(x) - t])
            if result:
                result = sorted(result, key=len)
                new_word = result[0]
                if new_word in self.AdjNoun:
                    return new_word, True, True
                else:
                    return new_word, False, True


            else:
                result = []
                for word in self.AdjNoun:
                    if word[-1] in 'pkt':
                        new = word[:-1] + self.end_change_2[word[-1]]
                        if len(x) > len(new) and new in x[:len(new)]:
                            result.append(word)

                if result:
                    result = sorted(result, key=len)
                    return result[-1], False, True
                else:
                    return x, False, False

    def existe_time_suffix(self, x):
        result = []
        suffix_result = []
        for suffix in self.TimeSuffix:
            t = len(suffix)
            try:
                if len(x) > t + 1:
                    if suffix == x[-t:]:
                        result.append(x[:len(x) - t])
                        suffix_result.append(suffix)
                else:
                    if suffix == x[-t:]:
                        if x[:len(x)-t] == 'o':
                            result.append(x[:len(x) - t])
                            suffix_result.append(suffix)
            except IndexError or TypeError:
                return False

        if result:
            result = sorted(result, key=len)
            suffix_result = sorted(suffix_result, key=len)
            new = self.control_end(result[0])
            if new[-1] == 'y':
                new = new[:-1]
            if suffix_result[-1] in self.NegationTimeSuffix:
                self.negative_words.append(new)
            return new


        else:
            return False

    def existe_kip_suffix(self, x):
        result = []

        for suffix in self.KipSuffix:
            t = len(suffix)
            if len(x) > t+1:
                if suffix in x[-t:]:
                    result.append(x[:len(x)-t])
        if result:
            result = sorted(result, key=len)
            return result[0]
        else:
            return False

    def existe_question_suffix(self, x):
        result = []
        for suffix in self.questSuffix:
            t = len(suffix)
            if len(x) >= t:
                if suffix == x[-t:]:
                    if len(x) == t:
                        return ""
                    else:
                        result.append(x[:len(x) - t])
        if result:
            result = sorted(result, key=len)
            return result[0]
        else:
            return x

    def existe_if_suffix(self, x):
        result = []
        for suffix in self.ifSuffix:
            t = len(suffix)
            if len(x) > t:
                if suffix == x[-t:]:
                    result.append(x[:len(x) - t])

        if result:
            result = sorted(result, key=len)
            return result[0]
        else:
            return x

    def control_end(self, x):
        if len(x) >= 3:
            # if x[-1] == 'm' and x[-2] not in self.Vowels:
            # if x[-3] in self.deepVowels:
            # x += 'e'
            # else:
            # x += 'a'
            # return x

            if x[-3:] in ['luy', 'lüy', 'lıy', 'liy']:
                x = x[:-1]
                return x
            else:
                try:
                    if x[-1] in self.EndLetter:
                        new_word = x.replace(x[-1], self.end_change[x[-1]])
                        return new_word
                    else:
                        return x
                except IndexError:
                    return x
        else:
            if len(x) > 1:
                try:
                    if x[-1] in self.EndLetter:
                        new_word = x.replace(x[-1], self.end_change[x[-1]])
                        return new_word
                    else:
                        return x
                except IndexError:
                    return x

    def control_adj(self, x):
        for word in self.AdjNoun:
            t = len(word)
            if len(x) >= t and word in x[:t]:
                return True
            else:
                continue
        return False

    @staticmethod
    def control_end_2(x):
        list_control_letters = []
        letters_list = list(x)
        k = []
        for i in range(len(letters_list) - 1):
            if letters_list[i] == letters_list[i + 1]:
                k.append(i)
            else:
                list_control_letters.append(k)
                k = []
        if k:
            list_control_letters.append(k)
        list_delete = []
        for j in range(len(list_control_letters)):
            if j == 0 or j == len(list_control_letters) - 1:
                if len(list_control_letters[j]) > 0:
                    list_delete.extend(list_control_letters[j])
            else:
                if len(list_control_letters[j]) > 1:
                    list_delete.extend(list_control_letters[j])

        if list_delete:
            new = ''
            for j in range(len(x)):
                if j not in list_delete:
                    new += x[j]
            return new
        else:
            return x

    # ini imi vs
    def delete_some_suffix_for_adj_noun(self, x):
        k = []
        for i in x:
            if i in self.Vowels:
                k.append(i)

        if k and (k[-1] == k[-2]):
            if x[-2] in "mn":
                new = x[:-3]
                new = self.control_end(new)
                return new
            elif x[-2] == 'y':
                new = x[:-2]
                return new
            else:
                return False
        return False

    def convert_to_verb(self, x):

        theLetters = []

        for j in list(x):
            if j in self.Vowels:
                theLetters.append(j)

        if theLetters:
            if theLetters[-1] in self.deepVowels:
                if 'mek' not in x[1:]:
                    new = x + 'mek'
                    return new
            else:
                if 'mak' not in x[1:]:
                    new = x + 'mak'
                    return new
        else:
            return x

    def StatuCaseSuffix(self, x):
        if x[-2:] in self.theStatusCaseSuffix:
            new = x[:-2]

            return new
        else:
            return False

    def ZarfFiilControl(self, x):
        for i in self.ZarfFiil:
            t = len(i)
            if x[-t:] == i:
                new = x[:-t]
                if new[-1] == 'y':
                    new = new[:-1]
                    return new
                else:
                    return new
            else:
                continue
        return False

    def stemming(self):
        result = []
        text_list = self.word_list
        for word in text_list:
            self.negative_words = []
            self.root = None
            result_verb = []
            result_adj_noun = []
            new = word

            if self.first_control_verb(new) is not False:
                self.root = self.first_control_verb(new)
                self.root = self.convert_to_verb(self.root)

            elif self.first_control_adj_noun(new) is not False:
                self.root = self.first_control_adj_noun(new)

            else:

                new = self.control_end_2(word)
                if self.control_adj(new) is not False:
                    self.root = self.existe_adj_noun(new)[0]
                else:
                    if self.control_adj(word) is not False:
                        self.root = self.existe_adj_noun(word)[0]
                        new = word

                result_verb.append(new)
                new = self.existe_if_suffix(new)
                result_verb.append(new)
                new = self.existe_comparaison(new)
                result_verb.append(new)
                for h in range(result_verb.count(word)):
                    result_verb.remove(word)
                try:
                    if self.existe_time_suffix(new) is not False:
                        new_word = self.existe_time_suffix(new)
                        result_verb.append(new_word)
                        if self.control_adj(new_word) is not True:
                            new_word_2 = self.existe_kip_suffix(new_word)
                            if new_word_2 is not False:
                                result_verb.append(new_word_2)

                            else:
                                result_verb.append(new_word)
                        else:
                            result_adj_noun.append(self.existe_adj_noun(new_word)[0])

                    else:

                        new_word = self.existe_kip_suffix(new)
                        if new_word is not False:
                            result_verb.append(new_word)
                            if self.control_adj(new_word) is not False:
                                result_adj_noun.append(self.existe_adj_noun(new_word)[0])

                    if (self.existe_adj_noun(new)[1], self.existe_adj_noun(new)[2]) != (False, False):

                        if (self.existe_adj_noun(new)[1], self.existe_adj_noun(new)[2]) == (True, True):
                            self.root = self.existe_adj_noun(new)[0]
                        else:
                            result_adj_noun.append(self.existe_adj_noun(new)[0])
                except TypeError:
                    continue
            # if self.negative_words:
                #result.append('-negative-')

            if self.root is None:
                if result_verb and result_adj_noun:

                    k = [len(i) for i in result_verb]
                    k1 = [len(i) for i in result_adj_noun]
                    m = min(k)
                    m1 = max(k1)
                    if m <= m1:
                        # a = self.convert_to_verb(result_verb[k.index(m)])
                        result.append(result_verb[k.index(m)])
                    else:
                        result.append(result_adj_noun[k1.index(m1)])
                else:
                    if result_verb:
                        k = [len(i) for i in result_verb]
                        m = min(k)
                        # a = self.convert_to_verb(result_verb[k.index(m)])
                        result.append(result_verb[k.index(m)])
                    elif result_adj_noun:
                        k1 = [len(i) for i in result_adj_noun]
                        m1 = max(k1)
                        result.append(result_adj_noun[k1.index(m1)])
                    else:
                        if self.ZarfFiilControl(new) is not False:
                            new = self.ZarfFiilControl(new)
                            result.append(new)

                        elif self.StatuCaseSuffix(new) is not False:
                            new = self.StatuCaseSuffix(new)
                            result.append(new)
                        else:
                            result.append(new)

            else:
                result.append(self.root)

        for i in result:
            if i == '-negative-':
                self.result += '-n-'
            else:
                if len(i) >= 2:
                    self.result += i
                    self.result += ' '
                else:
                    if len(i) > 0:
                        if i[0] in self.Vowels:
                            self.result += i
                            self.result += ' '

        return self.result

