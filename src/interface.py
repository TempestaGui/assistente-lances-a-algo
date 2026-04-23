import tkinter as tk
from tkinter import messagebox
import threading
from src.user import validar_nome
from src.scraper import capturar_valor, detectar_xpath_automatico
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
    frame_xpath = tk.Frame(janela)
    frame_xpath.pack()
    entrada_xpath = tk.Entry(frame_xpath, width=30)
    entrada_xpath.pack(side=tk.LEFT)

    def detectar():
        url = entrada_url.get().strip()
        if not url.startswith("http"):
            messagebox.showerror("Erro", "Informe a URL primeiro.")
            return
        print("Detectando XPath...")
        xpath = detectar_xpath_automatico(url)
        if xpath:
            entrada_xpath.delete(0, tk.END)
            entrada_xpath.insert(0, xpath)
            print(f"XPath detectado: {xpath}")
        else:
            messagebox.showerror("Erro", "Não foi possível detectar o XPath.")

    tk.Button(frame_xpath, text="Detectar", command=detectar).pack(side=tk.LEFT, padx=5)

    tk.Label(janela, text="Intervalo (segundos):").pack(pady=5)
    entrada_intervalo = tk.Entry(janela, width=40)
    entrada_intervalo.pack()

    tk.Label(janela, text="E-mail de destino:").pack(pady=5)
    entrada_email = tk.Entry(janela, width=40)
    entrada_email.pack()

    tk.Label(janela, text="Seu e-mail (remetente):").pack(pady=5)
    entrada_remetente = tk.Entry(janela, width=40)
    entrada_remetente.pack()

    tk.Label(janela, text="Senha de app do Gmail:").pack(pady=5)
    entrada_senha = tk.Entry(janela, width=40, show="*")
    entrada_senha.pack()

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
            args=(url, xpath, intervalo, email, entrada_remetente.get().strip(), entrada_senha.get().strip(), nome, logger),
            daemon=True
        )
        thread.start()

    tk.Button(janela, text="Iniciar monitoramento", command=iniciar).pack(pady=20)
    janela.mainloop()

if __name__ == "__main__":
    main()