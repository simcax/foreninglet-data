"""Test configuration for the ForeningLet Data module"""

import json
import sys
from random import randint
from unittest.mock import Mock

import pytest
from dotenv import load_dotenv

from .mock_member import MockMember
from .test_utils import TestUtils


@pytest.fixture(scope="module")
def vcr_config():
    """Make sure no credentials are saved to the vcr casettes"""
    return {
        # Replace the Authorization request header with "DUMMY" in cassettes
        "filter_headers": [("authorization", "DUMMY")],
    }


@pytest.fixture(autouse=True)
def load_env():
    """
    Loads the environment variables from a .env file
    It will load automatically, so the environment vars are ready
    """
    load_dotenv()


@pytest.fixture
def fl_member():
    """Fixture to create a random FL member"""
    mm_obj = MockMember()
    return mm_obj.mock_member(output_type="obj")


# @pytest.fixture
# def fl_patched(monkeypatch):
#     """Mock for the get_memberlist, in order to test without api access"""
#     monkeypatch.setattr(ForeningLet, "get_memberlist", __mock_memberlist)


# pylint: disable=unused-argument, unused-variable
def __mock_memberlist(self):
    """Creates a list of members as from the ForeningLet API"""
    mocked_members = "["
    mm_obj = MockMember()
    count = 10
    this_count = 0
    for a_count in range(0, count):
        this_count += 1
        mocked_members += mm_obj.mock_member()
        if this_count is not count:
            mocked_members += ","
    mocked_members += "]"
    return mocked_members


def __activity_data():
    activitydata = [
        {
            "ActivityId": "12345",
            "Name": "3 måneders medlemskab",
            "OnlineEnrollmentEnabled": "1",
            "SettlementDate": "0000-00-00T00:00:00+0000",
            "ExternalDescriptions": [...],
            "Categories": [...],
        },
        {
            "ActivityId": "12346",
            "Name": "Fitness",
            "OnlineEnrollmentEnabled": "0",
            "SettlementDate": "0000-00-00T00:00:00+0000",
            "ExternalDescriptions": [...],
            "Categories": [...],
        },
        {
            "ActivityId": "12347",
            "Name": "Fitness - 04:00 - 05:00",
            "OnlineEnrollmentEnabled": "1",
            "SettlementDate": "2020-11-27T03:00:00+0000",
            "ExternalDescriptions": [...],
            "Categories": [...],
        },
        {
            "ActivityId": "12348",
            "Name": "Fitness - 04:00 - 05:00",
            "OnlineEnrollmentEnabled": "1",
            "SettlementDate": "2020-11-28T03:00:00+0000",
            "ExternalDescriptions": [...],
            "Categories": [...],
        },
        {
            "ActivityId": "12222",
            "Name": "Fitness - 04:00 - 05:00",
            "OnlineEnrollmentEnabled": "1",
            "SettlementDate": "2020-11-29T03:00:00+0000",
            "ExternalDescriptions": [...],
            "Categories": [...],
        },
        {
            "ActivityId": "18564",
            "Name": "Fitness - 04:00 - 05:00",
            "OnlineEnrollmentEnabled": "1",
            "SettlementDate": "2020-11-30T03:00:00+0000",
            "ExternalDescriptions": [...],
            "Categories": [...],
        },
        {
            "ActivityId": "56416",
            "Name": "Fitness - 04:00 - 05:00",
            "OnlineEnrollmentEnabled": "1",
            "SettlementDate": "2020-12-01T03:00:00+0000",
            "ExternalDescriptions": [...],
            "Categories": [...],
        },
        {
            "ActivityId": "32165",
            "Name": "Fitness - 04:00 - 05:00",
            "OnlineEnrollmentEnabled": "1",
            "SettlementDate": "2020-12-02T03:00:00+0000",
            "ExternalDescriptions": [...],
            "Categories": [...],
        },
        {
            "ActivityId": "32166",
            "Name": "Fitness - 04:00 - 05:00",
            "OnlineEnrollmentEnabled": "1",
            "SettlementDate": "2020-12-03T03:00:00+0000",
            "ExternalDescriptions": [...],
            "Categories": [...],
        },
        {
            "ActivityId": "32167",
            "Name": "Fitness - 04:00 - 05:00",
            "OnlineEnrollmentEnabled": "1",
            "SettlementDate": "2020-12-04T03:00:00+0000",
            "ExternalDescriptions": [...],
            "Categories": [...],
        },
        {
            "ActivityId": "32168",
            "Name": "Fitness - 04:00 - 05:00",
            "OnlineEnrollmentEnabled": "1",
            "SettlementDate": "2020-12-05T03:00:00+0000",
            "ExternalDescriptions": [...],
            "Categories": [...],
        },
        {
            "ActivityId": "32169",
            "Name": "Fitness - 04:00 - 05:00",
            "OnlineEnrollmentEnabled": "1",
            "SettlementDate": "2020-12-06T03:00:00+0000",
            "ExternalDescriptions": [...],
            "Categories": [...],
        },
        {
            "ActivityId": "32170",
            "Name": "Fitness - 04:00 - 05:00",
            "OnlineEnrollmentEnabled": "1",
            "SettlementDate": "2020-12-07T03:00:00+0000",
            "ExternalDescriptions": [...],
            "Categories": [...],
        },
    ]
    return activitydata


# @pytest.fixture
# def activity_list_patched(monkeypatch):
#     """Mock get_activities"""
#     monkeypatch.setattr(ForeningLet, "get_activities",__activity_data)


@pytest.fixture
def activity_data():
    """Mock the activitylist data"""
    return __activity_data()


@pytest.fixture
def mocked_memberlist():
    """
    Fixture for creating fake memberlist data
    """

    def _mocked_memberlist(membercount: int, non_genuine_members: int) -> str:
        """Returns a mocked / fake memberlist"""
        # Generate a memberlist of mocked members
        memberlist = ""
        memberlist_comma = ","
        for i in range(1, membercount + 1):
            if i != membercount:
                memberlist_comma = ","
            else:
                memberlist_comma = ""

            member = MockMember().mock_member()
            memberlist += member + memberlist_comma
        memberlist.strip("'")
        memberlist = f"[{memberlist}]"
        return json.loads(memberlist)

    return _mocked_memberlist
