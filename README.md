<p align="center">
    <img src="https://66.media.tumblr.com/25b7e1192ace84e597a77130a6fc5d93/tumblr_o7osjb0JpM1vnlnoto1_400.png" />
</p>


# dicio 

[![Build Status](https://travis-ci.org/felipemfp/dicio.svg?branch=master)](https://travis-ci.org/felipemfp/dicio) [![Coverage Status](https://coveralls.io/repos/github/felipemfp/dicio/badge.svg?branch=master)](https://coveralls.io/github/felipemfp/dicio?branch=master)

Python API for [Dicio.com.br](http://www.dicio.com.br/)

![](https://67.media.tumblr.com/ed4ca12184eebd88bd57d42a12ff1729/tumblr_o7j7jpyDDX1vnlnoto1_1280.gif)


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
- **url** - Dicio.com.br url for the word
- **meaning** - the meaning

### Properties
- **synonyms** - list of synonyms
- **extra** - dictionary of extra information (keys in portuguese)

### Functions
- **load** - load information from Dicio.com.br

## Contribute
If you want to add new features or improve something, send a pull request!
