import time
import logging
from src.scraper import capturar_valor
from src.interactor import interagir_pagina_externa

logger = logging.getLogger(__name__)

def iniciar_monitoramento(url: str, xpath: str, intervalo: int, email_destino: str, usuario: str, logger_obj):
    """
    Monitora a página periodicamente e detecta alterações de valor.

    Args:
        url: Endereço da página monitorada.
        xpath: Seletor XPath do elemento.
        intervalo: Tempo em segundos entre cada verificação.
        email_destino: E-mail para notificação.
        usuario: Nome do usuário.
        logger_obj: Instância do Logger.
    
    Complexity:
        O(1) por iteração — cada verificação é independente.
    """
    valor_anterior = capturar_valor(url, xpath)
    print(f"[MONITOR] Valor inicial: {valor_anterior}")
    logger_obj.registrar(usuario, f"Valor inicial: {valor_anterior}")

    while True:
        time.sleep(intervalo)
        valor_atual = capturar_valor(url, xpath)

        if valor_atual is None:
            print("[MONITOR] Erro ao capturar valor. Tentando novamente...")
            logger_obj.registrar(usuario, "Erro ao capturar valor")
            continue

        print(f"[MONITOR] Verificação: {valor_atual}")
        logger_obj.registrar(usuario, f"Verificação: {valor_atual}")

        if valor_atual != valor_anterior:
            print(f"[MONITOR] Alteração detectada: {valor_anterior} → {valor_atual}")
            logger_obj.registrar(usuario, f"Alteração: {valor_anterior} → {valor_atual}")
            interagir_pagina_externa(valor_anterior, valor_atual, email_destino)
            valor_anterior = valor_atual