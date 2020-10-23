import pytest

import validators


def test_max_length_valid():
    # Given
    max_length_validator = validators.max_length(10)

    # When
    max_length_validator('a' * 9)

    # Then no invalid exception is raised


def test_max_length_invalid():
    # Given
    max_length_0_validator = validators.max_length(10)

    # When, then raises
    with pytest.raises(validators.Invalid):
        max_length_0_validator('a' * 11)


def test_unique_valid():
    # Given
    unique_validator = validators.unique()

    # When
    unique_validator('1')
    unique_validator('2')
    unique_validator('3')
    unique_validator('foo')
    unique_validator('bar')

    # Then no invalid exception is raised


def test_unique_invalid():
    # Given
    unique_validator = validators.unique()

    # When
    unique_validator('1')
    unique_validator('2')
    unique_validator('3')
    unique_validator('foo')

    # Then raises
    with pytest.raises(validators.Invalid):
        unique_validator('1')


def test_unique_validators_do_not_cross_validate():
    # Given
    unique_validator_1 = validators.unique()
    unique_validator_2 = validators.unique()

    # When
    unique_validator_1('a')
    unique_validator_2('a')

    # Then no invalid exception is raised


def test_mandatory_valid():
    # Given
    mandatory_validator = validators.mandatory()

    # When
    mandatory_validator('a')

    # Then no invalid exception is raised


def test_mandatory_invalid():
    # Given
    mandatory_validator = validators.mandatory()

    # When, then raises
    with pytest.raises(validators.Invalid):
        mandatory_validator('')


def test_numeric_valid():
    # Given
    numeric_validator = validators.numeric()

    # When
    numeric_validator('0123456789')

    # Then no invalid exception is raised


def test_numeric_invalid():
    # Given
    numeric_validator = validators.numeric()

    # When, then raises
    with pytest.raises(validators.Invalid):
        numeric_validator('a')

    with pytest.raises(validators.Invalid):
        numeric_validator('1.1')

    with pytest.raises(validators.Invalid):
        numeric_validator('_')


def test_lat_long_valid():
    # Given
    lat_long_validator = validators.latitude_longitude(max_scale=5, max_precision=10)

    # When
    lat_long_validator('1234.5678')

    # Then no invalid exception is raised


@pytest.mark.parametrize('value', [
    '1.1E-10',  # Python valid scientific notation
    '1.1e-10',
    '2e-4',
    '2E-4',
    '3E4',
    '3e5',
    '5.9238E-7',
    '0.2E-3',
    '23.4E-5',
    '1.2345E2',
    '1.2345*10^-3',  # Not python valid notation
    '1.2345*10**-3',
    '1.2345x10**-3',
    '1.2345x10^-3',
    'eggs'
])
def test_lat_long_scientific_notation_invalid(value):
    # Given
    lat_long_validator = validators.latitude_longitude(max_scale=5, max_precision=10)

    # When, then raises
    with pytest.raises(validators.Invalid):
        lat_long_validator(value)


def test_lat_long_malformed_decimal():
    # Given
    lat_long_validator = validators.latitude_longitude(max_scale=5, max_precision=10)

    # When, then raises
    with pytest.raises(validators.Invalid):
        lat_long_validator('1')


def test_lat_long_invalid_format():
    # Given
    lat_long_validator = validators.latitude_longitude(max_scale=5, max_precision=10)

    # When, then raises
    with pytest.raises(validators.Invalid):
        lat_long_validator('foo')


def test_lat_long_invalid_scale():
    # Given
    lat_long_validator = validators.latitude_longitude(max_scale=5, max_precision=10)

    # When, then raises
    with pytest.raises(validators.Invalid):
        lat_long_validator('1.567889')


def test_lat_long_invalid_precision():
    # Given
    lat_long_validator = validators.latitude_longitude(max_scale=10, max_precision=5)

    # When, then raises
    with pytest.raises(validators.Invalid):
        lat_long_validator('123456.7')


def test_in_set_valid():
    # Given
    in_set_validator = validators.in_set({'a', 'b', 'c'})

    # When
    in_set_validator('a')
    in_set_validator('b')
    in_set_validator('c')

    # Then no invalid exception is raised


def test_in_set_invalid():
    # Given
    in_set_validator = validators.in_set({'a'})

    # When, then raises
    with pytest.raises(validators.Invalid):
        in_set_validator('abc')


def test_set_equal_valid():
    # Given
    set_equal_validator = validators.set_equal({'a', 'b', 'c'})

    # When
    set_equal_validator(['a', 'b', 'c'])

    # Then no invalid exception is raised


def test_set_equal_invalid():
    # Given
    set_equal_validator = validators.set_equal({'a', 'b', 'c'})

    # When, then raises
    with pytest.raises(validators.Invalid):
        set_equal_validator(['a', 'b', 'c', 'blah'])


def test_no_padding_whitespace_check_valid():
    # Given
    no_padding_whitespace_validator = validators.no_padding_whitespace()

    # When
    no_padding_whitespace_validator('')

    # Then no invalid exception is raised


def test_no_padding_whitespace_check_invalid():
    # Given
    no_padding_whitespace_validator = validators.no_padding_whitespace()

    # When, then raises
    with pytest.raises(validators.Invalid):
        no_padding_whitespace_validator('  ')


def test_no_pipe_character_check_valid():
    # Given
    no_pipe_character_validator = validators.no_pipe_character()

    # When, then raises
    no_pipe_character_validator('test')

    # Then no invalid exception is raised


def test_no_pipe_character_check_invalid():
    # Given
    no_pipe_character_validator = validators.no_pipe_character()

    # When, then raises
    with pytest.raises(validators.Invalid):
        no_pipe_character_validator('|')


def test_region_matches_treatment_code_valid():
    # Given
    region_matches_treatment_code_validator = validators.region_matches_treatment_code()

    # When
    region_matches_treatment_code_validator('E0000', row={'TREATMENT_CODE': 'HH_TESTE'})

    # Then no invalid exception is raised


def test_region_matches_treatment_code_invalid():
    # Given
    region_matches_treatment_code_validator = validators.region_matches_treatment_code()

    # When, then raises
    with pytest.raises(validators.Invalid):
        region_matches_treatment_code_validator('N0000', row={'TREATMENT_CODE': 'HH_TESTE'})


def test_region_matches_treatment_code_empty_region_no_error():
    # Given
    region_matches_treatment_code_validator = validators.region_matches_treatment_code()

    # When, then doesn't error.
    region_matches_treatment_code_validator(' ', row={'TREATMENT_CODE': 'HH_TESTE'})


def test_region_matches_treatment_code_empty_treatment_no_error():
    # Given
    region_matches_treatment_code_validator = validators.region_matches_treatment_code()

    # When, then doesn't error.
    region_matches_treatment_code_validator('N0000', row={'TREATMENT_CODE': ' '})


def test_ce_u_has_expected_capacity_valid():
    # Given
    ce_u_has_expected_capacity_validator = validators.ce_u_has_expected_capacity()

    # When
    ce_u_has_expected_capacity_validator('5', row={'ADDRESS_TYPE': 'CE', 'ADDRESS_LEVEL': 'U'})

    # Then no invalid exception is raised


def test_ce_u_has_expected_capacity_invalid():
    # Given
    ce_u_has_expected_capacity_validator = validators.ce_u_has_expected_capacity()

    # When, then raises
    with pytest.raises(validators.Invalid):
        ce_u_has_expected_capacity_validator('a', row={'ADDRESS_TYPE': 'CE', 'ADDRESS_LEVEL': 'U'})


def test_ce_e_has_expected_capacity_valid():
    # Given
    ce_e_has_expected_capacity_validator = validators.ce_e_has_expected_capacity()

    # When
    ce_e_has_expected_capacity_validator('5', row={'ADDRESS_TYPE': 'CE', 'ADDRESS_LEVEL': 'E',
                                                   'TREATMENT_CODE': 'CE_TESTE'})

    # Then no invalid exception is raised


def test_ce_e_has_expected_capacity_invalid():
    # Given
    ce_e_has_expected_capacity_validator = validators.ce_e_has_expected_capacity()

    # When, then raises
    with pytest.raises(validators.Invalid):
        ce_e_has_expected_capacity_validator('0', row={'ADDRESS_TYPE': 'CE', 'ADDRESS_LEVEL': 'E',
                                                       'TREATMENT_CODE': 'CE_TESTE'})


def test_alphanumeric_postcode_valid():
    # Given
    alphanumeric_postcode_validator = validators.alphanumeric_postcode()

    # When
    alphanumeric_postcode_validator('TE25 5TE')

    # Then no invalid exception is raised


def test_alphanumeric_postcode_invalid():
    # Given
    alphanumeric_postcode_validator = validators.alphanumeric_postcode()

    # When, then raises
    with pytest.raises(validators.Invalid):
        alphanumeric_postcode_validator('TE5 5TE!')


def test_latitude_longitude_range_valid():
    # Given
    latitude_longitude_range_validator = validators.latitude_longitude_range()

    # When
    latitude_longitude_range_validator(50)

    # Then no invalid exception is raised


def test_latitude_longitude_range_invalid():
    # Given
    latitude_longitude_range_validator = validators.latitude_longitude_range()

    # When, then raises
    with pytest.raises(validators.Invalid):
        latitude_longitude_range_validator(360)


def test_alphanumeric_plus_hyphen_field_values_valid():
    # Given
    alphanumeric_plus_hyphen_field_validator = validators.alphanumeric_plus_hyphen_field_values()

    # When
    alphanumeric_plus_hyphen_field_validator('TE-STT1-ES-01')

    # Then no invalid exception is raised


def test_alphanumeric_plus_hyphen_field_values_invalid():
    # Given
    alphanumeric_plus_hyphen_field_validator = validators.alphanumeric_plus_hyphen_field_values()

    # When, then raises
    with pytest.raises(validators.Invalid):
        alphanumeric_plus_hyphen_field_validator('TE-STT1-ES-!!')
