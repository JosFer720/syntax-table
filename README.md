# First, Follow y Tabla de Análisis Sintáctico LL(1)

Implementación en Python para calcular FIRST, FOLLOW y construir la tabla de análisis predictivo LL(1).

## Ejecutar

```bash
python main.py
```

## Archivos

- `grammar.py` — representación y parseo de gramáticas
- `first_follow.py` — cálculo de FIRST y FOLLOW
- `parsing_table.py` — construcción de la tabla LL(1)
- `main.py` — pruebas con tres gramáticas

---

## Gramáticas probadas

### 1. Expresiones aritméticas (vista en clase)

```
E  -> T E'
E' -> + T E' | ε
T  -> F T'
T' -> * F T' | ε
F  -> ( E ) | id
```

**Resultado LL(1): sí**

No hay conflictos. La gramática ya tiene recursión izquierda eliminada y está factorizada, por lo que FIRST de cada alternativa es disjunto y FOLLOW no genera ambigüedad.

---

### 2. Sentencias If-Else

```
S  -> if E then S S' | other
S' -> else S | ε
E  -> bool
```

**Resultado LL(1): no**

Conflicto en `[S', else]`: al ver el token `else`, el parser no puede decidir entre aplicar `S' → else S` o `S' → ε`. Esto es el clásico problema del *dangling else*.

Se eligió esta gramática porque es el ejemplo más conocido de conflicto FIRST/FOLLOW y aparece en casi todo libro de compiladores. Sirve para mostrar que no toda gramática bien escrita es LL(1).

---

### 3. Listas anidadas (JSON simplificado)

```
L  -> [ I ] | [ ]
I  -> V I'
I' -> , V I' | ε
V  -> num | str | L
```

**Resultado LL(1): no**

Conflicto en `[L, []`: al ver `[`, el parser no puede saber si la lista tendrá elementos (`L → [ I ]`) o estará vacía (`L → [ ]`). Se resuelve con factorización: `L -> [ L'` donde `L' -> I ] | ]`.

Se eligió esta gramática porque representa una estructura recursiva real (listas que contienen listas), muestra un conflicto fácilmente soluble con factorización, y es un ejemplo cercano a lenguajes que los estudiantes ya conocen como JSON.
