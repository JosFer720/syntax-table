EPSILON = 'ε'
END_MARKER = '$'


class Grammar:
    def __init__(self):
        self.productions = {}   # Producciones
        self.terminals = set()
        self.non_terminals = set()
        self.start_symbol = None

    def add_production(self, head, body):
        """Agrega una producción."""
        if head not in self.productions:
            self.productions[head] = []
            self.non_terminals.add(head)
        self.productions[head].append(body)
        for sym in body:
            if sym != EPSILON:
                if not self._is_non_terminal(sym):
                    self.terminals.add(sym)

    def _is_non_terminal(self, sym):
        return sym in self.non_terminals

    def set_start(self, symbol):
        self.start_symbol = symbol

    def display(self):
        print("\nGramática")
        for head, bodies in self.productions.items():
            for i, body in enumerate(bodies):
                arrow = "→" if i == 0 else " |"
                body_str = " ".join(body)
                if i == 0:
                    print(f"  {head} {arrow} {body_str}")
                else:
                    print(f"  {' ' * len(head)} {arrow} {body_str}")
        print()


def parse_grammar(text):
    """Lee una gramática desde texto."""
    grammar = Grammar()
    lines = [l.strip() for l in text.strip().splitlines() if l.strip() and not l.startswith('#')]

    first_head = None
    current_head = None

    for line in lines:
        if '->' in line:
            head, rhs = line.split('->', 1)
            head = head.strip()
            current_head = head
            if first_head is None:
                first_head = head
        elif '|' in line and current_head:
            # Alternativa
            rhs = line
            head = current_head
        else:
            continue

        rhs = rhs.strip()
        alternatives = [alt.strip() for alt in rhs.split('|')]

        for alt in alternatives:
            if not alt:
                continue
            symbols = alt.split()
            if symbols == ['ε'] or symbols == ['epsilon']:
                grammar.add_production(head, [EPSILON])
            else:
                grammar.add_production(head, symbols)

    grammar.set_start(first_head)

    # Clasificar no-terminales
    for head, bodies in grammar.productions.items():
        for body in bodies:
            for sym in body:
                if sym in grammar.productions:
                    grammar.non_terminals.add(sym)
                    grammar.terminals.discard(sym)

    return grammar
