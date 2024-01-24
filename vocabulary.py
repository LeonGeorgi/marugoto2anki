from util.classes import Vocab
from util.config import Urls, Config
from util.user_input import ask_user_for_level_and_language
from util.vocab_export import FileExporter, AnkiExporter
from util.vocab_service import VocabService


def main():
    urls = Urls.parse_file("urls.json")
    config = Config.parse_file("config.json")

    language, level = ask_user_for_level_and_language(urls)
    vocabulary = VocabService(level, language, urls).retrieve_vocabulary()
    get_exporter(vocabulary, level, language, config).export_vocabulary()


def get_exporter(vocabulary: list[Vocab], level: str, language: str, config: Config):
    return AnkiExporter(vocabulary, level, language, config)


if __name__ == '__main__':
    main()
    # print(a1_to_list(read_excel_a1("starter_activities_vocabulary_index_en.xlsx")))
