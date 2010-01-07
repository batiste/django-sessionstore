# Django settings for testproj project.


DEBUG = True
TEMPLATE_DEBUG = DEBUG

ROOT_URLCONF = "urls"

ADMINS = (
    # ('Your Name', 'your_email@domain.com'),
)

TEST_RUNNER = "djsession.runners.run_tests"
TEST_APPS = (
    "djsession",
)


MANAGERS = ADMINS

DATABASE_ENGINE = 'sqlite3'
DATABASE_NAME = 'testdb.sqlite'
DATABASE_USER = ''
DATABASE_PASSWORD = ''
DATABASE_HOST = ''
DATABASE_PORT = ''

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'djsession',
)


try:
    import test_extensions
except ImportError:
    pass
else:
    pass
    #INSTALLED_APPS += ("test_extensions", )
