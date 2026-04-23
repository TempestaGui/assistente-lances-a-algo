import tkinter as tk
from tkinter import messagebox
import threading
from src.user import validar_nome
from src.scraper import capturar_valor
from src.monitor import iniciar_monitoramento
from src.logger import Logger

def main():
    janela = tk.Tk()
    janela.title("Assistente de Lances")
    janela.geometry("450x420")

    tk.Label(janela, text="Nome:").pack(pady=5)
    entrada_nome = tk.Entry(janela, width=40)
    entrada_nome.pack()

    tk.Label(janela, text="URL da página:").pack(pady=5)
    entrada_url = tk.Entry(janela, width=40)
    entrada_url.pack()

    tk.Label(janela, text="XPath do elemento:").pack(pady=5)
    entrada_xpath = tk.Entry(janela, width=40)
    entrada_xpath.pack()

    tk.Label(janela, text="Intervalo (segundos):").pack(pady=5)
    entrada_intervalo = tk.Entry(janela, width=40)
    entrada_intervalo.pack()

    tk.Label(janela, text="E-mail de destino:").pack(pady=5)
    entrada_email = tk.Entry(janela, width=40)
    entrada_email.pack()

    def iniciar():
        nome = entrada_nome.get().strip()
        url = entrada_url.get().strip()
        xpath = entrada_xpath.get().strip()
        email = entrada_email.get().strip()

        try:
            intervalo = int(entrada_intervalo.get().strip())
        except ValueError:
            messagebox.showerror("Erro", "Intervalo deve ser um número inteiro.")
            return

        if not validar_nome(nome):
            messagebox.showerror("Erro", "Nome inválido. Use ao menos 3 letras.")
            return

        if not url.startswith("http"):
            messagebox.showerror("Erro", "URL inválida.")
            return

        if not xpath:
            messagebox.showerror("Erro", "XPath não pode ser vazio.")
            return

        valor_inicial = capturar_valor(url, xpath)
        if valor_inicial is None:
            messagebox.showerror("Erro", "Valor não encontrado na página.")
            return

        logger = Logger()
        logger.registrar(nome, f"Monitoramento iniciado: {url}")

        messagebox.showinfo("Sucesso", f"Monitoramento iniciado!\nValor inicial: {valor_inicial}")

        thread = threading.Thread(
            target=iniciar_monitoramento,
            args=(url, xpath, intervalo, email, nome, logger),
            daemon=True
        )
        thread.start()

    tk.Button(janela, text="Iniciar monitoramento", command=iniciar).pack(pady=20)
    janela.mainloop()

if __name__ == "__main__":
    main()