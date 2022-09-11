# Confusable Serbian

In Serbian, 2 alphabets are used: a latin one and a cyrillic one. There is a one-to-one correspondence of the letters  in each alphabet. This means that any "character" has a "cyrillic symbol" and a "latin symbol". (Well, some latin symbols are actually two symbols, but these pairs are "considered to be one character" as well. See [Wikipedia](https://en.wikipedia.org/wiki/Serbian_Cyrillic_alphabet) for more information.) 

We can divide the characters up into 3 groups:

* Group 0. Most characters use a symbol in one alphabet that does not exist in the other (e.g. Ф <-> F). It's the presence of these characters that most obviously 'gives away' which alphabet a word is actually written in.

* Group 1. Some characters use symbols are or look the same (e.g. A <-> A) or essentially the same (e.g. K <-> К) in both alphabets. If a word consists entirely of these characters, we cannot tell if it is written in the latin or cyrillic alphabet, but this does not significantly matter as it has the same meaning. 

* Group 2. There is a third group of characters, and that is those that, in one alphabet, use a symbol that looks like the symbol used by a *different* chacaracter in the other alphabet. For example, the latin symbol B (Б in cyrillic) looks like the cyrillic symbol В (V in latin).

This last group of characters is interesting, because it allows for the following situation: there might be words that look like valid words in both cyrillic and latin, but that have distinct meanings.

This script goes through a word-list and tries to find those words.

## Rules

"Similarity" is somewhat subjective. Here are my rules.

* Comparison is between capitalized characters.

* Ј, А, Е, К, М, О, Т are symbols that are present in both alphabets that denote the same character.

* Н, С, В, Р are symbols that are present in both alphabets that denote distict characters. 

## Result

286 of these words are found, see `group2_confusable.txt`. Some are short or abbreviations, but many are actually "confusable". For example:

* "РОТОР" ('ротор' in lower case) in cyrillic is pronounced like the english "rotor" and means as much. 
* "POTOP" ('potop' in lower case) in latin is pronounced "potop" and means "flood".

Now, I don't actually speak Serbian :) and the translation part of the script depends on `googletrans` which was not working at the time of writing this. Maybe I'll get back to it. 
