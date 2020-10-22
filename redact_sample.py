import argparse
import csv
import logging
import os
import sys
from typing import Iterable
from pathlib import Path


from generate_sample_file import SampleGenerator

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())
SampleGen = SampleGenerator()
SENSITIVE_ESTAB_TYPES = ['MILITARY US SFA', 'MILITARY SFA', 'MILITARY US SLA', 'ROYAL HOUSEHOLD',
                         'MOD HOUSEHOLDS', 'HIGH SECURE MENTAL HEALTH', 'ROUGH SLEEPER', 'TRANSIENT PERSONS',
                         'TRAVELLING PERSONS', 'GRT SITE', 'MIGRANT WORKERS', 'IMMIGRATION REMOVAL CENTRE',
                         'SHELTERED ACCOMMODATION', 'APPROVED PREMISES', 'RESIDENTIAL CHILDRENS HOME',
                         'RELIGIOUS COMMUNITY', 'LOW/MEDIUM SECURE MENTAL HEALTH', 'BOARDING SCHOOL']
SAMPLE_UNIT_LOG_FREQUENCY = 50000
NON_SENSITIVE_ESTAB_TYPES = [estab for estab in SampleGen.ESTAB_TYPES if estab not in SENSITIVE_ESTAB_TYPES]
SampleGen.ESTAB_TYPES = NON_SENSITIVE_ESTAB_TYPES
SampleGen.read_words()


def parse_arguments():
    parser = argparse.ArgumentParser(description='Redact a sample file.')
    parser.add_argument('sample_file_path', help='path to the sample file', type=str)
    parser.add_argument('--redact-htc-only', help="redact HTC values only", default=False, action='store_true',
                        required=False)
    return parser.parse_args()


def redact_sample_file(sample_file_path: int, output_file_path: str,  redact_htc_only: bool = False):
    with open(sample_file_path) as sample_file:
        _redact_sample(sample_file, output_file_path, redact_htc_only)


def _redact_sample(sample_file: Iterable[str], output_file_path: str, redact_htc_only: bool):
    sample_file_reader = csv.DictReader(sample_file, delimiter=',')
    _redact_sample_units(sample_file_reader, output_file_path, redact_htc_only)


def _redact_sample_units(sample_file_reader: Iterable[str], output_file_path: str, redact_htc_only):
    logger.info('Redacting sample...')

    with open(output_file_path, 'w', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=SampleGenerator.FIELDNAMES)
        writer.writeheader()

        for count, sample_row in enumerate(sample_file_reader, 1):
            redacted_sample_row = _redact_sample_row(sample_row, redact_htc_only)
            _write_row(writer, redacted_sample_row)

            if count % SAMPLE_UNIT_LOG_FREQUENCY == 0:
                logger.info(f'{count} sample units redacted')

    logger.info('All sample units have been redacted')


def _redact_sample_row(sample_row: dict, redact_htc_only: bool):
    sample_row['HTC_WILLINGNESS'] = SampleGen.get_random_htc()
    sample_row['HTC_DIGITAL'] = SampleGen.get_random_htc()
    if not redact_htc_only:
        sample_row['ORGANISATION_NAME'] = ''
        if sample_row['ESTAB_TYPE'] in SENSITIVE_ESTAB_TYPES:
            sample_row['ESTAB_TYPE'] = SampleGen.get_random_estab_type()
            sample_row['ADDRESS_LINE1'] = SampleGen.get_random_address_line()
            address_line_2, address_line_3 = SampleGen.get_random_address_lines_2_and_3()
            sample_row['ADDRESS_LINE2'] = address_line_2
            sample_row['ADDRESS_LINE3'] = address_line_3
            sample_row['TOWN_NAME'] = SampleGen.get_random_post_town()
            sample_row['POSTCODE'] = SampleGen.get_random_post_code()
            sample_row['LATITUDE'] = SampleGen.get_random_lat_or_long()
            sample_row['LONGITUDE'] = SampleGen.get_random_lat_or_long()
    return sample_row


def _write_row(writer: csv.DictWriter, sample_row: dict):
    writer.writerow({
        'UPRN': sample_row['UPRN'],
        'ESTAB_UPRN': sample_row['ESTAB_UPRN'],
        'ADDRESS_TYPE': sample_row['ADDRESS_TYPE'],
        'ESTAB_TYPE': sample_row['ESTAB_TYPE'],
        'ADDRESS_LEVEL': sample_row['ADDRESS_LEVEL'],
        'ABP_CODE': sample_row['ABP_CODE'],
        'ORGANISATION_NAME': sample_row['ORGANISATION_NAME'],
        'ADDRESS_LINE1': sample_row['ADDRESS_LINE1'],
        'ADDRESS_LINE2': sample_row['ADDRESS_LINE2'],
        'ADDRESS_LINE3': sample_row['ADDRESS_LINE3'],
        'TOWN_NAME': sample_row['TOWN_NAME'],
        'POSTCODE': sample_row['POSTCODE'],
        'LATITUDE': sample_row['LATITUDE'],
        'LONGITUDE': sample_row['LONGITUDE'],
        'OA': sample_row['OA'],
        'LSOA': sample_row['LSOA'],
        'MSOA': sample_row['MSOA'],
        'LAD': sample_row['LAD'],
        'REGION': sample_row['REGION'],
        'HTC_WILLINGNESS': sample_row['HTC_WILLINGNESS'],
        'HTC_DIGITAL': sample_row['HTC_DIGITAL'],
        'TREATMENT_CODE': sample_row['TREATMENT_CODE'],
        'FIELDCOORDINATOR_ID': sample_row['FIELDCOORDINATOR_ID'],
        'FIELDOFFICER_ID': sample_row['FIELDOFFICER_ID'],
        'CE_EXPECTED_CAPACITY': sample_row['CE_EXPECTED_CAPACITY'],
        'CE_SECURE': sample_row['CE_SECURE'],
        'PRINT_BATCH': sample_row['PRINT_BATCH']})


def create_output_path(sample_file_path: Path, redact_htc_only: bool) -> Path:
    file_name_suffix = '_redacted.csv' if not redact_htc_only else '_redacted_htc_only.csv'
    redacted_file_name = f'{Path(sample_file_path).stem}{file_name_suffix}'
    output_file_path = Path('sample_files').joinpath(redacted_file_name)
    return output_file_path


def main():
    log_level = os.getenv('LOG_LEVEL')
    logging.basicConfig(handlers=[logging.StreamHandler(sys.stdout)], level=log_level or logging.ERROR)
    logger.setLevel(log_level or logging.INFO)
    args = parse_arguments()
    output_file_path = create_output_path(args.sample_file_path, args.redact_htc_only)
    redact_sample_file(args.sample_file_path, output_file_path, args.redact_htc_only)


if __name__ == "__main__":
    main()
