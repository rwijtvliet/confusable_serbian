# Serbian Look-alikes

In Serbian, 2 alphabets are used: a latin one and a cyrillic one. There is a one-to-one correspondence of the letters in each alphabet. (Well, some cyrillic characters are mapped onto a fixed pair of latin symbols, but these pairs are "considered to be one character" as well. See [Wikipedia](https://en.wikipedia.org/wiki/Serbian_Cyrillic_alphabet) for more information.) 

* Some characters in these alphabets are or look the same (e.g. A <-> A) or essentially the same (e.g. K <-> К), so changing from latin to cyrillic does not affect how the word is written for these characters.

* Most characters, however, have a form in one alphabet that does not exist in the other (e.g. Ф <-> F). It's the presence of these that most obviously 'give away' which alphabet a word is actually written in.  

* There is a third group of characters, and that is those that, in one alphabet, look like a chacaracter in the other that is *does not correspond* to. For example, the latin symbol B (Б in cyrillic) looks like the cyrillic symbol В (V in latin).

This last group of characters are interesting, because it allows for the following situation: there might be words that look like valid words in both cyrillic and latin, but that have distinct meanings. 

This script goes through a word-list and tries to find those words.

## Rules

"Similarity" is somewhat subjective. Here are my rules.

* Comparison is between capitalized characters.

* Ј, А, Е, К, М, О, Т are symbols that are present in both alphabets that denote the same character.

* Н, С, В, Р are symbols that are present in both alphabets that denote distict characters. 


## Result
