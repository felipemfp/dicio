# ![dicio](https://66.media.tumblr.com/ea845a051d316c335f21f084b0ca21b9/tumblr_o7osjb0JpM1vnlnoto1_r1_1280.png)

[![Build Status](https://travis-ci.org/felipemfp/dicio.svg?branch=master)](https://travis-ci.org/felipemfp/dicio) [![Coverage Status](https://coveralls.io/repos/github/felipemfp/dicio/badge.svg?branch=master)](https://coveralls.io/github/felipemfp/dicio?branch=master)

Python API for [Dicio.com.br](http://www.dicio.com.br/)

![Demo](https://cdn.jsdelivr.net/gh/felipemfp/dicio/demo.gif)

## Installation

```sh
$ pip install Dicio
```

## Usage

```python
from dicio import Dicio

# Create a Dicio object
dicio = Dicio()

# Search for "Doce" and return an object Word
word = dicio.search("Doce")

# Print the word, the url and the meaning
print(word, word.url, word.meaning)

# Print a list of synonyms
print(word.synonyms)

# Print a list of examples
print(word.examples)

# Print extra informations
for chave, valor in word.extra.items():
    print(chave, "=>", valor)

# Load information about the first synonym
# Print the word, the URL and the meaning of the first synonym
word.synonyms[0].load()
print(word.synonyms[0], word.synonyms[0].url, word.synonyms[0].meaning)
```

## Word details

### Attributes

- **word** - the word itself
- **url** - Dicio.com.br URL for the word
- **meaning** - the meaning

### Properties

- **synonyms** - list of synonyms
- **examples** - list of examples
- **extra** - dictionary of extra information (keys in portuguese)

### Functions

- **load** - load information from Dicio.com.br

## Contribute

If you want to add new features or improve something, send a pull request!
