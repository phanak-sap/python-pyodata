"""OData service implementation

   Details regarding batch requests and changesets:
   http://www.odata.org/documentation/odata-version-2-0/batch-processing/
"""

# pylint: disable=too-many-lines

import logging
from functools import partial
import json
import random
from email.parser import Parser
from http.client import HTTPResponse
from io import BytesIO
from urllib.parse import urlencode


from pyodata.exceptions import HttpError, PyODataException, ExpressionError, ProgramError
from . import model

LOGGER_NAME = 'pyodata.service'

HTTP_CODE_OK = 200
HTTP_CODE_CREATED = 201


def urljoin(*path):
    """Joins the passed string parts into a one string url"""
    pass


def encode_multipart(boundary, http_requests):
    """Encode list of requests into multipart body"""
    pass


def decode_multipart(data, content_type):
    """Decode parts of the multipart mime content"""

    def decode(message):
        pass

    pass


class ODataHttpResponse:
    """Representation of http response"""

    def __init__(self, headers, status_code, content=None, url=None):
        pass

    @staticmethod
    def from_string(data):
        """Parse http response to status code, headers and body
           Based on: https://stackoverflow.com/questions/24728088/python-parse-http-response-string
        """

        class FakeSocket:
            """Fake socket to simulate received http response content"""
            def __init__(self, response_str):
                pass

            def makefile(self, *args, **kwargs):
                """Fake file that provides string content"""
                pass

        pass

    def json(self):
        """Return response as decoded json"""
        # TODO: see implementation in python requests, our simple approach can bring issues with encoding
        # https://github.com/requests/requests/blob/master/requests/models.py#L868
        pass


class EntityKey:
    """An immutable entity-key, made up of either a single value (single)
       or multiple key-value pairs (complex).

      Every entity must have an entity-key. The entity-key must be unique
      within the entity-set, and thus defines an entity's identity.

      The string representation of an entity-key is wrapped with parentheses,
      such as (2), ('foo') or (a=1,foo='bar').

      Entity-keys are equal if their string representations are equal.
    """

    TYPE_SINGLE = 0
    TYPE_COMPLEX = 1

    def __init__(self, entity_type, single_key=None, **args):

        pass

    @property
    def key_properties(self):
        """Key properties"""

        pass

    def to_key_string_without_parentheses(self):
        """Gets the string representation of the key without parentheses"""

        pass

    def to_key_string(self):
        """Gets the string representation of the key, including parentheses"""

        pass

    def __repr__(self):
        pass


class ODataHttpRequest:
    """Deferred HTTP Request"""

    def __init__(self, url, connection, handler, headers=None):
        pass

    @property
    def handler(self):
        """Getter for handler"""
        pass

    def get_path(self):
        """Get path of the HTTP request"""
        pass

    def get_query_params(self):
        """Get query params"""
        pass

    def get_method(self):
        """Get HTTP method"""
        pass

    def get_body(self):
        """Get HTTP body or None if not applicable"""
        pass

    def get_default_headers(self):
        """Get dict of Child specific HTTP headers"""
        pass

    def get_headers(self):
        """Get dict of HTTP headers which is union of return value
           of the method get_default_headers() and the headers
           added via the method add_headers() where the latter
           headers have priority - same keys get value of the latter.
        """
        pass

    def add_headers(self, value):
        """Add the give dictionary of HTTP headers to
           HTTP request sent by this ODataHttpRequest instance.
        """
        pass

    def _build_request(self):
        pass

    async def async_execute(self):
        """Fetches HTTP response and returns processed result

                  Sends the query-request to the OData service, returning a client-side Enumerable for
                  subsequent in-memory operations.

                  Fetches HTTP response and returns processed result"""

        pass

    def execute(self):
        """Fetches HTTP response and returns processed result

           Sends the query-request to the OData service, returning a client-side Enumerable for
           subsequent in-memory operations.

           Fetches HTTP response and returns processed result"""

        pass

    def _call_handler(self, response):
        pass

    def custom(self, name, value):
        """Adds a custom name-value pair."""
        pass


class EntityGetRequest(ODataHttpRequest):
    """Used for GET operations of a single entity"""

    def __init__(self, handler, entity_key, entity_set_proxy):
        pass

    def nav(self, nav_property):
        """Navigates to given navigation property and returns the EntitySetProxy"""
        pass

    def select(self, select):
        """Specifies a subset of properties to return.

           @param select  a comma-separated list of selection clauses
        """
        pass

    def expand(self, expand):
        """Specifies related entities to expand inline as part of the response.

           @param expand  a comma-separated list of navigation properties
        """
        pass

    def get_path(self):
        pass

    def get_default_headers(self):
        pass

    def get_query_params(self):
        pass

    def get_value(self, connection=None):
        """Returns Value of Media EntityTypes also known as the $value URL suffix."""
        pass


class NavEntityGetRequest(EntityGetRequest):
    """Used for GET operations of a single entity accessed via a Navigation property"""

    def __init__(self, handler, master_key, entity_set_proxy, nav_property):
        pass

    def get_path(self):
        pass


class EntityCreateRequest(ODataHttpRequest):
    """Used for creating entities (POST operations of a single entity)

       Call execute() to send the create-request to the OData service
       and get the newly created entity."""

    def __init__(self, url, connection, handler, entity_set, last_segment=None):
        pass

    def get_path(self):
        pass

    def get_method(self):
        pass

    def _get_body(self):
        """Recursively builds a dictionary of values where some of the values
           might be another entities.
        """
        pass

    def get_body(self):
        pass

    def get_default_headers(self):
        pass

    @staticmethod
    def _build_values(entity_type, entity):
        """Recursively converts a dictionary of values where some of the values
           might be another entities (navigation properties) into the internal
           representation.
        """
        pass

    def set(self, **kwargs):
        """Set properties on the new entity."""
        pass


class EntityDeleteRequest(ODataHttpRequest):
    """Used for deleting entity (DELETE operations on a single entity)"""

    def __init__(self, url, connection, handler, entity_set, entity_key):
        pass

    def get_path(self):
        pass

    def get_method(self):
        pass


class EntityModifyRequest(ODataHttpRequest):
    """Used for modyfing entities (UPDATE/MERGE operations on a single entity)

       Call execute() to send the update-request to the OData service
       and get the modified entity."""

    ALLOWED_HTTP_METHODS = ['PATCH', 'PUT', 'MERGE']

    def __init__(self, url, connection, handler, entity_set, entity_key, method="PATCH"):
        pass

    def get_path(self):
        pass

    def get_method(self):
        pass

    def get_body(self):
        pass

    def get_default_headers(self):
        pass

    def set(self, **kwargs):
        """Set properties to be changed."""
        pass


class QueryRequest(ODataHttpRequest):
    """INTERFACE A consumer-side query-request builder. Call execute() to issue the request."""

    # pylint: disable=too-many-instance-attributes

    def __init__(self, url, connection, handler, last_segment):
        pass

    def count(self, inline=False):
        """Sets a flag to return the number of items. Can be inline with results or just the count."""
        pass

    def next_url(self, next_url):
        """
        Sets URL which identifies the next partial set of entities from the originally identified complete set. Once
        set, this URL takes precedence over all query parameters.

        For details, see section "6. Representing Collections of Entries" on
        https://www.odata.org/documentation/odata-version-2-0/json-format/
        """
        pass

    def expand(self, expand):
        """Sets the expand expressions."""
        pass

    def filter(self, filter_val):
        """Sets the filter expression."""
        # returns QueryRequest
        pass

    # def nav(self, key_value, nav_property):
    #    """Navigates to a referenced collection using a collection-valued navigation property."""
    #    # returns QueryRequest
    #    raise NotImplementedError

    def order_by(self, order_by):
        """Sets the ordering expressions."""
        pass

    def select(self, select):
        """Sets the selection clauses."""
        pass

    def skip(self, skip):
        """Sets the number of items to skip."""
        pass

    def top(self, top):
        """Sets the number of items to return."""
        pass

    def get_path(self):
        pass

    def get_default_headers(self):
        pass

    def get_query_params(self):
        pass


class FunctionRequest(QueryRequest):
    """Function import request (Service call)"""

    def __init__(self, url, connection, handler, function_import):
        pass

    def parameter(self, name, value):
        '''Sets value of parameter.'''

        # check if param is valid (is declared in metadata)
            # add parameter as custom query argument
        pass

    def get_method(self):
        pass

    def get_default_headers(self):
        pass


# pylint: disable=too-many-instance-attributes
class EntityProxy:
    """An immutable OData entity instance, consisting of an identity (an
       entity-set and a unique entity-key within that set), properties (typed,
       named values), and links (references to other entities).
    """

    def __init__(self, service, entity_set, entity_type, proprties=None, entity_key=None, etag=None):
        # New entity proxy instance of type %s from properties: %s', entity_type.name, proprties

        # cache values of individual properties if provided

            # first, cache values of direct properties

                    # Property value available

                    # Property value missing and user wants a type specific default value filled in

                    # Property is nullable - save it as such


            # then, assign all navigation properties

                    # entity type of navigation property

                    # cache value according to multiplicity

                        # cache None in case we receive nothing (null) instead of entity data

                        # default value is empty array

                        # if there are no entities available, received data consists of
                        # metadata properties only.

                            # available entities are serialized in results array

        # build entity key if not provided
            # try to build key from available property values

                # if key seems to be simple (consists of single property)

                    # build complex key
        pass

    def __repr__(self):
        pass

    def __getattr__(self, attr):
        pass

    async def async_getattr(self, attr):
        """Get cached value of attribute or do async call to service to recover attribute value"""
        pass

    def nav(self, nav_property):
        """Navigates to given navigation property and returns the EntitySetProxy"""

        # for now duplicated with simillar method in entity set proxy class

        # Get entity set of navigation property
        pass

    def _get_nav_entity(self, nav_property, navigation_entity_set):
        """Get entity based on Navigation property name"""

        def get_entity_handler(parent, nav_property, navigation_entity_set, response):
            """Gets entity from HTTP response"""

            pass

        pass

    def get_path(self):
        """Returns this entity's relative path - e.g. EntitySet(KEY)"""
        pass

    def get_proprty(self, name, connection=None):
        """Returns value of the property"""

        def proprty_get_handler(key, proprty, response):
            """Gets property value from HTTP Response"""

            pass

        pass

    def get_value(self, connection=None):
        "Returns $value of Stream entities"

        def value_get_handler(key, response):
            """Gets property value from HTTP Response"""

            pass

        pass

    @property
    def entity_set(self):
        """Entity set related to this entity"""
        pass

    @property
    def entity_key(self):
        """Key of entity"""
        pass

    @property
    def url(self):
        """URL of the real entity"""
        pass

    @property
    def etag(self):
        """ETag generated by service"""
        pass

    def equals(self, other):
        """Returns true if the self and the other contains the same data"""
        pass


class NavEntityProxy(EntityProxy):
    """Special case of an Entity access via 1 to 1 Navigation property"""

    def __init__(self, parent_entity, prop_name, entity_type, entity):
        pass

    def get_path(self):
        """Returns URL of the entity"""
        pass


class GetEntitySetFilter:
    """Create filters for humans"""

    def __init__(self, proprty):
        pass

    @staticmethod
    def build_expression(operator, operands):
        """Creates a expression by joining the operands with the operator"""
        pass

    @staticmethod
    def and_(*operands):
        """Creates logical AND expression from the operands"""
        pass

    @staticmethod
    def or_(*operands):
        """Creates logical OR expression from the operands"""
        pass

    @staticmethod
    def format_filter(proprty, operator, value):
        """Creates a filter expression """
        pass

    def __eq__(self, value):
        pass

    def __ne__(self, value):
        pass

    def __lt__(self, value):
        pass

    def __le__(self, value):
        pass

    def __ge__(self, value):
        pass

    def __gt__(self, value):
        pass


class FilterExpression:
    """A class representing named expression of OData $filter"""

    def __init__(self, **kwargs):
        pass

    @property
    def expressions(self):
        """Get expressions where key is property name with the operator suffix
           and value is the left hand side operand.
        """
        pass

    @property
    def other(self):
        """Get an instance of the other operand"""
        pass

    @property
    def operator(self):
        pass

    def __or__(self, other):
        pass

    def __and__(self, other):
        pass


class GetEntitySetFilterChainable:
    """
    Example expressions
        FirstName='Tim'
        FirstName__contains='Tim'
        Age__gt=56
        Age__gte=6
        Age__lt=78
        Age__lte=90
        Age__range=(5,9)
        FirstName__in=['Tim', 'Bob', 'Sam']
        FirstName__startswith='Tim'
        FirstName__endswith='mothy'
        Addresses__Suburb='Chatswood'
        Addresses__Suburb__contains='wood'
    """

    OPERATORS = [
        'startswith',
        'endswith',
        'lt',
        'lte',
        'gt',
        'gte',
        'contains',
        'range',
        'in',
        'length',
        'eq'
    ]

    def __init__(self, entity_type, filter_expressions, exprs):
        pass

    @property
    def expressions(self):
        """Get expressions as a list of tuples where the first item
           is a property name with the operator suffix and the second item
           is a left hand side value.
        """
        pass

    def proprty_obj(self, name):
        """Returns a model property for a particular property"""
        pass

    def _decode_and_combine_filter_expression(self, filter_expression):
        pass

    def _process_query_objects(self):
        """Processes FilterExpression objects to OData lookups"""
        pass

    def _process_expressions(self):
        pass

    def _decode_expression(self, expr, val):
        pass

    def _combine_expressions(self, expressions):
        pass

    def _build_expression(self, field_name, operator, value):
        pass

    def __str__(self):
        pass


class GetEntitySetRequest(QueryRequest):
    """GET on EntitySet"""

    def __init__(self, url, connection, handler, last_segment, entity_type):
        pass

    def __getattr__(self, name):
        pass

    def _set_filter(self, filter_val):
        pass

    def filter(self, *args, **kwargs):
        pass


class ListWithTotalCount(list):
    """
    A list with the additional property total_count and next_url.

    If set, use next_url to fetch the next batch of entities.
    """
    def __init__(self, total_count, next_url):
        pass

    @property
    def next_url(self):
        """
        URL which identifies the next partial set of entities from the originally identified complete set. None if no
        entities remaining.
        """
        pass

    @property
    def total_count(self):
        """Count of all entities"""
        if self._total_count is None:
            pass


class EntitySetProxy:
    """EntitySet Proxy"""

    def __init__(self, service, entity_set, alias=None, parent_last_segment=None):
        """Creates new Entity Set object

            @param alias  in case the entity set is access via assossiation
            @param parent_last_segment  in case of association also parent key must be used
        """
        pass

    @property
    def service(self):
        """Return service"""
        pass

    @property
    def last_segment(self):
        """Return last segment of url"""
        pass

    def nav(self, nav_property, key):
        """Navigates to given navigation property and returns the EntitySetProxy"""
        pass

    def _get_nav_entity(self, master_key, nav_property, navigation_entity_set):
        """Get entity based on provided key of the master and Navigation property name"""

        def get_entity_handler(parent, nav_property, navigation_entity_set, response):
            """Gets entity from HTTP response"""

            pass

        pass

    def get_entity(self, key=None, **args):
        """Get entity based on provided key properties"""

        def get_entity_handler(response):
            """Gets entity from HTTP response"""

            pass

        pass

    def get_entities(self):
        """Get some, potentially all entities"""

        def get_entities_handler(response):
            """Gets entity set from HTTP Response"""

            pass

        pass

    def create_entity(self, return_code=HTTP_CODE_CREATED):
        """Creates a new entity in the given entity-set."""

        def create_entity_handler(response):
            """Gets newly created entity encoded in HTTP Response"""

            pass

        pass

    def update_entity(self, key=None, method=None, **kwargs):
        """Updates an existing entity in the given entity-set."""

        def update_entity_handler(response):
            """Gets modified entity encoded in HTTP Response"""

            pass

        pass

    def delete_entity(self, key: EntityKey = None, **kwargs):
        """Delete the entity"""

        def delete_entity_handler(response):
            """Check if entity deletion was successful"""

            pass

        pass


# pylint: disable=too-few-public-methods
class EntityContainer:
    """Set of EntitSet proxies"""

    def __init__(self, service):
        pass

    def __getattr__(self, name):
        pass


class FunctionContainer:
    """Set of Function proxies

       Call a server-side functions (also known as a service operation).
    """

    def __init__(self, service):
        pass

    def __getattr__(self, name):
        def function_import_handler(fimport, response):
            """Get function call response from HTTP Response"""

            pass

        pass


class Service:
    """OData service"""

    def __init__(self, url, schema, connection, config=None):
        pass

    @property
    def schema(self):
        """Parsed metadata"""
        pass

    @property
    def url(self):
        """Service url"""
        pass

    @property
    def connection(self):
        """Service connection"""
        pass

    @property
    def retain_null(self):
        """Whether to respect null-ed values or to substitute them with type specific default values"""
        pass

    @property
    def entity_sets(self):
        """EntitySet proxy"""
        pass

    @property
    def functions(self):
        """Functions proxy"""
        pass

    @property
    def config(self):
        """Service specific configuration"""
        pass

    def http_get(self, path, connection=None):
        """HTTP GET response for the passed path in the service"""
        pass

    async def async_http_get(self, path, connection=None):
        """HTTP GET response for the passed path in the service"""
        pass

    def http_get_odata(self, path, handler, connection=None):
        """HTTP GET request proxy for the passed path in the service"""
        pass

    def create_batch(self, batch_id=None):
        """Create instance of OData batch request"""

        def batch_handler(batch, parts):
            """Process parsed multipart request (parts)"""
            pass

        pass

    def create_changeset(self, changeset_id=None):
        """Create instance of OData changeset"""

        def changeset_handler(changeset, parts):
            """Gets changeset response from HTTP response"""

            # check if changeset response consists of parts, this is important
            # to distinguish cases when server responds with single HTTP response
            # for whole request

                # raise error (even for successfull status codes) since such changeset response
                # always means something wrong happened on server


                # part represents single request, we have to parse
                # content (without checking Content type for binary/http)

            pass

        return Changeset(self._url, self._connection, changeset_handler, changeset_id)


class MultipartRequest(ODataHttpRequest):
    """HTTP Batch request"""

    def __init__(self, url, connection, handler, request_id=None):
        pass

    @property
    def handler(self):
        pass

    def get_boundary(self):
        pass

    def get_default_headers(self):
        pass

    def get_body(self):
        pass

    def add_request(self, request):
        """Add request to be sent in batch"""
        pass

    @staticmethod
    def http_response_handler(request, response):
        """Process HTTP response to multipart HTTP request"""
        pass


class BatchRequest(MultipartRequest):
    """HTTP Batch request"""
    def get_boundary(self):
        pass

    def get_path(self):
        pass

    def get_method(self):
        pass


class Changeset(MultipartRequest):
    """Representation of changeset (unsorted group of requests)"""

    def get_boundary(self):
        pass
