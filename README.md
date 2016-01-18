Python API para [Dicio.com.br](http://www.dicio.com.br/)

## Uso

```python
# Instancia o objeto Dicio
dicio = Dicio()

# Pesquisa por "Carambola" e retorna um objeto Word
word = Dicio().search("Carambola")

# Apresenta a palavra, a URL e o significado
print(word.word, word.url, word.meaning)
```

## Detalhes das Palavras
### Atributos
- **word** - a própria palavra
- **url** - o endereço Dicio.com.br da palavra
- **meaning** - o significado da palavra

## Colaborar
Se quiser adicionar novas funções ou melhorar alguma, sinta-se livre e envie uma Pull Request!
