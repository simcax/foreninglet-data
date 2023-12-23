"""Class to contain common testing utility methods"""
import random
import string


class TestUtils:
    """The test utility class"""

    @classmethod
    def create_random_string(cls):
        """'Helper function to create a random string - 10 chars long"""
        random_string = "".join(random.choice(string.ascii_letters) for x in range(10))
        return random_string

    def create_random_email(self):
        """Helper function to create a random email address"""
        firstpart = self.create_random_string()
        email = f"{firstpart}@example.com"
        return email
