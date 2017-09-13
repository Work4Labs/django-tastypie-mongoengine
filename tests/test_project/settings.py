# Django settings for test_project project

DEBUG = True

# We are not really using a relational database, but tests fail without
# defining it because flush command is being run, which expects it
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Make this unique, and don't share it with anybody
SECRET_KEY = 'sq=uf!nqw=aibl+y1&5pp=)b7pc=c$4hnh$om*_c48r)^t!ob)'

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
)

ROOT_URLCONF = 'test_project.urls'

TEST_RUNNER = 'tastypie_mongoengine.test_runner.MongoEngineTestSuiteRunner'

INSTALLED_APPS = (
    'django.contrib.contenttypes',
    'tastypie',
    'tastypie_mongoengine',
    'test_project.test_app',
)

MONGO_DATABASE_NAME = 'test_project'

import mongoengine
mongoengine.connect(MONGO_DATABASE_NAME)
