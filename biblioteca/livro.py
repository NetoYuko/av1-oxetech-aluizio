class Livro:
    def __init__(self, id_livro, titulo, autor, categoria, quantidade):
        self.id_livro = id_livro
        self.titulo = titulo
        self.autor = autor
        self.categoria = categoria
        self.qtd = quantidade
        self.qtd_total = quantidade