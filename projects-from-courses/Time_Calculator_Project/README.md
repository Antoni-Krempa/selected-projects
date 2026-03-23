# Time Calculator

Projekt stworzony w ramach kursu **freeCodeCamp – Scientific Computing with Python**.

## Opis

Funkcja `add_time` dodaje czas trwania (`duration`) do zadanego czasu początkowego (`start`) w formacie 12-godzinnym (AM/PM). Opcjonalnie można także podać dzień tygodnia. Funkcja zwraca nową godzinę w tym samym formacie, uwzględniając również:

- przekroczenie północy (zmiana dnia),
- odpowiedni dzień tygodnia po dodaniu czasu,
- adnotację `(next day)` lub `(n days later)`.

## Przykład działania

```python
print(add_time('3:30 PM', '22:12', 'Monday'))
# Zwraca: 1:42 PM, Tuesday (next day)