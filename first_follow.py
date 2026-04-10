from grammar import EPSILON, END_MARKER


def compute_first(grammar):
    """Calcula el conjunto FIRST."""
    first = {sym: set() for sym in grammar.non_terminals}

    # FIRST de terminales
    for t in grammar.terminals:
        first[t] = {t}
    first[EPSILON] = {EPSILON}
    first[END_MARKER] = {END_MARKER}

    changed = True
    while changed:
        changed = False
        for head, bodies in grammar.productions.items():
            for body in bodies:
                before = len(first[head])
                added = _first_of_sequence(body, first)
                first[head] |= added
                if len(first[head]) > before:
                    changed = True

    return first


def _first_of_sequence(sequence, first_sets):
    """Calcula FIRST de una secuencia."""
    result = set()

    if sequence == [EPSILON]:
        return {EPSILON}

    all_have_epsilon = True
    for sym in sequence:
        sym_first = first_sets.get(sym, set())
        result |= (sym_first - {EPSILON})
        if EPSILON not in sym_first:
            all_have_epsilon = False
            break

    if all_have_epsilon:
        result.add(EPSILON)

    return result


def compute_follow(grammar, first):
    """Calcula el conjunto FOLLOW."""
    follow = {nt: set() for nt in grammar.non_terminals}
    follow[grammar.start_symbol].add(END_MARKER)

    changed = True
    while changed:
        changed = False
        for head, bodies in grammar.productions.items():
            for body in bodies:
                for i, sym in enumerate(body):
                    if sym not in grammar.non_terminals:
                        continue

                    before = len(follow[sym])
                    beta = body[i + 1:]  # Símbolos siguientes

                    if beta:
                        first_beta = _first_of_sequence(beta, first)
                        follow[sym] |= (first_beta - {EPSILON})
                        if EPSILON in first_beta:
                            follow[sym] |= follow[head]
                    else:
                        # Al final de la producción
                        follow[sym] |= follow[head]

                    if len(follow[sym]) > before:
                        changed = True

    return follow


def display_first_follow(grammar, first, follow):
    """Imprime FIRST y FOLLOW."""

    print("FIRST")
    for nt in grammar.productions:
        f = ", ".join(sorted(first[nt]))
        print(f"  {nt}  ->  {{ {f} }}")

    print()
    print("FOLLOW")
    for nt in grammar.productions:
        f = ", ".join(sorted(follow[nt]))
        print(f"  {nt}  ->  {{ {f} }}")
    print()
