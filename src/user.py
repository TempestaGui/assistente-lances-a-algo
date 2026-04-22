# identificação do usuário
import re
import logging
 
logger = logging.getLogger(__name__)
 
 
def validar_nome(nome: str) -> bool:
    """Retorna True se o nome tem ao menos 3 letras e contém apenas letras (compostos permitidos)."""
    nome = nome.strip()
    if len(nome) < 3:
        return False
    return bool(re.fullmatch(r'[A-Za-zÀ-ÿ]+( [A-Za-zÀ-ÿ]+)*', nome))
 
 
def obter_nome_usuario() -> str:
    """
    Solicita o nome do usuário via terminal, valida e o retorna.
    O nome é armazenado e registrado nos logs do sistema.
    """
    while True:
        nome = input("Informe seu nome: ").strip()
 
        if validar_nome(nome):
            logger.info("Usuário identificado: %s", nome)
            return nome
 
        if len(nome) < 3:
            print(f"  Erro: nome muito curto ({len(nome)} caractere(s)). Mínimo: 3.\n")
        else:
            print("  Erro: use apenas letras. Nomes compostos são permitidos.\n")