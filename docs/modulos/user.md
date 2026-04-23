# user.py

Responsável pelo cadastro e validação do nome do usuário.

---

## `validar_nome(nome)`

Validar se o nome informado é composto apenas por letras e tem ao menos 3 caracteres.

**Parâmetros:**

| Nome | Tipo | Descrição |
|------|------|-----------|
| `nome` | `str` | Nome a ser validado |

**Retorno:** `True` se valido, `False` caso contrário.

**Regras de validação:**

- Mínimo de 3 caracteres
- Apenas letras (acentuadas permitidas)
- Nomes compostos são permitidos (ex: "João Silva")
- Números e caracteres especiais são rejeitados

**Exemplos:**

```python
from src.user import validar_nome
 
validar_nome("João")         # True
validar_nome("Jo")           # False — muito curto
validar_nome("João Silva")   # True — nome composto
validar_nome("João123")      # False — contém números
validar_nome("@dm1n")        # False — caracteres especiais
```

---

## `obter_nome_usuario()`

Solicita o nome do usuário via terminal em loop até receber uma entrada válida.

**Retorno:** `str` com o nome válido do usuário.

**Exemplo:**

```python
from src.user import obter_nome_usuario
 
nome = obter_nome_usuario()
print(f"Bem-vindo, {nome}!")
```

**Saída esperada no terminal:**

```
Informe seu nome: Jo
  Erro: nome muito curto (2 caractere(s)). Mínimo: 3.
 
Informe seu nome: João Silva
```
