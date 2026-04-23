import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)

def interagir_pagina_externa(valor_anterior: float, valor_atual: float, email_destino: str):
    """
    Abre o Gmail, preenche um rascunho com os valores e clica em enviar.

    Args:
        valor_anterior: Valor antes da alteração.
        valor_atual: Valor após a alteração.
        email_destino: E-mail do destinatário.
    
    Complexity:
        O(1) — operações fixas independente dos valores.
    """
    mensagem = f"Valor alterado: {valor_anterior} → {valor_atual}"
    print(f"[INTERACTOR] {mensagem}")
    logger.info(mensagem)

    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        driver.get("https://mail.google.com")
        wait = WebDriverWait(driver, 20)

        botao_escrever = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Escrever']")))
        botao_escrever.click()

        campo_para = wait.until(EC.presence_of_element_located((By.NAME, "to")))
        campo_para.send_keys(email_destino)

        campo_assunto = driver.find_element(By.NAME, "subjectbox")
        campo_assunto.send_keys("Alteração de valor detectada")

        campo_corpo = driver.find_element(By.XPATH, "//div[@aria-label='Corpo da mensagem']")
        campo_corpo.send_keys(mensagem)

        botao_enviar = driver.find_element(By.XPATH, "//div[text()='Enviar']")
        botao_enviar.click()

        print("[INTERACTOR] E-mail enviado com sucesso!")
        logger.info("E-mail enviado para %s", email_destino)

    except Exception as e:
        print(f"[INTERACTOR] Erro ao interagir com Gmail: {e}")
        logger.error("Erro ao interagir com Gmail: %s", e)

    finally:
        driver.quit()