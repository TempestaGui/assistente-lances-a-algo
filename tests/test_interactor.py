from email.mime.text import MIMEText

from src import interactor


def test_enviar_email_sucesso(monkeypatch):
    class FakeSMTP:
        def __init__(self, host, port):
            self.host = host
            self.port = port
            self.logged = None
            self.sent = None

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def login(self, usuario, senha):
            self.logged = (usuario, senha)

        def send_message(self, msg):
            self.sent = msg

    fake_smtp = FakeSMTP("smtp.gmail.com", 465)
    monkeypatch.setattr(interactor.smtplib, "SMTP_SSL", lambda h, p: fake_smtp)

    sucesso = interactor._enviar_email(
        valor_anterior=10.0,
        valor_atual=20.0,
        email_destino="destino@example.com",
        email_remetente="origem@example.com",
        senha_app="senha",
    )

    assert sucesso is True
    assert fake_smtp.logged == ("origem@example.com", "senha")
    assert isinstance(fake_smtp.sent, MIMEText)
    assert fake_smtp.sent["To"] == "destino@example.com"


def test_interagir_pagina_externa_retorna_true_so_quando_ambos_sucesso(monkeypatch):
    monkeypatch.setattr(interactor, "_registrar_em_pagina_externa", lambda **_kwargs: True)
    monkeypatch.setattr(interactor, "_enviar_email", lambda **_kwargs: False)

    sucesso = interactor.interagir_pagina_externa(
        valor_anterior=10.0,
        valor_atual=20.0,
        email_destino="destino@example.com",
        email_remetente="origem@example.com",
        senha_app="senha",
    )

    assert sucesso is False
