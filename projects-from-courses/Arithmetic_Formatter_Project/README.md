# Arithmetic Formatter

Projekt wykonany w ramach kursu **freeCodeCamp – Scientific Computing with Python**.

## Opis

Celem projektu jest sformatowanie listy zadań arytmetycznych w taki sposób, aby były wyświetlane **pionowo i obok siebie**, jak to często robią uczniowie szkoły podstawowej. Program przyjmuje operacje dodawania i odejmowania, a opcjonalnie może również wyświetlać **wyniki obliczeń**.

### Obsługiwane operacje
- Dodawanie (`+`)
- Odejmowanie (`-`)

## Przykład działania

```python
arithmetic_arranger(["32 + 698", "3801 - 2", "45 + 43", "123 + 49"], True)

Wynik:
  32         1      9999      523
+  8    - 3801    + 9999    -  49
----    ------    ------    -----
  40     -3800     19998      474