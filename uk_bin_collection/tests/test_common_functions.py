from uk_bin_collection.common import *
import pytest


def test_check_postcode_valid():
    valid_postcode = 'SW1A 1AA'
    result = check_postcode(valid_postcode)
    assert result is True

def test_check_postcode_invalid(capfd):
    invalid_postcode = 'BADPOSTCODE'
    with pytest.raises(SystemExit) as exc_info:
        result = check_postcode(invalid_postcode)
    out, err = capfd.readouterr()
    assert out == 'Exception encountered: Invalid postcode\nPlease check the provided postcode. If this error continues, please first trying setting the postcode manually on line 24 before raising an issue.\n'
    assert exc_info.type == SystemExit
    assert exc_info.value.code == 1

def test_check_paon():
    valid_house_num = '1'
    result = check_paon(valid_house_num)
    assert result is True

def test_check_paon_invalid(capfd):
    invalid_house_num = None
    with pytest.raises(SystemExit) as exc_info:
        result = check_paon(invalid_house_num)
    out, err = capfd.readouterr()
    assert out == 'Exception encountered: Invalid house number\nPlease check the provided house number. If this error continues, please first trying setting the house number manually on line 25 before raising an issue.\n'
    assert exc_info.type == SystemExit
    assert exc_info.value.code == 1

def test_get_date_with_ordinal():
    date_number = 1
    result = get_date_with_ordinal(date_number)
    assert result == '1st'

def test_get_date_with_ordinal_exception():
    date_number = 'a'
    with pytest.raises(TypeError) as exc_info:
         result = get_date_with_ordinal(date_number)
    assert exc_info.type == TypeError
    assert exc_info.value.args[0] == 'not all arguments converted during string formatting'

