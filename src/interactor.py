import logging
import smtplib
from email.mime.text import MIMEText

logger = logging.getLogger(__name__)

def interagir_pagina_externa(valor_anterior: float, valor_atual: float, email_destino: str, email_remetente: str, senha_app: str):
    """
    Envia um e-mail via SMTP ao detectar alteração de valor.

    Args:
        valor_anterior: Valor antes da alteração.
        valor_atual: Valor após a alteração.
        email_destino: E-mail do destinatário.
        email_remetente: E-mail do remetente (Gmail).
        senha_app: Senha de app gerada no Google.

    Complexity:
        O(1) — operações fixas independente dos valores.
    """
    mensagem = f"Valor alterado: {valor_anterior} → {valor_atual}"
    print(f"[INTERACTOR] {mensagem}")
    logger.info(mensagem)

    try:
        msg = MIMEText(mensagem)
        msg['Subject'] = "Alteração de valor detectada"
        msg['From'] = email_remetente
        msg['To'] = email_destino

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_remetente, senha_app)
            smtp.send_message(msg)
            print("[INTERACTOR] E-mail enviado com sucesso!")
            logger.info("E-mail enviado para %s", email_destino)

    except Exception as e:
        print(f"[INTERACTOR] Erro ao enviar e-mail: {e}")
        logger.error("Erro ao enviar e-mail: %s", e)