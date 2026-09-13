import datetime
import logging

# Configuração base
logging.basicConfig(
    level=logging.INFO, 
    format='%(levelname)s: %(message)s'
    )

class Sistema:
    LIMITES_EMPRESTIMO = {"comum": 3, "premium": 5, "funcionario": 10}
    PRAZOS_DEVOLUCAO = {"comum": 7, "premium": 14, "funcionario": 30}
    MULTAS_ATRASO = {"comum": 2, "premium": 1, "funcionario": 0}
    
    def __init__(self):
        self.livros = {}
        self.usuarios = {}
        self.emprestimos = []

    # Métodos para LGPD
    def _mascarar_cpf(self, cpf):
        if len(cpf) == 11:
            return f"***.***.{cpf[6:9]}-{cpf[9:]}"
        return "***.***.***-**"

    def _mascarar_email(self, email):
        if "@" in email:
            nome, dominio = email.split("@")
            return f"{nome[0]}***@{dominio}"
        return "***@***"

    def add_livro(self, id_livro, titulo, autor, categoria, quantidade):
        self.livros[id_livro] = {
            "titulo": titulo, 
            "autor": autor, 
            "categoria": categoria, 
            "qtd": quantidade, 
            "qtd_total": quantidade
            }

    def add_usuario(self, id_usuario, nome, cpf, email, tipo):
        self.usuarios[id_usuario] = {
            "nome": nome, 
            "cpf": cpf, 
            "email": email, 
            "tipo": tipo, 
            "emprestimos_ativos": 0, 
            "bloqueado": False
            }

    def emprestar(self, id_usuario, id_livro):
        #Guard clauses
        if id_usuario not in self.usuarios:
            logging.warning("Usuario não encontrado.")
            return False
        if id_livro not in self.livros:
            logging.warning("Livro não encontrado.")
            return False
        
        usuario = self.usuarios[id_usuario]
        livro = self.livros[id_livro]
        
        logging.info(f"Processando emprestimo: usuario {id_usuario} CPF {usuario['cpf']} livro {id_livro}")

        if usuario["bloqueado"]:
            logging.warning("Usuario bloqueado")
            return False

        if livro["qtd"] <= 0:
            logging.warning("Livro indisponivel")
            return False

        tipo_usuario = usuario["tipo"]
        limite = self.LIMITES_EMPRESTIMO.get(tipo_usuario, 1)
        
        if usuario["emprestimos_ativos"] >= limite:
            logging.warning("Limite de emprestimos atingido")
            return False

        prazo = self.PRAZOS_DEVOLUCAO.get(tipo_usuario, 3)
        
        try:
            livro["qtd"] -= 1
            usuario["emprestimos_ativos"] += 1
            venc = datetime.date.today() + datetime.timedelta(days=prazo)
            self.emprestimos.append({"usuario": id_usuario, "livro": id_livro, "vencimento": venc, "devolvido": False})
            
            logging.info(f"Emprestimo OK para {usuario['nome']} email {usuario['email']} vence em {venc}")
            return True
            
        except Exception as erro:
            logging.error(f"Erro interno ao registrar emprestimo: {erro}")
            return False

    def devolver(self, id_usuario, id_livro):
        #Guard clause
        if id_usuario not in self.usuarios:
            logging.warning("Usuario nao encontrado")
            return -1
        
        usuario = self.usuarios[id_usuario]
        logging.info(f"Processando devolucao: usuario {id_usuario} CPF {usuario['cpf']} | livro {id_livro}")
        
        for emprestimo in self.emprestimos:
            if emprestimo["usuario"] == id_usuario and emprestimo["livro"] == id_livro and not emprestimo["devolvido"]:
                emprestimo["devolvido"] = True
                self.livros[id_livro]["qtd"] += 1
                usuario["emprestimos_ativos"] -= 1
                
                hoje = datetime.date.today()
                if hoje > emprestimo["vencimento"]:
                    dias_atraso = (hoje - emprestimo["vencimento"]).days
                    tipo_usuario = usuario["tipo"]
                    multiplicador_multa = self.MULTAS_ATRASO.get(tipo_usuario, 3)
                    
                    multa = dias_atraso * multiplicador_multa
                    logging.info(f"Devolucao com atraso. Multa: {multa}")
                    return multa
                
                logging.info("Devolucao OK no prazo")
                return 0
                
        logging.warning("Emprestimo nao encontrado")
        return -1

    def relatorio(self):
        logging.info("=== RELATORIO DA BIBLIOTECA ===")
        for id_livro in self.livros:
            logging.info("Livro: " + self.livros[id_livro]["titulo"] + " | Disponivel: " + str(self.livros[id_livro]["qtd"]) + "/" + str(self.livros[id_livro]["qtd_total"]))
        for id_usuario in self.usuarios:
            logging.info("Usuario: " + self.usuarios[id_usuario]["nome"] + " CPF: " + self.usuarios[id_usuario]["cpf"] + " | Emprestimos: " + str(self.usuarios[id_usuario]["emprestimos_ativos"]))


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
 
    print("========== CENARIO 1: emprestimos normais ==========")
    s.emprestar("U1", "L1")   # comum pega tecnico -> prazo 7 dias
    s.emprestar("U2", "L2")   # premium pega ficcao -> prazo 14 dias
    s.emprestar("U3", "L3")   # funcionario pega tecnico -> prazo 30 dias
 
    print()
    print("========== CENARIO 2: livro esgotado ==========")
    # L2 so tinha 1 exemplar, ja emprestado para U2
    s.emprestar("U1", "L2")   # deve falhar: indisponivel
 
    print()
    print("========== CENARIO 3: limite de emprestimos (comum = 3) ==========")
    # Ana (comum) ja tem L1. Vamos testar o limite.
    s.add_livro("L4", "Livro Extra 1", "Autor", "geral", 5)
    s.add_livro("L5", "Livro Extra 2", "Autor", "geral", 5)
    s.add_livro("L6", "Livro Extra 3", "Autor", "geral", 5)
    s.emprestar("U1", "L4")   # 2o emprestimo de Ana -> OK
    s.emprestar("U1", "L5")   # 3o emprestimo de Ana -> OK
    s.emprestar("U1", "L6")   # 4o emprestimo -> deve falhar (limite 3)
 
    print()
    print("========== CENARIO 4: devolucao no prazo (sem multa) ==========")
    s.devolver("U1", "L1")    # devolvido no prazo -> multa 0
 
    print()
    print("========== CENARIO 5: devolucao com ATRASO e multa por tipo ==========")
    # Para demonstrar multa, forcamos o vencimento de alguns emprestimos para o passado.
    # (Na pratica isso aconteceria com o tempo, aqui será apenas uma simulação)
    import datetime as _dt
 
    # Ana (comum): multa de 2/dia. Atraso de 5 dias -> multa 10
    for _e in s.emprestimos:
        if _e["usuario"] == "U1" and _e["livro"] == "L4":
            _e["vencimento"] = _dt.date.today() - _dt.timedelta(days=5)
    s.devolver("U1", "L4")    # esperado: multa 10
 
    # Bruno (premium): multa de 1/dia. Atraso de 10 dias -> multa 10
    for _e in s.emprestimos:
        if _e["usuario"] == "U2" and _e["livro"] == "L2":
            _e["vencimento"] = _dt.date.today() - _dt.timedelta(days=10)
    s.devolver("U2", "L2")    # esperado: multa 10
 
    # Carla (funcionario): multa 0/dia. Mesmo com atraso -> multa 0
    for _e in s.emprestimos:
        if _e["usuario"] == "U3" and _e["livro"] == "L3":
            _e["vencimento"] = _dt.date.today() - _dt.timedelta(days=20)
    s.devolver("U3", "L3")    # esperado: multa 0 (funcionario nao paga)
 
    print()
    print("========== CENARIO 6: relatorio final ==========")
    s.relatorio()
