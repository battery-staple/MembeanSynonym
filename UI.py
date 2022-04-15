import re
from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Set

try:
    import pyperclip

    pyperclip_available = True
except ModuleNotFoundError:
    print("Pyperclip not found; you'll have to enter your essay manually.")
    pyperclip_available = False


@dataclass
class Word:
    text: str
    indices: List[int]


def get_essay() -> List[Word]:
    essay_words_text = re.split(r'\W+', __get_essay_text())
    essay_words_to_indices: Dict[str, List[int]] = dict()
    for i, text in enumerate(essay_words_text):
        key = text.strip(',.;"\' \n\r\t')
        if key in essay_words_to_indices:
            essay_words_to_indices[key].append(i + 1)
        else:
            essay_words_to_indices[key] = [i + 1]

    return [Word(text, indices) for (text, indices) in essay_words_to_indices.items()]


def get_levels() -> Set[int]:
    levels_text = input(
        "Which membean levels would you like to include? Enter a comma separated list, "
        "or press enter to include words from all levels.\n"
    )
    return set(int(level.strip()) for level in levels_text.split(',')) if levels_text.strip() != '' else None


class InputType(Enum):
    Manual = 'm'
    Clipboard = 'c'


def __get_input_type() -> InputType:
    if not pyperclip_available:
        return InputType.Manual

    input_type_string = input(
        "How do you want to input your essay (type 'c' to get it from your clipboard; "
        "type 'm' to type/paste it in manually)\n"
    ).lower()

    while input_type_string not in [t.value for t in InputType]:
        input_type_string = input("Invalid input type. Try inputting 'c' or 'm'.\n").lower()

    return InputType(input_type_string)


def __get_essay_text() -> str:
    if __get_input_type() == InputType.Manual:
        essay = input("Paste in the text to analyze (press enter twice to mark the end):\n")
        while (line := input()) != '':
            essay += line
    else:
        print("Copy your text, and press enter (without typing anything else) when ready.")
        input()
        essay = pyperclip.paste()
        print("Got the following:")
        print(essay)
        print()
    return essay
