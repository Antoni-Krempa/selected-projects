# Budget App

Projekt stworzony w ramach kursu **freeCodeCamp – Scientific Computing with Python**.

## Opis

Celem projektu jest stworzenie klasy `Category`, która umożliwia prowadzenie **budżetów dla różnych kategorii wydatków**, takich jak żywność, ubrania, transport itp. 

Dodatkowo, program generuje **tekstowy wykres słupkowy** (`create_spend_chart`), który pokazuje procentowy udział wydatków w każdej kategorii.

---

## Funkcjonalność klasy `Category`

### Metody:

- `deposit(amount, description="")`  
  Dodaje kwotę do budżetu z opcjonalnym opisem.

- `withdraw(amount, description="")`  
  Odejmuje kwotę z budżetu, jeśli są środki. Zwraca `True`/`False`.

- `get_balance()`  
  Zwraca aktualne saldo.

- `transfer(amount, category)`  
  Przesyła środki do innej kategorii budżetowej.

- `check_funds(amount)`  
  Sprawdza, czy wystarczy środków.

- `__str__()`  
  Zwraca reprezentację kategorii — nazwa, operacje, saldo.

---

## Wykres wydatków

Funkcja `create_spend_chart(categories)` generuje tekstowy wykres pokazujący procentowy udział wydatków dla każdej kategorii.

Przykład użycia:

```python
food = Category('Food')
food.deposit(1000, 'deposit')
food.withdraw(10.15, 'groceries')
food.withdraw(15.89, 'restaurant and more food for dessert')

clothing = Category('Clothing')
food.transfer(50, clothing)

auto = Category('Auto')
auto.deposit(1000, 'deposit')
auto.withdraw(500, 'repair')

print(create_spend_chart([food, clothing, auto]))

Wynik:
*************Food*************
deposit                1000.00
groceries               -10.15
restaurant and more foo -15.89
Transfer to Clothing    -50.00
Total: 923.96
Percentage spent by category
100|          
 90|          
 80|       o   
 70|       o  
 60|       o   
 50|       o   
 40|       o   
 30|       o   
 20|       o   
 10|    o  o  
  0| o  o  o  
    ----------
     C  F  A  
     l  o  u  
     o  o  t  
     t  d  o  
     h        
     i        
     n        
     g        
