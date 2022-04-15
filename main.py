from UI import get_essay, get_levels
from words import membean_synonyms, is_membean_word, cache_membean_words, cache_thesaurus

try:
    from termcolor import colored
except ModuleNotFoundError:
    print("Termcolor not found; will use plain colors.")
    def colored(text, *args, **kwargs): return text


if __name__ == '__main__':
    print("Ready!")
    cache_membean_words()
    cache_thesaurus()

    essay = get_essay()
    levels = get_levels()

    word_count = len(essay)

    membean_words_in_essay = []
    replacement_candidates_count = 0
    for word in essay:
        word_count += 1
        synonyms = membean_synonyms(word.text, levels)

        if len(synonyms) > 0:
            formatted_word = colored(word.text, "red", attrs=["bold"])
            formatted_word_counts = ", ".join([colored(f"#{i}", "green") for i in word.indices])

            if is_membean_word(word.text, levels):
                membean_words_in_essay.append(word.text)
                print(
                    f'{formatted_word} (word(s) {formatted_word_counts})'
                    f' is already a membean word!')
            else:
                formatted_replacements = ", ".join([colored(word, "blue") for word in synonyms])
                print(
                    f'{formatted_word} (word(s) {formatted_word_counts}) could be '
                    f'replaced with one of: {formatted_replacements}')
            replacement_candidates_count += 1

    print(f"Found {colored(f'{replacement_candidates_count}/{word_count}', 'red', attrs=['bold'])} "
          f"word(s) with possible membean word replacements "
          f"({replacement_candidates_count/word_count*100:.2f}% of the essay).")
    print(f"Found {colored(len(set(membean_words_in_essay)), 'red', attrs=['bold'])} "
          f"distinct membean word(s) already in the essay: "
          f"{colored(', '.join(set(membean_words_in_essay)), attrs=['bold'])}")
