import logging
from biblioteca.utils import mascarar_cpf

class GeradorRelatorio:
    @staticmethod
    def relatorio_completo(livros, usuarios):
        logging.info("=== RELATORIO DA BIBLIOTECA ===")
        for id_livro, livro in livros.items():
            logging.info(f"Livro: {livro.titulo} | Disponivel: {livro.qtd}/{livro.qtd_total}")
        for id_usuario, usuario in usuarios.items():
            cpf_seguro = mascarar_cpf(usuario.cpf)
            logging.info(f"Usuario: {usuario.nome} CPF: {cpf_seguro} | Emprestimos: {usuario.emprestimos_ativos}")

    @staticmethod
    def relatorio_resumido(livros, usuarios):
        logging.info("=== RELATORIO RESUMIDO ===")
        total_usuarios = len(usuarios)
        livros_disponiveis = sum(l.qtd for l in livros.values())
        livros_total = sum(l.qtd_total for l in livros.values())
        
        logging.info(f"Total de Usuarios: {total_usuarios}")
        logging.info(f"Acervo de Livros: {livros_disponiveis}/{livros_total} disponiveis")