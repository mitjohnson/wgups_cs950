from dataclasses import dataclass, field
from typing import Any, Optional


def make_10_lists() -> list[list]:
    return [[] for _ in range(10)]


@dataclass
class Hashtable:
    """Class to manage a variation of a hash table"""

    capacity: int = 10
    size: int = 0
    buckets: list[list[Optional[tuple]]] = field(default_factory=make_10_lists)

    def _hash_function(self, key: int) -> int:
        """Computes a hash for a key-value pair"""
        return key % self.capacity

    def insert(self, value: Any, key: Optional[int] = None) -> bool:
        """Inserts a value into the hash table"""

        if key is None:
            key = value.id

        bucket = self.buckets[self._hash_function(key)]
        for idx, (k, _) in enumerate(bucket):
            if k == key:
                bucket[idx] = (key, value)
                return True
        bucket.append((key, value))
        self.size += 1
        return True

    def remove(self, key: int) -> bool:
        """Removes a value from the hash table."""

        idx = self._hash_function(key)
        bucket = self.buckets[idx]

        for idx, (k, v) in enumerate(bucket):
            if k == v:
                bucket.pop(idx)
                self.size -= 1
                return True
        return False

    def get(self, key: int) -> Any or None:
        """Obtains a value from the hash table"""
        for _, (k, v) in enumerate(self.buckets[self._hash_function(key)]):
            if k == key:
                return v
        return None
