import datetime
import logging
from biblioteca.usuario import UsuarioFactory
from biblioteca.livro import Livro
from biblioteca.relatorio import GeradorRelatorio
from biblioteca.utils import mascarar_cpf, mascarar_email

class Sistema:
    def __init__(self):
        self.livros = {}
        self.usuarios = {}
        self.emprestimos = []
        self.reservas = []

    def add_livro(self, id_livro, titulo, autor, categoria, quantidade):
        self.livros[id_livro] = Livro(id_livro, titulo, autor, categoria, quantidade)

    def add_usuario(self, id_usuario, nome, cpf, email, tipo):
        self.usuarios[id_usuario] = UsuarioFactory.criar(id_usuario, nome, cpf, email, tipo)

    def emprestar(self, id_usuario, id_livro):
        if id_usuario not in self.usuarios:
            logging.warning("Usuario nao encontrado")
            return False
            
        if id_livro not in self.livros:
            logging.warning("Livro nao encontrado")
            return False

        usuario = self.usuarios[id_usuario]
        livro = self.livros[id_livro]
        
        cpf_seguro = mascarar_cpf(usuario.cpf)
        logging.info(f"Processando emprestimo: usuario {id_usuario} CPF {cpf_seguro} livro {id_livro}")

        if usuario.bloqueado:
            logging.warning("Usuario bloqueado")
            return False

        if livro.qtd <= 0:
            logging.warning("Livro indisponivel")
            return False

        if usuario.emprestimos_ativos >= usuario.limite_emprestimos:
            logging.warning("Limite de emprestimos atingido")
            return False
        
        try:
            livro.qtd -= 1
            usuario.emprestimos_ativos += 1
            venc = datetime.date.today() + datetime.timedelta(days=usuario.prazo_devolucao)
            self.emprestimos.append({"usuario": id_usuario, "livro": id_livro, "vencimento": venc, "devolvido": False})
            
            email_seguro = mascarar_email(usuario.email)
            logging.info(f"Emprestimo OK para {usuario.nome} email {email_seguro} vence em {venc}")
            return True
            
        except Exception as erro:
            logging.error(f"Erro interno ao registrar emprestimo: {erro}")
            return False

    def devolver(self, id_usuario, id_livro):
        if id_usuario not in self.usuarios:
            logging.warning("Usuario nao encontrado")
            return -1

        usuario = self.usuarios[id_usuario]
        cpf_seguro = mascarar_cpf(usuario.cpf)
        logging.info(f"Processando devolucao: usuario {id_usuario} CPF {cpf_seguro} | livro {id_livro}")
        
        for emprestimo in self.emprestimos:
            if emprestimo["usuario"] == id_usuario and emprestimo["livro"] == id_livro and not emprestimo["devolvido"]:
                emprestimo["devolvido"] = True
                self.livros[id_livro].qtd += 1
                usuario.emprestimos_ativos -= 1
                
                hoje = datetime.date.today()
                if hoje > emprestimo["vencimento"]:
                    dias_atraso = (hoje - emprestimo["vencimento"]).days
                    multa = dias_atraso * usuario.multiplicador_multa
                    logging.info(f"Devolucao com atraso. Multa: {multa}")
                    return multa
                
                logging.info("Devolucao OK no prazo")
                return 0
                
        logging.warning("Emprestimo nao encontrado")
        return -1

    def reservar(self, id_usuario, id_livro):
        if id_usuario not in self.usuarios:
            logging.warning("Usuario nao encontrado para reserva")
            return False
            
        if id_livro not in self.livros:
            logging.warning("Livro nao encontrado para reserva")
            return False

        usuario = self.usuarios[id_usuario]
        livro = self.livros[id_livro]

        if livro.qtd > 0:
            logging.warning(f"Reserva negada: O livro '{livro.titulo}' esta disponivel para emprestimo.")
            return False

        self.reservas.append({"usuario": id_usuario, "livro": id_livro, "data": datetime.date.today()})
        logging.info(f"Reserva OK: '{usuario.nome}' reservou o livro '{livro.titulo}'")
        return True

    def relatorio(self):
        GeradorRelatorio.relatorio_completo(self.livros, self.usuarios)

    def relatorio_resumido(self):
        GeradorRelatorio.relatorio_resumido(self.livros, self.usuarios)