# 📚 Sistema de Gestão de Biblioteca (Refatorado)

Este projeto é resultado da Avaliação (AV1) do curso de Boas Práticas de Desenvolvimento de Software. O objetivo principal foi aplicar técnicas de refatoração em um código legado monolítico, elevando sua qualidade arquitetural sem alterar o comportamento esperado, além de expandir a aplicação com novas regras de negócio.

## 🚀 O que o sistema faz
O sistema gerencia as operações básicas de uma biblioteca, permitindo:
- Cadastro de Livros e Usuários.
- Processamento de empréstimos e devoluções com cálculo dinâmico de multas por atraso.
- Geração de relatórios (completos e resumidos) do acervo e status de usuários.
- Sistema de reservas para livros esgotados.

## 🛠️ Arquitetura e Boas Práticas Aplicadas
O código foi inteiramente refatorado aplicando os seguintes conceitos:
- **SOLID (SRP & OCP):** Extração de regras de relatórios para o `GeradorRelatorio` e implementação de Polimorfismo nas entidades de `Usuario`, permitindo adicionar novos perfis sem modificar a lógica principal.
- **Design Patterns:** Uso de `Factory Pattern` para orquestrar a criação de diferentes instâncias de usuários.
- **Guard Clauses:** Remoção de aninhamento excessivo (Arrow Anti-Pattern) para um *Happy Path* legível.
- **DRY & LGPD:** Centralização da ofuscação de dados sensíveis (CPF e E-mail) em um módulo utilitário independente.
- **Logging:** Substituição de saídas de console brutas por registros de log formatados e classificados por nível de criticidade.

## ⚙️ Como executar o projeto

Certifique-se de ter o **Python 3.x** instalado. 

1. Clone o repositório.
2. Navegue até a pasta do projeto.
3. Execute o script principal para ver a simulação dos cenários:
   ```
   python main.py
   ```

## 🧪 Executando os Testes (Pytest)

O projeto conta com uma suíte de testes de caracterização para garantir a preservação das regras de negócio.

Instale o framework de testes:
```
pip install pytest
```
Execute a suíte de testes na raiz do projeto:
```
pytest test_sistema.py -v
```