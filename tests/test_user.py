import pytest
from src.user import validar_nome
 
 
@pytest.mark.parametrize("nome", [
    "Ana", "João", "Maria Silva", "José Carlos Andrade", "abc",
])
def test_nomes_validos(nome):
    assert validar_nome(nome) is True
 
 
@pytest.mark.parametrize("nome, motivo", [
    ("",          "vazio"),
    ("ab",        "menos de 3 caracteres"),
    ("Jo3o",      "contém número"),
    ("Ana!",      "caractere especial"),
    ("Ana  Silva","espaço duplo"),
])
def test_nomes_invalidos(nome, motivo):
    assert validar_nome(nome) is False, f"Deveria ser inválido: {motivo}"
 
 
def test_espacos_nas_bordas_sao_ignorados():
    assert validar_nome("  Ana  ") is True