from grammar import parse_grammar
from first_follow import compute_first, compute_follow, display_first_follow
from parsing_table import build_parsing_table, display_table, is_ll1


def run_analysis(name, grammar_text):
    print(f"\n[ {name} ]")

    grammar = parse_grammar(grammar_text)
    grammar.display()

    first  = compute_first(grammar)
    follow = compute_follow(grammar, first)
    display_first_follow(grammar, first, follow)

    table, conflicts = build_parsing_table(grammar, first, follow)
    display_table(grammar, table, conflicts)

    resultado = "LL(1)" if is_ll1(conflicts) else "NO LL(1)"
    print(f"  Resultado LL(1): {resultado}\n")


# Gramática 1: Expresión aritmética
GRAMMAR_ARITHMETIC = """
E  -> T E'
E' -> + T E' | ε
T  -> F T'
T' -> * F T' | ε
F  -> ( E ) | id
"""

# Gramática 2: If-else
GRAMMAR_IF_ELSE = """
S -> if E then S S'
S -> other
S' -> else S | ε
E -> bool
"""

# Gramática 3: Listas
GRAMMAR_LIST = """
L  -> [ I ]
L  -> [ ]
I  -> V I'
I' -> , V I' | ε
V  -> num | str | L
"""


if __name__ == "__main__":
    run_analysis("Expresiones Aritméticas", GRAMMAR_ARITHMETIC)
    run_analysis("Sentencias If-Else (dangling else)", GRAMMAR_IF_ELSE)
    run_analysis("Listas Anidadas (JSON simplificado)", GRAMMAR_LIST)
