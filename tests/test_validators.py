from unittest import TestCase

import pytest

import validators


class TestValidators(TestCase):

    def test_max_length_valid(self):
        # Given
        max_length_validator = validators.max_length(10)

        # When
        max_length_validator('a' * 9, None)

        # Then no invalid exception is raised

    def test_max_length_invalid(self):
        # Given
        max_length_0_validator = validators.max_length(10)

        # When, then raises
        with pytest.raises(validators.Invalid):
            max_length_0_validator('a' * 11, None)

    def test_unique_valid(self):
        # Given
        unique_validator = validators.unique()

        # When
        unique_validator('1', None)
        unique_validator('2', None)
        unique_validator('3', None)
        unique_validator('foo', None)
        unique_validator('bar', None)

        # Then no invalid exception is raised

    def test_unique_invalid(self):
        # Given
        unique_validator = validators.unique()

        # When
        unique_validator('1', None)
        unique_validator('2', None)
        unique_validator('3', None)
        unique_validator('foo', None)

        # Then raises
        with pytest.raises(validators.Invalid):
            unique_validator('1', None)

    def test_unique_validators_do_not_cross_validate(self):
        # Given
        unique_validator_1 = validators.unique()
        unique_validator_2 = validators.unique()

        # When
        unique_validator_1('a', None)
        unique_validator_2('a', None)

        # Then no invalid exception is raised

    def test_mandatory_valid(self):
        # Given
        mandatory_validator = validators.mandatory()

        # When
        mandatory_validator('a', None)

        # Then no invalid exception is raised

    def test_mandatory_invalid(self):
        # Given
        mandatory_validator = validators.mandatory()

        # When, then raises
        with pytest.raises(validators.Invalid):
            mandatory_validator('', None)

    def test_numeric_valid(self):
        # Given
        numeric_validator = validators.numeric()

        # When
        numeric_validator('0123456789', None)

        # Then no invalid exception is raised

    def test_numeric_invalid(self):
        # Given
        numeric_validator = validators.numeric()

        # When, then raises
        with pytest.raises(validators.Invalid):
            numeric_validator('a', None)

        with pytest.raises(validators.Invalid):
            numeric_validator('1.1', None)

        with pytest.raises(validators.Invalid):
            numeric_validator('_', None)

    def test_lat_long_valid(self):
        # Given
        lat_long_validator = validators.latitude_longitude(max_scale=5, max_precision=10)

        # When
        lat_long_validator('1234.5678', None)

        # Then no invalid exception is raised

    def test_lat_long_invalid_format(self):
        # Given
        lat_long_validator = validators.latitude_longitude(max_scale=5, max_precision=10)

        # When, then raises
        with pytest.raises(validators.Invalid):
            lat_long_validator('foo', None)

    def test_lat_long_invalid_scale(self):
        # Given
        lat_long_validator = validators.latitude_longitude(max_scale=5, max_precision=10)

        # When, then raises
        with pytest.raises(validators.Invalid):
            lat_long_validator('1.567889', None)

    def test_lat_long_invalid_precision(self):
        # Given
        lat_long_validator = validators.latitude_longitude(max_scale=10, max_precision=5)

        # When, then raises
        with pytest.raises(validators.Invalid):
            lat_long_validator('123456.7', None)

    def test_in_set_valid(self):
        # Given
        in_set_validator = validators.in_set({'a', 'b', 'c'})

        # When
        in_set_validator('a', None)
        in_set_validator('b', None)
        in_set_validator('c', None)

        # Then no invalid exception is raised

    def test_in_set_invalid(self):
        # Given
        in_set_validator = validators.in_set({'a'})

        # When, then raises
        with pytest.raises(validators.Invalid):
            in_set_validator('abc', None)

    def test_set_equal_valid(self):
        # Given
        set_equal_validator = validators.set_equal({'a', 'b', 'c'})

        # When
        set_equal_validator(['a', 'b', 'c'], None)

        # Then no invalid exception is raised

    def test_set_equal_invalid(self):
        # Given
        set_equal_validator = validators.set_equal({'a', 'b', 'c'})

        # When, then raises
        with pytest.raises(validators.Invalid):
            set_equal_validator(['a', 'b', 'c', 'blah'], None)

    def test_no_padding_whitespace_check_valid(self):
        # Given
        no_whitespace_check_validator = validators.no_padding_whitespace()

        # When
        no_whitespace_check_validator('', None)

        # Then no invalid exception is raised

    def test_no_padding_whitespace_check_invalid(self):
        # Given
        no_whitespace_check_validator = validators.no_padding_whitespace()

        # When, then raises
        with pytest.raises(validators.Invalid):
            no_whitespace_check_validator('  ', None)

    def test_region_matches_treatment_code_valid(self):
        # Given
        region_matches_treatment_code_validator = validators.region_matches_treatment_code()

        # When
        region_matches_treatment_code_validator('E0000', {'TREATMENT_CODE': 'HH_TESTE'})

        # Then no invalid exception is raised

    def test_region_matches_treatment_code_invalid(self):
        # Given
        region_matches_treatment_code_validator = validators.region_matches_treatment_code()

        # When, then raises
        with pytest.raises(validators.Invalid):
            region_matches_treatment_code_validator('N0000', {'TREATMENT_CODE': 'HH_TESTE'})