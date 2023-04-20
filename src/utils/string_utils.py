import string, random

class string_utils():
    def random_string(len) -> str:
        # I bet you can figure out this one.
        return "".join(random.choice(string.digits + string.ascii_letters) for i in range(len))