from cPickle import loads, dumps

from django.contrib.sessions.backends.base import SessionBase, CreateError
from django.conf import settings

from djsession.backends.cached_db import SessionStore as CachedDBSessionStore

import redis


r = redis.Redis(
    host=getattr(settings, 'REDIS_SESSION_HOST', None),
    port=int(getattr(settings, 'REDIS_SESSION_PORT', None)),
    socket_timeout=int(getattr(settings, 'REDIS_SESSION_SOCKET_TIMEOUT', None)),
    db=int(getattr(settings, 'REDIS_SESSION_DB', None)))


class SessionStore(SessionBase):
    """
    A redis-based session store.
    """
    def __init__(self, session_key=None):
        self.cached_db = CachedDBSessionStore(session_key=session_key)
        self.redis = r
        # self.redis.connect()
        super(SessionStore, self).__init__(session_key)

    def load(self):
        session_data = self.redis.get(self.session_key)
        if session_data is not None:
            return loads(session_data)
        else:
            session_data = self.cached_db.load()
            self.save(session_data=session_data)
            self.cached_db.delete(self.session_key)
            return session_data

    def create(self, session_data=None):
        while True:
            self.session_key = self._get_new_session_key()
            try:
                self.save(must_create=True, session_data=session_data)
            except CreateError:
                # Would be raised if the key wasn't unique
                continue
            self.modified = True
            return

    def save(self, must_create=False, session_data=None):
        # MULTI/EXEC command is disabled for the moment as it doesn't seem 
        # to be support in stable versions of redis yet (as of 1.2.6)
        # self.redis.execute_command('MULTI')
        if not session_data:
            session_data = self._get_session(no_load=must_create)
        if must_create:
            # preserve=True -> SETNX
            result = self.redis.set(
                self.session_key, dumps(session_data), preserve=True)
            if result == 0: # 0 == not created, 1 == created.
                raise CreateError
        else:
            self.redis.set(self.session_key, dumps(session_data),)
        
        if (session_data.get('_auth_user_id', False)):
            self.redis.execute_command('EXPIRE', self.session_key, getattr(settings, 'REDIS_AUTHENTICATED_SESSION_KEY_TTL', 60 * 60 * 24 * 30))
        else:
            self.redis.execute_command('EXPIRE', self.session_key, getattr(settings, 'REDIS_ANONYMOUS_SESSION_KEY_TTL', 60 * 60 * 24 * 2))
        
        # :FIXME: the EXEC is currently commented out, see MULTI/EXEC note above
        # self.redis.execute_command('EXEC')

    def exists(self, session_key):
        if self.redis.exists(session_key):
            return True
        return False

    def delete(self, session_key=None):
        if session_key is None:
            if self._session_key is None:
                return
            session_key = self._session_key
        self.redis.delete(session_key)
