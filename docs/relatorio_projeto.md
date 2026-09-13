# Relatório de Refatoração - AV1 Boas Práticas de Desenvolvimento

## 1. Problemas Identificados e 2. Justificativas (Categorias A-E)

### A. Qualidade e Code Smells (Aula 2)
*   **Problemas:** Uso de números mágicos espalhados pelo código para limites, prazos e multas; uso de estruturas anêmicas e siglas confusas para as coleções de dados (`self.d`, `self.u`, `self.emp`).
*   **Justificativa:** A extração de estruturas de dados obscuras para entidades de domínio reais (ex: classe `Livro`) e a remoção de números mágicos previnem falhas de manutenção acidental e tornam o código mais legível.

### B. Nomenclatura e Funções Pequenas (Aula 3)
*   **Problemas:** Variáveis de escopo interno com nomenclaturas de uma letra ou abreviações sem significado (`id_u`, `id_l`, `t`, `cat`, `e`); método `emprestar` excessivamente longo acumulando lógicas de validação.
*   **Justificativa:** A aplicação de nomes intencionais (como `id_usuario` e `emprestimo`) e a simplificação do escopo das funções reduzem drasticamente a carga cognitiva necessária para compreender o fluxo de execução.

### C. Aninhamento e Tratamento de Erros (Aula 4)
*   **Problemas:** Aninhamento vertical extremo de condicionais `if/else` (Arrow Anti-Pattern); uso de `except: pass`, silenciando falhas críticas no registro de empréstimos e dificultando o *debugging*.
*   **Justificativa:** A inversão das condições através de *Guard Clauses* permitiu retornar falhas antecipadamente, eliminando a identação profunda e isolando o "caminho feliz" com um tratamento de exceções explícito e seguro.

### D. Logging e Princípios (Aula 5)
*   **Problemas:** Uso indiscriminado da função `print()` para auditoria; vazamento de dados pessoais sensíveis (CPF e E-mail) no terminal em texto plano, violando a LGPD; repetição de lógicas de formatação (violação do DRY).
*   **Justificativa:** A implementação da biblioteca nativa `logging` e a centralização de métodos de ofuscação no arquivo `utils.py` garantem conformidade com a privacidade de dados e rastreabilidade profissional através de níveis de severidade (INFO, WARNING, ERROR).

### E. SOLID (Aula 6)
*   **Problemas:** A classe `Sistema` possuía múltiplas razões para mudar, gerenciando cálculos, regras de negócio e formatação visual (violação do SRP); a adição de novos perfis exigiria a alteração direta de cadeias de `if/elif` nas entranhas do método (violação do OCP).
*   **Justificativa:** A delegação da formatação visual para a classe `GeradorRelatorio` (SRP) e a criação de entidades polimórficas instanciadas via `UsuarioFactory` (OCP) desacoplaram a arquitetura, permitindo injetar novos comportamentos (como o usuário Professor) sem alterar as regras centrais.

---

## 3. Correção de Bug Crítico (Parte 1-C)

**O Bug:**
Ocorria um `KeyError` fatal que causava a interrupção abrupta (crash) de todo o sistema.

**Por que acontecia:**
Na primeira linha do método `emprestar` legado, havia uma concatenação de string em um `print()` que tentava acessar diretamente o dicionário do usuário: `self.u[id_u]["cpf"]`. O código tentava extrair o CPF *antes* de executar a verificação de segurança (`if id_u in self.u`). Caso o ID do usuário fornecido não existisse no banco de dados, o Python lançava a exceção ao tentar buscar uma chave inexistente.

**Como foi corrigido:**
O erro foi sanado organicamente durante a refatoração para *Guard Clauses*. A verificação de existência do usuário (`if id_usuario not in self.usuarios: return False`) foi realocada para o topo absoluto do método. O acesso aos dados e a geração do log de processamento só ocorrem se o objeto do usuário for validado e retornado com sucesso.