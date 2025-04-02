"""Tests for the resigned memberlist class"""

import pytest
import vcr

from foreninglet_data.api import ForeningLet
from foreninglet_data.memberlist import Memberlist


@vcr.use_cassette(
    "tests/cassettes/fl_api_get_resigned_members.yaml", filter_headers=["authorization"]
)
@pytest.mark.vcr
def test_resigned_memberlist_class_works_with_real_api_data():
    """
    Tests the resigned memberlist class works with memberlist data
    coming from the ForeningLet API
    """
    fl_obj = ForeningLet()
    memberlist = fl_obj.get_resigned_members()
    memberlist_obj_resigned = Memberlist(memberlist)

    assert isinstance(memberlist_obj_resigned.member_count, int)
