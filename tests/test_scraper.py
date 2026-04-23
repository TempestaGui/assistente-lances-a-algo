# testes unitários

from src.scraper import extrair_valor_numerico

def test_valor_formato_brasileiro():
    assert extrair_valor_numerico("R$ 1.234,56") == 1234.56

def test_valor_formato_americano():
    assert extrair_valor_numerico("$1,000.00") == 1000.00

def test_sem_valor():
    assert extrair_valor_numerico("Sem valor") is None

def test_texto_vazio():
    assert extrair_valor_numerico("") is None