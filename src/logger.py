import logging
import os
from datetime import datetime

class Logger:
    """
    Registra todas as ações do usuário em arquivo de log.

    Complexity:
        O(1) por operação de registro.
    """

    def __init__(self):
        os.makedirs('logs', exist_ok=True)
        logging.basicConfig(
            filename=f'logs/acoes_{datetime.now().strftime("%Y%m%d_%H%M%S")}.log',
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        self.logger = logging.getLogger('assistente')

    def registrar(self, usuario: str, acao: str):
        """
        Registra uma ação do usuário no log.

        Args:
            usuario: Nome do usuário que realizou a ação.
            acao: Descrição da ação realizada.
        
        Complexity:
            O(1).
        """
        mensagem = f"[{usuario}] {acao}"
        self.logger.info(mensagem)
        print(f"[LOG] {mensagem}")