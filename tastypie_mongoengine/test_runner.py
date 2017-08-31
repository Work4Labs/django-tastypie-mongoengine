from unittest import TestCase, TestSuite
import urlparse

from django.conf import settings
from django.test import client, runner, TestCase

from mongoengine import connect, connection


class MongoEngineTestSuiteRunner(runner.DiscoverRunner):
    """
    It is the same as in DiscoverRunner, but without relational databases.

    It also supports filtering only wanted tests through ``TEST_RUNNER_FILTER``
    Django setting.
    """

    db_name = 'test_%s' % settings.MONGO_DATABASE_NAME

    def _filter_suite(self, suite):
        filters = getattr(settings, 'TEST_RUNNER_FILTER', None)

        if filters is None:
            # We do NOT filter if filters are not set
            return suite

        filtered = TestSuite()

        for test in suite:
            if isinstance(test, TestSuite):
                filtered.addTests(self._filter_suite(test))
            else:
                for f in filters:
                    if test.id().startswith(f):
                        filtered.addTest(test)

        return filtered

    def build_suite(self, test_labels, extra_tests=None, **kwargs):
        suite = super(MongoEngineTestSuiteRunner, self).build_suite(test_labels, extra_tests=None, **kwargs)
        suite = self._filter_suite(suite)
        return runner.reorder_suite(suite, (TestCase,))

    def setup_databases(self, **kwargs):
        connection.disconnect()
        connect(self.db_name, **getattr(settings, 'MONGO_DATABASE_OPTIONS', {}))

    def teardown_databases(self, old_config, **kwargs):
        connection.get_connection().drop_database(self.db_name)


class MongoEngineTestCase(TestCase):
    """
    From https://github.com/MongoEngine/mongoengine/blob/v0.9.0/mongoengine/django/tests.py
    MongoEngine dropped its Django support since then. (Well, moved to a separate repo, which is dead)

    TestCase class that clear the collection between the tests
    """

    @property
    def db_name(self):
        from django.conf import settings
        return 'test_%s' % getattr(settings, 'MONGO_DATABASE_NAME', 'dummy')

    def __init__(self, methodName='runtest'):
        connect(self.db_name)
        self.db = connection.get_db()
        super(MongoEngineTestCase, self).__init__(methodName)

    def dropCollections(self):
        for collection in self.db.collection_names():
            if collection.startswith('system.'):
                continue
            self.db.drop_collection(collection)

    def tearDown(self):
        self.dropCollections()


# We also patch Django so that it supports PATCH requests (used by Tastypie)
# Taken from https://code.djangoproject.com/attachment/ticket/17797/django-test-client-PATCH.patch

def requestfactory_patch(self, path, data=None, content_type=client.MULTIPART_CONTENT, **extra):
    """
    Construct a PATCH request.
    """

    data = data or {}
    patch_data = self._encode_data(data, content_type)

    parsed = urlparse.urlparse(path)
    request = {
        'CONTENT_LENGTH': len(patch_data),
        'CONTENT_TYPE': content_type,
        'PATH_INFO': self._get_path(parsed),
        'QUERY_STRING': parsed[4],
        'REQUEST_METHOD': 'PATCH',
        'wsgi.input': client.FakePayload(patch_data),
    }
    request.update(extra)
    return self.request(**request)


def client_patch(self, path, data=None, content_type=client.MULTIPART_CONTENT, follow=False, **extra):
    """
    Send a resource to the server using PATCH.
    """

    data = data or {}
    response = super(client.Client, self).patch(path, data=data, content_type=content_type, **extra)
    if follow:
        response = self._handle_redirects(response, **extra)
    return response

if not hasattr(client.RequestFactory, 'patch'):
    client.RequestFactory.patch = requestfactory_patch

if not hasattr(client.Client, 'patch'):
    client.Client.patch = client_patch
