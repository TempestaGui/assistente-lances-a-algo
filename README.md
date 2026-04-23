# Assistente de Lances

Sistema de monitoramento automático de valores em páginas web. O usuário informa uma URL e indica qual elemento da página deseja monitorar. O sistema acessa a página periodicamente, detecta alterações no valor e envia uma notificação por e-mail automaticamente.

## Funcionalidades

- Captura de valores numéricos em qualquer página web via Selenium
- Detecção automática do elemento por clique na página
- Monitoramento periódico com intervalo configurável
- Notificação por e-mail ao detectar alteração
- Registro de todas as ações do usuário em arquivo de log
- Interface gráfica desktop

## O que é Selenium?

Selenium é uma biblioteca Python que permite controlar um navegador web automaticamente via código. Em vez de um humano abrir o Chrome e clicar em elementos, o Selenium faz isso programaticamente.

Neste projeto, o Selenium é responsavel por: 

- Abrir o Chrome e acessar a URL informada pelo usuário
- Localizar o elemento a página pelo XPath
- Extrair o texto do elemento para capturar o valor númerico

---

## O que é XPath?

XPath é uma linguagem de consulta usada para localizar elementos dentro de uma página HTML. Funcionando como um "endereço" do elemento na estrutura da página.

**Exemplo:**

```
  //*[@id="counterBrasil"]
```

Esse XPath localiza qualquer elemento da página que tenha o atributo `id="counterBrasil"`.

---

## O que é RegEx?

RegEx (Expressão Regular) é uma linguagem para buscar e extração de padrões em texto. Neste projeto é usada para extrair o valor numérico do texto bruto retornado pelo Selenium.

Por exemplo, o elemento pode retornar o texto `"R$ 1.234,56"`. O RegEx limpa os símbolos e extrai apenas `1234.56` como número.

---

## O que é SMTP? 

SMTP (Simple Mail Transfer Protocol) é o protocolo padrão para envio de e-mails. A bibliotea `smtplib` do Python permite conectar ao serviço do Gmail e envar e-mails diretamente pelo código, sem precisr abrir o navegador.

---

## Como o sistema funciona

### 1. Entrada de dados
A interface gráfica (tkinter) solicita ao usuário:
- Nome (validado com RegEx — mínimo 3 letras, apenas letras)
- URL da página a monitorar
- XPath do elemento com o valor
- Intervalo de verificação em segundos
- E-mail de destino para notificações
- E-mail remetente e senha de app do Gmail

### 2. Captura do valor inicial
O Selenium abre o Chrome, acessa a URL e localiza o elemento pelo XPath. 
O texto do elemento é processado pelo RegEx para extrair o valor numérico. 
Se o elemento não for encontrado, o sistema exibe uma mensagem de erro e 
encerra sem travar.

### 3. Monitoramento periódico
O monitoramento roda em uma thread separada para não travar a interface. 
A cada X segundos, o sistema acessa a página novamente e compara o valor 
atual com o anterior.

### 4. Detecção de alteração
Se o valor mudar, o sistema registra a alteração no log e aciona o módulo 
de notificação.

### 5. Notificação por e-mail
O `smtplib` conecta ao servidor SMTP do Gmail e envia um e-mail com o 
valor anterior e o novo para o destinatário informado.

### 6. Log de ações
Todas as ações do usuário — início do monitoramento, verificações, 
alterações detectadas e e-mails enviados — são gravadas em arquivo `.log` 
na pasta `logs/` com timestamp.

## Como executar

```bash
git clone https://github.com/TempestaGui/assistente-lances-a-algo
git checkout develop
pip install selenium webdriver-manager
python main.py
```

## Membros

- [David Lopes](https://github.com/DavidLBO)
- [Guilherme Tempesta](https://github.com/TempestaGui)
- [Gabriel Feitosa](https://github.com/GabriFrnd)
- [Gabrielle Rodrigues](https://github.com/gabzbiriba)
