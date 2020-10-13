import shutil
from pathlib import Path
from unittest import TestCase

import redact_sample
from validate_sample import SampleValidator


class TestRedactSample(TestCase):
    RESOURCE_FILE_PATH = Path(__file__).parent.joinpath('resources')
    TMP_TEST_DIRECTORY_PATH = RESOURCE_FILE_PATH.joinpath('sample_files')

    def setUp(self) -> None:
        shutil.rmtree(self.TMP_TEST_DIRECTORY_PATH, ignore_errors=True)
        self.TMP_TEST_DIRECTORY_PATH.mkdir()

    def tearDown(self) -> None:
        shutil.rmtree(self.TMP_TEST_DIRECTORY_PATH, ignore_errors=True)

    def test_redact_sample_valid_output(self):
        # Given
        sample_file_path = self.RESOURCE_FILE_PATH.joinpath('sample_file_1_per_treatment_code.csv')
        sample_redacted_file_path = self.TMP_TEST_DIRECTORY_PATH.joinpath(
            'sample_file_1_per_treatment_code_redacted.csv')

        # When
        redact_sample.redact_sample_file(sample_file_path, sample_redacted_file_path)
        sample_validator = SampleValidator()
        validation_failures = sample_validator.validate(sample_redacted_file_path)

        # Then
        self.assertEqual(validation_failures, [])

    def test_redact_random_htc(self):
        # Given
        sample_dict_row = {'UPRN': '10008677190', 'ESTAB_UPRN': '10008677194', 'ADDRESS_TYPE': 'HH',
                           'ESTAB_TYPE': 'HOUSEHOLD', 'ADDRESS_LEVEL': 'U', 'ABP_CODE': 'RD06', 'ORGANISATION_NAME': '',
                           'ADDRESS_LINE1': 'Flat 56 Francombe House',
                           'ADDRESS_LINE2': 'Commercial Road', 'ADDRESS_LINE3': '', 'TOWN_NAME': 'Windleybury',
                           'POSTCODE': 'XX1 0XX', 'LATITUDE': '51.4463421', 'LONGITUDE': '-2.5924477',
                           'OA': 'E00073438', 'LSOA': 'E01014540', 'MSOA': 'E02003043', 'LAD': 'E06000023',
                           'REGION': 'E12000009', 'HTC_WILLINGNESS': '1',
                           'HTC_DIGITAL': '5', 'FIELDCOORDINATOR_ID': '1', 'FIELDOFFICER_ID': '2',
                           'TREATMENT_CODE': 'HH_LF3R2E', 'CE_EXPECTED_CAPACITY': '3', 'CE_SECURE': '0',
                           'PRINT_BATCH': '2'}

        # When
        redacted_sample_row = redact_sample._redact_sample_row(sample_dict_row)

        # Then
        self.assertTrue(1 <= int(redacted_sample_row['HTC_WILLINGNESS']) <= 5)

        self.assertTrue(1 <= int(redacted_sample_row['HTC_DIGITAL']) <= 5)

    def test_redact_fields_sensitive_estab(self):
        # Given
        sample_dict_row = {'UPRN': '10008677190', 'ESTAB_UPRN': '10008677194', 'ADDRESS_TYPE': 'HH',
                           'ESTAB_TYPE': 'MILITARY SFA', 'ADDRESS_LEVEL': 'U', 'ABP_CODE': 'RD06',
                           'ORGANISATION_NAME': '', 'ADDRESS_LINE1': 'Flat 56 Francombe House',
                           'ADDRESS_LINE2': 'Commercial Road', 'ADDRESS_LINE3': 'Another Address Line',
                           'TOWN_NAME': 'Windleybury',
                           'POSTCODE': 'XX1 0XX', 'LATITUDE': '51.4463421', 'LONGITUDE': '-2.5924477',
                           'OA': 'E00073438', 'LSOA': 'E01014540', 'MSOA': 'E02003043', 'LAD': 'E06000023',
                           'REGION': 'E12000009', 'HTC_WILLINGNESS': '1',
                           'HTC_DIGITAL': '5', 'FIELDCOORDINATOR_ID': '1', 'FIELDOFFICER_ID': '2',
                           'TREATMENT_CODE': 'HH_LF3R2E', 'CE_EXPECTED_CAPACITY': '3', 'CE_SECURE': '0',
                           'PRINT_BATCH': '2'}

        sample_dict_row_reference = {'UPRN': '10008677190', 'ESTAB_UPRN': '10008677194', 'ADDRESS_TYPE': 'HH',
                                     'ESTAB_TYPE': 'MILITARY SFA', 'ADDRESS_LEVEL': 'U', 'ABP_CODE': 'RD06',
                                     'ORGANISATION_NAME': '', 'ADDRESS_LINE1': 'Flat 56 Francombe House',
                                     'ADDRESS_LINE2': 'Commercial Road', 'ADDRESS_LINE3': 'Another Address Line',
                                     'TOWN_NAME': 'Windleybury', 'POSTCODE': 'XX1 0XX', 'LATITUDE': '51.4463421',
                                     'LONGITUDE': '-2.5924477', 'OA': 'E00073438', 'LSOA': 'E01014540',
                                     'MSOA': 'E02003043', 'LAD': 'E06000023', 'REGION': 'E12000009',
                                     'HTC_WILLINGNESS': '1',
                                     'HTC_DIGITAL': '5', 'FIELDCOORDINATOR_ID': '1', 'FIELDOFFICER_ID': '2',
                                     'TREATMENT_CODE': 'HH_LF3R2E', 'CE_EXPECTED_CAPACITY': '3', 'CE_SECURE': '0',
                                     'PRINT_BATCH': '2'}

        # When
        redacted_sample_row = redact_sample._redact_sample_row(sample_dict_row)

        # Then
        self.assertNotEqual(sample_dict_row_reference['ESTAB_TYPE'], redacted_sample_row['ESTAB_TYPE'])

        self.assertNotEqual(sample_dict_row_reference['ADDRESS_LINE1'], redacted_sample_row['ADDRESS_LINE1'])

        self.assertNotEqual(sample_dict_row_reference['TOWN_NAME'], redacted_sample_row['TOWN_NAME'])

        self.assertNotEqual(sample_dict_row_reference['POSTCODE'], redacted_sample_row['POSTCODE'])

        self.assertNotEqual(sample_dict_row_reference['LATITUDE'], redacted_sample_row['LATITUDE'])

        self.assertNotEqual(sample_dict_row_reference['LONGITUDE'], redacted_sample_row['LONGITUDE'])

        self.assertNotEqual(sample_dict_row_reference['ADDRESS_LINE2'], redacted_sample_row['ADDRESS_LINE2'])

        self.assertNotEqual(sample_dict_row_reference['ADDRESS_LINE3'], redacted_sample_row['ADDRESS_LINE3'])
