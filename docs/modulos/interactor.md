# interactor.py

Responsável por notificar o usuário por e-mail quando uma alteração de valor é detectada.

## `interagir_pagina_externa(valor_anterior, valor_atual, email_destino, email_remetente, senha_app)`

Envia um e-mail via SMTP ao detectar alteração de valor.

**Parâmetros:**

| Nome | Tipo | Descrição |
|------|------|-----------|
| `valor_anterior` | `float` | Valor antes da alteração |
| `valor_atual` | `float` | Valor após a alteração |
| `email_destino` | `str` | E-mail do destinatário |
| `email_remetente` | `str` | E-mail do remetente (Gmail) |
| `senha_app` | `str` | Senha de app gerada no Google |


**Retorno:** `None`

**Exemplo:**

```python
from src.interactor import interagir_pagina_externa
 
interagir_pagina_externa(
    valor_anterior=1000.0,
    valor_atual=1200.0,
    email_destino="destino@gmail.com",
    email_remetente="remetente@gmail.com",
    senha_app="abcdabcdabcdabcd"
)
```

**Saída esperadfa no console:**

```
[INTERACTOR] Valor alterado: 1000.0 → 1200.0
[INTERACTOR] E-mail enviado com sucesso!
```

**Como gerar a senha de app:**
 
1. Acesse `myaccount.google.com`
2. Segurança → Verificação em duas etapas → Senhas de app
3. Crie uma senha para "Outro aplicativo"
4. Use a senha de 16 caracteres gerada (sem espaços)


