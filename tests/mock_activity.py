"""Mocks an activity from ForeningLet API"""

from random import randint

from faker import Faker

from foreninglet_data.models.activities_model import Activity

from foreninglet_data.models.activities_model import Activity


class MockActivity(Activity):
    """Class moocking an activity from ForeningLet API"""

    def mock_activity(self, output_type: str = "json"):
        """Mock an activity"""
        fake = Faker()
        ActivityId = randint(0, 1000)
        Name = fake.word()
        OnlineEnrollmentEnabled = randint(0, 1)
        SettlementDate = fake.date_of_birth(minimum_age=1).strftime("%Y-%m-%d")
        ExternalDescriptions = fake.word()
