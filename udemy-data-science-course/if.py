def count(numbers):
    total = 0
    for x in numbers:
        if x <= 20:
            total += 1
    return total

list_of_numbers = [1, 3, 4, 10, 12, 28, 56, 78, 90]
count(list_of_numbers)
