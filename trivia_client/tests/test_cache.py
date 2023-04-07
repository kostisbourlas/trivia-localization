from django.test import TestCase

from trivia_client.cache import DictCache


class CacheTestCase(TestCase):
    def setUp(self):
        self.cache = DictCache()

    def test_cache_put_and_get(self):
        self.cache.set("key1", "value1")
        self.cache.set("key2", "value2")
        self.assertEqual(self.cache.get("key1"), "value1")
        self.assertEqual(self.cache.get("key2"), "value2")
