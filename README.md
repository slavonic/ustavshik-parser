# ustavshik parser

Utility to parse https://ustavshik.ru/books texts. These are Church Slavonic texts (books).

These texts are renedered with HTML and use obsolete USC encoding (a variant of USC, actually, that is based on utf-8, not cp1251).

The goal of this utility is to convert Ustavshik HTML into XML format with text encoding
following Unicode standard.

## Installation

Requires Python3

It is recommended to use virtual Python environment, like this:

```bash
mkdir workdir
cd workdir
python3 -m venv .venv
source .v env/bin/activate
```

Then, install the package directly from GitHub:

```bash
pip install https://github.com/slavonic/ustavshik-parser
```

## Usage

Once installed, you can run thee utility like this:

```bash
python -m ustav
```

This will give you the basic usage information, like this:

```bash
usage: ustav [-h] source target
ustav: error: the following arguments are required: source, target
```

### Capture text directly from website

```bash
python -m ustav https://ustavshik.ru/books/chasoslov chasoslov.xml
```

The command above reads the web page, does the format conversion, and saves XML as `chasoslov.xml`.

### Download html document and convert

You can download HTML first, and save as local files:

```bash
wget https://ustavshik.ru/books/chasoslov > chasoslov.html
```

and then use this utility to do the conversion from HTML:

```bash
python -m ustav chasoslov.html chasoslov.xml
```
