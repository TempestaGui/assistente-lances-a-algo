# Logger

Classe que gerencia o registro de ações em arquivos `.log` com timestamp.

Os arquivos de log são salvos na pasta `logs/` com o nome no formato `acoes_YYYYMMDD_HHMMSS.log`.

---

## `Logger.__init__()`

Inicializa o logger criando a pasta `logs/` e configurando o arquivo de logs.

**Exemplo:**

```python
from src.logger import Logger
 
logger = Logger()
```

## `Logger.registrar(usuario, acao)`

Registrar uma ação do usuário no arquivo de log e exibe no console.

**Parâmetros:**

| Nome | Tipo | Descrição |
|------|------|-----------|
| `usuario` | `str` | Nome do usuário que realizou a ação |
| `acao` | `str` | Descrição da ação realizada |

**Retorno:** `None`

**Exemplo:**

```python
from src.logger import Logger
 
logger = Logger()
logger.registrar("João", "Monitoramento iniciado: https://impostometro.com.br")
logger.registrar("João", "Valor inicial capturado: 1308966795246.0")
logger.registrar("João", "Alteração detectada: 1308966795246.0 → 1308966795247.0")
```

**Saída no console:**

```
[LOG] [João] Monitoramento iniciado: https://impostometro.com.br
[LOG] [João] Valor inicial capturado: 1308966795246.0
[LOG] [João] Alteração detectada: 1308966795246.0 → 1308966795247.0
```

**Exemplo de arquivo de log gerado (`logs/acoes_20260422_170000.log`):**

```
2026-04-22 17:00:00,123 - INFO - [João] Monitoramento iniciado: https://impostometro.com.br
2026-04-22 17:00:05,456 - INFO - [João] Valor inicial capturado: 1308966795246.0
2026-04-22 17:00:35,789 - INFO - [João] Alteração detectada: 1308966795246.0 → 1308966795247.0
```


