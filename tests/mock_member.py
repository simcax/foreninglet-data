"""Enables mocking of a member as returned from the ForeningLet API"""

import random
from random import randint

from faker import Faker

from foreninglet_data.fl_types import Member


# pylint: disable=too-few-public-methods
class MockMember(Member):
    """
    Extends the Member dataclass and adds a method to mock a member instance
    """

    genders = ["Mand", "Kvinde"]
    delivery_methods = ["Manuelt", "Email/Dankort", "Email/Udenlandsk kort"]
    member_field_1 = 1  # Document what this field signifies.
    member_field_2 = "Ja"  # Yes, but to what?
    member_field_3 = "240"  # What does this number signify??
    activity_ids = "86407"  # 3 month membership activity id

    # Disabling no-member for this_member.to_json implemented by dataclass_json
    # pylint: disable=no-member
    def mock_member(self, output_type="json"):
        """Mocks a member instance of the dataclass Member type"""
        fake = Faker()
        sex = {"M": "M", "F": "K"}
        this_member = Member(
            MemberId=randint(0, 1000),
            MemberNumber=randint(0, 1000),
            MemberCode=fake.password(),
            FirstName=fake.first_name(),
            LastName=fake.last_name(),
            Address=fake.street_address(),
            Zip=fake.postcode(),
            City=fake.city(),
            CountryCode="DK",
            Email=fake.email(),
            Birthday=fake.date_of_birth(minimum_age=15).strftime("%Y-%m-%d"),
            Gender=sex[fake.profile()["sex"]],
            Phone=fake.phone_number(),
            Mobile=fake.phone_number(),
            EnrollmentDate=fake.date_of_birth(minimum_age=1).strftime("%Y-%m-%d"),
            DeliveryMethod=self.delivery_methods[randint(0, 2)],
            Created=fake.date_of_birth(minimum_age=1).strftime("%Y-%m-%d"),
            Updated=fake.date_of_birth(minimum_age=1).strftime("%Y-%m-%d"),
            GenuineMember=random.choice([0, 1]),
            activity_ids={"12345"},
        )
        if output_type == "json":
            return_obj = this_member.to_json()
        else:
            return_obj = this_member
        return return_obj
