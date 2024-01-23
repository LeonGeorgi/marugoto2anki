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

You might have to create a config file called `config.json`. It is used to define your Anki user, the storage path and the card model used for the import. Those parameters will use default values if not specified. An example can be found in `example.config.json`

`anki_user`: Name of the profile you are using. *Default: User 1*

`anki_path`: Only need to be used if a non-standard location is used! <https://docs.ankiweb.net/files.html>

`card_model`: Name of the card you are using. *Default: Vocabulary Simple*  
Needed card fields: `sort_id`, `uid`, `kanjis`, `kana`, `translation`, `kanji_meaning`, `accent`

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
