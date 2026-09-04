class Node:
    def __init__(self, key, val):
        self.key = key
        self.val = val
        self.prev: Node | None = None
        self.next: Node | None = None


class LRUCache:
    def __init__(self, capacity):
        if not isinstance(capacity, int) or capacity <= 0:
            raise ValueError("Capacity must be greater than 0")

        self.cap = capacity
        self.cache = {}

        self.head: Node = Node(0, 0)
        self.tail: Node = Node(0, 0)

        self.head.next = self.tail
        self.tail.prev = self.head

        self.hits = 0
        self.misses = 0
        self.evictions = 0

    def _delete(self, node):
        if node is None:
            return

        if node.prev is not None:
            node.prev.next = node.next
        if node.next is not None:
            node.next.prev = node.prev

        node.prev = None
        node.next = None

    def _insert_mru(self, node):
        prev = self.tail.prev
        if prev is None:
            raise RuntimeError("Tail sentinel has no previous node")

        node.prev = prev
        node.next = self.tail
        prev.next = node
        self.tail.prev = node

    def get(self, key):
        if key not in self.cache:
            self.misses += 1
            return None

        node = self.cache[key]
        self._delete(node)
        self._insert_mru(node)
        self.hits += 1
        return node.val

    def put(self, key, value):
        if key in self.cache:
            node = self.cache[key]
            node.val = value
            self._delete(node)
            self._insert_mru(node)
            return

        if len(self.cache) >= self.cap:
            lru = self.head.next
            if lru is not None and lru is not self.tail:
                self._delete(lru)
                del self.cache[lru.key]
                self.evictions += 1

        node = Node(key, value)
        self._insert_mru(node)
        self.cache[key] = node

    def reset(self):
        self.cache.clear()
        self.head.prev = None
        self.head.next = self.tail
        self.tail.prev = self.head
        self.tail.next = None
        self.hits = 0
        self.misses = 0
        self.evictions = 0

    def items(self):
        result = []
        current = self.head.next
        while current is not None and current is not self.tail:
            result.append({"key": current.key, "value": current.val})
            current = current.next
        return result

    def state(self):
        total = self.hits + self.misses
        return {
            "capacity": self.cap,
            "size": len(self.cache),
            "items": self.items(),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": round((self.hits / total) * 100, 2) if total else 0.0,
            "evictions": self.evictions,
        }

    def __len__(self):
        return len(self.cache)
