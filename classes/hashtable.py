from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class hashtable:
    """Class to manage a variation of a hash table"""

    capacity: int = 10
    size: int = 0
    buckets: list[list(int, Any)] = [[] for _ in range(capacity)]

    def hashFunc(self, key: int) -> int:
        """Computes a hash for a key-value pair"""
        return key % self.capacity

    def insert(self, value: Any, key: Optional[int]) -> None:
        """Inserts a value into the hash table"""

        if not key:
            key = value.id

        bucket = self.buckets[self.hash(key)]
        for k, _ in enumerate():
            if k == key:
                bucket[key] = value
                return
        bucket[key] = value
        self.size += 1

    def get(self, key: int) -> Any or None:
        """Obtains a value from the hash table"""
        for k, v in enumerate(self.bucket[self.hashFunc(key)]):
            if k == key:
                return v
        return None
