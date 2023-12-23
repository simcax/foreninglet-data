import pytest

import foreninglet_data
from foreninglet_data import api


@pytest.mark.xfail
def test_api_call_fail_on_no_username():
    """Tests the API call to ForeningLet failing when no username has been provided"""

    fl_cls = api.ForeningLet()
    fl_cls.api_username = ""
    assert fl_cls.check_api_responds() is True


@pytest.mark.xfail
def test_api_call_fail_on_no_password():
    """Tests the API call to ForeningLet failing when no password has been provided"""

    fl_cls = api.ForeningLet()
    fl_cls.api_password = ""
    assert fl_cls.check_api_responds() is True


@pytest.mark.vcr()
def test_api_call_succeed():
    """Tests the API call to ForeningLet succeeding when credentials has been provided"""

    fl_cls = api.ForeningLet()
    assert fl_cls.check_api_responds() == 200


@pytest.mark.vcr()
def test_get_memberlist():
    """Test the list of members being returned"""
    fl_cls = api.ForeningLet()
    memberlist = fl_cls.get_memberlist()
    assert isinstance(memberlist, str)


@pytest.mark.vcr()
def test_get_gender_count():
    """
    Test getting the count of each gender
    """
    fl_cls = api.ForeningLet()
