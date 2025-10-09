from src.models.restaurante_model import Restaurante
import re

def validar_restaurante(nome, cnpj, email, telefone, senha, confirmar_senha, cpf, tel_resp, hora_abertura, hora_fechamento):
    erros = []

    if not nome or not cnpj or not email or not telefone or not senha or not confirmar_senha or not cpf or not tel_resp or not hora_abertura or not hora_fechamento:
        erros.append("Todos os campos são obrigatórios.")

    if len(cnpj) != 14 or not cnpj.isdigit():
        erros.append("CNPJ inválido. Deve conter 14 dígitos numéricos.") # Regra muda em JUL/2026
    
    # Checar CNPJ existente no banco de dados
    if len(cnpj) == 14 and cnpj.isdigit():
        restaurante_existente = Restaurante.query.filter_by(cnpj=cnpj).first()
        if restaurante_existente:
            erros.append("O CNPJ informado já está cadastrado no sistema.")
    
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        erros.append("Email inválido.")

    if re.match(r"[^@]+@[^@]+\.[^@]+", email):
        email_existente = Restaurante.query.filter_by(email_responsavel=email).first()
        if email_existente:
            erros.append("O email informado já está cadastrado no sistema.")

    # validação de telefone com ddd inicial:
    if not re.match(r"^\(\d{2}\) \d{4,5}-\d{4}$", telefone):
        erros.append("Telefone inválido. Formato esperado: (XX) XXXX-XXXX ou (XX) XXXXX-XXXX")

    if len(senha) < 8:
        erros.append("A senha deve ter pelo menos 8 caracteres.")
    if not re.search(r'[A-Z]', senha):
        erros.append("A senha deve conter pelo menos uma letra maiúscula.")
    if not re.search(r'[0-9]', senha):
        erros.append("A senha deve conter pelo menos um número.")
    if not re.search(r'[^A-Za-z0-9]', senha):
        erros.append("A senha deve conter pelo menos um caractere especial.")

    if confirmar_senha != senha:
        erros.append("As senha não coincidem.")
    
    if not re.match(r"^\(\d{2}\) \d{4,5}-\d{4}$", tel_resp):
        erros.append("Telefone do responsável inválido. Formato esperado: (XX) XXXX-XXXX ou (XX) XXXXX-XXXX")

    # Validação de CPF (apenas números, 11 dígitos)
    if len(cpf) != 11 or not cpf.isdigit():
        erros.append("CPF inválido. Deve conter 11 dígitos numéricos.")

    # Validação de horário no formato HH:MM
    if not re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", hora_abertura):
        erros.append("Hora de abertura inválida. Formato esperado: HH:MM (00:00 a 23:59).")
    if not re.match(r"^(?:[01]\d|2[0-3]):[0-5]\d$", hora_fechamento):
        erros.append("Hora de fechamento inválida. Formato esperado: HH:MM (00:00 a 23:59).")

    return erros