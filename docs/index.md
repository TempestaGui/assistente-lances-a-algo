# Assistente de Lances

Sistema de monitoramento automático de valores em páginas web. O usuário informa uma URL e um elemento da página, e o sistema monitora periodicamente aquele valor, detectando alterações e enviando notificações por e-mail.

## Como executar

```bash
python main.py
```

## Estrutura do projeto


```
assistente-lances/
├── src/
│   ├── scraper.py       # Captura de valor e detecção de XPath
│   ├── interactor.py    # Envio de e-mail via SMTP
│   ├── monitor.py       # Monitoramento periódico
│   ├── user.py          # Cadastro e validação do usuário
│   └── logger.py        # Registro de ações
│   └── Interface.py     # Interface desktop da aplicação
├── tests/
│   └── test_scraper.py  # Testes unitários
├── docs/                # Esta documentação
├── logs/                # Logs gerados em execução
├── main.py
└── requirements.txt
```


## Dependências
 
```bash
pip install selenium webdriver-manager
```
