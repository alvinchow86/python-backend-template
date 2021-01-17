import random
import string


alphabet = string.ascii_letters + string.digits


def random_string(num_chars=16):
    return ''.join(random.choice(alphabet) for i in range(num_chars))
