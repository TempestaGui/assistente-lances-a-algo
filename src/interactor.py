# interagir com outra página
import logging
import smtplib
import time
from email.mime.text import MIMEText

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, WebDriverException

logger = logging.getLogger(__name__)

URL_PAGINA_TESTE = "https://www.selenium.dev/selenium/web/web-form.html"


# ── Driver ────────────────────────────────────────────────────────────────────

def _criar_driver(headless: bool = False) -> webdriver.Chrome:
    """
    Instancia e retorna um WebDriver Chrome configurado.

    Args:
        headless: Se True, executa o navegador sem interface gráfica.

    Returns:
        Instância configurada do WebDriver.

    Complexity:
        O(1) — inicialização fixa do driver.
    """
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1280,900")
    return webdriver.Chrome(options=options)


# ── Automação web ─────────────────────────────────────────────────────────────

def _registrar_em_pagina_externa(
    valor_anterior: float,
    valor_atual: float,
    headless: bool = False,
    timeout: int = 20,
) -> bool:
    """
    Abre o site de teste do Selenium, preenche o campo de texto com a
    mensagem de alteração de valor e clica no botão "Submit" da página.

    Página alvo: https://www.selenium.dev/selenium/web/web-form.html

    Fluxo:
        1. Abre o navegador e navega até a página de formulário de teste.
        2. Localiza o campo "Text input" e insere a mensagem com os valores.
        3. Clica no botão "Submit" da tela.
        4. Aguarda a página de confirmação e registra o resultado.

    Args:
        valor_anterior: Valor antes da alteração detectada.
        valor_atual:    Valor após a alteração detectada.
        headless:       Executa o Chrome sem interface gráfica quando True.
        timeout:        Tempo máximo (segundos) de espera por cada elemento.

    Returns:
        True se o formulário foi submetido com sucesso, False caso contrário.

    Complexity:
        O(1) — número fixo de interações com a página.
    """
    mensagem = f"Valor alterado: {valor_anterior} -> {valor_atual}"
    driver = None

    try:
        driver = _criar_driver(headless=headless)
        wait = WebDriverWait(driver, timeout)

        # ── 1. Abrir página de teste do Selenium ──────────────────────────────
        driver.get(URL_PAGINA_TESTE)
        logger.info("[INTERACTOR] Página de teste aberta: %s", URL_PAGINA_TESTE)

        # ── 2. Preencher campo de texto com a mensagem de alteração ───────────
        campo_texto = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[id='my-text-id']"))
        )
        campo_texto.clear()
        campo_texto.send_keys(mensagem)
        logger.info("[INTERACTOR] Campo de texto preenchido: %s", mensagem)
        print(f"[INTERACTOR] Texto inserido na página: {mensagem}")

        # ── 3. Clicar no botão "Submit" da tela ──────────────────────────────
        botao_submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))
        )
        botao_submit.click()
        logger.info("[INTERACTOR] Botão 'Submit' clicado.")
        print("[INTERACTOR] Botão 'Submit' clicado com sucesso!")

        # ── 4. Verificar página de confirmação ────────────────────────────────
        wait.until(EC.url_contains("web-form-result"))
        logger.info("[INTERACTOR] Submissão confirmada — página de resultado carregada.")
        print("[INTERACTOR] Formulário submetido e confirmado na página externa!")

        time.sleep(1)
        return True

    except TimeoutException as e:
        msg = f"Timeout aguardando elemento na página: {e}"
        print(f"[INTERACTOR] ERRO — {msg}")
        logger.error("[INTERACTOR] %s", msg)
        return False

    except WebDriverException as e:
        msg = f"Falha no WebDriver: {e}"
        print(f"[INTERACTOR] ERRO — {msg}")
        logger.error("[INTERACTOR] %s", msg)
        return False

    except Exception as e:
        msg = f"Erro inesperado na automação web: {e}"
        print(f"[INTERACTOR] ERRO — {msg}")
        logger.error("[INTERACTOR] %s", msg)
        return False

    finally:
        if driver:
            driver.quit()
            logger.info("[INTERACTOR] Driver encerrado.")


# ── Envio de e-mail ───────────────────────────────────────────────────────────

def _enviar_email(
    valor_anterior: float,
    valor_atual: float,
    email_destino: str,
    email_remetente: str,
    senha_app: str,
) -> bool:
    """
    Envia um e-mail via SMTP ao detectar alteração de valor.

    Args:
        valor_anterior:  Valor antes da alteração.
        valor_atual:     Valor após a alteração.
        email_destino:   E-mail do destinatário.
        email_remetente: E-mail do remetente (Gmail).
        senha_app:       Senha de app gerada no Google.

    Returns:
        True se o e-mail foi enviado com sucesso, False caso contrário.

    Complexity:
        O(1) — operações fixas independente dos valores.
    """
    mensagem = f"Valor alterado: {valor_anterior} → {valor_atual}"

    try:
        msg = MIMEText(mensagem)
        msg['Subject'] = "Alteração de valor detectada"
        msg['From'] = email_remetente
        msg['To'] = email_destino

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_remetente, senha_app)
            smtp.send_message(msg)
            print("[INTERACTOR] E-mail enviado com sucesso!")
            logger.info("[INTERACTOR] E-mail enviado para %s", email_destino)
            return True

    except Exception as e:
        print(f"[INTERACTOR] Erro ao enviar e-mail: {e}")
        logger.error("[INTERACTOR] Erro ao enviar e-mail: %s", e)
        return False


# ── Ponto de entrada principal ────────────────────────────────────────────────

def interagir_pagina_externa(
    valor_anterior: float,
    valor_atual: float,
    email_destino: str,
    email_remetente: str,
    senha_app: str,
    headless: bool = False,
    timeout: int = 20,
) -> bool:
    """
    Ponto de entrada principal do interactor. Ao detectar uma alteração de
    valor, executa duas ações:

        1. Automação web (Selenium): abre a página de teste do Selenium,
           insere a mensagem de alteração no campo de texto e clica no
           botão "Submit" da tela — cumprindo o requisito de identificar
           a alteração, registrar em outra página e acionar um botão.

        2. Notificação por e-mail (SMTP): envia um e-mail via Gmail com
           os valores anterior e atual — mantendo o comportamento original.

    Args:
        valor_anterior:  Valor antes da alteração detectada.
        valor_atual:     Valor após a alteração detectada.
        email_destino:   E-mail do destinatário da notificação.
        email_remetente: Conta Gmail usada para envio via SMTP.
        senha_app:       Senha de aplicativo gerada nas configurações do Google.
        headless:        Executa o Chrome sem interface gráfica quando True.
        timeout:         Tempo máximo (segundos) de espera por elemento na página.

    Returns:
        True se ambas as ações foram concluídas com sucesso, False se
        qualquer uma delas falhar.

    Complexity:
        O(1) — número fixo de operações independente dos valores.
    """
    mensagem_log = f"Valor alterado: {valor_anterior} → {valor_atual}"
    print(f"[INTERACTOR] {mensagem_log}")
    logger.info("[INTERACTOR] %s", mensagem_log)

    # Ação 1: registrar na página externa e acionar botão via Selenium
    sucesso_web = _registrar_em_pagina_externa(
        valor_anterior=valor_anterior,
        valor_atual=valor_atual,
        headless=headless,
        timeout=timeout,
    )

    # Ação 2: notificar por e-mail via SMTP
    sucesso_email = _enviar_email(
        valor_anterior=valor_anterior,
        valor_atual=valor_atual,
        email_destino=email_destino,
        email_remetente=email_remetente,
        senha_app=senha_app,
    )

    return sucesso_web and sucesso_email