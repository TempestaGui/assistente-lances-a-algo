## extrair_valor_numerico

### Complexidade de tempo

| Caso        | Notação | Condição                        |
|-------------|---------|---------------------------------|
| Melhor caso | O(n)    | Padrão BR encontrado (2 scans)  |
| Caso médio  | O(n)    | 3–4 padrões tentados            |
| Pior caso   | O(n)    | Todos os 5 padrões tentados     |

`n` = comprimento do texto de entrada após `re.sub`.
O número de padrões é constante (k=6), logo O(k·n) = **O(n)**.

### Complexidade de espaço

**O(n)** — `re.sub` aloca uma nova string proporcional à entrada.
Os objetos `Match` dos `re.search` são O(1).

### Observação
A função usa early return: ao encontrar um match ela retorna
imediatamente, sem tentar os padrões seguintes. No caso médio
real (preços em BRL), raramente passa do padrão 1.