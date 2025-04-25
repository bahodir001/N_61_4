import re
import random

def is_email(identifier):
    return re.match(r"[^@]+@[^@]+\.[^@]+", identifier)

def generate_code():
    return str(random.randint(100000, 999999))
