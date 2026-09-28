import re

def is_valid_phone(phone):
    pattern = re.compile(r'^\+?\d{1,3}?[-\s]?\(?\d{2,4}\)?[-\s]?\d{3,4}[-\s]?\d{4}$')
    return pattern.match(phone) is not None

print(input("01040424387"))