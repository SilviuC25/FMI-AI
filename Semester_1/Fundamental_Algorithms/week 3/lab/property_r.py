# R5. The element has repeating digits.

def has_repeating_digits(number):
    digits = str(abs(number))
    return len(digits) != len(set(digits))

def remove_repeating_digit_numbers(numbers):
    return [number for number in numbers if not has_repeating_digits(number)]