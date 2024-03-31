"""Enables mocking of a member as returned from the ForeningLet API"""

import json
import random
from random import randint

from attr import asdict
from faker import Faker

from foreninglet_data.activities import Activities
from foreninglet_data.api import ForeningLet
from foreninglet_data.models.member_model import Member

from .test_utils import TestUtils


class MockMember:
    """
    Create a mocked member from the member object
    """

    def mock_member(self, output_type="json"):
        """Mock a member object"""
        member = Member(**TestUtils().dict_for_member())
        if output_type == "json":
            return member.model_dump_json()

        else:
            return member
