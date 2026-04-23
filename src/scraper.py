import re
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

logger = logging.getLogger(__name__)

def extrair_valor_numerico(texto: str) -> float | None:
    """
    Extrai o primeiro valor numérico encontrado em um texto.

    Args:
        texto: String contendo o valor a ser extraído.

    Returns:
        Float com o valor extraído, ou None se não encontrado.

    Complexity:
        O(n) — onde n é o comprimento do texto.
    """
    # Junta tudo em uma linha só
    texto = texto.replace('\n', ' ')
    texto = re.sub(r'[R\$€£¥]', '', texto)

    # Padrão impostômetro: "1 Bilhões 308 Milhões 966 Mil 795 Reais 246"
    try:
        partes = {
            'trilhão': 0, 'trilhões': 0,
            'bilhão': 0, 'bilhões': 0,
            'milhão': 0, 'milhões': 0,
            'mil': 0,
            'reais': 0
        }
        tokens = texto.lower().split()
        for i, token in enumerate(tokens):
            if token in partes and i > 0:
                try:
                    partes[token] = int(tokens[i - 1])
                except ValueError:
                    pass

        total = (
            (partes['trilhão'] + partes['trilhões']) * 1_000_000_000_000 +
            (partes['bilhão'] + partes['bilhões']) * 1_000_000_000 +
            (partes['milhão'] + partes['milhões']) * 1_000_000 +
            partes['mil'] * 1_000 +
            partes['reais']
        )
        if total > 0:
            return float(total)
    except Exception:
        pass

    # Padrões normais como fallback
    padrao_br = re.search(r'\d{1,3}(?:\.\d{3})+,\d{2}', texto)
    if padrao_br:
        return float(padrao_br.group().replace('.', '').replace(',', '.'))

    padrao_us = re.search(r'\d{1,3}(?:,\d{3})+\.\d{2}', texto)
    if padrao_us:
        return float(padrao_us.group().replace(',', ''))

    padrao_virgula = re.search(r'\d+,\d+', texto)
    if padrao_virgula:
        return float(padrao_virgula.group().replace(',', '.'))

    padrao_ponto = re.search(r'\d+\.\d+', texto)
    if padrao_ponto:
        return float(padrao_ponto.group())

    padrao_int = re.search(r'\d+', texto)
    if padrao_int:
        return float(padrao_int.group())

    return None


def capturar_valor(url: str, xpath: str) -> float | None:
    """
    Acessa a URL e extrai o valor numérico do elemento indicado.

    Args:
        url: Endereço da página a ser monitorada.
        xpath: Seletor XPath do elemento na página.

    Returns:
        Float com o valor encontrado, ou None se não encontrar.

    Complexity:
        O(n) — onde n é o tamanho do conteúdo da página.
    """
    options = webdriver.ChromeOptions()

    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        driver.get(url)

        wait = WebDriverWait(driver, 15)
        elemento = wait.until(EC.presence_of_element_located((By.XPATH, xpath)))

        location = elemento.location
        print(f"Elemento encontrado!")
        print(f"XPath: {xpath}")
        print(f"Posição: x={location['x']}, y={location['y']}")
        logger.info("Elemento encontrado no XPath: %s | Posição: x=%s, y=%s", xpath, location['x'], location['y'])

        texto = elemento.text
        print(f"Texto capturado: '{texto}'")
        logger.info("Texto capturado: %s", texto)

        valor = extrair_valor_numerico(texto)

        if valor is None:
            print(f"Erro: valor numérico não encontrado. Texto lido: '{texto}'")
            logger.warning("Valor não encontrado no elemento. Texto: %s", texto)

        return valor

    except Exception as e:
        print(f"Erro ao capturar valor: {e}")
        logger.error("Erro ao capturar valor: %s", e)
        return None

    finally:
        driver.quit()

def detectar_xpath_automatico(url: str) -> str | None:
    """
    Abre a página e aguarda o usuário clicar no elemento desejado.

    Args:
        url: Endereço da página a ser monitorada.

    Returns:
        String com o XPath do elemento clicado, ou None se falhar.

    Complexity:
        O(1).
    """
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(
        service=Service(ChromeDriverManager().install()),
        options=options
    )

    try:
        driver.get(url)
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        # Injeta script que captura o XPath do elemento clicado
        driver.execute_script("""
            window._xpathCapturado = null;
            document.addEventListener('click', function(e) {
                e.preventDefault();
                e.stopPropagation();
                var el = e.target;
                function getXPath(el) {
                    if (el.id) return '//*[@id="' + el.id + '"]';
                    if (el === document.body) return '/html/body';
                    if (!el.parentNode) return '';
                    var ix = 1;
                    var siblings = el.parentNode.children;
                    for (var i = 0; i < siblings.length; i++) {
                        if (siblings[i] === el) break;
                        if (siblings[i].tagName === el.tagName) ix++;
                    }
                    return getXPath(el.parentNode) + '/' + el.tagName.toLowerCase() + '[' + ix + ']';
                }
                window._xpathCapturado = getXPath(el);
            }, true);
        """)

        print("Clique no elemento que deseja monitorar no navegador...")

        # Aguarda até 30 segundos o usuário clicar
        import time
        for _ in range(30):
            time.sleep(1)
            xpath = driver.execute_script("return window._xpathCapturado;")
            if xpath:
                print(f"XPath capturado: {xpath}")
                return xpath

        print("Tempo esgotado. Nenhum elemento clicado.")
        return None

    except Exception as e:
        print(f"Erro ao detectar XPath: {e}")
        return None

    finally:
        driver.quit()