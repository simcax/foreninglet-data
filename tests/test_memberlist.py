"""
Testing the ForeningLet Data Memberlist class
"""
import json

import pandas as pd
import pytest

from foreninglet_data.api import ForeningLet
from foreninglet_data.memberlist import Memberlist


def test_memberlist_isobject(mocked_memberlist):
    """
    A test to see a memberlist object has the correct membercount attribute
    """
    memberlist_obj = Memberlist(mocked_memberlist(2))
    assert isinstance(memberlist_obj, object)


def test_memberlist_loads_memberlist(mocked_memberlist):
    """
    Test to make sure the passed memberlist is held by the memberlist object
    """
    memberlist = mocked_memberlist(5)
    memberlist_obj = Memberlist(memberlist)
    assert memberlist_obj.memberlist == memberlist


def test_memberlist_has_correct_membercount(mocked_memberlist):
    """
    Tests the memberlist object to initialize the count of members as an attribute
    """
    memberlist = mocked_memberlist(11)
    memberlist_obj = Memberlist(memberlist)
    assert memberlist_obj.member_count == 11


def test_memberlist_has_correct_gender_count(mocked_memberlist):
    """
    Tests the memberlist object to initialize the count of members for each gender
    as attributes
    """
    memberlist = mocked_memberlist(12)
    df = pd.read_json(json.dumps(memberlist))
    groups = df.groupby("Gender").size()
    males = 0
    females = 0
    if groups.get("M", "") != "":
        males = groups["M"]
    if groups.get("Mand", "") != "":
        males += groups["Mand"]
    if groups.get("K", "") != "":
        females = groups["K"]
    if groups.get("Kvinde", "") != "":
        females += groups["Kvinde"]
    memberlist_obj = Memberlist(memberlist)
    assert memberlist_obj.count_men == males
    assert memberlist_obj.count_women == females


@pytest.mark.vcr()
def test_memberlist_class_works_with_real_api_data():
    """
    Tests the memberlist class works with memberlist data
    coming from the ForeningLet API
    """
    fl_obj = ForeningLet()
    memberlist = fl_obj.get_memberlist()
    memberlist_obj = Memberlist(memberlist)
    assert isinstance(memberlist_obj.member_count, int)


def test_memberlist_only_genuine_members(mocked_memberlist):
    """
    Test to only get members where genuinemember == 1
    """
    memberlist = mocked_memberlist(20)
    memberlist_obj = Memberlist(memberlist)

    gen_member_count = 0
    for member in memberlist:
        gen_member_count += member["GenuineMember"]
    assert memberlist_obj.genuine_member_count == gen_member_count


def test_memberlist_age_counts_totals_returns_dict(mocked_memberlist):
    """
    Test to retrieve the number of members for each age group
    """
    memberlist = mocked_memberlist(20)
    memberlist_obj = Memberlist(memberlist)
    age_counts = memberlist_obj.members_age_list
    assert isinstance(age_counts, dict)


def test_memberlist_age_counts_totals_returns_dict_matching_genuine_membercount(
    mocked_memberlist,
):
    """
    Test to retrieve the number of members for each age group
    """
    memberlist = mocked_memberlist(20)
    memberlist_obj = Memberlist(memberlist)
    age_counts = memberlist_obj.members_age_list
    member_counts_total = 0
    for member_count in age_counts.values():
        member_counts_total += member_count
    assert member_counts_total == 20
