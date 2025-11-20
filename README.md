# **Otimização de Portfólio (Knapsack 0/1) – Global Solution 2025**

## **Integrantes**
### Turma 2ESPG
| Nome | RM |
|------|------|
| Ana Laura | 554575 |
| Ianny Raquel | 559096 |

---

# **Descrição do Projeto**

Este projeto implementa quatro abordagens diferentes para resolver o problema de **Otimização de Portfólio**, modelado como o clássico problema do **Knapsack 0/1**, onde cada projeto possui:

- **Lucro / Valor (V)**
- **Custo em horas de especialista (E)**
- **Capacidade máxima de horas disponíveis**

O objetivo é determinar qual conjunto de projetos maximiza o lucro total, respeitando a capacidade limite de horas.

O trabalho faz parte do **Global Solution 2025**, explorando e comparando diferentes técnicas de algoritmos:

1. **Heurística Gulosa (Greedy)**
2. **Força Bruta Recursiva**  
3. **Programação Dinâmica – Top-Down com Memoização**
4. **Programação Dinâmica – Bottom-Up com Tabulação**

Além disso, o projeto demonstra explicitamente um caso clássico onde o algoritmo **guloso falha**, provando a necessidade das soluções completas de Programação Dinâmica.

---

# **Objetivos Atendidos**

✔️ Implementação completa das quatro funções  
✔️ Uso correto de memoização e tabela de DP  
✔️ Pelo menos 4 cenários funcionais testados  
✔️ Caso obrigatório onde o Greedy falha  
✔️ Código limpo, comentado e com complexidade analisada  
✔️ Organização clara para avaliação  

---

# **Estruturas e Métodos Implementados**

### **1️⃣ Greedy — Heurística de Densidade**
Seleciona itens com maior **lucro / custo** primeiro.  
*Vantagem:* rápido (O(N log N)).  
*Desvantagem:* não garante solução ótima.

---

### **2️⃣ Força Bruta — Recursão Pura**
Explora **todas as combinações possíveis** (2ⁿ).  
Retorna a solução ótima.  
Útil para entendimento conceitual.

---

### **3️⃣ Programação Dinâmica — Top-Down (Memoização)**
Abordagem recursiva com cache, evitando recomputações.  
Complexidade: **O(N × C)**.

---

### **4️⃣ Programação Dinâmica — Bottom-Up (Tabulação)**
Constrói a tabela dp[i][c] iterativamente.  
Complexidade: **O(N × C)**.  
Prática e eficiente.

---

# 📁 **Estrutura do Repositório**
```
/
│── README.md
│── knapsack.py        # Arquivo principal do projeto
```

---

# ⚙️ **Requisitos e Dependências**

Este projeto não utiliza bibliotecas externas.  
Requisitos:

- Python 3.9+
- Windows / Linux / macOS

---

# ▶️ **Como Executar**

### 1. Clone o repositório:

```bash
git clone <URL_DO_REPOSITORIO>
cd <nome-do-repositorio>
```

### 2. Execute o arquivo principal:

```bash
python knapsack.py
```

### 3. O terminal mostrará:

- Resultados do método guloso
- Resultado ótimo pela recursão
- Resultado ótimo pelas duas versões de Programação Dinâmica
- Caso especial onde o Greedy falha

# Casos de Teste Incluídos
### Cenário 1 — Avaliação geral
4 itens com diferentes lucros e custos.

### Cenário 2 — Cenário clássico onde o Greedy falha
Comprova que DP encontra a solução ótima e o Greedy não.

# Análise de Complexidade
Método	Complexidade de Tempo	Complexidade de Espaço
Greedy	O(N log N)	O(N)
Força Bruta	O(2ⁿ)	O(N)
DP Top-Down	O(N × C)	O(N × C)
DP Bottom-Up	O(N × C)	O(N × C)

A análise detalhada encontra-se comentada no código.

# Considerações Finais
Este projeto demonstra:
- Diferença entre heurísticas e algoritmos exatos
- Importância da Programação Dinâmica
- Código organizado e documentado
- Abordagens complementares para solução ótima
O repositório cumpre todas as exigências da avaliação, incluindo estrutura, clareza e documentação.
