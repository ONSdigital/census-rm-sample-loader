import shutil
from pathlib import Path
from unittest import TestCase

from generate_sample_file import SampleGenerator
from validate_sample import SampleValidator


class TestValidateSample(TestCase):
    RESOURCE_FILE_PATH = Path(__file__).parent.joinpath('resources')
    TMP_TEST_DIRECTORY_PATH = RESOURCE_FILE_PATH.joinpath('tmp')

    def setUp(self) -> None:
        shutil.rmtree(self.TMP_TEST_DIRECTORY_PATH, ignore_errors=True)
        self.TMP_TEST_DIRECTORY_PATH.mkdir()

    def tearDown(self) -> None:
        shutil.rmtree(self.TMP_TEST_DIRECTORY_PATH, ignore_errors=True)

    def test_validate_sample_success(self):
        # Given
        sample_validator = SampleValidator()
        valid_sample_file_path = self.RESOURCE_FILE_PATH.joinpath('sample_file_1_per_treatment_code.csv')

        # When
        validation_failures = sample_validator.validate(valid_sample_file_path)

        # Then
        self.assertEqual(validation_failures, [])

    def test_validate_sample_duplicate_arids(self):
        # Given
        sample_validator = SampleValidator()
        invalid_sample_file_path = self.RESOURCE_FILE_PATH.joinpath('sample_file_duplicate_arid.csv')

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
        invalid_sample_file_path = self.RESOURCE_FILE_PATH.joinpath('sample_file_invalid_treatment_code.csv')

        # When
        validation_failures = sample_validator.validate(invalid_sample_file_path)

        # Then
        self.assertEqual(len(validation_failures), 1)
        failure = validation_failures[0]
        self.assertEqual(failure.line_number, 2)
        self.assertEqual(failure.column, 'TREATMENT_CODE')

    def test_generate_and_validate_random_arids(self):
        # Given
        sample_validator = SampleValidator()
        generated_sample_file_path = self.TMP_TEST_DIRECTORY_PATH.joinpath('generated_sample.csv')
        treatment_code_quantities_path = self.RESOURCE_FILE_PATH.joinpath('treatment_code_quantities_1_per.csv')

        # When
        SampleGenerator().generate_sample_file(generated_sample_file_path, treatment_code_quantities_path,
                                               sequential_arid=False)
        validation_failures = sample_validator.validate(generated_sample_file_path)

        # Then
        self.assertEqual(validation_failures, [])

    def test_generate_and_validate_sequential_arids(self):
        # Given
        sample_validator = SampleValidator()
        generated_sample_file_path = self.TMP_TEST_DIRECTORY_PATH.joinpath('generated_sample.csv')
        treatment_code_quantities_path = self.RESOURCE_FILE_PATH.joinpath('treatment_code_quantities_1_per.csv')

        # When
        SampleGenerator().generate_sample_file(generated_sample_file_path, treatment_code_quantities_path,
                                               sequential_arid=True)
        validation_failures = sample_validator.validate(generated_sample_file_path)

        # Then
        self.assertEqual(validation_failures, [])
