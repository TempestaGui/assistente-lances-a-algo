# Relatório de Análise de Complexidade
**Disciplina:** Análise de Algoritmos  
**Projeto:** Assistente de Lances para Sites de Leilão  
**Linguagem:** Python  

---

## Sumário

1. [user.py](#1-userpy)
2. [logger.py](#2-loggerpy)
3. [interactor.py](#3-interactorpy)
4. [scraper.py](#4-scraperpy)
5. [monitor.py](#5-monitorpy)
6. [interface.py](#6-interfacepy)
7. [Resumo Geral](#7-resumo-geral)

---

## 1. `user.py`

### `validar_nome(nome: str) -> bool`
**Complexidade: O(n)**

Essa função precisa olhar o nome caractere por caractere — primeiro para remover espaços nas bordas, depois para verificar se ele segue o padrão esperado (apenas letras, com ao menos 3 caracteres). Quanto maior o nome, mais trabalho ela faz, por isso a complexidade cresce linearmente com o tamanho da entrada.

---

### `obter_nome_usuario() -> str`
**Complexidade: O(k × n)**

A função fica em loop pedindo um nome até que o usuário forneça um válido. Cada tentativa chama `validar_nome`, que custa O(n). No total, o custo depende de quantas tentativas foram feitas (k) e do tamanho de cada nome digitado (n). Considerando uma única tentativa bem-sucedida, o custo por chamada é O(n).

---

## 2. `logger.py`

### `Logger.__init__(self)`
**Complexidade: O(1)**

A inicialização cria o diretório de logs e configura o sistema de registro. São sempre as mesmas operações, independentemente de qualquer entrada — o custo é fixo e constante.

---

### `Logger.registrar(usuario: str, acao: str)`
**Complexidade: O(1)**

Registrar uma ação é sempre a mesma operação: formatar uma mensagem e gravá-la no arquivo de log. O tamanho do nome ou da ação não muda a estrutura do trabalho realizado, então o custo permanece constante.

---

## 3. `interactor.py`

### `_criar_driver(headless: bool) -> webdriver.Chrome`
**Complexidade: O(1)**

Instancia e configura um WebDriver Chrome com um conjunto fixo de argumentos. Independentemente dos parâmetros recebidos, o número de operações realizadas é sempre o mesmo — custo constante.

---

### `_registrar_em_pagina_externa(valor_anterior, valor_atual, headless, timeout) -> bool`
**Complexidade: O(1)**

Abre uma página de formulário de teste, preenche um campo de texto com a mensagem de alteração e clica no botão de submit. O fluxo tem sempre o mesmo número de etapas: abrir página, localizar elemento, preencher, clicar e verificar confirmação. Não há iteração sobre estruturas de dados variáveis, portanto o custo é constante. O tempo de espera pelo DOM é limitado pelo parâmetro `timeout`, que é um valor fixo.

---

### `_enviar_email(valor_anterior, valor_atual, email_destino, email_remetente, senha_app) -> bool`
**Complexidade: O(1)**

Monta uma mensagem de e-mail e a envia via SMTP. São sempre os mesmos passos, sem nenhum laço ou estrutura que cresça com a entrada. O tempo de resposta da rede pode variar, mas isso não faz parte da análise de complexidade algorítmica.

---

### `interagir_pagina_externa(...)` *(ponto de entrada principal)*
**Complexidade: O(1)**

Essa função orquestra as duas ações anteriores em sequência: chama `_registrar_em_pagina_externa` e depois `_enviar_email`, ambas de custo O(1). Como as chamadas são sequenciais e independentes, a complexidade total permanece O(1) — constante e independente de qualquer entrada.

---

## 4. `scraper.py`

### `extrair_valor_numerico(texto: str) -> float | None`
**Complexidade: O(n)**

Essa é uma das funções mais ricas do projeto. Ela percorre o texto de várias formas diferentes: remove símbolos de moeda, divide o texto em palavras e procura por padrões numéricos usando expressões regulares. Cada uma dessas etapas lê o texto do começo ao fim, mas como são feitas uma após a outra (e não dentro de outras), o custo total cresce de forma linear com o tamanho do texto recebido.

---

### `_aguardar_texto_nao_vazio(driver, xpath: str, timeout: int) -> str | None`
**Complexidade: O(timeout)**

Essa função foi adicionada para lidar com páginas que carregam o conteúdo de forma dinâmica via JavaScript — casos em que o elemento já está no DOM, mas seu texto ainda está vazio. Ela executa um loop de polling que verifica o elemento a cada 0,5 segundo até encontrar texto não vazio ou o tempo se esgotar. O número de iterações é diretamente proporcional ao valor de `timeout`, portanto a complexidade é **O(timeout)**. Na prática, o custo real tende a ser bem menor, pois o loop encerra assim que o texto é encontrado.

---

### `capturar_valor(url: str, xpath: str, timeout: int) -> float | None`
**Complexidade: O(n)**

O Selenium abre a página e aguarda o elemento aparecer no DOM. Em seguida, delega para `_aguardar_texto_nao_vazio` — que tem custo O(timeout), tratado como constante — e então passa o texto capturado para `extrair_valor_numerico`, de custo O(n). A operação dominante é o processamento do texto, mantendo a complexidade em **O(n), onde n é o comprimento do texto do elemento localizado**. A descrição indicada no código ("n é o tamanho do conteúdo da página") continua imprecisa pelo mesmo motivo já apontado anteriormente.

---

### `detectar_xpath_automatico(url: str) -> str | None`
**Complexidade: O(p × s)** *(corrigida — estava indicada como O(1) no código)*

Essa função injeta um script JavaScript na página que, ao detectar um clique do usuário, calcula o XPath do elemento clicado. Para fazer isso, o script sobe recursivamente pela árvore do DOM, do elemento clicado até a raiz da página. Em cada nível dessa subida, ele também conta os elementos irmãos para montar o endereço correto. O loop Python de espera (`for _ in range(30)`) executa no máximo 30 vezes — custo fixo, portanto O(1). Porém, ele é dominado pela execução do script JS, cuja complexidade real é **O(p × s)**, onde **p** é a profundidade do elemento na árvore e **s** é a quantidade de elementos irmãos em cada nível. A indicação O(1) no código estava errada.

---

## 5. `monitor.py`

### `iniciar_monitoramento(...)`
**Complexidade: O(n) por verificação**

Essa função roda indefinidamente em segundo plano, verificando o valor da página a cada intervalo de tempo configurado. Como o loop não tem fim previsto, não faz sentido calcular um custo total — o que importa é o custo de cada ciclo. A cada iteração, `capturar_valor` é chamado com custo O(n), `registrar` com custo O(1) e, quando há alteração de valor, `interagir_pagina_externa` também com custo O(1). A operação dominante é `capturar_valor`, tornando o custo por iteração **O(n), onde n é o comprimento do texto capturado**.

---

## 6. `interface.py`

### `detectar()` *(função interna de `main`)*
**Complexidade: O(p × s)**

Após uma validação rápida da URL, essa função chama `detectar_xpath_automatico`, que é a operação mais custosa. O custo total segue o mesmo raciocínio explicado anteriormente: depende da profundidade do elemento no DOM e da quantidade de irmãos em cada nível.

---

### `iniciar()` *(função interna de `main`)*
**Complexidade: O(n)**

Essa função valida as entradas do usuário e inicia o monitoramento em uma thread separada. A operação dominante é `validar_nome`, de custo O(n). O monitoramento em si roda de forma assíncrona e não afeta o custo da função `iniciar` em si.

---

### `main()`
**Complexidade: O(1) na inicialização**

A função cria um número fixo de componentes visuais (labels, campos de texto, botões) e abre a janela. Esse processo tem custo constante. O loop de eventos do Tkinter que mantém a janela aberta é orientado a interações do usuário e não se enquadra na análise de Big O.

---

## 7. Resumo Geral

A tabela abaixo consolida a complexidade de tempo de todas as funções analisadas ao longo do projeto. De forma geral, o comportamento dominante do sistema é **linear — O(n)** — o que é esperado para uma aplicação que lida principalmente com processamento de texto e varredura de strings. As únicas exceções notáveis são a função `detectar_xpath_automatico`, cuja complexidade real é **O(p × s)** devido à travessia recursiva da árvore DOM, e as funções de log, automação web e envio de e-mail, que operam em **tempo constante O(1)** por não dependerem de nenhuma estrutura de dados variável.

| Arquivo | Função | Complexidade de Tempo |
|---|---|---|
| `user.py` | `validar_nome` | O(n) |
| `user.py` | `obter_nome_usuario` | O(k × n) |
| `logger.py` | `Logger.__init__` | O(1) |
| `logger.py` | `Logger.registrar` | O(1) |
| `interactor.py` | `_criar_driver` | O(1) |
| `interactor.py` | `_registrar_em_pagina_externa` | O(1) |
| `interactor.py` | `_enviar_email` | O(1) |
| `interactor.py` | `interagir_pagina_externa` | O(1) |
| `scraper.py` | `extrair_valor_numerico` | O(n) |
| `scraper.py` | `_aguardar_texto_nao_vazio` | O(timeout) |
| `scraper.py` | `capturar_valor` | O(n) |
| `scraper.py` | `detectar_xpath_automatico` | O(p × s) |
| `monitor.py` | `iniciar_monitoramento` | O(n) por iteração |
| `interface.py` | `detectar` | O(p × s) |
| `interface.py` | `iniciar` | O(n) |
| `interface.py` | `main` | O(1) na inicialização |

> **Legenda de variáveis:**
> - **n** — comprimento da string de entrada (nome, texto do elemento, etc.)
> - **k** — número de tentativas do usuário
> - **p** — profundidade do elemento na árvore DOM
> - **s** — número de elementos irmãos (*siblings*) em cada nível do DOM
> - **timeout** — tempo máximo de espera configurado para o polling do elemento
