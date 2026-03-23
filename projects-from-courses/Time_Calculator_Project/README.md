# Time Calculator

Project completed as part of the **freeCodeCamp – Scientific Computing with Python** course.

## Description

The `add_time` function adds a duration to a given start time in 12-hour format (AM/PM).  
An optional weekday can also be provided.

The function returns the resulting time in the same format, correctly handling:

- day transitions (crossing midnight),
- updating the day of the week,
- annotations such as `(next day)` or `(n days later)`.

---

## Example

```python
print(add_time("3:30 PM", "22:12", "Monday"))
# Returns: 1:42 PM, Tuesday (next day)
