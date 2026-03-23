# Budget App

Project completed as part of the **freeCodeCamp – Scientific Computing with Python** course.

## Description

The goal of this project is to create a `Category` class for managing **budgets across different spending categories**, such as food, clothing, transportation, and others.

In addition, the program generates a **text-based bar chart** (`create_spend_chart`) showing the percentage of spending in each category.

---

## `Category` Class Functionality

### Methods

- `deposit(amount, description="")`  
  Adds funds to the category with an optional description.

- `withdraw(amount, description="")`  
  Withdraws funds from the category if enough money is available. Returns `True` or `False`.

- `get_balance()`  
  Returns the current balance.

- `transfer(amount, category)`  
  Transfers funds to another budget category.

- `check_funds(amount)`  
  Checks whether enough funds are available.

- `__str__()`  
  Returns a string representation of the category, including its name, transactions, and total balance.

---

## Spending Chart

The `create_spend_chart(categories)` function generates a text-based chart showing the percentage of total spending for each category.

## Example

```python
food = Category("Food")
food.deposit(1000, "deposit")
food.withdraw(10.15, "groceries")
food.withdraw(15.89, "restaurant and more food for dessert")

clothing = Category("Clothing")
food.transfer(50, clothing)

auto = Category("Auto")
auto.deposit(1000, "deposit")
auto.withdraw(500, "repair")

print(create_spend_chart([food, clothing, auto]))

Output:
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
