import datetime

class Sistema:
    LIMITES_EMPRESTIMO = {"comum": 3, "premium": 5, "funcionario": 10}
    PRAZOS_DEVOLUCAO = {"comum": 7, "premium": 14, "funcionario": 30}
    MULTAS_ATRASO = {"comum": 2, "premium": 1, "funcionario": 0}
    
    def __init__(self):
        self.livros = {}
        self.usuarios = {}
        self.emprestimos = []

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
            print("Usuario não encontrado.")
            return False
        if id_livro not in self.livros:
            print("Livro não encontrado.")
            return False
        
        print("Processando emprestimo: usuario " + id_usuario + " CPF " + self.usuarios[id_usuario]["cpf"] + " livro " + id_livro)
        if id_usuario in self.usuarios:
            if id_livro in self.livros:
                if self.usuarios[id_usuario]["bloqueado"] == False:
                    if self.livros[id_livro]["qtd"] > 0:
                        # limite de emprestimos por tipo de usuario
                        if self.usuarios[id_usuario]["tipo"] == "comum":
                            lim = 3
                        elif self.usuarios[id_usuario]["tipo"] == "premium":
                            lim = 5
                        elif self.usuarios[id_usuario]["tipo"] == "funcionario":
                            lim = 10
                        else:
                            lim = 1
                        if self.usuarios[id_usuario]["emprestimos_ativos"] < lim:
                            # prazo por tipo
                            if self.usuarios[id_usuario]["tipo"] == "comum":
                                prazo = 7
                            elif self.usuarios[id_usuario]["tipo"] == "premium":
                                prazo = 14
                            elif self.usuarios[id_usuario]["tipo"] == "funcionario":
                                prazo = 30
                            else:
                                prazo = 3
                            try:
                                self.livros[id_livro]["qtd"] = self.livros[id_livro]["qtd"] - 1
                                self.usuarios[id_usuario]["emprestimos_ativos"] = self.usuarios[id_usuario]["emprestimos_ativos"] + 1
                                venc = datetime.date.today() + datetime.timedelta(days=prazo)
                                self.emp.append({"usuario": id_usuario, "livro": id_livro, "vencimento": venc, "devolvido": False})
                                print("Emprestimo OK para " + self.usuarios[id_usuario]["nome"] + " email " + self.usuarios[id_usuario]["email"] + " vence em " + str(venc))
                                return True
                            except:
                                pass
                        else:
                            print("Limite de emprestimos atingido")
                            return False
                    else:
                        print("Livro indisponivel")
                        return False
                else:
                    print("Usuario bloqueado")
                    return False
            else:
                print("Livro nao encontrado")
                return False
        else:
            print("Usuario nao encontrado")
            return False

    def devolver(self, id_usuario, id_livro):
        #Guard clause
        if id_usuario not in self.usuarios:
            print("Usuario nao encontrado")
            return -1
        print("Processando devolucao: usuario " + id_usuario + " CPF " + self.usuarios[id_usuario]["cpf"] + " | " + "livro " + id_livro)
        for emprestimo in self.emprestimos:
            if emprestimo["usuario"] == id_usuario and emprestimo["livro"] == id_livro and emprestimo["devolvido"] == False:
                emprestimo["devolvido"] = True
                self.d[id_livro]["qtd"] = self.d[id_livro]["qtd"] + 1
                self.usuarios[id_usuario]["emprestimos_ativos"] = self.usuarios[id_usuario]["emprestimos_ativos"] - 1
                # calculo de multa
                hoje = datetime.date.today()
                if hoje > emprestimo["vencimento"]:
                    dias = (hoje - emprestimo["vencimento"]).days
                    if self.usuarios[id_usuario]["tipo"] == "comum":
                        multa = dias * 2
                    elif self.usuarios[id_usuario]["tipo"] == "premium":
                        multa = dias * 1
                    elif self.usuarios[id_usuario]["tipo"] == "funcionario":
                        multa = 0
                    else:
                        multa = dias * 3
                    print("Devolucao com atraso. Multa: " + str(multa))
                    return multa
                else:
                    print("Devolucao OK no prazo")
                    return 0
        print("Emprestimo nao encontrado")
        return -1

    def relatorio(self):
        print("=== RELATORIO DA BIBLIOTECA ===")
        for id_livro in self.livros:
            print("Livro: " + self.livros[id_livro]["titulo"] + " | Disponivel: " + str(self.livros[id_livro]["qtd"]) + "/" + str(self.livros[id_livro]["qtd_total"]))
        for id_usuario in self.usuarios:
            print("Usuario: " + self.usuarios[id_usuario]["nome"] + " CPF: " + self.usuarios[id_usuario]["cpf"] + " | Emprestimos: " + str(self.usuarios[id_usuario]["emprestimos_ativos"]))


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
