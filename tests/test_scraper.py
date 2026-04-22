# testes unitários
import pytest
from src.scraper import extrair_valor_numerico


# ── Padrão 1: Brasileiro/Europeu ──────────────────────────────────────────────

@pytest.mark.parametrize("texto, esperado", [
    ("R$ 1.234,56",     1234.56),
    ("€ 2.000,00",      2000.00),
    ("Preço: 9.999,99", 9999.99),
])
def test_padrao_br_eu(texto, esperado):
    assert extrair_valor_numerico(texto) == pytest.approx(esperado)


# ── Padrão 2: Americano ────────────────────────────────────────────────────────

@pytest.mark.parametrize("texto, esperado", [
    ("$1,234.56",        1234.56),
    ("Total: 1,000.00",  1000.00),
    ("Price: 9,999.99",  9999.99),
])
def test_padrao_us(texto, esperado):
    assert extrair_valor_numerico(texto) == pytest.approx(esperado)


# ── Padrão 3: Decimal com vírgula ─────────────────────────────────────────────

@pytest.mark.parametrize("texto, esperado", [
    ("49,90",   49.90),
    ("0,99",     0.99),
    ("100,50", 100.50),
])
def test_padrao_decimal_virgula(texto, esperado):
    assert extrair_valor_numerico(texto) == pytest.approx(esperado)


# ── Padrão 4: Decimal com ponto ───────────────────────────────────────────────

@pytest.mark.parametrize("texto, esperado", [
    ("199.00", 199.00),
    ("0.5",      0.50),
    ("3.14",     3.14),
])
def test_padrao_decimal_ponto(texto, esperado):
    assert extrair_valor_numerico(texto) == pytest.approx(esperado)


# ── Padrão 5: Inteiro simples ─────────────────────────────────────────────────

@pytest.mark.parametrize("texto, esperado", [
    ("42",                   42.0),
    ("1000",               1000.0),
    ("Quantidade: 7 itens",   7.0),
])
def test_padrao_inteiro(texto, esperado):
    assert extrair_valor_numerico(texto) == pytest.approx(esperado)


# ── Sem número → None ─────────────────────────────────────────────────────────

@pytest.mark.parametrize("texto", [
    "",
    "Sem número aqui!",
    "R$ ---",
])
def test_sem_numero_retorna_none(texto):
    assert extrair_valor_numerico(texto) is None


# ── Símbolos monetários são removidos ─────────────────────────────────────────

@pytest.mark.parametrize("texto, esperado", [
    ("R$1.500,00",  1500.00),
    ("€2.000,00",   2000.00),
    ("£999.99",      999.99),
    ("¥1,500.00",   1500.00),
])
def test_simbolos_monetarios(texto, esperado):
    assert extrair_valor_numerico(texto) == pytest.approx(esperado)


# ── Prioridade entre padrões ──────────────────────────────────────────────────

def test_br_tem_prioridade_sobre_decimal_virgula():
    # "1.234,56" deve ser lido como BR (1234.56), não como dois números separados
    assert extrair_valor_numerico("1.234,56") == pytest.approx(1234.56)

def test_us_tem_prioridade_sobre_decimal_ponto():
    # "1,234.56" deve ser lido como US (1234.56), não como inteiro 1
    assert extrair_valor_numerico("1,234.56") == pytest.approx(1234.56)