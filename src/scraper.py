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