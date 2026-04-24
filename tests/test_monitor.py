import pytest

from src import monitor


def test_iniciar_monitoramento_detecta_alteracao_e_interage(monkeypatch):
    valores = iter([10.0, 12.0])
    eventos = []

    class FakeLogger:
        def registrar(self, usuario, msg):
            eventos.append((usuario, msg))

    def fake_interagir(*_args, **_kwargs):
        raise SystemExit

    monkeypatch.setattr(monitor, "capturar_valor", lambda *_a, **_k: next(valores))
    monkeypatch.setattr(monitor.time, "sleep", lambda _n: None)
    monkeypatch.setattr(monitor, "interagir_pagina_externa", fake_interagir)

    with pytest.raises(SystemExit):
        monitor.iniciar_monitoramento(
            url="https://exemplo.com",
            xpath="//div",
            intervalo=1,
            email_destino="destino@example.com",
            email_remetente="origem@example.com",
            senha_app="senha",
            usuario="Rodri",
            logger_obj=FakeLogger(),
        )

    assert any("Valor inicial" in msg for _user, msg in eventos)
    assert any("Alteracao" in msg or "Alteração" in msg for _user, msg in eventos)
