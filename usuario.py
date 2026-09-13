from abc import ABC, abstractmethod

class Usuario(ABC):
    def __init__(self, id_usuario, nome, cpf, email):
        self.id_usuario = id_usuario
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.emprestimos_ativos = 0
        self.bloqueado = False

    @property
    @abstractmethod
    def limite_emprestimos(self): pass

    @property
    @abstractmethod
    def prazo_devolucao(self): pass

    @property
    @abstractmethod
    def multiplicador_multa(self): pass


class UsuarioComum(Usuario):
    @property
    def limite_emprestimos(self): return 3
    @property
    def prazo_devolucao(self): return 7
    @property
    def multiplicador_multa(self): return 2


class UsuarioPremium(Usuario):
    @property
    def limite_emprestimos(self): return 5
    @property
    def prazo_devolucao(self): return 14
    @property
    def multiplicador_multa(self): return 1


class UsuarioFuncionario(Usuario):
    @property
    def limite_emprestimos(self): return 10
    @property
    def prazo_devolucao(self): return 30
    @property
    def multiplicador_multa(self): return 0

class UsuarioProfessor(Usuario):
    @property
    def limite_emprestimos(self): return 15
    @property
    def prazo_devolucao(self): return 60
    @property
    def multiplicador_multa(self): return 0


class UsuarioFactory:
    @staticmethod
    def criar(id_usuario, nome, cpf, email, tipo):
        tipos = {
            "comum": UsuarioComum,
            "premium": UsuarioPremium,
            "funcionario": UsuarioFuncionario,
            "professor": UsuarioProfessor
        }
        classe = tipos.get(tipo)
        if not classe:
            raise ValueError(f"Tipo de usuario invalido: {tipo}")
        return classe(id_usuario, nome, cpf, email)