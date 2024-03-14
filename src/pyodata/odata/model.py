"""
Simple representation of Metadata of OData V2

Author: Jakub Filak <jakub.filak@sap.com>
Date:   2017-08-21
"""
# pylint: disable=missing-docstring,too-many-instance-attributes,too-many-arguments,protected-access,no-member,line-too-long,logging-format-interpolation,too-few-public-methods,too-many-lines, too-many-public-methods

import base64
import collections
import datetime
from enum import Enum, auto
import io
import itertools
import logging
import re
import warnings
from abc import ABC, abstractmethod

from lxml import etree

from pyodata.exceptions import PyODataException, PyODataModelError, PyODataParserError

LOGGER_NAME = 'pyodata.model'
FIX_SCREWED_UP_MINIMAL_DATETIME_VALUE = False
FIX_SCREWED_UP_MAXIMUM_DATETIME_VALUE = False


IdentifierInfo = collections.namedtuple('IdentifierInfo', 'namespace name')
TypeInfo = collections.namedtuple('TypeInfo', 'namespace name is_collection')
# What for?

def modlog():
    pass


class NullAssociation:
    def __init__(self, name):
        pass

    def __getattr__(self, item):
        pass

class NullType:
    def __init__(self, name):
        pass

    def __getattr__(self, item):
        pass


class ErrorPolicy(ABC):
    @abstractmethod
    def resolve(self, ekseption):
        pass


class PolicyFatal(ErrorPolicy):
    def resolve(self, ekseption):
        pass


class PolicyWarning(ErrorPolicy):
    def __init__(self):
        pass

    def resolve(self, ekseption):
        pass


class PolicyIgnore(ErrorPolicy):
    def resolve(self, ekseption):
        pass


class ParserError(Enum):
    PROPERTY = auto()
    ANNOTATION = auto()
    ASSOCIATION = auto()

    ENUM_TYPE = auto()
    ENTITY_TYPE = auto()
    COMPLEX_TYPE = auto()


class Config:

    def __init__(self,
                 custom_error_policies=None,
                 default_error_policy=None,
                 xml_namespaces=None,
                 retain_null=False):

        """
        :param custom_error_policies: {ParserError: ErrorPolicy} (default None)
                                      Used to specified individual policies for XML tags. See documentation for more
                                      details.

        :param default_error_policy: ErrorPolicy (default PolicyFatal)
                                     If custom policy is not specified for the tag, the default policy will be used.

        :param xml_namespaces: {str: str} (default None)

        :param retain_null: bool (default False)
                            If true, do not substitute missing (and null-able) values with default value.
        """

        pass

    def err_policy(self, error: ParserError):
        pass

    def set_default_error_policy(self, policy: ErrorPolicy):
        pass

    def set_custom_error_policy(self, policies: dict):
        pass

    @property
    def namespaces(self):
        pass

    @namespaces.setter
    def namespaces(self, value: dict):
        pass

    @property
    def retain_null(self):
        pass


class Identifier:
    def __init__(self, name):
        pass

    def __repr__(self):
        pass

    def __str__(self):
        pass

    @property
    def name(self):
        pass

    @staticmethod
    def parse(value):
        pass


class Types:
    """Repository of all available OData V2 primitive types + their Collection variants

       Since each type has instance of appropriate type, this
       repository acts as central storage for all instances. The
       rule is: don't create any type instances if not necessary,
       always reuse existing instances if possible
    """

    Types = None

    @staticmethod
    def _build_types():
        pass

    @staticmethod
    def register_type(typ):
        pass

    @staticmethod
    def from_name(name):
        pass

    @staticmethod
    def parse_type_name(type_name):
        pass


class EdmStructTypeSerializer:
    """Basic implementation of (de)serialization for Edm complex types

       All properties existing in related Edm type are taken
       into account, others are ignored

       TODO: it can happen that inifinite recurision occurs for cases
       when property types are referencich each other. We need some research
       here to avoid such cases.
    """

    @staticmethod
    def to_literal(edm_type, value):
        pass

    @staticmethod
    def from_json(edm_type, value):
        pass

    @staticmethod
    def from_literal(edm_type, value):
        pass


class TypTraits:
    """Encapsulated differences between types"""

    def __repr__(self):
        return self.__class__.__name__

    # pylint: disable=no-self-use
    def to_literal(self, value):
        return value

    # pylint: disable=no-self-use
    def from_json(self, value):
        return value

    def to_json(self, value):
        return value

    def from_literal(self, value):
        return value


class EdmPrefixedTypTraits(TypTraits):
    """Is good for all types where values have form: prefix'value'"""

    def __init__(self, prefix):
        pass

    def to_literal(self, value):
        pass

    def from_literal(self, value):
        pass


class EdmBinaryTypTraits(EdmPrefixedTypTraits):
    """Edm.Binary traits"""

    def to_literal(self, value):
        pass

    def from_literal(self, value):
        pass


def ms_since_epoch_to_datetime(value, tzinfo):
    """Convert milliseconds since midnight 1.1.1970 to datetime"""
    pass


class EdmDateTimeTypTraits(EdmPrefixedTypTraits):
    """Edm.DateTime traits

       Represents date and time with values ranging from 12:00:00 midnight,
       January 1, 1753 A.D. through 11:59:59 P.M, December 9999 A.D.

       Literal form:
       datetime'yyyy-mm-ddThh:mm[:ss[.fffffff]]'
       NOTE: Spaces are not allowed between datetime and quoted portion.
       datetime is case-insensitive

       Example 1: datetime'2000-12-12T12:00'
       JSON has following format: /Date(1516614510000)/
       https://blogs.sap.com/2017/01/05/date-and-time-in-sap-gateway-foundation/
    """

    def __init__(self):
        pass

    def to_literal(self, value):
        """Convert python datetime representation to literal format

           None: this could be done also via formatting string:
           value.strftime('%Y-%m-%dT%H:%M:%S.%f')
        """

        pass

    def to_json(self, value):
        pass

    def from_json(self, value):
        pass

    def from_literal(self, value):
        pass


class EdmDateTimeOffsetTypTraits(EdmPrefixedTypTraits):
    """Edm.DateTimeOffset traits

       Represents date and time, plus an offset in minutes from UTC, with values ranging from 12:00:00 midnight,
       January 1, 1753 A.D. through 11:59:59 P.M, December 9999 A.D

       Literal forms:
       datetimeoffset'yyyy-mm-ddThh:mm[:ss]±ii:nn' (works for all time zones)
       datetimeoffset'yyyy-mm-ddThh:mm[:ss]Z' (works only for UTC)
       NOTE: Spaces are not allowed between datetimeoffset and quoted portion.
       The datetime part is case-insensitive, the offset one is not.

       Example 1: datetimeoffset'1970-01-01T00:00:01+00:30'
        - /Date(1000+0030)/ (As DateTime, but with a 30 minutes timezone offset)
       Example 1: datetimeoffset'1970-01-01T00:00:01-00:60'
        - /Date(1000-0030)/ (As DateTime, but with a negative 60 minutes timezone offset)
       https://blogs.sap.com/2017/01/05/date-and-time-in-sap-gateway-foundation/
    """

    def __init__(self):
        pass

    def to_literal(self, value):
        pass

    def to_json(self, value):
        pass

    def from_json(self, value):
        pass

    def from_literal(self, value):
        pass


class EdmStringTypTraits(TypTraits):
    """Edm.String traits"""

    # pylint: disable=no-self-use
    def to_literal(self, value):
        pass

    # pylint: disable=no-self-use
    def from_json(self, value):
        pass

    def from_literal(self, value):
        pass


class EdmBooleanTypTraits(TypTraits):
    """Edm.Boolean traits"""

    # pylint: disable=no-self-use
    def to_literal(self, value):
        pass

    # pylint: disable=no-self-use
    def from_json(self, value):
        pass

    def from_literal(self, value):
        pass


class EdmIntTypTraits(TypTraits):
    """All Edm Integer traits"""

    # pylint: disable=no-self-use
    def to_literal(self, value):
        pass

    # pylint: disable=no-self-use
    def from_json(self, value):
        pass

    def from_literal(self, value):
        pass


class EdmLongIntTypTraits(TypTraits):
    """All Edm Integer for big numbers traits"""

    # pylint: disable=no-self-use
    def to_literal(self, value):
        pass

    # pylint: disable=no-self-use
    def from_json(self, value):
        pass

    def from_literal(self, value):
        pass


class EdmFPNumTypTraits(TypTraits):
    """Edm Floating Point Number traits"""

    def __init__(self, precision, suffix, conversion):
        pass

    def __repr__(self):
        pass

    @staticmethod
    def edm_float():
        pass

    @staticmethod
    def edm_double():
        pass

    @staticmethod
    def edm_single():
        pass

    # pylint: disable=no-self-use
    def to_literal(self, value):
        pass

    def to_json(self, value):
        pass

    # pylint: disable=no-self-use
    def from_json(self, value):
        pass

    def from_literal(self, value):
        pass


class EdmStructTypTraits(TypTraits):
    """Edm structural types (EntityType, ComplexType) traits"""

    def __init__(self, edm_type=None):
        pass

    # pylint: disable=no-self-use
    def to_literal(self, value):
        pass

    # pylint: disable=no-self-use
    def from_json(self, value):
        pass

    def from_literal(self, value):
        pass


class EnumTypTrait(TypTraits):
    def __init__(self, enum_type):
        pass

    def to_literal(self, value):
        pass

    def from_json(self, value):
        pass

    def from_literal(self, value):
        pass


class Typ(Identifier):
    Types = None

    Kinds = Enum('Kinds', 'Primitive Complex')

    def __init__(self, name, null_value, traits=TypTraits(), kind=None):
        pass

    @property
    def null_value(self):
        pass

    @property
    def traits(self):
        pass

    @property
    def is_collection(self):
        pass

    @property
    def kind(self):
        pass


class Collection(Typ):
    """Represents collection items"""

    def __init__(self, name, item_type):
        pass

    def __repr__(self):
        pass

    @property
    def is_collection(self):
        return True

    @property
    def item_type(self):
        return self._item_type

    @property
    def traits(self):
        return self

    # pylint: disable=no-self-use
    def to_literal(self, value):
        pass

    # pylint: disable=no-self-use
    def from_json(self, value):
        pass


class VariableDeclaration(Identifier):
    MAXIMUM_LENGTH = -1

    def __init__(self, name, type_info, nullable, max_length, precision, scale, fixed_length=None):
        pass

    @property
    def type_info(self):
        pass

    @property
    def typ(self):
        pass

    @typ.setter
    def typ(self, value):
        pass

    @property
    def nullable(self):
        pass

    @property
    def max_length(self):
        pass

    @property
    def precision(self):
        pass

    @property
    def scale(self):
        pass

    @property
    def fixed_length(self):
        pass

    def from_literal(self, value):
        pass

    def to_literal(self, value):
        pass

    def from_json(self, value):
        pass

    def to_json(self, value):
        pass

    def _check_scale_value(self):
        pass


class Schema:
    class Declaration:
        def __init__(self, namespace):
            # generated collections for ease of lookup (e.g. function import return type)
            self._collections_entity_types = dict()
            self._collections_complex_types = dict()

        def list_entity_types(self):
            pass

        def list_complex_types(self):
            pass

        def list_enum_types(self):
            pass

        def list_entity_sets(self):
            pass

        def list_function_imports(self):
            pass

        def list_associations(self):
            pass

        def list_association_sets(self):
            pass

        def add_entity_type(self, etype):
            pass

        def add_complex_type(self, ctype):
            pass

        def add_enum_type(self, etype):
            pass

    class Declarations(dict):

        def __getitem__(self, key):
            pass

    def __init__(self, config: Config):
        pass

    def __str__(self):
        pass

    @property
    def namespaces(self):
        pass

    @property
    def config(self):
        pass

    @property
    def is_valid(self):
        """Returns if metadata provided were parsed to schema without any problem regardless of Policies (Fatal, Warning, Ignore).

        Policies affects behaviour o parser while this property represents status.
        """
        return self._is_valid

    def typ(self, type_name, namespace=None):
        """Returns either EntityType, ComplexType or EnumType that matches the name.
        """
        pass


    def entity_type(self, type_name, namespace=None):
        pass

    def _collections_entity_types(self, type_name, namespace=None):
        pass

    def complex_type(self, type_name, namespace=None):
        pass

    def _collections_complex_types(self, type_name, namespace=None):
        pass

    def enum_type(self, type_name, namespace=None):
        pass

    def get_type(self, type_info):
        pass

    @property
    def entity_types(self):
        pass

    @property
    def complex_types(self):
        pass

    @property
    def enum_types(self):
        pass

    def entity_set(self, set_name, namespace=None):
        pass

    @property
    def entity_sets(self):
        pass

    def function_import(self, function_import, namespace=None):
        pass

    @property
    def function_imports(self):
        pass

    def association(self, association_name, namespace=None):
        pass

    @property
    def associations(self):
        pass

    def association_set_by_association(self, association_name, namespace=None):
        pass

    def association_set(self, set_name, namespace=None):
        pass

    @property
    def association_sets(self):
        pass

    def check_role_property_names(self, role, entity_type_name, namespace):
        pass

    # pylint: disable=too-many-locals,too-many-branches,too-many-statements
    @staticmethod
    def from_etree(schema_nodes, config: Config):
        # Parse Schema nodes by parts to get over the problem of not-yet known
        # entity types referenced by entity sets, function imports and
        # annotations.

        # First, process EnumType, EntityType and ComplexType nodes. They have almost no dependencies on other elements.

        # resolve types of properties

            # skip collections (no need to assign any types since type of collection
            # items is resolved separately

        # Then, process Associations nodes because they refer EntityTypes and
        # they are referenced by AssociationSets.

            # Check if the role was defined in the current association
            # Check if principal role properties exist
            # Check if the role was defined in the current association
            # Check if dependent role properties exist

        # resolve navigation properties
            # skip null type
            # skip collections

        # Then, process EntitySet, FunctionImport and AssociationSet nodes.
            # complete type information for return type and parameters

            # Check if an entity set exists in the current scheme
            # and add a reference to the corresponding entity set

            # Check if role is defined in Association

        # Finally, process Annotation nodes when all Scheme nodes are completely processed.
        pass


class StructType(Typ):
    def __init__(self, name, label, is_value_list):
        super(StructType, self).__init__(name, None, EdmStructTypTraits(self), Typ.Kinds.Complex)
        #
        pass

    @property
    def label(self):
        pass

    @property
    def is_value_list(self):
        pass

    def proprty(self, property_name):
        pass

    def proprties(self):
        pass

    def has_proprty(self, proprty_name):
        pass

    @classmethod
    def from_etree(cls, type_node, config: Config):
        pass
    # implementation of Typ interface

    @property
    def is_collection(self):
        pass

    @property
    def kind(self):
        pass

    @property
    def null_value(self):
        pass

    @property
    def traits(self):
        pass

class ComplexType(StructType):
    """Representation of Edm.ComplexType"""


class EnumMember:
    def __init__(self, parent, name, value):
        self._parent = parent
        self._name = name
        self._value = value

    def __str__(self):
        pass

    @property
    def name(self):
        pass

    @property
    def value(self):
        pass

    @property
    def parent(self):
        pass


class EnumType(Identifier):
    def __init__(self, name, is_flags, underlying_type, namespace):
        pass

    def __str__(self):
        pass

    def __getattr__(self, item):
        pass

    def __getitem__(self, item):
        pass

    # pylint: disable=too-many-locals
    @staticmethod
    def from_etree(type_node, namespace, config: Config):
        pass

    @property
    def is_flags(self):
        pass

    @property
    def traits(self):
        pass

    @property
    def namespace(self):
        pass


class EntityType(StructType):
    def __init__(self, name, label, is_value_list):
        pass

    @property
    def key_proprties(self):
        pass

    @property
    def nav_proprties(self):
        pass

    def nav_proprty(self, property_name):
        pass

    @classmethod
    def from_etree(cls, type_node, config: Config):
        pass


class EntitySet(Identifier):
    def __init__(self, name, entity_type_info, addressable, creatable, updatable, deletable, searchable, countable,
                 pageable, topable, req_filter, label):
        pass

    @property
    def entity_type_info(self):
        pass

    @property
    def entity_type(self):
        pass

    @entity_type.setter
    def entity_type(self, value):
        pass

    @property
    def addressable(self):
        pass

    @property
    def creatable(self):
        pass

    @property
    def updatable(self):
        pass

    @property
    def deletable(self):
        pass

    @property
    def searchable(self):
        pass

    @property
    def countable(self):
        pass

    @property
    def pageable(self):
        pass

    @property
    def topable(self):
        pass

    @property
    def requires_filter(self):
        pass

    @property
    def label(self):
        pass

    @staticmethod
    def from_etree(entity_set_node):
        pass

class StructTypeProperty(VariableDeclaration):

    # pylint: disable=too-many-locals
    def __init__(self, name, type_info, nullable, max_length, precision, scale, uncode, label, creatable, updatable,
                 sortable, filterable, filter_restr, req_in_filter, text, visible, display_format, value_list,
                 fixed_length=None):
        pass


    @property
    def struct_type(self):
        pass

    @struct_type.setter
    def struct_type(self, value):
        pass

    @property
    def text_proprty_name(self):
        pass

    @property
    def text_proprty(self):
        pass

    @property
    def uncode(self):
        pass

    @property
    def label(self):
        pass

    @property
    def creatable(self):
        pass

    @property
    def updatable(self):
        pass

    @property
    def sortable(self):
        pass

    @property
    def filterable(self):
        pass

    @property
    def filter_restriction(self):
        pass

    @property
    def required_in_filter(self):
        pass

    @property
    def visible(self):
        pass

    @property
    def upper_case(self):
        pass

    @property
    def date(self):
        pass

    @property
    def non_negative(self):
        pass

    @property
    def value_helper(self):
        pass

    @property
    def value_list(self):
        pass

    @value_helper.setter
    def value_helper(self, value):
        pass

    @staticmethod
    def from_etree(entity_type_property_node):

        return StructTypeProperty(
            entity_type_property_node.get('Name'),
            Types.parse_type_name(entity_type_property_node.get('Type')),
            attribute_get_bool(entity_type_property_node, 'Nullable', True),
            entity_type_property_node.get('MaxLength'),
            entity_type_property_node.get('Precision'),
            entity_type_property_node.get('Scale'),
            # TODO: create a class SAP attributes
            sap_attribute_get_bool(entity_type_property_node, 'unicode', True),
            sap_attribute_get_string(entity_type_property_node, 'label'),
            sap_attribute_get_bool(entity_type_property_node, 'creatable', True),
            sap_attribute_get_bool(entity_type_property_node, 'updatable', True),
            sap_attribute_get_bool(entity_type_property_node, 'sortable', True),
            sap_attribute_get_bool(entity_type_property_node, 'filterable', True),
            sap_attribute_get_string(entity_type_property_node, 'filter-restriction'),
            sap_attribute_get_bool(entity_type_property_node, 'required-in-filter', False),
            sap_attribute_get_string(entity_type_property_node, 'text'),
            sap_attribute_get_bool(entity_type_property_node, 'visible', True),
            sap_attribute_get_string(entity_type_property_node, 'display-format'),
            sap_attribute_get_string(entity_type_property_node, 'value-list'),
            # Back to regular, non-SAP attributes.
            attribute_get_bool(entity_type_property_node, 'FixedLength', False),
        )


class NavigationTypeProperty(VariableDeclaration):
    """Defines a navigation property, which provides a reference to the other end of an association

       Unlike properties defined with the Property element, navigation properties do not define the
       shape and characteristics of data. They provide a way to navigate an association between two
       entity types.

       Note that navigation properties are optional on both entity types at the ends of an association.
       If you define a navigation property on one entity type at the end of an association, you do not
       have to define a navigation property on the entity type at the other end of the association.

       The data type returned by a navigation property is determined by the multiplicity of its remote
       association end. For example, suppose a navigation property, OrdersNavProp, exists on a Customer
       entity type and navigates a one-to-many association between Customer and Order. Because the
       remote association end for the navigation property has multiplicity many (*), its data type is
       a collection (of Order). Similarly, if a navigation property, CustomerNavProp, exists on the Order
       entity type, its data type would be Customer since the multiplicity of the remote end is one (1).
    """

    def __init__(self, name, from_role_name, to_role_name, association_info):
        pass

    @property
    def association_info(self):
        pass

    @property
    def association(self):
        return self._association

    @association.setter
    def association(self, value):
        pass

    @property
    def to_role(self):
        pass

    @property
    def typ(self):
        pass

    @staticmethod
    def from_etree(node):
        pass


class EndRole:
    MULTIPLICITY_ONE = '1'
    MULTIPLICITY_ZERO_OR_ONE = '0..1'
    MULTIPLICITY_ZERO_OR_MORE = '*'

    def __init__(self, entity_type_info, multiplicity, role):
        pass

    def __repr__(self):
        pass

    @property
    def entity_type_info(self):
        pass

    @property
    def entity_type_name(self):
        pass

    @property
    def entity_type(self):
        pass

    @entity_type.setter
    def entity_type(self, value):
        pass

    @property
    def multiplicity(self):
        pass

    @property
    def role(self):
        pass

    @staticmethod
    def from_etree(end_role_node):
        pass


class ReferentialConstraintRole:
    def __init__(self, name, property_names):
        pass

    @property
    def name(self):
        pass

    @property
    def property_names(self):
        pass


class PrincipalRole(ReferentialConstraintRole):
    pass


class DependentRole(ReferentialConstraintRole):
    pass


class ReferentialConstraint:
    def __init__(self, principal, dependent):
        pass

    @property
    def principal(self):
        pass

    @property
    def dependent(self):
        pass

    @staticmethod
    def from_etree(referential_constraint_node, config: Config):
        pass

class Association:
    """Defines a relationship between two entity types.

       An association must specify the entity types that are involved in
       the relationship and the possible number of entity types at each
       end of the relationship, which is known as the multiplicity.
       The multiplicity of an association end can have a value of one (1),
       zero or one (0..1), or many (*). This information is specified in
       two child End elements.
    """

    def __init__(self, name):
        pass

    def __str__(self):
        pass

    @property
    def name(self):
        pass

    @property
    def end_roles(self):
        pass

    def end_by_role(self, end_role):
        pass

    @property
    def referential_constraint(self):
        pass

    @staticmethod
    def from_etree(association_node, config: Config):
        pass

class AssociationSetEndRole:
    def __init__(self, role, entity_set_name):
        pass

    def __repr__(self):
        pass

    @property
    def role(self):
        pass

    @property
    def entity_set_name(self):
        pass

    @property
    def entity_set(self):
        pass

    @entity_set.setter
    def entity_set(self, value):
        pass

    @staticmethod
    def from_etree(end_node):
        pass


class AssociationSet:
    def __init__(self, name, association_type_name, association_type_namespace, end_roles):
        pass

    def __str__(self):
        pass

    @property
    def name(self):
        pass

    @property
    def association_type(self):
        pass

    @property
    def association_type_name(self):
        pass

    @property
    def association_type_namespace(self):
        pass

    @property
    def end_roles(self):
        pass

    def end_by_role(self, end_role):
        pass

    def end_by_entity_set(self, entity_set):
        pass

    @association_type.setter
    def association_type(self, value):
        pass

    @staticmethod
    def from_etree(association_set_node, config: Config):
        pass


class Annotation:
    Kinds = Enum('Kinds', 'ValueHelper')

    def __init__(self, kind, target, qualifier=None):
        pass

    def __str__(self):
        pass

    @property
    def element_namespace(self):
        pass

    @property
    def element(self):
        pass

    @property
    def target(self):
        pass

    @property
    def kind(self):
        pass

    @staticmethod
    def from_etree(target, annotation_node):
        pass

class ExternalAnnontation:
    @staticmethod
    def from_etree(annotations_node):
        pass


class ValueHelper(Annotation):
    def __init__(self, target, collection_path, label, search_supported):

        # pylint: disable=unused-argument

        super(ValueHelper, self).__init__(Annotation.Kinds.ValueHelper, target)

        pass

    def __str__(self):
        pass

    @property
    def proprty_name(self):
        pass

    @property
    def proprty_entity_type_name(self):
        pass

    @property
    def proprty(self):
        pass

    @proprty.setter
    def proprty(self, value):
        pass

    @property
    def collection_path(self):
        pass

    @property
    def entity_set(self):
        pass

    @entity_set.setter
    def entity_set(self, value):
        pass

    @property
    def label(self):
        pass

    @property
    def parameters(self):
        pass

    def local_property_param(self, name):
        pass

    def list_property_param(self, name):
        pass

    @staticmethod
    def from_etree(target, annotation_node):
        pass


class ValueHelperParameter:
    Direction = Enum('Direction', 'In InOut Out DisplayOnly FilterOnly')

    def __init__(self, direction, local_property_name, list_property_name):
        pass

    def __str__(self):
        pass

    @property
    def value_helper(self):
        pass

    @value_helper.setter
    def value_helper(self, value):
        pass

    @property
    def direction(self):
        pass

    @property
    def local_property_name(self):
        pass

    @property
    def local_property(self):
        pass

    @local_property.setter
    def local_property(self, value):
        pass

    @property
    def list_property_name(self):
        pass

    @property
    def list_property(self):
        pass

    @list_property.setter
    def list_property(self, value):
        pass

    @staticmethod
    def from_etree(value_help_parameter_node):
        pass


class FunctionImport(Identifier):
    def __init__(self, name, return_type_info, entity_set, parameters, http_method='GET'):
        pass

    @property
    def return_type_info(self):
        pass

    @property
    def return_type(self):
        pass

    @return_type.setter
    def return_type(self, value):
        pass

    @property
    def entity_set_name(self):
        pass

    @property
    def parameters(self):
        pass

    def get_parameter(self, parameter):
        pass

    @property
    def http_method(self):
        pass

    # pylint: disable=too-many-locals
    @staticmethod
    def from_etree(function_import_node, config: Config):
        pass



class FunctionImportParameter(VariableDeclaration):
    Modes = Enum('Modes', 'In Out InOut')

    def __init__(self, name, type_info, nullable, max_length, precision, scale, mode):
        pass

    @property
    def mode(self):
        pass


def sap_attribute_get(node, attr):
    pass


def metadata_attribute_get(node, attr):
    pass


def sap_attribute_get_string(node, attr):
    pass


def str_to_bool(value, attr, default):
    pass


def attribute_get_bool(node, attr, default):
    pass


def sap_attribute_get_bool(node, attr, default):
    pass


ANNOTATION_NAMESPACES = {
    'edm': 'http://docs.oasis-open.org/odata/ns/edm',
    'edmx': 'http://docs.oasis-open.org/odata/ns/edmx'
}

SAP_VALUE_HELPER_DIRECTIONS = {
    'com.sap.vocabularies.Common.v1.ValueListParameterIn': ValueHelperParameter.Direction.In,
    'com.sap.vocabularies.Common.v1.ValueListParameterInOut': ValueHelperParameter.Direction.InOut,
    'com.sap.vocabularies.Common.v1.ValueListParameterOut': ValueHelperParameter.Direction.Out,
    'com.sap.vocabularies.Common.v1.ValueListParameterDisplayOnly': ValueHelperParameter.Direction.DisplayOnly,
    'com.sap.vocabularies.Common.v1.ValueListParameterFilterOnly': ValueHelperParameter.Direction.FilterOnly
}


SAP_ANNOTATION_VALUE_LIST = ['com.sap.vocabularies.Common.v1.ValueList']


class MetadataBuilder:
    EDMX_WHITELIST = [
        'http://schemas.microsoft.com/ado/2007/06/edmx',
        'http://docs.oasis-open.org/odata/ns/edmx',
    ]

    EDM_WHITELIST = [
        'http://schemas.microsoft.com/ado/2006/04/edm',
        'http://schemas.microsoft.com/ado/2007/05/edm',
        'http://schemas.microsoft.com/ado/2008/09/edm',
        'http://schemas.microsoft.com/ado/2009/11/edm',
        'http://docs.oasis-open.org/odata/ns/edm'
    ]

    def __init__(self, xml, config=None):
        pass

    @property
    def config(self):
        pass


    def build(self):
        """ Build model from the XML metadata"""

        # parse the input as XML

        # DataServices element

        # Schema element

        # edmx and edm Namespaces

        # parse the schema from etree Schema.from_etree()

        #return parsed schema

    @staticmethod
    def get_aliases(edmx, config: Config):
        """Get all aliases"""

        # Namespace / Alias

        pass

    @staticmethod
    def update_global_variables_with_alias(aliases):
        """Update global variables with aliases"""



def schema_from_xml(metadata_xml, namespaces=None):
    """Parses XML data and returns Schema representing OData Metadata"""

    meta = MetadataBuilder(
        metadata_xml,
        config=Config(
            xml_namespaces=namespaces,
        ))

    return meta.build()

# TODO Delete, deprecated from 1.02
class Edmx:
    @staticmethod
    def parse(metadata_xml, namespaces=None):
        warnings.warn("Edmx class is deprecated in favor of MetadataBuilder", DeprecationWarning)
        return schema_from_xml(metadata_xml, namespaces)
