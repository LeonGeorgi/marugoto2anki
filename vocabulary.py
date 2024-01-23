from util.classes import Vocab
from util.config import Config
from util.user_input import ask_user_for_level_and_language
from util.vocab_export import FileExporter, AnkiExporter, GenankiExporter
from util.vocab_service import VocabService


def main():
    config = Config.parse_file("config.json")
    language, level = ask_user_for_level_and_language(config)
    vocabulary = VocabService(level, language, config).retrieve_vocabulary()
    get_exporter().export_vocabulary(vocabulary, level, language)


def get_exporter():
    # return AnkiExporter()
    #return FileExporter()
    return GenankiExporter()


if __name__ == '__main__':
    main()
    # print(a1_to_list(read_excel_a1("starter_activities_vocabulary_index_en.xlsx")))
