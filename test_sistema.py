import pytest
import datetime
from sistema import Sistema

@pytest.fixture
def biblioteca():
    s = Sistema()
    s.add_livro("L1", "Python Fluente", "Luciano Ramalho", "tecnico", 1)
    s.add_livro("L2", "Design Patterns", "GoF", "tecnico", 5)
    s.add_usuario("U1", "Comum User", "11122233344", "comum@email.com", "comum")
    s.add_usuario("U2", "Premium User", "55566677788", "premium@email.com", "premium")
    return s

def test_emprestimo_bem_sucedido_reduz_estoque(biblioteca):
    sucesso = biblioteca.emprestar("U1", "L1")
    assert sucesso is True
    assert biblioteca.livros["L1"].qtd == 0
    assert biblioteca.usuarios["U1"].emprestimos_ativos == 1

def test_nao_deve_emprestar_livro_sem_estoque(biblioteca):
    biblioteca.emprestar("U1", "L1") # Esgota o livro L1
    sucesso = biblioteca.emprestar("U2", "L1") # Tenta emprestar novamente
    assert sucesso is False

def test_respeito_ao_limite_de_emprestimos_comum(biblioteca):
    biblioteca.add_livro("L3", "Livro 3", "Autor", "geral", 5)
    biblioteca.add_livro("L4", "Livro 4", "Autor", "geral", 5)
    
    biblioteca.emprestar("U1", "L2")
    biblioteca.emprestar("U1", "L3")
    biblioteca.emprestar("U1", "L4") # Atinge o limite de 3
    
    biblioteca.add_livro("L5", "Livro 5", "Autor", "geral", 5)
    sucesso = biblioteca.emprestar("U1", "L5") # O 4º empréstimo deve falhar
    assert sucesso is False

def test_calculo_de_multa_com_atraso(biblioteca):
    biblioteca.emprestar("U1", "L2")
    
    # Simula o vencimento para 5 dias no passado
    for emp in biblioteca.emprestimos:
        if emp["usuario"] == "U1" and emp["livro"] == "L2":
            emp["vencimento"] = datetime.date.today() - datetime.timedelta(days=5)
            
    # Usuário comum: 2 reais por dia de atraso (5 * 2 = 10)
    multa = biblioteca.devolver("U1", "L2")
    assert multa == 10