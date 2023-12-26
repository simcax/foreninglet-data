"""
Testing the ForeningLet Data Memberlist class
"""
from foreninglet_data import memberlist


def test_memberlist_membercount():
    """
    A test to see a memberlist object has the correct membercount attribute
    """
    memberlist_obj = memberlist.Memberlist()
    assert isinstance(memberlist_obj, object)
