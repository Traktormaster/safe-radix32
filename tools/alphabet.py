"""
Alphabet generator and tester for safe_radix32.

:copyright: 2021 Nándor Mátravölgyi
:license: Apache2, see LICENSE for more details.
"""
import itertools
import os
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))


def create_alphabet():
    a = set(
        chr(i)
        for i in itertools.chain(
            range(ord("0"), ord("9") + 1), range(ord("A"), ord("Z") + 1), range(ord("a"), ord("z") + 1)
        )
    )
    # vowel elimination
    a.difference_update(list("aAeEiIoOuU"))
    # visually similar eliminations of vowels and high frequency consonants
    a.difference_update(list("oO0"))
    a.difference_update(list("iI1l"))  # capital "L" is not removed
    a.difference_update(list("sS5"))
    # letter frequency eliminations (https://en.wikipedia.org/wiki/Letter_frequency)
    a.difference_update(list("tT"))
    a.difference_update(list("nN"))
    a.difference_update(list("hH"))
    a.difference_update(list("rR"))
    a.difference_update(list("dD"))
    # "X" is eliminated in spite of the lower frequency to avoid "xxx".
    a.difference_update(list("xX"))
    # "Y" is eliminated in spite of the lower frequency because it often plays a vowel-like role in words.
    a.difference_update(list("yY"))

    # Further H4x0r-like number replacements are ignored. For example:
    # If someone wishes to read "G4Y" as "GAY" then it's their choosing. The string is "G"-"four"-"Y" and not "gay".

    return a


def included_words(alphabet):
    words_path = os.path.join(HERE, "words.txt")
    if not os.path.exists(words_path):
        with open(words_path, "wb") as f:
            f.write(
                urllib.request.urlopen("https://github.com/dwyl/english-words/blob/master/words.txt?raw=true").read()
            )
    with open(words_path, "r") as f:
        lines = f.read().replace("\r", "").split("\n")
    included = []
    for line in lines:
        if line.isupper():  # skip all-capital words, we can't avoid all acronyms
            continue
        if all(c in alphabet for c in line):
            included.append(line)
    return included


if __name__ == "__main__":
    a = create_alphabet()
    ws = included_words(a)
    for w in ws:
        print(w)
    print("---")
    print("Alphabet size:", len(a))
    print("Alphabet:", "".join(sorted(a)))
    print("Included words:", len(ws), "(see above)")
