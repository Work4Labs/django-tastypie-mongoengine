from tastypie import authorization as tastypie_authorization, fields as tastypie_fields

from tastypie_mongoengine import fields, paginator, resources

from test_project.test_app import documents


class StrangePersonResource(resources.MongoEngineResource):
    class Meta:
        queryset = documents.StrangePerson.objects.all()
        excludes = ('hidden',)


class OtherStrangePersonResource(resources.MongoEngineResource):
    class Meta:
        queryset = documents.StrangePerson.objects.all()
        excludes = ('hidden',)


class PersonResource(resources.MongoEngineResource):
    class Meta:
        # Ordering by id so that pagination is predictable
        queryset = documents.Person.objects.all().order_by('id')
        allowed_methods = ('get', 'post', 'put', 'patch', 'delete')
        authorization = tastypie_authorization.Authorization()
        ordering = ('name',)
        excludes = ('hidden',)
        paginator_class = paginator.Paginator

        polymorphic = {
            'person': 'self',
            'strangeperson': StrangePersonResource,
        }


class PersonObjectClassResource(resources.MongoEngineResource):
    class Meta:
        object_class = documents.Person
        allowed_methods = ('get', 'post')
        authorization = tastypie_authorization.Authorization()
        resource_name = 'personobjectclass'


class OnlySubtypePersonResource(resources.MongoEngineResource):
    class Meta:
        queryset = documents.Person.objects.all()
        allowed_methods = ('get', 'post', 'put', 'patch', 'delete')
        authorization = tastypie_authorization.Authorization()
        excludes = ('hidden',)

        polymorphic = {
            'strangeperson': StrangePersonResource,
        }


class EmbeddedStrangePersonResource(resources.MongoEngineResource):
    class Meta:
        object_class = documents.EmbeddedStrangePerson


class EmbeddedPersonResource(resources.MongoEngineResource):
    class Meta:
        object_class = documents.EmbeddedPerson
        allowed_methods = ('get', 'post', 'put', 'patch', 'delete')
        authorization = tastypie_authorization.Authorization()
        ordering = ('name',)
        excludes = ('hidden',)

        polymorphic = {
            'person': 'self',
            'strangeperson': EmbeddedStrangePersonResource,
        }


class IndividualResource(resources.MongoEngineResource):
    class Meta:
        queryset = documents.Individual.objects.all()
        allowed_methods = ('get', 'post', 'put', 'patch', 'delete')
        authorization = tastypie_authorization.Authorization()
        paginator_class = paginator.Paginator


class CompanyResource(resources.MongoEngineResource):
    class Meta:
        queryset = documents.Company.objects.all()
        allowed_methods = ('get', 'post', 'put', 'patch', 'delete')
        authorization = tastypie_authorization.Authorization()
        paginator_class = paginator.Paginator


class UnregisteredCompanyResource(resources.MongoEngineResource):
    class Meta:
        queryset = documents.UnregisteredCompany.objects.all()
        allowed_methods = ('get', 'post', 'put', 'patch', 'delete')
        authorization = tastypie_authorization.Authorization()
        paginator_class = paginator.Paginator


class ContactResource(resources.MongoEngineResource):
    class Meta:
        queryset = documents.Contact.objects.all()
        allowed_methods = ('get', 'post', 'put', 'patch', 'delete')
        authorization = tastypie_authorization.Authorization()

        prefer_polymorphic_resource_uri = True
        polymorphic = {
            'individual': IndividualResource,
            'company': CompanyResource,
            'unregisteredcompany': UnregisteredCompanyResource,
        }


class ContactGroupResource(resources.MongoEngineResource):
    contacts = fields.ReferencedListField(of='test_project.test_app.api.resources.ContactResource', attribute='contacts', null=True)

    class Meta:
        queryset = documents.ContactGroup.objects.all()
        allowed_methods = ('get', 'post', 'put', 'patch', 'delete')
        authorization = tastypie_authorization.Authorization()


class CustomerResource(resources.MongoEngineResource):
    person = fields.ReferenceField(to='test_project.test_app.api.resources.PersonResource', attribute='person', full=True)

    class Meta:
        queryset = documents.Customer.objects.all()
        allowed_methods = ('get', 'post', 'put', 'patch', 'delete')
        authorization = tastypie_authorization.Authorization()


class EmbeddedCommentResource(resources.MongoEngineResource):
    class Meta:
        object_class = documents.EmbeddedComment


class EmbeddedDocumentFieldTestResource(resources.MongoEngineResource):
    customer = fields.EmbeddedDocumentField(embedded='test_project.test_app.api.resources.EmbeddedPersonResource', attribute='customer', null=True)

    class Meta:
        queryset = documents.EmbeddedDocumentFieldTest.objects.all()
        allowed_methods = ('get', 'post', 'put', 'patch', 'delete')
        authorization = tastypie_authorization.Authorization()


class DictFieldTestResource(resources.MongoEngineResource):
    class Meta:
        queryset = documents.DictFieldTest.objects.all()
        allowed_methods = ('get', 'post', 'put', 'patch', 'delete')
        authorization = tastypie_authorization.Authorization()


class ListFieldTestResource(resources.MongoEngineResource):
    extra_list = tastypie_fields.ListField()

    class Meta:
        queryset = documents.ListFieldTest.objects.all()
        allowed_methods = ('get', 'post', 'put', 'patch', 'delete')
        authorization = tastypie_authorization.Authorization()


class ReferencedListFieldTestResource(resources.MongoEngineResource):
    referencedlist = fields.ReferencedListField(of='test_project.test_app.api.resources.PersonResource', attribute='referencedlist', full=True, null=True)

    class Meta:
        queryset = documents.ReferencedListFieldTest.objects.all()
        allowed_methods = ('get', 'post', 'put', 'patch', 'delete')
        authorization = tastypie_authorization.Authorization()


class ReferencedListFieldNonFullTestResource(resources.MongoEngineResource):
    referencedlist = fields.ReferencedListField(of='test_project.test_app.api.resources.PersonResource', attribute='referencedlist', full=False, null=True)

    class Meta:
        queryset = documents.ReferencedListFieldTest.objects.all()
        allowed_methods = ('get', 'post', 'put', 'patch', 'delete')
        authorization = tastypie_authorization.Authorization()


class BooleanMapTestResource(resources.MongoEngineResource):
    is_published_defined = tastypie_fields.BooleanField(default=False, null=False, attribute='is_published_defined')

    class Meta:
        queryset = documents.BooleanMapTest.objects.all()
        allowed_methods = ('get', 'post', 'put', 'patch', 'delete')
        authorization = tastypie_authorization.Authorization()


class AutoAllocationFieldTestResource(resources.MongoEngineResource):
    slug = tastypie_fields.CharField(readonly=True, attribute='slug')

    class Meta:
        queryset = documents.AutoAllocationFieldTest.objects.all()
        allowed_methods = ('get', 'post', 'put', 'patch', 'delete')
        authorization = tastypie_authorization.Authorization()


class ExporterResource(resources.MongoEngineResource):
    class Meta:
        queryset = documents.Exporter.objects.all()
        resource_name = 'exporters'
        allowed_methods = ('get', 'post', 'put', 'delete')
        authorization = tastypie_authorization.Authorization()


class EmbeddedExporterListResource(resources.MongoEngineResource):
    exporter = fields.ReferenceField(to='test_project.test_app.api.resources.ExporterResource', attribute='exporter', full=True)

    class Meta:
        object_class = documents.PipeExporterEmbedded


class BlankableEmbeddedResource(resources.MongoEngineResource):
    class Meta:
        object_class = documents.BlankableEmbedded


class BlankableParentResource(resources.MongoEngineResource):
    embedded = fields.EmbeddedDocumentField(embedded='test_project.test_app.api.resources.BlankableEmbeddedResource', attribute='embedded', blank=True)

    class Meta:
        queryset = documents.BlankableParent.objects.all()
        allowed_methods = ('get', 'post', 'put', 'patch', 'delete')
        authorization = tastypie_authorization.Authorization()


class TimezonedDateTimeResource(resources.MongoEngineResource):
    class Meta:
        object_class = documents.TimezonedDateTime


class ReadonlyParentResource(resources.MongoEngineResource):
    tzdt = fields.EmbeddedDocumentField(embedded='test_project.test_app.api.resources.TimezonedDateTimeResource', attribute='tzdt', readonly=True)

    class Meta:
        queryset = documents.ReadonlyParent.objects.all()
        allowed_methods = ('get', 'post', 'put', 'patch', 'delete')
        authorization = tastypie_authorization.Authorization()


class DatetimeFieldTestResource(resources.MongoEngineResource):
    class Meta:
        queryset = documents.DatetimeFieldTest.objects.all()
        allowed_methods = ('get', 'post', 'put', 'patch', 'delete')
        authorization = tastypie_authorization.Authorization()
