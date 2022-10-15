"""
    Test of simple valid v4 primitive types

    Specification copy:


    """


# pylint: disable=line-too-long,too-many-locals,too-many-statements,invalid-name, too-many-lines, no-name-in-module, expression-not-assigned, pointless-statement

import pytest
import logging
from pyodata.v4.model import Types


def test_traits():
    """Test individual traits"""

    # generic
    typ = Types.from_name('Edm.Byte')
    assert repr(typ.traits) == 'TypTraits'
    assert typ.traits.to_literal('85') == '85'
    assert typ.traits.from_literal('170') == '170'

    # binary
    typ = Types.from_name('Edm.Binary')
    assert repr(typ.traits) == 'EdmBinaryTypTraits'
    assert typ.traits.to_literal('wAHK/rqt8A0=') == 'binary\'C001CAFEBAADF00D\''
    assert typ.traits.from_literal('binary\'C001cafeBAADF00D\'') == 'wAHK/rqt8A0='
    assert typ.traits.from_literal('X\'C001cafeBAADF00D\'') == 'wAHK/rqt8A0='
    assert typ.traits.to_json('cHlvZGF0YQ==') == 'cHlvZGF0YQ=='
    assert typ.traits.from_json('cHlvZGF0YQ==') == 'cHlvZGF0YQ=='

    # bool
    typ = Types.from_name('Edm.Boolean')
    assert repr(typ.traits) == 'EdmBooleanTypTraits'
    assert typ.traits.to_literal(True) == 'true'
    assert typ.traits.from_literal('true') is True
    assert typ.traits.to_literal(False) == 'false'
    assert typ.traits.from_literal('false') is False
    assert typ.traits.to_literal(1) == 'true'
    assert typ.traits.to_literal(0) == 'false'

    assert typ.traits.from_json(True) is True
    assert typ.traits.from_json(False) is False

    """
    # string
    typ = Types.from_name('Edm.String')
    assert repr(typ.traits) == 'EdmStringTypTraits'
    assert typ.traits.to_literal('Foo Foo') == "'Foo Foo'"
    assert typ.traits.from_literal("'Alice Bob'") == 'Alice Bob"

    # integers
    typ = Types.from_name('Edm.Int16')
    assert repr(typ.traits) == 'EdmIntTypTraits'
    assert typ.traits.to_literal(23) == '23'
    assert typ.traits.from_literal('345') == 345

    typ = Types.from_name('Edm.Int32')
    assert repr(typ.traits) == 'EdmIntTypTraits'
    assert typ.traits.to_literal(23) == '23'
    assert typ.traits.from_literal('345') == 345

    typ = Types.from_name('Edm.Int64')
    assert repr(typ.traits) == 'EdmLongIntTypTraits'
    assert typ.traits.to_literal(23) == '23L'
    assert typ.traits.from_literal('345L') == 345
    assert typ.traits.from_json('345L') == 345
    assert typ.traits.from_literal('345') == 345
    assert typ.traits.from_json('345') == 345
    assert typ.traits.from_literal('0') == 0
    assert typ.traits.from_json('0') == 0
    assert typ.traits.from_literal('0L') == 0
    assert typ.traits.from_json('0L') == 0

    typ = Types.from_name('Edm.Double')
    assert repr(typ.traits) == 'EdmFPNumTypTraits(15,d)'
    assert typ.traits.from_literal('1E+10d') == 10.0**10
    assert typ.traits.from_literal('1E+10') == 10.0**10
    assert typ.traits.from_literal('2.029d') == 2.029
    assert typ.traits.from_literal('2.0d') == 2.0
    assert typ.traits.from_json('2.0d') == 2.0
    assert typ.traits.to_literal(10.0**10) == '1.000000E+10'
    assert typ.traits.to_literal(2.029) == '2.029000E+00'
    assert typ.traits.to_literal(2.0) == '2.000000E+00'
    assert typ.traits.to_json(2.0) == '2.000000E+00'

    typ = Types.from_name('Edm.Single')
    assert repr(typ.traits) == 'EdmFPNumTypTraits(7,f)'
    assert typ.traits.from_literal('2.029f') == 2.029
    assert typ.traits.from_literal('2.029') == 2.029
    assert typ.traits.from_json('2.029f') == 2.029
    assert typ.traits.to_literal(2.029) == '2.029000'
    assert typ.traits.to_json(2.029) == '2.029000'

    typ = Types.from_name('Edm.Float')
    assert repr(typ.traits) == 'EdmFPNumTypTraits(7,d)'
    assert typ.traits.from_literal('2.029d') == 2.029
    assert typ.traits.from_literal('2.029') == 2.029
    assert typ.traits.from_json('2.029d') == 2.029
    assert typ.traits.from_json('3.76000000E+04') == 3.76*10**4
    assert typ.traits.to_literal(2.029) == '2.029000E+00'
    assert typ.traits.to_json(2.029) == '2.029000E+00'

    # GUIDs
    typ = Types.from_name('Edm.Guid')
    assert repr(typ.traits) == 'EdmPrefixedTypTraits'
    assert typ.traits.to_literal('000-0000') == "guid'000-0000'"
    assert typ.traits.from_literal("guid'1234-56'") == '1234-56'
    with pytest.raises(PyODataModelError) as e_info:
        typ.traits.from_literal("'1234-56'")
    assert str(e_info.value).startswith("Malformed value '1234-56' for primitive")

    """