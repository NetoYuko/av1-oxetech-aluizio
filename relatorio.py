import logging
from utils import mascarar_cpf

class GeradorRelatorio:
    @staticmethod
    def relatorio_completo(livros, usuarios):
        logging.info("=== RELATORIO DA BIBLIOTECA ===")
        for id_livro, livro in livros.items():
            logging.info(f"Livro: {livro['titulo']} | Disponivel: {livro['qtd']}/{livro['qtd_total']}")
        for id_usuario, usuario in usuarios.items():
            cpf_seguro = mascarar_cpf(usuario.cpf)
            logging.info(f"Usuario: {usuario.nome} CPF: {cpf_seguro} | Emprestimos: {usuario.emprestimos_ativos}")