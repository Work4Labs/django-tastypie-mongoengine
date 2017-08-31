from django.conf.urls import include, url

from tastypie import api

from test_project.test_app.api import resources

v1_api = api.Api(api_name='v1')
v1_api.register(resources.PersonResource())
v1_api.register(resources.PersonObjectClassResource())
v1_api.register(resources.OnlySubtypePersonResource())
v1_api.register(resources.IndividualResource())
v1_api.register(resources.CompanyResource())
v1_api.register(resources.ContactResource())
v1_api.register(resources.ContactGroupResource())
v1_api.register(resources.CustomerResource())
v1_api.register(resources.DictFieldTestResource())
v1_api.register(resources.ListFieldTestResource())
v1_api.register(resources.ReferencedListFieldTestResource())
v1_api.register(resources.ReferencedListFieldNonFullTestResource())
v1_api.register(resources.BooleanMapTestResource())
v1_api.register(resources.AutoAllocationFieldTestResource())
v1_api.register(resources.ExporterResource())
v1_api.register(resources.BlankableParentResource())
v1_api.register(resources.ReadonlyParentResource())
v1_api.register(resources.DatetimeFieldTestResource())

urlpatterns = [
    url(r'^api/', include(v1_api.urls)),
]
