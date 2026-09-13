# métodos para LGPD
def mascarar_cpf(cpf):
    if len(cpf) == 11:
        return f"***.***.{cpf[6:9]}-{cpf[9:]}"
    return "***.***.***-**"

def mascarar_email(email):
    if "@" in email:
        nome, dominio = email.split("@")
        return f"{nome[0]}***@{dominio}"
    return "***@***"