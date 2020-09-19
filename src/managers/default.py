from accessors import UrlsTabAccessor
from managers import ShortUrlManager, NotFoundException
from managers.generators import UniqueShortKeyGenerator
from utils.redis import redis_client

class DefaultShortUrlManager(ShortUrlManager):
    def __init__(self, urls_tab_accessor: UrlsTabAccessor, short_key_generator: UniqueShortKeyGenerator):
        super().__init__(urls_tab_accessor, short_key_generator)

    def resolve(self, short_key: str) -> str:
        """
        Return the latest source url for the short key.
        """

        redis = redis_client()
        cached_url = redis.get(short_key)

        # cache hit
        if cached_url:
            return cached_url

        # cache miss, query DB
        db_url = self.urls_tab_accessor.find_last_by_short_key(short_key)
        if db_url is None:
            raise NotFoundException(f'url not found for short_key: {short_key}')

        # update cache
        redis.setnx(short_key, db_url)
        return db_url

    def create(self, url: str) -> str:
        """
        Return a short key for the url.
        """
        redis = redis_client()
        cached_short_key = redis.get(url)

        # cache hit
        if cached_short_key:
            return cached_short_key

        short_key, matched = self.urls_tab_accessor.find_match_by_url(url)
        if matched == url:
            return short_key

        # just create a new short_key
        generated_short_key = self._generate_new_short_key(url)

        # add generated key to cache
        redis.setnx(url, generated_short_key)

        return generated_short_key

    def _generate_new_short_key(self, url):
        short_key = self.short_key_generator.generate(url)
        self.urls_tab_accessor.create(short_key, url)
        return short_key
