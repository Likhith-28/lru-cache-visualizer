import pytest

from backend.lru_cache import LRUCache


def test_put_then_get_returns_value_and_tracks_hits():
    cache = LRUCache(3)

    cache.put("user1", "Ramdas")
    assert cache.get("user1") == "Ramdas"
    assert cache.hits == 1
    assert cache.misses == 0
    assert cache.items() == [{"key": "user1", "value": "Ramdas"}]


def test_missing_key_counts_miss_and_returns_none():
    cache = LRUCache(2)

    assert cache.get("missing") is None
    assert cache.misses == 1
    assert cache.hits == 0


def test_get_moves_item_to_mru_end():
    cache = LRUCache(3)
    cache.put("A", 1)
    cache.put("B", 2)
    cache.put("C", 3)

    assert cache.items() == [
        {"key": "A", "value": 1},
        {"key": "B", "value": 2},
        {"key": "C", "value": 3},
    ]

    cache.get("A")

    assert cache.items() == [
        {"key": "B", "value": 2},
        {"key": "C", "value": 3},
        {"key": "A", "value": 1},
    ]


def test_put_on_full_cache_evicts_lru_item():
    cache = LRUCache(2)
    cache.put("A", 1)
    cache.put("B", 2)
    cache.put("C", 3)

    assert cache.items() == [
        {"key": "B", "value": 2},
        {"key": "C", "value": 3},
    ]
    assert cache.evictions == 1
    assert "A" not in cache.cache


def test_put_on_existing_key_updates_without_duplicate_and_keeps_mru_order():
    cache = LRUCache(3)
    cache.put("A", 1)
    cache.put("B", 2)
    cache.put("A", 10)

    assert cache.items() == [
        {"key": "B", "value": 2},
        {"key": "A", "value": 10},
    ]
    assert len(cache.cache) == 2


def test_reset_clears_cache_and_statistics():
    cache = LRUCache(2)
    cache.put("A", 1)
    cache.put("B", 2)
    cache.get("A")
    cache.put("C", 3)

    cache.reset()

    assert cache.items() == []
    assert cache.hits == 0
    assert cache.misses == 0
    assert cache.evictions == 0
    assert len(cache.cache) == 0


def test_capacity_one_works():
    cache = LRUCache(1)
    cache.put("A", 1)
    cache.put("B", 2)

    assert cache.items() == [{"key": "B", "value": 2}]
    assert cache.get("A") is None
    assert cache.hits == 0
    assert cache.misses == 1
    assert cache.evictions == 1


def test_invalid_capacity_raises_value_error():
    with pytest.raises(ValueError):
        LRUCache(0)
