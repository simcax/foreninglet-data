"""A data class for a ForeningLet Member, to map a member from the API to an object"""
from dataclasses import dataclass, field

# from .forening_let import ForeningLet
from functools import lru_cache
from random import random

from dataclasses_json import dataclass_json
from faker import Faker


# pylint: disable=invalid-name, too-many-instance-attributes
@dataclass_json
@dataclass
class Member:
    """Implements a Foreninglet Member"""

    fake = Faker("da_DK")
    MemberId: int = random()  # '123456' - The global member id in ForeningLet
    MemberNumber: int = (
        random()
    )  # '1' - The internal member number in the individual association
    MemberCode: str = fake.password()  # 'd8a8d9241f0ec44' - The members password
    FirstName: str = fake.first_name()  # 'John' - First name
    LastName: str = fake.last_name()  # 'Doe', - Last name
    Address: str = fake.street_address()  # 'Femvej 7' - Address line 1
    Address2: str = ""  # - Address line 2
    Zip: int = fake.postcode()  # '4320'
    City: str = fake.city()  # 'Byen'
    CountryCode: str = "DK"  # 'DK'
    Email: str = fake.email()  # 'me@me.com'
    Birthday: str = fake.date_of_birth(minimum_age=15).strftime(
        "%Y-%m-%d"
    )  # '1977-01-01'
    Gender: str = ""  # 'Mand','Kvinde' - Danish words for 'Male' and 'Female'
    Phone: int = 00000000  # '12345678
    Mobile: str = ""
    EnrollmentDate: str = ""  # - the date the member joined, as a string representation
    DeliveryMethod: str = ""  # - How invoicing will be handled for this member
    PbsAgreementNumber: int = 0
    Note: str = ""
    Password: str = ""
    Saldo: int = ""
    SaldoPaymentDeadline: str = ""
    Created: str = ""
    Updated: str = ""
    Property: str = ""
    GenuineMember: bool = False
    Image: str = "0"
    MemberField1: str = ""
    MemberField2: str = ""
    MemberField3: str = ""
    MemberField4: str = ""
    MemberField5: str = ""
    MemberField6: str = ""
    MemberField7: str = ""
    MemberField8: str = ""
    MemberField9: str = ""
    MemberField10: str = ""
    MemberField11: str = ""
    MemberField12: str = ""
    MemberField13: str = ""
    MemberField14: str = ""
    MemberField15: str = ""
    MemberField16: str = ""
    MemberField17: str = ""
    MemberField18: str = ""
    MemberField19: str = ""
    MemberField20: str = ""
    ConsentField1: str = ""
    ConsentField2: str = ""
    ConsentField3: str = ""
    ConsentField4: str = ""
    ConsentField5: str = ""
    Activities: str = ""
    activity_ids: str = ""
    Membership: str = ""

    def __post_init__(self):
        """Add membership to the member object"""
        # self.Membership = self.register_membership()
        # object.__setattr__(self,'Membership',self.register_membership())

    # @lru_cache
    # def register_membership(self) -> str:
    #     """
    #         Maps the members activity ids to a membership,
    #         and adds the membership to the member objects
    #         membership attribute
    #     """
    #     membership_found = ""
    #     fl_obj = ForeningLet()
    #     activity_list = fl_obj.get_activities()
    #     memberships = fl_obj.get_memberships(activity_list)
    #     for activity_id in self.activity_ids:
    #         for membership in memberships:
    #             if activity_id == membership.get('ActivityId'):
    #                 membership_found = membership.get('Name')
    #                 break
    #     return membership_found
