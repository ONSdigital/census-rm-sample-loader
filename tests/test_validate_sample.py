from pathlib import Path
from unittest import TestCase

from validate_sample import SampleValidator


class TestValidateSample(TestCase):

    def test_validate_sample_success(self):
        # Given
        sample_validator = SampleValidator()
        valid_sample_file_path = Path(__file__).parent.joinpath('resources', 'sample_file_1_per_treatment_code.csv')

        # When
        validation_failures = sample_validator.validate(valid_sample_file_path)

        # Then
        self.assertEqual(validation_failures, [])

    def test_validate_sample_duplicate_arids(self):
        # Given
        sample_validator = SampleValidator()
        invalid_sample_file_path = Path(__file__).parent.joinpath('resources', 'sample_file_duplicate_arid.csv')

        # When
        validation_failures = sample_validator.validate(invalid_sample_file_path)

        # Then
        self.assertEqual(len(validation_failures), 1)
        failure = validation_failures[0]
        self.assertEqual(failure.line_number, 3)
        self.assertEqual(failure.column, 'ARID')

    def test_validate_sample_invalid_treatment_code(self):
        # Given
        sample_validator = SampleValidator()
        invalid_sample_file_path = Path(__file__).parent.joinpath('resources', 'sample_file_invalid_treatment_code.csv')

        # When
        validation_failures = sample_validator.validate(invalid_sample_file_path)

        # Then
        self.assertEqual(len(validation_failures), 1)
        failure = validation_failures[0]
        self.assertEqual(failure.line_number, 2)
        self.assertEqual(failure.column, 'TREATMENT_CODE')
