# Marugoto2Anki

Scripts to create Anki cards directly from Marugoto website

## Setup

```bash
pipenv install
```

## Usage

### Create vocab cards

```bash
pipenv run python vocabulary.py
```

You might have to create a config file called `config.ini`. It is used to define your Anki user, the storage path, the
anki deck and the card model used for the import. Those parameters will use default values if not specified. An example
can be found in `example.config.ini`

#### [anki]

`exporter`: Name of the exporter which should be used.  
Available exporters are: `anki`, `file`, `genanki`.  
The first one edits the Anki database on your system, while the last will generate a deck which can be importer. The file exporter just outputs the vocabulary as CSV files split into lessons.  
You only need the exporter section related to your selection.

#### [exporter.anki]

`user`: Name of the profile you are using. *Default: User 1*

`path`: Only need to be used if a non-standard location is used! <https://docs.ankiweb.net/files.html>

`deck`: Name of Anki deck that the cards should be imported to. *Default: Vocabulary::Japanese*

`card_model`: Name of the card you are using. *Default: Vocabulary Simple*  
Needed card fields: `sort_id`, `uid`, `kanjis`, `kana`, `translation`, `kanji_meaning`, `accent`, `type`

#### [exporter.file]

`out`: Output folder of the CSV files. *Default: out/*

#### [exporter.genanki]

`deck`: Name of Anki deck that the cards should be imported to. *Default: Vocabulary::Japanese*

`card_model`: Name of the card you are using. *Default: Vocabulary Simple*

`out`: Output location of the Anki deck file. *Default: out/*

### Create kanji cards

```bash
pipenv run python kanji.py
```

### Import

First of all, import the templates in the `templates/` folder with the
[Template Export/Import extension](https://ankiweb.net/shared/info/712027367).
You only have to do that once.

After that you can import the generated CSV files into Anki.
Select the previously imported templates as card type.

And last but not least, all downloaded media have to be copied in Anki's media folder.
On macOS this folder is `~/Library/Application Support/Anki2/[User]/collection.media/`
