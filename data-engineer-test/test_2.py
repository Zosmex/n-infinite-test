
def reverse_string(s: str) -> str:
    # Write your code here.
    # Do not use list reverse method
    result = ''

    for c in s:
        result = c + result

    return result

assert reverse_string("abcd") == "dcba"
assert reverse_string("a3bE5dQPos") == "soPQd5Eb3a"
assert reverse_string("aka$aka") == "aka$aka"