from django.core.cache import cache
from requests import delete
from rest_framework.exceptions import NotFound
import uuid


def generate_uuid():
    return str(uuid.uuid4())


def generate_cache_key(prefix, key):
    return f"{prefix}{key}"


def generate_cache_key_with_uuid(prefix, key):
    return f"{prefix}{key}_{generate_uuid()}"


def generate_pagination_cache_key(prefix, page_size, page):
    return f"{prefix}_{page_size}_{page}"


def generate_keys_cache_key(prefix, key):
    return f"{prefix}{key}_keys"


class Cache:
    """
    Cache class to handle cache operations

    Attributes
    ----------
        prefix (str): Prefix to be added to the cache key
        timeout (int): Time in seconds for the cache to expire

    Example
    -------
        >>> cache = Cache()
        >>> cache.set('key', 'value')
        >>> cache.get('key')
        'value'
        >>> cache.invalidate('key')
        >>> cache.get('key')
        NotFound: Cache key cache_key not found


    Methods
    -------
        get: Get the cached data for the given key
        set: Set the cached data for the given key
        invalidate_all: Invalidate all the cache keys
        invalidate: Invalidate the cache for the given key
        get_list: Get the cached data for the given key
        set_list: Set the cached data for the given key
        invalidate_list: Invalidate the cache for the given key
    """

    def __init__(self, prefix="cached_", timeout=3600 * 48):
        self.prefix = prefix
        self.timeout = timeout

    def _generate_cache_key(self, key: str) -> str:
        """
        Generate the cache key for the given key

        Parameters
        ----------
            key (str): Key to be used to generate the cache key

        Returns
        -------
            cache_key (str): Cache key for the given key

        Example
        -------
            >>> cache = Cache()
            >>> cache._generate_cache_key('key')
            'cache_key_prefix_uuid'
        """
        return generate_cache_key(self.prefix, key)

    def get(self, key, paginate=None):
        """
        Get the cached data for the given key

        Parameters
        ----------
            key (str): Key to be used to get the cached data

        Returns
        -------
            data (any): Cached data for the given key

        Raises
        ------
            NotFound: If the key is not found in the cache

        Example
        -------
            >>> cache = Cache()
            >>> cache.set('key', 'value')
            >>> cache.get('key')
            'value'
        """

        key = self._generate_cache_key(key)

        if paginate is not None:
            key = generate_pagination_cache_key(
                key, paginate.get("page_size"), paginate.get("page")
            )

        cached_data = cache.get(key)
        return cached_data

    def set(self, key: str, data, paginate=None, store_keys=True, keys_key=None) -> None:
        # -- when data is set in the cache
        # it stores the key in list that's
        # related to the object saved
        # e.g cached_order_keys=[<all order related object keys>] --
        if keys_key is None:
            keys_key = generate_keys_cache_key(self.prefix, key)

        key = self._generate_cache_key(key)

        if paginate is not None:
            key = generate_pagination_cache_key(
                key, paginate.get("page_size"), paginate.get("page")
            )

        cache.set(key, data, self.timeout)

        # -- tries to store new keys to the list --
        if store_keys is True:
            keys = cache.get(keys_key)
            if keys is not None and len(keys) > 0:
                tmp = keys.copy()  # copies keys from memory first
                tmp.append(key)  # appends new key
                cache.delete(keys_key)  # delete old keys
                cache.set(keys_key, tmp, self.timeout)  # replace with new keys
            else:
                data = [key]
                cache.set(keys_key, data, self.timeout)

    def invalidate(self, key):
        key = self._generate_cache_key(key)

        try:
            cache.delete(key)
        except Exception as error:
            print(error)

    def get_many(self, keys):
        cache_keys = [self._generate_cache_key(key) for key in keys]
        cached_data = cache.get_many(cache_keys)
        return cached_data

    def set_many(self, data_dict):
        cache_keys = {
            self._generate_cache_key(key): data for key, data in data_dict.items()
        }
        cache.set_many(cache_keys, self.timeout)

    def invalidate_many(self, key_prefix, key=None, keys=None):
        keys_key = key
        if key is None:
            keys_key = generate_keys_cache_key(self.prefix, key_prefix)

        if keys is None:
            # -- get keys from cache
            # should be a list of keys --
            keys = cache.get(keys_key)

        if keys is None:
            # -- set to empty list --
            keys = []

            print("couldn't find keys to delete, nothing would be deleted")

        # -- delete objects --
        try:
            cache.delete_many(keys)
        except Exception as error:
            print(error)
