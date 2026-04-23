# Assistente de Lances

Sistema de monitoramento automático de valores em páginas web. O usuário informa uma URL e indica qual elemento da página deseja monitorar. O sistema acessa a página periodicamente, detecta alterações no valor e envia uma notificação por e-mail automaticamente.

## Funcionalidades

- Captura de valores numéricos em qualquer página web via Selenium
- Detecção automática do elemento por clique na página
- Monitoramento periódico com intervalo configurável
- Notificação por e-mail ao detectar alteração
- Registro de todas as ações do usuário em arquivo de log
- Interface gráfica desktop

## Como executar

```bash
pip install selenium webdriver-manager
python main.py
```

## Membros

- David Lopes
- Guilherme Tempesta
- Gabriel Feitosa
- Gabrielle Rodrigues
