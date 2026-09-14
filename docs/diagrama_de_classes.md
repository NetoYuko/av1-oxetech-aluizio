```mermaid
classDiagram
    class Sistema {
        - dict livros
        - dict usuarios
        - list emprestimos
        - list reservas
        + add_livro(id, titulo, autor, cat, qtd)
        + add_usuario(id, nome, cpf, email, tipo)
        + emprestar(id_usuario, id_livro) bool
        + devolver(id_usuario, id_livro) float
        + reservar(id_usuario, id_livro) bool
        + relatorio()
        + relatorio_resumido()
    }

    class Livro {
        + str id_livro
        + str titulo
        + str autor
        + str categoria
        + int qtd
        + int qtd_total
    }

    class Usuario {
        <<Abstract>>
        + str id_usuario
        + str nome
        + str cpf
        + str email
        + int emprestimos_ativos
        + bool bloqueado
        + limite_emprestimos()*
        + prazo_devolucao()*
        + multiplicador_multa()*
    }

    class GeradorRelatorio {
        + relatorio_completo(livros, usuarios)$
        + relatorio_resumido(livros, usuarios)$
    }

    class UsuarioFactory {
        + criar(id, nome, cpf, email, tipo)$ Usuario
    }

    Usuario <|-- UsuarioComum
    Usuario <|-- UsuarioPremium
    Usuario <|-- UsuarioFuncionario
    Usuario <|-- UsuarioProfessor
    
    Sistema --> Livro : gerencia
    Sistema --> Usuario : gerencia
    Sistema ..> UsuarioFactory : utiliza
    Sistema ..> GeradorRelatorio : delega
