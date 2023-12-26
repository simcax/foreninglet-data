"""
Testing the ForeningLet Data Memberlist class
"""
import json

import pandas as pd

from foreninglet_data.memberlist import Memberlist


def test_memberlist_isobject():
    """
    A test to see a memberlist object has the correct membercount attribute
    """
    memberlist_obj = Memberlist()
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
    memberlist = mocked_memberlist(11)
    df = pd.read_json(json.dumps(memberlist))
    males = df["Gender"].value_counts()["M"]
    females = df["Gender"].value_counts()["K"]
    memberlist_obj = Memberlist(memberlist)
    assert memberlist_obj.count_men == males
    assert memberlist_obj.count_women == females
