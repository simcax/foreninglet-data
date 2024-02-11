"""Testing the activities module."""

# The test file is named test_activities.py, and the module is named activities.py.

import pytest

from foreninglet_data.activities import Activities
from foreninglet_data.api import ForeningLet
from foreninglet_data.models.activities_model import Activity


def test_activities_initialize():
    """Test the initialize function."""
    activities_obj = Activities()
    assert isinstance(activities_obj, Activities)


def test_get_activities():
    """Test the get_activities function."""
    fl_obj = ForeningLet()
    activity_list = fl_obj.get_activities()
    assert isinstance(activity_list, list)


def test_make_activity_map():
    """Test the make_activity_map function."""
    fl_obj = ForeningLet()
    activity_list = fl_obj.get_activities()
    activity_obj = Activities(activity_list)
    activity_map = activity_obj.make_activity_map()
    assert isinstance(activity_map, dict)


def test_mapping_activity_to_model():
    """Test mapping activity to model"""
    fl_obj = ForeningLet()
    activity_list = fl_obj.get_activities()
    activity = activity_list[0]
    activity_model = Activity.from_dict(activity)
    assert isinstance(activity_model, Activity)
