 # Módulo de operações com expressões regulares (RegEx)
import re

def extrair_valor_numerico(texto: str) -> float | None:
    # Remover símbolos monetários e espaços
    texto = re.sub(r'[R$€£¥\s]', '', texto)

    # Padrão 1: formato brasileiro/europeu -> 1.234,56
    padrao_br = re.search(r'\d{1,3}(?:\.\d{3})+,\d{2}', texto)

    if padrao_br:
        valor = padrao_br.group().replace('.', '').replace(',', '.')
        return float(valor)
    
    # Padrão 2: formato americano -> 1,234.56
    padrao_us = re.search(r'\d{1,3}(?:,\d{3})+\.\d{2}', texto)

    if padrao_us:
        valor = padrao_us.group().replace(',', '')
        return float(valor)
    
    # Padrão 3: decimal com vírgula (sem separador de milhar) -> 1234,56
    padrao_virgula = re.search(r'\d+,\d+', texto)

    if padrao_virgula:
        valor = padrao_virgula.group().replace(',', '.')
        return float(valor)
    
    # Padrão 4: decimal com ponto -> 1234.56
    padrao_ponto = re.search(r'\d+\.\d+', texto)

    if padrao_ponto:
        return float(padrao_ponto.group())
    
    # Padrão 5: inteiro simples -> 1234
    padrao_int = re.search(r'\d+', texto)

    if padrao_int:
        return float(padrao_int.group())
    
    return None # Nenhum número encontrado