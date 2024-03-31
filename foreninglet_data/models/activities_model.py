"""Model for the foreninglet Activities"""

from dataclasses import dataclass, field
from typing import List, Optional

from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class Activity:
    """Implements a Foreninglet Activities model"""

    ActivityId: int
    Name: str
    OnlineEnrollmentEnabled: bool
    Categories: List[str]
    DepartmentId: Optional[int] = None
    ExternalDescriptions: Optional[List[dict[str, str]]] = field(default_factory=list)
    PriceNow: Optional[float] = "0.00"
    SettlementDate: Optional[str] = None
    CloseDate: Optional[str] = None


@dataclass
@dataclass_json
class ActivityList:
    """List of Activity objects"""

    Activities: List[Activity]
