# Polygon Area Calculator

Projekt wykonany w ramach kursu **freeCodeCamp – Scientific Computing with Python**.

## Opis

Celem projektu było stworzenie klas `Rectangle` i `Square`, które modelują odpowiednie figury geometryczne. Klasy umożliwiają m.in. obliczenie pola, obwodu, przekątnej, a także wygenerowanie tekstowej reprezentacji graficznej kształtu.

Klasa `Square` dziedziczy po klasie `Rectangle`, ale zawiera dodatkowe metody specyficzne dla kwadratu.

---

## Klasa `Rectangle`

### Metody:

- `set_width(new_width)` – ustawia nową szerokość
- `set_height(new_height)` – ustawia nową wysokość
- `get_area()` – zwraca pole (width * height)
- `get_perimeter()` – zwraca obwód (2 × width + 2 × height)
- `get_diagonal()` – zwraca długość przekątnej
- `get_picture()` – zwraca tekstową reprezentację prostokąta z `*`  
  (maksymalnie 50 × 50 – w przeciwnym razie zwraca `"Too big for picture."`)
- `get_amount_inside(other_shape)` – ile razy dany kształt mieści się w tym prostokącie (bez rotacji)
- `__str__()` – zwraca np. `Rectangle(width=10, height=5)`

---

## Klasa `Square` (dziedziczy po `Rectangle`)

### Dodatkowe metody:

- `set_side(side)` – ustawia jednocześnie wysokość i szerokość
- Nadpisane metody `set_width` i `set_height`, aby również zmieniały oba wymiary
- `__str__()` – zwraca np. `Square(side=9)`