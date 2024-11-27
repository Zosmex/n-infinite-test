def reverse_num(num: int) -> int:
    # Write your code here.
    result = 0

    while num > 0:
        last_digit = num % 10
        result = (result * 10) + last_digit
        num = num // 10 # Remove last digit

    return result

# Run this file for test
assert reverse_num(1234) == 4321
assert reverse_num(20903) == 30902
assert reverse_num(1_000_234) == 4320001
assert reverse_num(4444) == 4444
assert reverse_num(1) == 1
assert reverse_num(0) == 0