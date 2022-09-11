"""Script to find 'confusable' words in Serbian."""

from typing import Iterator
from tqdm import tqdm
from googletrans import Translator

correspondence_c2l = {
    "А": "A",
    "Б": "B",
    "В": "V",
    "Г": "G",
    "Д": "D",
    "Ђ": "Đ",
    "Е": "E",
    "Ж": "Ž",
    "З": "Z",
    "И": "I",
    "Ј": "J",
    "К": "K",
    "Л": "L",
    "Љ": "LJ",  # made both uppercase
    "М": "M",
    "Н": "N",
    "Њ": "NJ",  # mode both uppercase
    "О": "O",
    "П": "P",
    "Р": "R",
    "С": "S",
    "Т": "T",
    "Ћ": "Ć",
    "У": "U",
    "Ф": "F",
    "Х": "H",
    "Ц": "C",
    "Ч": "Č",
    "Џ": "DŽ",  # made both uppercase
    "Ш": "Š",
}

lookalike_c2l = {
    "А": "A",
    "В": "B",
    "Е": "E",
    "Ј": "J",
    "К": "K",
    "М": "M",
    "Н": "H",
    "О": "O",
    "Р": "P",
    "С": "C",
    "Т": "T",
}

alphabet_c = list(correspondence_c2l.keys())
alphabet_l = list(correspondence_c2l.values())

two_symbol_latin = {w for w in correspondence_c2l.values() if len(w) > 1}


def cyrillic_to_lookalike_latin(word: str) -> str:
    """In word (in cyrillic characters), replace the characters that have a latin look-
    alike by their lookalike."""
    return "".join(lookalike_c2l.get(c, c) for c in word)


def word_generator(input_cyr: bool, group: int) -> Iterator[str]:
    """Generator of serbian words in cyrillic (if ``input_cyr == True``) or latin (False)
    (called the "source language"), that fulfil the following conditions:
    * group == 0: words contain at least 1 symbol that does not exist in the other alphabet.
    The word is clearly written in source alphabet. This is the vast majority of words in
    the source list.
    * group == 1: words only contain symbols that also exist in the other alphabet, and all
    symbols refer to the same characters in cyrillic and latin. So, the word exists
    "in both alphabets" and is only slightly interesting, in that it's not clear from
    reading it, if it is written with latin or cyrillic characters.
    * group == 2: words only contain symbols that also exist in the other alphabet, and at
    least 1 symbol refers to a different character in that other alphabet. The word
    requires further processing to see if the word it looks like in the other alphabet is
    a "valid" word (i.e., actually means something in serbian).
    """
    if input_cyr:
        file = "source/serbian-cyrillic.txt"
        lookslike_samechar = set(
            [c for c, l in lookalike_c2l.items() if correspondence_c2l[c] == l]
        )
        lookslike_diffchar = set(
            [c for c, l in lookalike_c2l.items() if correspondence_c2l[c] != l]
        )
    else:
        file = "source/serbian-latin.txt"
        lookslike_samechar = set(
            [l for c, l in lookalike_c2l.items() if correspondence_c2l[c] == l]
        )
        lookslike_diffchar = set(
            [l for c, l in lookalike_c2l.items() if correspondence_c2l[c] != l]
        )
        # We don't need to worry about the 2-symbol latin characters, as all of them have
        # at least 1 symbol that is not present in cyrillic.

    def group_char(c: str) -> int:
        """Returns 0 if symbol ``c`` is unambiguously in source alphabet, 1 if its denotes
        a character whose symbol is similarly looking in the both alphabets, 2 if its
        denotes a character that could be mistaken for a different character (i.e., with
        a similar symbol) in the target alphabet."""
        if c in lookslike_diffchar:
            return 2
        if c in lookslike_samechar:
            return 1
        return 0

    def group_word(word: str) -> int:
        """Returns 0 if word ``word`` is unambiguously in source alphabet (because at least
        one of its characters is), 1 if it consists entirely of symbols that denote the same
        character in both alphabets, 2 if it consists entirely of symbols that exist in both
        alphabets with at least one of them denoting distinct characters."""
        includes_group2 = False
        for c in word:
            chargroup = group_char(c)
            if chargroup == 0:
                return 0
            elif not includes_group2 and chargroup == 2:
                includes_group2 = True
        # None of the characters is in group 0.
        return 2 if includes_group2 else 1

    candidates = open(file, encoding="utf-8")

    while True:
        word = candidates.readline().removesuffix("\n").upper()
        if not len(word):
            break  # end of file
        if group_word(word) == group:
            yield word


def find_and_save(iterator: Iterator[str], filename: str) -> None:
    """Loop through iterator and save each item to file."""
    with open(filename, "w", encoding="utf-8") as f:
        for word in iterator:
            f.write(word + "\n")


# Check: list of words in group 1 should be identical - whether starting from
# latin or cyrillic, the words that only use group-1 characters are valid words in both
# languages. The lists are probably not exactly identical, because they come from "imperfect"
# sources.

# . Find.
group1_cyrillic = word_generator(True, 1)
find_and_save(group1_cyrillic, "group1_cyrillic.txt")
group1_latin = word_generator(False, 1)
find_and_save(group1_latin, "group1_latin.txt")

# . Compare.
gr1_lat = {
    word.removesuffix("\n") for word in open("group1_latin.txt", "r").readlines()
}
gr1_cyr = {
    word.removesuffix("\n") for word in open("group1_cyrillic.txt", "r").readlines()
}
gr2_c_as_l = {cyrillic_to_lookalike_latin(word) for word in gr1_cyr}

both = gr1_lat.intersection(gr2_c_as_l)  # Should be near 100%
just_lat = gr1_lat.difference(gr2_c_as_l)
just_cyr = gr2_c_as_l.difference(gr1_lat)

# . Results.
print("---Group 1---")
print(
    f"Found in latin dictionary: {len(gr1_lat)}. Found in cyrillic dictionary: {len(gr1_cyr)}."
)
print(
    f"Found in both: {len(both)}. Only found in latin dictionary: {len(just_lat)} (= {len(just_lat)/len(gr1_lat):.2%}). Only found in cyrillic dictionary: {len(just_cyr)} (= {len(just_cyr)/len(gr1_cyr):.2%})."
)
if len(just_lat):
    subset = [word for i, word in enumerate(just_lat) if i < 100]
    print(
        f"A few examples of words that are only in the latin dictionary: {', '.join(subset)}."
    )
if len(just_cyr):
    subset = [word for i, word in enumerate(just_cyr) if i < 100]
    print(
        f"A few examples of words that are only in the cyrillic dictionary: {', '.join(subset)}."
    )

find_and_save(both, "group1_both.txt")


# Real purpose: list of words that mean distinct things in both alphabets.
# Method: get list of words in group 2 for each alphabet. These groups will be very different.
# Then go through 1 of the lists, and for each word, see if it exists in the other. Will
# be a VERY small percentage of the words.

# . Find.
group2_cyrillic = word_generator(True, 2)
find_and_save(group2_cyrillic, "group2_cyrillic.txt")
group2_latin = word_generator(False, 2)
find_and_save(group2_latin, "group2_latin.txt")

# . Compare.
gr2_lat = {
    word.removesuffix("\n") for word in open("group2_latin.txt", "r").readlines()
}
gr2_cyr = {
    word.removesuffix("\n") for word in open("group2_cyrillic.txt", "r").readlines()
}
gr2_c_as_l = {cyrillic_to_lookalike_latin(word) for word in gr2_cyr}
hits = []
for cyr in gr2_cyr:
    c_as_l = cyrillic_to_lookalike_latin(cyr)
    if c_as_l in gr2_lat:
        hits.append(cyr)

# . Results.
print("---Group 2---")
print(
    f"Candidates in latin dictionary: {len(gr2_lat)}. Candidates in cyrillic dictionary: {len(gr2_cyr)}."
)
nl = "\n"
print(f"Confusable words found: {len(hits)}: {nl}{', '.join(hits)}")
find_and_save(hits, "group2_confusable.txt")

# . Translate.
translator = Translator()


def meaning_in_english(word_in_serbian: str) -> str:
    result = translator.translate(word_in_serbian, src="sr")
    return result.text


hits_incl_translation = []
for cyr in hits:
    c_as_l = cyrillic_to_lookalike_latin(cyr)
    hits_incl_translation.append(
        {
            "cyrillic": {"word": cyr, "meaning": meaning_in_english(cyr)},
            "latin": {"word": c_as_l, "meaning": meaning_in_english(c_as_l)},
        }
    )


def present_result(hit) -> str:
    return "\n".join(
        [
            f"{hit['latin']['word']}:",
            f"- latin: {hit['latin']['meaning']}",
            f"- cyril: {hit['cyrillic']['meaning']}",
        ]
    )


# . Results.
for hit in hits_incl_translation:
    print(present_result(hit))

find_and_save(hits_incl_translation, "group2_confusable_incl_translation.txt")
