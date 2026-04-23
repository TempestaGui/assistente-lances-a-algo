# Documentação do Projeto

Documentação técnica do scraper de monitoramento de preços.

## Módulos

- **scraper.py** — extração e parsing de valores numéricos via RegEx
- **monitor.py** — agendamento e rastreamento de variações
- **interactor.py** — ações em páginas externas
- **logger.py** — registro de eventos e histórico
- **user.py** — cadastro e validação de usuário

## Análise de Complexidade (Big O)

Cada módulo possui uma página dedicada com a análise de complexidade
de tempo e espaço de suas funções principais. Acesse pelo menu
lateral em **Análise Big O**.

## Como rodar o projeto

```bash
pip install -r requirements.txt
python main.py
```

## Como rodar os testes

```bash
pytest tests/
```