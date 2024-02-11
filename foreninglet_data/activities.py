"""Modules to handle member activities"""
from foreninglet_data.models.activities_model import Activity


class Activities:
    """Class to handle member activities"""

    def __init__(self, activities: list):
        self.activities = activities

    def get_activities(self):
        """Return the list of activities"""
        return self.activities

    def make_activity_map(self):
        """Return a dictionary of activities"""
        activity_map = {}
        for activity in self.activities:
            activity_model = Activity.from_dict(activity)
            activity_map[activity["ActivityId"]] = activity_model.Name
        return activity_map
