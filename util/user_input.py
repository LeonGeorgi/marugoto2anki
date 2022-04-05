from util.config import Config


def ask_user_for_language(available_languages: set[str]) -> str:
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


def ask_user_for_level(available_levels: list[str]):
    level: str = input(f"Level [{','.join(available_levels)}]: ").strip().lower()
    if level not in available_levels:
        raise Exception(f"Level \"{level}\" not available")
    return level


def ask_user_for_language_based_on_previous_language(config: Config, level: str) -> str:
    available_languages = get_languages_for_prompt(config, level)
    return ask_user_for_language(available_languages)


def get_languages_for_prompt(config, level):
    previous_level = config.get_previous_level(level)
    if previous_level is None:
        ask_user_to_continue_without_previous_level()
        available_languages = config.get_available_languages_for_level(level)
    else:
        available_languages = config.get_available_languages_for_this_and_previous_level(level)
    return available_languages


def ask_user_to_continue_without_previous_level():
    continue_anyway = input("No previous level found. continue anyway [Y/n]? ").lower() in {"", "y", "yes"}
    if not continue_anyway:
        raise Exception("TODO")


def ask_user_for_level_and_language(config):
    level = ask_user_for_level(config.available_levels)
    language = ask_user_for_language_based_on_previous_language(config, level)
    return language, level