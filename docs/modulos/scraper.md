# scraper.py

Classe responsável por acessar páginas web via selenium e extrair valores númericos dos elementos indicados.

---

## `extrair_valor_numerico(texto)`

Extrai o primeiro valor numérico encontrado em um texto bruto.

**Parâmetros**

| Nome | Tipo | Descrição |
|------|------|-----------|
| `texto` | `str` | Texto bruto contendo o valor a ser extraído |

**Retorno:** ``float` com o valor extraido, ou `None` se nenhum número for encontrado.

**Formatos suportados:**

- Impostometro: `"1 Trilhões 308 Bilhões 966 Milhões 795 Mil 246 Reais"`  
- Brasileiro: `"R$ 1.234,56"`  
- Americano: `"$1,234.56"`  
- Decimal com vírgula: `"1234,56"`  
- Decimal com ponto: `"1234.56"`  
- Inteiro simples: `"1234"`

**Exemplo:**

```python
from src.scraper import extrair_valor_numerico
 
valor = extrair_valor_numerico("R$ 1.234,56")
print(valor)  # 1234.56
```

## `capturar_valor(url, xpath)`

Acessa a URL via Selenium e retorna o valor numérico do elemento indicado pelo xpath

**Parâmetros:**

| Nome | Tipo | Descrição |
|------|------|-----------|
| `url` | `str` | Endereço da página a ser monitorada |
| `xpath` | `str` | Seletor XPath do elemento na página |


**Retorno:** `float` com o valor encontrado, ou `None` se não encotrar.

**Exemplo:**

```python
from src.scraper import capturar_valor
 
valor = capturar_valor("https://impostometro.com.br", '//*[@id="counterBrasil"]')
print(valor)
```

**Logs gerados:**

```
Elemento encontrado!
XPath: //*[@id="counterBrasil"]
Posição: x=65, y=403
Texto capturado: '...'
```

## `detectar_xpath_automatico(url)`

Abre a página no navegador e aguarda o usúario clicr no elemento desejado, retornando o XPath automaticamente.

**Parâmetros:**

| Nome | Tipo | Descrição |
|------|------|-----------|
| `url` | `str` | Endereço da página |


**Retorno:** `str` com o XPath do elemento clicado, ou `None` se o tempo esgotar.
 
**Exemplo:**
 
```python
from src.scraper import detectar_xpath_automatico
 
xpath = detectar_xpath_automatico("https://impostometro.com.br")
print(xpath)  # //*[@id="counterBrasil"]
```





