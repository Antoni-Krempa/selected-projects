# Probability Calculator

Projekt wykonany w ramach kursu **freeCodeCamp – Scientific Computing with Python**.

## Opis

Celem projektu było stworzenie klasy `Hat`, która umożliwia losowanie kul z kapelusza, oraz funkcji `experiment`, która pozwala **oszacować prawdopodobieństwo** uzyskania określonego układu kul przy wielokrotnych losowaniach.

---

## Jak to działa?

1. Tworzysz obiekt `Hat`, który zawiera kule różnych kolorów.
2. Używasz funkcji `draw(n)`, aby wylosować `n` kul bez zwracania.
3. Funkcja `experiment()` powtarza ten proces wiele razy i sprawdza, jak często wśród wylosowanych kul pojawił się oczekiwany zestaw.

---

## Przykład użycia

```python
hat = Hat(black=6, red=4, green=3)

probability = experiment(
    hat=hat,
    expected_balls={'red': 2, 'green': 1},
    num_balls_drawn=5,
    num_experiments=2000
)

print(probability) #0.356