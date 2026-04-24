import pytest

from src.user import obter_nome_usuario, validar_nome


@pytest.mark.parametrize(
    "nome,esperado",
    [
        ("Ana", True),
        ("Joao Silva", True),
        (" Jose ", True),
        ("Al", False),
        ("Jo4o", False),
        ("", False),
    ],
)
def test_validar_nome(nome, esperado):
    assert validar_nome(nome) is esperado


def test_obter_nome_usuario_repite_ate_nome_valido(monkeypatch):
    entradas = iter(["ab", "Jo4o", "Maria Clara"])
    mensagens = []

    monkeypatch.setattr("builtins.input", lambda _: next(entradas))
    monkeypatch.setattr("builtins.print", lambda msg: mensagens.append(msg))

    resultado = obter_nome_usuario()

    assert resultado == "Maria Clara"
    assert any("nome muito curto" in msg for msg in mensagens)
    assert any("use apenas letras" in msg for msg in mensagens)
