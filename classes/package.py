from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Package:
    id: int
    address: str
    city: str
    state: str
    zip: str
    weight: int
    delivery_deadline: datetime
    delivery_status: str = 'at the hub'
    special_notes: Optional[str] = None
    delivery_time: Optional[datetime] = None
    loading_time: Optional[datetime] = None
