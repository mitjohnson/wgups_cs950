from dataclasses import dataclass
from datetime import time


@dataclass
class Package:
    """Class to manage delivery packages"""

    id: int
    address: str
    city: str
    state: str
    zip: str
    weight: int
    devlivery_time: time or None = None
    loading_time: time or None = None
