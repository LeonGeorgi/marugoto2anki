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
