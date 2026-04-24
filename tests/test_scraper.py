from types import SimpleNamespace

import pytest
from selenium.common.exceptions import TimeoutException

from src import scraper


@pytest.mark.parametrize(
    "texto,esperado",
    [
        ("R$ 1.234,56", 1234.56),
        ("1,234.56", 1234.56),
        ("Valor: 99", 99.0),
        ("1 bilhões 308 milhões 966 mil 795 reais 246", 1308966795.0),
        ("sem numero", None),
    ],
)
def test_extrair_valor_numerico(texto, esperado):
    assert scraper.extrair_valor_numerico(texto) == esperado


def test_aguardar_texto_nao_vazio_retorna_texto_do_elemento():
    elemento = SimpleNamespace(text=" 123,45 ")
    driver = SimpleNamespace(
        find_element=lambda *_args, **_kwargs: elemento,
        execute_script=lambda *_args, **_kwargs: "",
    )

    resultado = scraper._aguardar_texto_nao_vazio(driver, "//div", timeout=1)

    assert resultado == "123,45"


def test_capturar_valor_fluxo_sucesso(monkeypatch):
    class FakeDriver:
        def __init__(self):
            self.quit_called = False

        def get(self, _url):
            return None

        def find_element(self, *_args, **_kwargs):
            return SimpleNamespace(location={"x": 10, "y": 20})

        def quit(self):
            self.quit_called = True

    fake_driver = FakeDriver()

    monkeypatch.setattr(scraper.webdriver, "ChromeOptions", lambda: SimpleNamespace(add_argument=lambda *_a: None))
    monkeypatch.setattr(scraper, "Service", lambda *_a, **_k: object())
    monkeypatch.setattr(scraper.ChromeDriverManager, "install", lambda self: "driver")
    monkeypatch.setattr(scraper.webdriver, "Chrome", lambda **_kwargs: fake_driver)
    monkeypatch.setattr(scraper, "WebDriverWait", lambda *_a, **_k: SimpleNamespace(until=lambda _cond: True))
    monkeypatch.setattr(scraper.EC, "presence_of_element_located", lambda _locator: object())
    monkeypatch.setattr(scraper, "_aguardar_texto_nao_vazio", lambda *_a, **_k: "R$ 1.234,56")

    valor = scraper.capturar_valor("https://exemplo.com", "//div", timeout=1)

    assert valor == 1234.56
    assert fake_driver.quit_called is True


def test_capturar_valor_timeout(monkeypatch):
    class FakeDriver:
        def __init__(self):
            self.quit_called = False

        def get(self, _url):
            return None

        def quit(self):
            self.quit_called = True

    fake_driver = FakeDriver()

    monkeypatch.setattr(scraper.webdriver, "ChromeOptions", lambda: SimpleNamespace(add_argument=lambda *_a: None))
    monkeypatch.setattr(scraper, "Service", lambda *_a, **_k: object())
    monkeypatch.setattr(scraper.ChromeDriverManager, "install", lambda self: "driver")
    monkeypatch.setattr(scraper.webdriver, "Chrome", lambda **_kwargs: fake_driver)

    def _raise_timeout(_cond):
        raise TimeoutException("timeout")

    monkeypatch.setattr(scraper, "WebDriverWait", lambda *_a, **_k: SimpleNamespace(until=_raise_timeout))

    valor = scraper.capturar_valor("https://exemplo.com", "//div", timeout=1)

    assert valor is None
    assert fake_driver.quit_called is True
