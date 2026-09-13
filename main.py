import logging
import datetime as _dt
from sistema import Sistema

# Configuração de logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

if __name__ == "__main__":
    s = Sistema()
 
    # --- Cadastro de livros ---
    s.add_livro("L1", "Clean Code", "Robert Martin", "tecnico", 2)
    s.add_livro("L2", "O Hobbit", "Tolkien", "ficcao", 1)
    s.add_livro("L3", "SICP", "Abelson", "tecnico", 3)
 
    # --- Cadastro de usuarios (um de cada tipo) ---
    s.add_usuario("U1", "Ana", "11122233344", "ana@email.com", "comum")
    s.add_usuario("U2", "Bruno", "55566677788", "bruno@email.com", "premium")
    s.add_usuario("U3", "Carla", "99988877766", "carla@email.com", "funcionario")
    s.add_usuario("U4", "Davyd", "12312312312", "Davyd@email.com", "professor")
 
    print("\n========== CENARIO 1: emprestimos normais ==========")
    s.emprestar("U1", "L1")   # comum pega tecnico -> prazo 7 dias
    s.emprestar("U2", "L2")   # premium pega ficcao -> prazo 14 dias
    s.emprestar("U3", "L3")   # funcionario pega tecnico -> prazo 30 dias
    s.emprestar("U4", "L1")   # professor pegando emprestado
 
    print("\n========== CENARIO 2: livro esgotado e reserva ==========")
    s.emprestar("U1", "L2")   # deve falhar: indisponivel
    s.reservar("U1", "L1")    # deve falhar: L1 está disponível
    s.reservar("U1", "L2")    # Sucesso: l2 está esgotado
 
    print("\n========== CENARIO 3: limite de emprestimos (comum = 3) ==========")
    s.add_livro("L4", "Livro Extra 1", "Autor", "geral", 5)
    s.add_livro("L5", "Livro Extra 2", "Autor", "geral", 5)
    s.add_livro("L6", "Livro Extra 3", "Autor", "geral", 5)
    s.emprestar("U1", "L4")   # 2o emprestimo de Ana -> OK
    s.emprestar("U1", "L5")   # 3o emprestimo de Ana -> OK
    s.emprestar("U1", "L6")   # 4o emprestimo -> deve falhar (limite 3)
 
    print("\n========== CENARIO 4: devolucao no prazo (sem multa) ==========")
    s.devolver("U1", "L1")    # devolvido no prazo -> multa 0
 
    print("\n========== CENARIO 5: devolucao com ATRASO e multa por tipo ==========")
    for _e in s.emprestimos:
        if _e["usuario"] == "U1" and _e["livro"] == "L4":
            _e["vencimento"] = _dt.date.today() - _dt.timedelta(days=5)
    s.devolver("U1", "L4")    # esperado: multa 10
 
    for _e in s.emprestimos:
        if _e["usuario"] == "U2" and _e["livro"] == "L2":
            _e["vencimento"] = _dt.date.today() - _dt.timedelta(days=10)
    s.devolver("U2", "L2")    # esperado: multa 10
 
    for _e in s.emprestimos:
        if _e["usuario"] == "U3" and _e["livro"] == "L3":
            _e["vencimento"] = _dt.date.today() - _dt.timedelta(days=20)
    s.devolver("U3", "L3")    # esperado: multa 0 (funcionario nao paga)
 
    print("\n========== CENARIO 6: relatorio final ==========")
    s.relatorio()
    print("")
    s.relatorio_resumido()