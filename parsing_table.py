from grammar import EPSILON, END_MARKER
from first_follow import _first_of_sequence


def build_parsing_table(grammar, first, follow):
    """Construye la tabla LL(1)."""
    table = {}
    conflicts = []

    for head, bodies in grammar.productions.items():
        for body in bodies:
            first_alpha = _first_of_sequence(body, first)
            production_str = f"{head} → {' '.join(body)}"

            for terminal in first_alpha - {EPSILON}:
                key = (head, terminal)
                if key in table:
                    if production_str not in table[key]:
                        table[key].append(production_str)
                        conflicts.append(key)
                else:
                    table[key] = [production_str]

            if EPSILON in first_alpha:
                for terminal in follow[head]:
                    key = (head, terminal)
                    if key in table:
                        if production_str not in table[key]:
                            table[key].append(production_str)
                            conflicts.append(key)
                    else:
                        table[key] = [production_str]

    return table, list(set(conflicts))


def is_ll1(conflicts):
    return len(conflicts) == 0


def display_table(grammar, table, conflicts):
    """Imprime la tabla."""
    non_terminals = list(grammar.productions.keys())
    terminals = sorted(grammar.terminals) + [END_MARKER]

    nt_w = max(len(nt) for nt in non_terminals) + 2
    all_prods = [p for prods in table.values() for p in prods]
    cell_w = max((len(p) for p in all_prods), default=10) + 2

    print("Tabla de análisis")
    header = f"  {'':>{nt_w}}  " + "  ".join(f"{t:^{cell_w}}" for t in terminals)
    print(header)

    for nt in non_terminals:
        cells = []
        for t in terminals:
            key = (nt, t)
            if key in table:
                cell = " / ".join(table[key])
                if key in conflicts:
                    cell = "** " + cell
            else:
                cell = "-"
            cells.append(f"{cell:^{cell_w}}")
        print(f"  {nt:>{nt_w}}  " + "  ".join(cells))

    print()
    if is_ll1(conflicts):
        print("  LL(1): si")
    else:
        print("  LL(1): no")
        for (nt, t) in conflicts:
            prods = " | ".join(table[(nt, t)])
            print(f"    [{nt}, {t}]  ->  {prods}")
    print()
