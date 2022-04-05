from typing import Dict, List


def select_language(available_languages: set[str]):
    if len(available_languages) == 1:
        language = next(iter(available_languages))
        print(f"Using language \"{language}\"")
    else:
        selected_language = input(f"Select language [{','.join(available_languages)}]: ").strip().lower()
        if selected_language not in available_languages:
            raise Exception(f"Language \"{selected_language}\" not available")
        else:
            language = selected_language

    return language


def determine_level(levels: list[str]):
    level: str = input(f"Level [{','.join(levels)}]: ").strip().lower()
    if level not in levels:
        raise Exception(f"Level \"{level}\" not available")
    return level, levels


def determine_language(config, level, levels):
    urls: Dict[str, Dict[str, List[str]]] = config["urls"]
    level_index = levels.index(level)
    if level_index == 0:
        continue_anyway = input("No previous level found. continue anyway [Y/n]? ").lower() in {"", "y", "yes"}
        if not continue_anyway:
            raise Exception("TODO")
        available_languages = set(urls[level].keys())
    else:
        prev_level = levels[level_index - 1]
        available_languages = set(urls[level].keys()).intersection(urls[prev_level].keys())
    language = select_language(available_languages)
    return language