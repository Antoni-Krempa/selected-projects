# Polygon Area Calculator

Project completed as part of the **freeCodeCamp – Scientific Computing with Python** course.

## Description

The goal of this project was to implement `Rectangle` and `Square` classes that model basic geometric shapes.

The classes provide methods for calculating properties such as area, perimeter, and diagonal length, as well as generating a simple text-based representation of the shape.

The `Square` class inherits from `Rectangle` and extends its functionality with behavior specific to squares.

---

## `Rectangle` Class

### Methods

- `set_width(new_width)` – sets the width  
- `set_height(new_height)` – sets the height  
- `get_area()` – returns the area (`width * height`)  
- `get_perimeter()` – returns the perimeter (`2 * width + 2 * height`)  
- `get_diagonal()` – returns the diagonal length  
- `get_picture()` – returns a text-based representation of the rectangle using `*`  
  (maximum size: 50 × 50, otherwise returns `"Too big for picture."`)  
- `get_amount_inside(other_shape)` – calculates how many times another shape can fit inside the rectangle (without rotation)  
- `__str__()` – returns a string representation, e.g. `Rectangle(width=10, height=5)`  

---

## `Square` Class (inherits from `Rectangle`)

### Additional functionality

- `set_side(side)` – sets both width and height  
- overridden `set_width` and `set_height` methods to keep both dimensions equal  
- `__str__()` – returns a string representation, e.g. `Square(side=9)`  

---

## Example

```python
rect = Rectangle(10, 5)
print(rect.get_area())

rect.set_height(3)
print(rect.get_perimeter())
print(rect)
print(rect.get_picture())

sq = Square(9)
print(sq.get_area())

sq.set_side(4)
print(sq.get_diagonal())
print(sq)
print(sq.get_picture())

rect.set_height(8)
rect.set_width(16)
print(rect.get_amount_inside(sq))
print(Rectangle(4,8).get_amount_inside(Rectangle(3, 6)))

Output:
50
26
Rectangle(width=10, height=3)
**********
**********
**********

81
5.656854249492381
Square(side=4)
****
****
****
****

8
1
