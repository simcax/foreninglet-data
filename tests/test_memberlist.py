"""
Testing the ForeningLet Data Memberlist class
"""
import json

import pandas as pd

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


def test_memberlist_class_works_with_real_api_data():
    """
    Tests the memberlist class works with memberlist data
    coming from the ForeningLet API
    """
    fl_obj = ForeningLet()
    memberlist = fl_obj.get_memberlist()
    memberlist_obj = Memberlist(memberlist)
    assert isinstance(memberlist_obj.member_count, int)
