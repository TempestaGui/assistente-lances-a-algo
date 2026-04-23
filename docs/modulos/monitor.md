# monitor.py

Responsável pelo monitoamento periódico da página e detecção de alterações de valor.

## `iniciar_monitoramento(url, xpath, intervalo, email_destino, email_remetente, senha_app, usuario, logger_obj)`

Monitora a página e cada `intervalo` segundos e notifica por e-mail quando o valor muda.

**Parâmetros:**

| Nome | Tipo | Descrição |
|------|------|-----------|
| `url` | `str` | Endereço da página monitorada |
| `xpath` | `str` | Seletor XPath do elemento |
| `intervalo` | `int` | Tempo em segundos entre cada verificação |
| `email_destino` | `str` | E-mail para notificação |
| `email_remetente` | `str` | E-mail remetente |
| `senha_app` | `str` | Senha de app do Gmail |
| `usuario` | `str` | Nome do usuário |
| `logger_obj` | `Logger` | Instância do Logger para registro de ações |

**Retorno:** `None` — executa em loop infinito até ser interrompido.  

**Exemplo:**
 
```python
from src.monitor import iniciar_monitoramento
from src.logger import Logger
 
logger = Logger()
 
iniciar_monitoramento(
    url="https://impostometro.com.br",
    xpath='//*[@id="counterBrasil"]',
    intervalo=30,
    email_destino="destino@gmail.com",
    email_remetente="remetente@gmail.com",
    senha_app="abcdabcdabcdabcd",
    usuario="João",
    logger_obj=logger
)
```
 
**Saída esperada no console:**
 
```
[MONITOR] Valor inicial: 1308966795246.0
[MONITOR] Verificação: 1308966795246.0
[MONITOR] Verificação: 1308966795247.0
[MONITOR] Alteração detectada: 1308966795246.0 → 1308966795247.0
[INTERACTOR] Valor alterado: 1308966795246.0 → 1308966795247.0
[INTERACTOR] E-mail enviado com sucesso!
```
