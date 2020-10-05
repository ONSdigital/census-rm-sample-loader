import argparse
import csv
import logging
import os
import sys
from typing import Iterable

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

FIELDNAMES = ('UPRN', 'ESTAB_UPRN', 'ADDRESS_TYPE', 'ESTAB_TYPE', 'ADDRESS_LEVEL', 'ABP_CODE',
              'ORGANISATION_NAME', 'ADDRESS_LINE1', 'ADDRESS_LINE2', 'ADDRESS_LINE3',
              'TOWN_NAME', 'POSTCODE', 'LATITUDE', 'LONGITUDE', 'OA', 'LSOA',
              'MSOA', 'LAD', 'REGION', 'HTC_WILLINGNESS', 'HTC_DIGITAL', 'TREATMENT_CODE',
              'FIELDCOORDINATOR_ID', 'FIELDOFFICER_ID', 'CE_EXPECTED_CAPACITY', 'CE_SECURE', 'PRINT_BATCH')


def parse_arguments():
    parser = argparse.ArgumentParser(description='Load a sample file into response management.')
    parser.add_argument('sample_file_path', help='path to the sample file', type=str)
    return parser.parse_args()


def redact_sample_file(sample_file_path):
    with open(sample_file_path) as sample_file:
        redact_sample(sample_file)


def redact_sample(sample_file: Iterable[str]):
    sample_file_reader = csv.DictReader(sample_file, delimiter=',')
    _redact_sample_units(sample_file_reader)


def _redact_sample_units(sample_file_reader: Iterable[str],
                       sample_unit_log_frequency=5000):
    logger.info(f'Redacting sample...')

    with open("redacted_sample.csv", 'w', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=FIELDNAMES)
        writer.writeheader()

        for count, sample_row in enumerate(sample_file_reader, 1):
            writer.writerow({
                'UPRN': sample_row['UPRN'],
                'ESTAB_UPRN': sample_row['ESTAB_UPRN'],
                'ADDRESS_TYPE': sample_row['ADDRESS_TYPE'],
                'ESTAB_TYPE': sample_row['ESTAB_TYPE'],
                'ADDRESS_LEVEL': sample_row['ADDRESS_LEVEL'],
                'ABP_CODE': sample_row['ABP_CODE'],
                'ORGANISATION_NAME': 'Acme Widget Company',
                'ADDRESS_LINE1': "123 fake street",
                'ADDRESS_LINE2': 'Banana sausage',
                'ADDRESS_LINE3': 'Frugal penny',
                'TOWN_NAME': "Flibbleville",
                'POSTCODE': "AB1 2XY",
                'LATITUDE': "12.3",
                'LONGITUDE': "50.60",
                'OA': sample_row['OA'],
                'LSOA': sample_row['LSOA'],
                'MSOA': sample_row['MSOA'],
                'LAD': sample_row['LAD'],
                'REGION': sample_row['REGION'],
                'HTC_WILLINGNESS': "1",
                'HTC_DIGITAL': "1",
                'TREATMENT_CODE': sample_row['TREATMENT_CODE'],
                'FIELDCOORDINATOR_ID': sample_row['FIELDCOORDINATOR_ID'],
                'FIELDOFFICER_ID': sample_row['FIELDOFFICER_ID'],
                'CE_EXPECTED_CAPACITY': sample_row['CE_EXPECTED_CAPACITY'],
                'CE_SECURE': sample_row['CE_SECURE'],
                'PRINT_BATCH': sample_row['PRINT_BATCH']})

        if count % sample_unit_log_frequency == 0:
            logger.info(f'{count} sample units redacted')

    if count % sample_unit_log_frequency:
        logger.info(f'{count} sample units redacted')

    logger.info(f'All sample units have been redacted')


def main():
    log_level = os.getenv('LOG_LEVEL')
    logging.basicConfig(handlers=[logging.StreamHandler(sys.stdout)], level=log_level or logging.ERROR)
    logger.setLevel(log_level or logging.INFO)
    args = parse_arguments()
    redact_sample_file(args.sample_file_path)


if __name__ == "__main__":
    main()
