"""Class to contain common testing utility methods"""

import random
import string

from faker import Faker

from foreninglet_data.activities import Activities
from foreninglet_data.api import ForeningLet


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

    def dict_for_member(self):
        """Create a dict to be used as input to a member object"""
        genders = ["Mand", "Kvinde"]
        delivery_methods = ["Manuelt", "Email/Dankort", "Email/Udenlandsk kort"]
        member_field_1 = 1  # Document what this field signifies.
        member_field_2 = "Ja"  # Yes, but to what?
        member_field_3 = "240"  # What does this number signify??
        # Build a list of activity ids to be used in the mock member
        fl_obj = ForeningLet()
        actvity_list = fl_obj.get_activities()
        activity_obj = Activities(actvity_list)
        membership_keywords = ["medlemskab", "medlemsskab"]
        memberships = activity_obj.identify_memberships(tuple(membership_keywords))
        activity_ids = random.choice(list(memberships.keys()))
        sex = {"M": "M", "F": "K"}
        fake = Faker("da_DK")
        member_data_dict = {
            "MemberId": random.randint(0, 1000),
            "MemberNumber": random.randint(0, 1000),
            "MemberCode": fake.password(),
            "FirstName": fake.first_name(),
            "LastName": fake.last_name(),
            "Address": fake.street_address(),
            "Zip": int(fake.postcode()),
            "City": fake.city(),
            "CountryCode": "DK",
            "Email": fake.email(),
            "Birthday": fake.date_of_birth(minimum_age=15).strftime("%Y-%m-%d"),
            "Gender": sex[fake.profile()["sex"]],
            "Phone": fake.phone_number().replace(" ", ""),
            "Mobile": fake.phone_number().replace(" ", ""),
            "EnrollmentDate": fake.date_of_birth(minimum_age=1).strftime("%Y-%m-%d"),
            "DeliveryMethod": random.choice(delivery_methods),
            "Created": fake.date_of_birth(minimum_age=1).strftime("%Y-%m-%d"),
            "Updated": fake.date_of_birth(minimum_age=1).strftime("%Y-%m-%d"),
            "GenuineMember": random.choice([0, 1]),
            "activity_ids": activity_ids,
        }
        return member_data_dict
