import pytest

from foreninglet_data import fl_types

from .mock_member import MockMember


def test_create_member_object():
    """Test of getting a ForeningLet Member Objet"""
    member = fl_types.Member()
    assert isinstance(member, fl_types.Member)


def test_mock_member_firstname():
    """
    Testing the mock member class
    - to see the name being different from the baseclass of Member
    """
    member = fl_types.Member()
    name = member.FirstName
    mocked_member_obj = MockMember()
    mocked_member = mocked_member_obj.mock_member(output_type="obj")
    assert mocked_member.FirstName != name


def test_mock_member_lastname():
    """
    Testing the mock member class
    - to see the name being different from the baseclass of Member
    """
    member = fl_types.Member()
    name = member.LastName
    mocked_member_obj = MockMember()
    mocked_member = mocked_member_obj.mock_member(output_type="obj")
    assert mocked_member.LastName != name


def test_mock_member_memberid():
    """
    Testing the mock member class
    - to see the name being different from the baseclass of Member
    """
    member = fl_types.Member()
    name = member.MemberId
    mocked_member_obj = MockMember()
    mocked_member = mocked_member_obj.mock_member(output_type="obj")
    assert mocked_member.MemberId != name
