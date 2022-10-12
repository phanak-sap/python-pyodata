"""
    Test of simple valid v4 metadata.

    Specification copy:



    """


# pylint: disable=line-too-long,too-many-locals,too-many-statements,invalid-name, too-many-lines, no-name-in-module, expression-not-assigned, pointless-statement

import pytest
import logging
import os


from pyodata.v4.model import schema_from_xml
from pyodata.exceptions import PyODataParserError

def content_of_metadata_file(file_name):
    path_to_current_file = os.path.realpath(__file__)
    current_directory = os.path.split(path_to_current_file)[0]
    path_to_file = os.path.join(current_directory, file_name)

    with open(path_to_file, 'rb') as md_file:
        return md_file.read()

    #TODO refactor to pathlib


def test_edmx_valid_xml():
    """Test Edmx class"""
    schema = schema_from_xml(content_of_metadata_file("metadata_simple.xml"))
    assert schema.is_valid == True
    assert set(schema.namespaces) == {'com.example.ODataDemo', 'V2_Compatible_Primitive_Types','V4_Only_Primitive_Types'}

