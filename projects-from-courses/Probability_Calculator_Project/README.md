# Probability Calculator

Project completed as part of the **freeCodeCamp – Scientific Computing with Python** course.

## Description

The goal of this project was to implement a `Hat` class that simulates drawing colored balls from a container, along with an `experiment` function used to **estimate probabilities** through repeated random sampling.

The approach is based on Monte Carlo simulation to approximate the likelihood of obtaining a specific combination of balls.

---

## How It Works

1. Create a `Hat` object containing balls of different colors.  
2. Use the `draw(n)` method to randomly draw `n` balls without replacement.  
3. The `experiment()` function repeats this process multiple times and checks how often the expected outcome occurs.

---

## Example

```python
hat = Hat(black=6, red=4, green=3)

probability = experiment(
    hat=hat,
    expected_balls={"red": 2, "green": 1},
    num_balls_drawn=5,
    num_experiments=2000
)

print(probability)  # 0.356

