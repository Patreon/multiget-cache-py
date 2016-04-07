Multiget Cache
=====
Python library for turning N O(1) function calls into 1 O(1) function call.


## Introduction

For functions that are closer to O(1) than O(N),
it often makes sense to queue up a list of desired executions,
and then execute the function just once, rather than N times.
The MultigetCacheWrapper assists in this,
by allowing the client to add to a queue of function calls,
and then flushing that queue when a client actually needs the response synchronously.
Once the queue is flushed, the results of each member of the queue are placed into a cache
such that an individual function call is not made aware of any other members in the queue.
This can be particularly beneficial for SQL queries,
where each client is interested in getting just one row,
but they are all requesting different rows.
You probably don't want to execute N SQL queries,
so MultigetCacheWrapper can turn those N queries into 1 query that populates N entries in the cache.


## Installation & Usage

```
> pip install multiget-cache
```

```python
import multiget_cache
from multiget_cache.multiget_cache_wrapper import multiget_cached
from generic_social_network.app import db
from sqlalchemy import Column, Integer, String


multiget_cache.register_cache(multiget_cache.flask_request_cache.get_request_cache)


class User(db.Model):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True, nullable=False)
    name = Column(String(512), default='')

    @multiget_cached(object_key='user_id')
    def get(id_):
        # id_ will be a list
        User.query.filter(User.user_id.in_(id_)).all()


User.get.prime(1); User.get.prime(2); User.get.prime(3)

my_user = User.get(1)
# SQL echo: `SELECT * FROM users WHERE user_id IN (1, 2, 3)`
# my_user == <User user_id: 1>

my_other_user = User.get(2)
# no SQL execution needed, as result is in our cache
# my_other_user == <User user_id: 2>
```