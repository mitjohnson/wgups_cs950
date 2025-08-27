from dataclasses import dataclass
from datetime import time
from typing import Optional


@dataclass
class Package:
    """Class to manage delivery packages"""

    id: int
    address: str
    city: str
    state: str
    zip: str
    weight: int
    delivery_deadline: time
    special_notes: Optional[str] = None
    devlivery_time: Optional[time] = None
    loading_time: Optional[time] = None
