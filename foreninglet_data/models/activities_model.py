"""Model for the foreninglet Activities"""
from dataclasses import dataclass, field
from typing import List

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Activity:
    """Implements a Foreninglet Activities model"""

    ActivityId: int
    Name: str
    PriceNow: float
    OnlineEnrollmentEnabled: bool
    SettlementDate: str
    CloseDate: str
