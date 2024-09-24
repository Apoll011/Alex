import re
import random
from core.log import LOG

log = LOG


class Key:
    def __init__(self, word, weight, decomps):
        self.word = word
        self.weight = weight
        self.decomps = decomps


class Decomp:
    def __init__(self, parts, save, reasmbs):
        self.parts = parts
        self.save = save
        self.reasmbs = reasmbs
        self.next_reasmb_index = 0


class Eliza:
    initials: list[str]
    finals: list[str]
    quits: list[str]
    def __init__(self):
        self.initials = []
        self.finals = []
        self.quits = []
        self.pres = {}
        self.posts = {}
        self.synons = {}
        self.keys = {}
        self.memory = []

    def script(self, path):
        key = None
        decomp = None
        with open(path) as file:
            for line in file:
                if not line.strip():
                    continue
                tag, content = [part.strip() for part in line.split(':')]
                if tag == 'initial':
                    self.initials.append(content)
                elif tag == 'final':
                    self.finals.append(content)
                elif tag == 'quit':
                    self.quits.append(content)
                elif tag == 'pre':
                    parts = content.split(' ')
                    self.pres[parts[0]] = parts[1:]
                elif tag == 'post':
                    parts = content.split(' ')
                    self.posts[parts[0]] = parts[1:]
                elif tag == 'synon':
                    parts = content.split(' ')
                    self.synons[parts[0]] = parts
                elif tag == 'key':
                    parts = content.split(' ')
                    word = parts[0]
                    weight = int(parts[1]) if len(parts) > 1 else 1
                    key = Key(word, weight, [])
                    self.keys[word] = key
                elif tag == 'decomp':
                    parts = content.split(' ')
                    save = False
                    if parts[0] == '$':
                        save = True
                        parts = parts[1:]
                    decomp = Decomp(parts, save, [])
                    key.decomps.append(decomp)
                elif tag == 'reasmb':
                    parts = content.split(' ')
                    decomp.reasmbs.append(parts)

    def __match_decomp_r(self, parts, words, results):
        if not parts and not words:
            return True
        if not parts or (not words and parts != ['*']):
            return False
        if parts[0] == '*':
            for index in range(len(words), -1, -1):
                results.append(words[:index])
                if self.__match_decomp_r(parts[1:], words[index:], results):
                    return True
                results.pop()
            return False
        elif parts[0].startswith('@'):
            root = parts[0][1:]
            if not root in self.synons:
                raise ValueError("Unknown synonym root {}".format(root))
            if not words[0].lower() in self.synons[root]:
                return False
            results.append([words[0]])
            return self.__match_decomp_r(parts[1:], words[1:], results)
        elif parts[0].lower() != words[0].lower():
            return False
        else:
            return self.__match_decomp_r(parts[1:], words[1:], results)

    def __match_decomp(self, parts, words):
        results = []
        if self.__match_decomp_r(parts, words, results):
            return results
        return None

    def __next_reasmb(self, decomp):
        index = decomp.next_reasmb_index
        result = decomp.reasmbs[index % len(decomp.reasmbs)]
        decomp.next_reasmb_index = index + 1
        return result

    def __reassemble(self, reasmb, results):
        output = []
        for reword in reasmb:
            if not reword:
                continue
            if reword[0] == '(' and reword[-1] == ')':
                index = int(reword[1:-1])
                if index < 1 or index > len(results):
                    raise ValueError("Invalid result index {}".format(index))
                insert = results[index - 1]
                for punct in [',', '.', ';']:
                    if punct in insert:
                        insert = insert[:insert.index(punct)]
                output.extend(insert)
            else:
                output.append(reword)
        return output

    def __sub(self, words, sub):
        output = []
        for word in words:
            word_lower = word.lower()
            if word_lower in sub:
                output.extend(sub[word_lower])
            else:
                output.append(word)
        return output

    def __match_key(self, words, key):
        for decomp in key.decomps:
            results = self.__match_decomp(decomp.parts, words)
            if results is None:
                log.debug('Decomp did not match: %s', decomp.parts)
                continue
            log.debug('Decomp matched: %s', decomp.parts)
            log.debug('Decomp results: %s', results)
            results = [self.__sub(words, self.posts) for words in results]
            log.debug('Decomp results after posts: %s', results)
            reasmb = self.__next_reasmb(decomp)
            log.debug('Using reassembly: %s', reasmb)
            if reasmb[0] == 'goto':
                goto_key = reasmb[1]
                if not goto_key in self.keys:
                    raise ValueError("Invalid goto key {}".format(goto_key))
                log.debug('Goto key: %s', goto_key)
                return self.__match_key(words, self.keys[goto_key])
            output = self.__reassemble(reasmb, results)
            if decomp.save:
                self.memory.append(output)
                log.debug('Saved to memory: %s', output)
                continue
            return output
        return None

    def respond(self, text):
        if text.lower() in self.quits:
            return None

        text = re.sub(r'\s*\.+\s*', ' . ', text)
        text = re.sub(r'\s*,+\s*', ' , ', text)
        text = re.sub(r'\s*;+\s*', ' ; ', text)
        log.debug('After punctuation cleanup: %s', text)

        words = [w for w in text.split(' ') if w]
        log.debug('Input: %s', words)

        words = self.__sub(words, self.pres)
        log.debug('After pre-substitution: %s', words)

        keys = [self.keys[w.lower()] for w in words if w.lower() in self.keys]
        keys = sorted(keys, key=lambda k: -k.weight)
        log.debug('Sorted keys: %s', [(k.word, k.weight) for k in keys])

        output = None

        for key in keys:
            output = self.__match_key(words, key)
            if output:
                log.debug('Output from key: %s', output)
                break
        if not output:
            if self.memory:
                index = random.randrange(len(self.memory))
                output = self.memory.pop(index)
                log.debug('Output from memory: %s', output)
            else:
                output = self.__next_reasmb(self.keys['xnone'].decomps[0])
                log.debug('Output from xnone: %s', output)

        return " ".join(output)

    def initial(self):
        return random.choice(self.initials)

    def final(self):
        return random.choice(self.finals)

    def run(self):
        print(self.initial())

        while True:
            sent = input('> ')

            output = self.respond(sent)
            if output is None:
                break

            print(output)

        print(self.final())
