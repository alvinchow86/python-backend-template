import re
import random
import string


alphabet = string.ascii_letters + string.digits


def random_string(num_chars=16):
    return ''.join(random.choice(alphabet) for i in range(num_chars))


def camel_to_snake_case(string):
    return re.sub(r'(?<!^)(?=[A-Z])', '_', string).lower()
