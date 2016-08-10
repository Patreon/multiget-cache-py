from typing import List
from nose.tools import assert_equals, with_setup

import multiget_cache
from multiget_cache.multiget_cache_wrapper import multiget_cached


class CallCounter(object):
    fake_db = {}
    call_count = 0

    def __init__(self, id_):
        self.uid = id_

    @classmethod
    def reset(cls):
        cls.fake_db = {}
        cls.call_count = 0

    @classmethod
    def create(cls, id_):
        cls.fake_db[id_] = CallCounter(id_)
        return cls.fake_db[id_]

    @staticmethod
    @multiget_cached(object_key='uid')
    def get(ids):
        CallCounter.call_count += 1
        return [CallCounter.fake_db[one_id] for one_id in ids]

    @staticmethod
    @multiget_cached(object_key='uid')
    def get_with_typehints(ids: List[int]) -> List['CallCounter']:
        CallCounter.call_count += 1
        return [CallCounter.fake_db[one_id] for one_id in ids]


def reset_all():
    CallCounter.reset()
    multiget_cache.register_cache({})


@with_setup(setup=reset_all)
def test_multiget_simple_cache():
    for i in range(5):
        CallCounter.create(i)
        CallCounter.get.prime(i)

    first_get = CallCounter.get(0)
    assert_equals(first_get.uid, 0)
    assert_equals(CallCounter.call_count, 1)

    second_get = CallCounter.get(1)
    assert_equals(second_get.uid, 1)
    assert_equals(CallCounter.call_count, 1)

    CallCounter.create(9)
    cache_miss = CallCounter.get(9)
    assert_equals(cache_miss.uid, 9)
    assert_equals(CallCounter.call_count, 2)

    cache_hit = CallCounter.get(2)
    assert_equals(cache_hit.uid, 2)
    assert_equals(CallCounter.call_count, 2)


@with_setup(setup=reset_all)
def test_multiget_simple_cache_with_typehints():
    for i in range(5):
        CallCounter.create(i)
        CallCounter.get_with_typehints.prime(i)

    first_get = CallCounter.get_with_typehints(0)
    assert_equals(first_get.uid, 0)
    assert_equals(CallCounter.call_count, 1)

    second_get = CallCounter.get_with_typehints(1)
    assert_equals(second_get.uid, 1)
    assert_equals(CallCounter.call_count, 1)

    CallCounter.create(9)
    cache_miss = CallCounter.get_with_typehints(9)
    assert_equals(cache_miss.uid, 9)
    assert_equals(CallCounter.call_count, 2)

    cache_hit = CallCounter.get_with_typehints(2)
    assert_equals(cache_hit.uid, 2)
    assert_equals(CallCounter.call_count, 2)
