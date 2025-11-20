import sys

# Aumentar o limite de recursão para permitir testes com profundidade maior
sys.setrecursionlimit(2000)


# -----------------------------
# DEFINIÇÃO DA ESTRUTURA ITEM
# -----------------------------
class ItemProjeto:
    """
    Representa um projeto com:
    - nome: identificador textual
    - lucro: valor / benefício associado (V)
    - custo_horas: horas de especialista necessárias (E)
    """
    def __init__(self, nome, lucro, custo_horas):
        self.nome = nome
        self.lucro = lucro          # Lucro / Impacto (V)
        self.custo_horas = custo_horas  # Custo em horas (E)

    def __repr__(self):
        return f"{self.nome}(V={self.lucro}, E={self.custo_horas})"


# ---------------------------------------------------------
# FUNÇÃO 1: GREEDY (ESTRATÉGIA GULOSA BASEADA EM DENSIDADE)
# ---------------------------------------------------------
def greedy_select(cap_max, itens):
    """
    Seleciona projetos usando uma heurística gulosa baseada na razão
    lucro / horas (densidade).

    Estratégia:
    1. Calcular a densidade (lucro / custo_horas) de cada item.
    2. Ordenar do maior para o menor.
    3. Inserir sequencialmente enquanto couber na capacidade restante.

    Observação: método rápido, mas nem sempre retorna a solução ótima
    para o problema do Knapsack 0/1.

    Retorno:
    - (lucro_total, lista_nomes_selecionados)
    """
    # Ordena os itens por densidade (lucro por hora) decrescente
    itens_ordenados = sorted(itens, key=lambda it: it.lucro / it.custo_horas, reverse=True)

    lucro_total = 0
    horas_consumidas = 0
    selecionados = []

    for it in itens_ordenados:
        if horas_consumidas + it.custo_horas <= cap_max:
            selecionados.append(it.nome)
            lucro_total += it.lucro
            horas_consumidas += it.custo_horas

    return lucro_total, selecionados


# ---------------------------------------------------------
# FUNÇÃO 2: FORÇA BRUTA RECURSIVA (EXPORA TODAS AS COMBINAÇÕES)
# ---------------------------------------------------------
def brute_force_knapsack(cap_max, itens, k):
    """
    Solução recursiva que avalia incluir ou não cada item (0/1 knapsack),
    explorando toda a árvore de decisões.

    Recorrência:
    F(k, c) = max(
        F(k-1, c),                                   # não incluir o k-ésimo item
        lucro_k + F(k-1, c - custo_k)    if cabe      # incluir o k-ésimo item
    )

    Caso base:
    - k == 0 (nenhum item disponível) -> 0
    - c == 0 (capacidade zero) -> 0

    Complexidade de tempo: O(2^N) — exponencial (cada item gera 2 ramos).
    Uso: apenas para instâncias pequenas ou para demonstrar conceito.
    """
    # Caso base: sem itens ou sem capacidade
    if k == 0 or cap_max == 0:
        return 0

    item_atual = itens[k-1]

    # Se o item atual requer mais horas do que a capacidade restante -> não pode incluir
    if item_atual.custo_horas > cap_max:
        return brute_force_knapsack(cap_max, itens, k-1)
    else:
        # opção incluir
        incluir = item_atual.lucro + brute_force_knapsack(cap_max - item_atual.custo_horas, itens, k-1)
        # opção não incluir
        nao_incluir = brute_force_knapsack(cap_max, itens, k-1)
        return max(incluir, nao_incluir)


# ---------------------------------------------------------
# FUNÇÃO 3: TOP-DOWN COM MEMOIZAÇÃO (PD - RECURSIVA + CACHE)
# ---------------------------------------------------------
def memoized_knapsack(cap_max, itens, k, cache=None):
    """
    Versão top-down (recursiva) com memoização para evitar recomputações
    dos subproblemas repetidos.

    Estado do subproblema:
    - (k, cap) onde k = número de itens considerados (prefixo), cap = capacidade restante

    Cache (dicionário) armazena o resultado de cada estado para reaproveitamento.

    Complexidade de tempo: O(N * C) — cada par (k, cap) é resolvido no máximo uma vez.
    Complexidade de espaço: O(N * C) para o cache (no pior caso).
    """
    if cache is None:
        cache = {}

    chave = (k, cap_max)
    if chave in cache:
        return cache[chave]

    # Caso base
    if k == 0 or cap_max == 0:
        cache[chave] = 0
        return 0

    item_atual = itens[k-1]

    if item_atual.custo_horas > cap_max:
        resposta = memoized_knapsack(cap_max, itens, k-1, cache)
    else:
        incluir = item_atual.lucro + memoized_knapsack(cap_max - item_atual.custo_horas, itens, k-1, cache)
        nao_incluir = memoized_knapsack(cap_max, itens, k-1, cache)
        resposta = max(incluir, nao_incluir)

    cache[chave] = resposta
    return resposta


# ---------------------------------------------------------
# FUNÇÃO 4: BOTTOM-UP (PROGRAMACAO DINAMICA ITERATIVA / TABULAÇÃO)
# ---------------------------------------------------------
def dp_iterative_knapsack(cap_max, itens):
    """
    Construção iterativa da tabela DP (tabulação).

    Definição da tabela:
    dp[i][c] = lucro máximo considerando os primeiros i itens (i de 0..n)
               com capacidade c (c de 0..cap_max)

    Interpretação:
    - Cada célula dp[i][c] representa a melhor solução possível usando apenas
      os i primeiros itens e com limite de horas igual a c.
    - dp[0][*] = 0 (sem itens não há lucro)
    - dp[*][0] = 0 (capacidade zero => lucro zero)

    Atualização (transição):
    Se custo_i <= c:
        dp[i][c] = max(dp[i-1][c], lucro_i + dp[i-1][c - custo_i])
    Caso contrário:
        dp[i][c] = dp[i-1][c]

    Complexidade de tempo: O(N * C)
    Complexidade de espaço: O(N * C) (pode ser reduzida para O(C) com otimização de espaço)
    """
    n = len(itens)
    # tabela com (n+1) linhas e (cap_max+1) colunas, inicializada com zeros
    dp = [[0 for _ in range(cap_max + 1)] for _ in range(n + 1)]

    for i in range(1, n + 1):
        item = itens[i-1]
        lucro = item.lucro
        custo = item.custo_horas

        for c in range(1, cap_max + 1):
            if custo <= c:
                # máximo entre: não pegar o item (linha anterior) ou pegar e somar com espaço restante
                dp[i][c] = max(dp[i-1][c], lucro + dp[i-1][c - custo])
            else:
                # não cabe: copia valor da linha anterior
                dp[i][c] = dp[i-1][c]

    # dp[n][cap_max] contém o lucro máximo para todos os n itens com capacidade cap_max
    return dp[n][cap_max]


# ---------------------------------------------------------
# BLOCOS DE TESTE / EXECUÇÃO (EXEMPLOS)
# ---------------------------------------------------------
if __name__ == "__main__":
    print("=== OTIMIZAÇÃO DE PORTFÓLIO - GLOBAL SOLUTION 2025 (VERSÃO REFORMULADA) ===\n")

    # Exemplo 1 - cenário simples
    capacidade_total = 10
    inventario = [
        ItemProjeto("Projeto A", 12, 4),
        ItemProjeto("Projeto B", 10, 3),
        ItemProjeto("Projeto C", 7, 2),
        ItemProjeto("Projeto D", 4, 3)
    ]

    print("--- CENÁRIO 1: DADOS INICIAIS ---")
    print(f"Capacidade: {capacidade_total}")
    print(f"Itens: {inventario}\n")

    # Greedy
    lucro_greedy, itens_greedy = greedy_select(capacidade_total, inventario)
    print(f"Greedy: Lucro = {lucro_greedy} | Selecionados: {itens_greedy}")

    # Recursiva pura (força bruta)
    lucro_brut = brute_force_knapsack(capacidade_total, inventario, len(inventario))
    print(f"Recursiva (Força Bruta): Lucro = {lucro_brut}")

    # Memoização (top-down)
    lucro_memo = memoized_knapsack(capacidade_total, inventario, len(inventario))
    print(f"PD (Top-Down memo): Lucro = {lucro_memo}")

    # PD iterativa (bottom-up)
    lucro_dp = dp_iterative_knapsack(capacidade_total, inventario)
    print(f"PD (Bottom-Up): Lucro = {lucro_dp}")

    print("\n" + "="*50 + "\n")

    # Exemplo 2 - cenário clássico que demonstra falha do greedy
    print("--- CENÁRIO 2: PROVA DE FALHA DO ALGORITMO GULOSO ---")
    cap_teste = 50
    conjunto_teste = [
        ItemProjeto("Proj A", 60, 10),   # densidade = 6.0
        ItemProjeto("Proj B", 100, 20),  # densidade = 5.0
        ItemProjeto("Proj C", 120, 30)   # densidade = 4.0
    ]
    print(f"Capacidade: {cap_teste}")
    print(f"Itens: {conjunto_teste}\n")

    lucro_g, selec_g = greedy_select(cap_teste, conjunto_teste)
    lucro_opt = dp_iterative_knapsack(cap_teste, conjunto_teste)

    print(f"Resultado Greedy: {lucro_g} (Escolheu {selec_g})")
    print(f"Resultado Ótimo (PD): {lucro_opt}")

    if lucro_g < lucro_opt:
        print("\n>> CONCLUSÃO: O método guloso falhou em encontrar a solução ótima.")
        print("   Ele priorizou a maior densidade (Proj A), impedindo a combinação B+C,")
        print("   que gera lucro superior (B + C = 220).")
    else:
        print("Neste caso o greedy encontrou a solução ótima (situação atípica para este exemplo).")


# ---------------------------------------------------------
# ANÁLISE DE COMPLEXIDADE (BLOCO RESUMO PARA AVALIAÇÃO)
# ---------------------------------------------------------
"""
Resumo teórico das complexidades temporais das quatro abordagens:

1) greedy_select (Guloso por densidade)
   - Complexidade de tempo: O(N log N) dominante pela ordenação dos itens.
   - Complexidade de espaço: O(N) para a lista ordenada/resultado.
   - Observação: muito eficiente, porém não garante solução ótima para Knapsack 0/1.

2) brute_force_knapsack (Recursiva pura - força bruta)
   - Complexidade de tempo: O(2^N) (exponencial) — cada item gera duas decisões.
   - Complexidade de espaço: O(N) pela profundidade da pilha de chamadas (recursão).
   - Observação: impraticável para N moderadamente grande.

3) memoized_knapsack (Top-down com memoização)
   - Complexidade de tempo: O(N * C) — cada estado (k, cap) é computado no máximo uma vez.
   - Complexidade de espaço: O(N * C) devido ao cache.
   - Observação: Mantém a clareza da recursão e traz ganho dramático de desempenho
     em relação à recursão pura.

4) dp_iterative_knapsack (Bottom-up / Tabulação)
   - Complexidade de tempo: O(N * C)
   - Complexidade de espaço: O(N * C) (pode ser otimizada para O(C) com técnica rolling array)
   - Observação: geralmente a implementação preferida em produção didática
     por ser simples de entender e permitir recuperação da solução (com rastreamento adicional).

Qual é a mais eficiente?
- Em termos de complexidade assintótica e para instâncias com capacidade C relativamente pequena,
  as abordagens 3 (memoized) e 4 (bottom-up DP) são as mais eficientes (ambas O(N*C)).
- A abordagem gulosa é a mais rápida na prática (ordenar + varredura) mas não é correta
  para todas as instâncias do problema 0/1 knapsack.
"""
