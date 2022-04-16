import os
import sys
from itertools import chain
from pathlib import Path
from typing import Set, Dict, List, Optional

if getattr(sys, 'frozen', False):
    application_path = Path(os.path.dirname(sys.executable))
else:
    application_path = Path(os.path.dirname(os.path.abspath(__file__)))


def membean_synonyms(word: str, levels: Optional[Set[int]] = None) -> List[str]:
    if levels:
        return list(
            chain.from_iterable(membean_thesaurus_by_level.get(level, {}).get(word.lower(), []) for level in levels))
    else:
        return full_membean_thesaurus.get(word.lower(), [])


def is_membean_word(word: str, levels: Optional[Set[int]] = None) -> bool:
    if levels:
        return word in chain.from_iterable(membean_words_by_level[level] for level in levels)
    else:
        return word in all_membean_words


membean_words_by_level: Dict[int, Set[str]] = {}
all_membean_words: Set[str] = set()


def cache_membean_words():
    print("Loading membean words...")

    print(application_path)

    with open(application_path/'res'/'MembeanWordlist.txt') as wordlist:
        while line := wordlist.readline():
            level = int(line[6])
            words = line[9:].strip().split()
            membean_words_by_level[level] = set(words)
            all_membean_words.update(words)


membean_thesaurus_by_level: Dict[int, Dict[str, List[str]]] = {}
full_membean_thesaurus: Dict[str, List[str]] = {}


def cache_thesaurus():
    print("Loading thesaurus...")
    with open(application_path/'res'/'MobyWords.txt') as f:
        while line := f.readline():
            word, *synonyms = line.split(',')
            full_membean_thesaurus[word] = [synonym for synonym in synonyms if synonym in all_membean_words]

            for level, membean_words in membean_words_by_level.items():
                if level not in membean_thesaurus_by_level:
                    membean_thesaurus_by_level[level] = {}
                membean_thesaurus_by_level[level][word] = [synonym for synonym in full_membean_thesaurus[word] if
                                                           synonym in membean_words]
