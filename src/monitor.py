import time
import logging
from src.scraper import capturar_valor
from src.interactor import interagir_pagina_externa

logger = logging.getLogger(__name__)

def iniciar_monitoramento(url, xpath, intervalo, email_destino, email_remetente, senha_app, usuario, logger_obj):
    """
    Monitora um valor em uma página e dispara uma ação quando ele muda.

    Args:
        url: Endereço da página monitorada.
        xpath: Caminho XPath usado para localizar o valor.
        intervalo: Tempo de espera entre cada verificação.
        email_destino: E-mail que receberá a interação externa.
        email_remetente: E-mail usado no envio.
        senha_app: Senha de aplicativo para autenticação.
        usuario: Nome do usuário associado ao monitoramento.
        logger_obj: Instância responsável por registrar as ações.

    Complexity:
        O(1) por verificação, com execução contínua enquanto o monitor estiver ativo.
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
            interagir_pagina_externa(valor_anterior, valor_atual, email_destino, email_remetente, senha_app)
            valor_anterior = valor_atual