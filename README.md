Python API para [Dicio.com.br](http://www.dicio.com.br/)

| Situação de Build | Cobertura de Testes |
| ------------ | ------------- | 
| [![Build Status](https://travis-ci.org/felipemfp/dicio.svg?branch=master)](https://travis-ci.org/felipemfp/dicio) | [![Coverage Status](https://coveralls.io/repos/github/felipemfp/dicio/badge.svg?branch=master)](https://coveralls.io/github/felipemfp/dicio?branch=master) |

## Uso

```python
# Instancia o objeto Dicio
dicio = Dicio()

# Pesquisa por "Doce" e retorna um objeto Word
word = dicio.search("Doce")

# Apresenta a palavra, a URL e o significado
print(word, word.url, word.meaning)

# Apresenta a lista de sinônimos
print(word.synonyms)

# Apresenta as informações adicionais
for chave, valor in word.extra.items(): 
    print(chave, "=>", valor)

# Apresenta a palavra, a URL e o significado do primeiro sinônimo
word.synonyms[0].load()
print(word.synonyms[0], word.synonyms[0].url, word.synonyms[0].meaning)
```

## Detalhes das Palavras
### Atributos
- **word** - a própria palavra
- **url** - o endereço Dicio.com.br da palavra
- **meaning** - o significado da palavra

### Propriedades
- **synonyms** - a lista de sinônimos
- **extra** - o dicionário de informações adicionais

### Funções
- **load** - ler informações do Dicio.com.br

## Colaborar
Se quiser adicionar novas funções ou melhorar alguma, sinta-se livre e envie uma Pull Request!
