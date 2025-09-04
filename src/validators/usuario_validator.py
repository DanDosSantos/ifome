import re

def validar_usuario(nome, email, senha, confirmar_senha, telefone):
    erros = []

    if not nome or not email or not senha or not telefone:
        erros.append("Todos os campos são obrigatórios.")
    
    if len(nome.split()) < 2:
        erros.append("Digite seu nome completo.")
    
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        erros.append("Email inválido.")
    
    if len(senha) < 6:
        erros.append("A senha deve ter pelo menos 6 caracteres.")

    if senha != confirmar_senha:
        erros.append("As senhas não coincidem.")
    
    if not re.match(r"^\+?\d{10,15}$", telefone):
        erros.append("Telefone inválido. Deve conter apenas números e pode incluir o código do país.")
    
    return erros